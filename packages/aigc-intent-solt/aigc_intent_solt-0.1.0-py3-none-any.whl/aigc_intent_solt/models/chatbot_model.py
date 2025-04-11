# -*- coding:utf-8 -*-
import logging

from aigc_intent_solt.config import RELATED_INTENT_THRESHOLD
from aigc_intent_solt.scene_processor.impl.common_processor import CommonProcessor
from aigc_intent_solt.utils.data_format_utils import extract_continuous_digits, extract_float
from aigc_intent_solt.utils.helpers import send_message
# 修改导入部分
from aigc_intent_solt.utils.db_utils import (
    init_db,
    save_conversation,
    get_conversation_history,
    save_current_scene,
    get_current_purpose  # 添加新增的方法导入
)

class ChatbotModel:
    def __init__(self, scene_templates: dict):
        init_db()
        self.scene_templates = scene_templates
        self.processors = {}
        # 移除原有的 current_purpose 实例变量

    def is_related_to_last_intent(self, user_input, session_id):
        current_purpose = get_current_purpose(session_id)
        if not current_purpose:
            return False
        prompt = f"判断当前用户输入内容与当前对话场景的关联性:\n\n当前对话场景: {self.scene_templates[current_purpose]['description']}\n当前用户输入: {user_input}\n\n这两次输入是否关联（仅用小数回答关联度，得分范围0.0至1.0）"
        result = send_message(prompt, None, None)
        return extract_float(result) > RELATED_INTENT_THRESHOLD

    def recognize_intent(self, user_input, session_id):
        # 根据场景模板生成选项
        purpose_options = {}
        purpose_description = {}
        index = 1
        for template_key, template_info in self.scene_templates.items():
            purpose_options[str(index)] = template_key
            purpose_description[str(index)] = template_info["description"]
            index += 1
        options_prompt = "\n".join([f"{key}. {value} - 请回复{key}" for key, value in purpose_description.items()])
        options_prompt += "\n0. 其他场景 - 请回复0"

        # 发送选项给用户，传入空历史记录
        user_choice = send_message(
            f"有下面多种场景，需要你根据用户输入进行判断，只答选项\n{options_prompt}\n用户输入：{user_input}\n请回复序号：", 
            user_input, 
            None  # 传入None作为历史记录
        )

        logging.debug(f'purpose_options: %s', purpose_options)
        logging.debug(f'user_choice: %s', user_choice)

        user_choices = extract_continuous_digits(user_choice)

        # 根据当前轮用户选择获取对应场景
        if user_choices and user_choices[0] != '0':
            new_purpose = purpose_options[user_choices[0]]
            save_current_scene(session_id, new_purpose)
            print(f"用户选择了场景：{self.scene_templates[new_purpose]['name']}")
        else:
            save_current_scene(session_id, '')
            print("无效的选项，请重新选择")

    @classmethod
    def load_scene_processor(cls, scene_config, session_id):
        try:
            return CommonProcessor(scene_config, session_id)
        except (ImportError, AttributeError, KeyError):
            raise ImportError(f"未找到场景处理器 scene_config: {scene_config}")

    def get_processor_for_scene(self, scene_name, session_id):
        # 当会话ID变化时创建新处理器
        if session_id not in self.processors:
            config = self.get_scene_config(scene_name)
            self.processors[session_id] = CommonProcessor(config, session_id)
        return self.processors[session_id]

    def process_multi_question(self, user_input, session_id=None):
        if not session_id:
            session_id = self.start_new_session()
        
        history = get_conversation_history(session_id)
        original_purpose = get_current_purpose(session_id)
        current_purpose = original_purpose
        logging.info('original_purpose: %s', original_purpose)

        if not self.is_related_to_last_intent(user_input, session_id):
            self.recognize_intent(user_input, session_id)  # 如果不关联就保存新的意图
            current_purpose = get_current_purpose(session_id)  # 重新获取更新后的意图
            logging.info('上下文不关联current_purpose: %s', current_purpose)

        if current_purpose in self.scene_templates:
            processor = self.get_processor_for_scene(current_purpose, session_id)
            # 这里使用原始问题向量化，关联历史会话，检索出有效的上下文，并重新组装成新的问题进行后续处理。
            # enhanced_question = self.enhance_question(session_id, user_input)
            # response = processor.process(current_purpose, enhanced_question, history, session_id)
            response = processor.process(current_purpose, user_input, history, session_id)
        else:
            response = '未命中场景'
        
        save_conversation(session_id, user_input, response)
        return response

    # #问题改写
    # def enhance_question(self, session_id, question):
    #     # 新增上下文关联逻辑
    #     print("原始问题：", question)
    #     memory = MemoryRetrieval()
    #
    #     # 1. 获取历史对话记录
    #     history = get_conversation_history(session_id)
    #     if history:
    #         # 2. 插入历史记录到记忆库（根据新表结构格式化）
    #         memory_records = []
    #         for h in history:
    #             memory_records.append(f"user: {h['user_input']}")
    #             memory_records.append(f"assistant: {h['bot_response']}")
    #         memory.insert_memory(memory_records)
    #
    #         # 3. 上下文增强的问题重写
    #         related_passages = memory.query_memory(question)
    #         enhanced_question = memory.rerank_with_llm(question, related_passages)
    #     else:
    #         enhanced_question = question
    #     print("增强后的问题：", enhanced_question)
    #     return enhanced_question

    def start_new_session(self):
        """生成新会话ID（仅在后端需要创建时使用）"""

        import uuid
        return str(uuid.uuid4())  # 直接返回新ID，不存储状态

    def get_processor(self, session_id):
        return self.processors.get(session_id)

    def get_scene_config(self, scene_name):
        """公共方法用于获取最新场景配置"""
        config = self.scene_templates.get(scene_name)
        if not config:
            raise ValueError(f"无效的场景名称: {scene_name}")
        return {
            "name": scene_name,
            "parameters": config["parameters"],
            "example": config.get("example", "")
        }



