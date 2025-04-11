# -*- coding:utf-8 -*-

import logging

from aigc_intent_solt.scene_config import scene_prompts
from aigc_intent_solt.scene_processor.scene_processor import SceneProcessor
from aigc_intent_solt.utils.helpers import get_raw_slot, update_slot, format_name_value_for_logging, is_slot_fully_filled, send_message, \
    extract_json_from_string, get_dynamic_example
from aigc_intent_solt.utils.prompt_utils import get_slot_update_message, get_slot_query_user_message
from aigc_intent_solt.utils.db_utils import get_slot_data, get_conversation_history


class CommonProcessor(SceneProcessor):
    def __init__(self, scene_config, session_id):  # 新增session_id参数
        parameters = scene_config["parameters"]
        self.scene_config: dict = scene_config
        self.scene_name: str = scene_config["name"]
        self.session_id = session_id  # 存储会话ID
        
        # 从数据库获取该会话的已有槽位配置
        self.slot_template: list = get_raw_slot(parameters, session_id)
        existing_slot = get_slot_data(session_id) or self.slot_template
        
        self.slot: list = existing_slot  # 使用会话关联的槽位数据
        self.slot_dynamic_example: str = get_dynamic_example(scene_config)
        self.scene_prompts = scene_prompts
        self.conversation_context = {}
        self.turn_count = 0

    # 新增方法获取最新场景配置
    def get_updated_scene_config(self, scene_name):
        from aigc_intent_solt.models.chatbot_model import ChatbotModel
        from aigc_intent_solt.utils.helpers import load_all_scene_configs
        # 实例化ChatbotModel
        chatbot_model = ChatbotModel(load_all_scene_configs())
        return chatbot_model.get_scene_config(scene_name)


    def process(self, original_purpose, user_input, context, session_id):
        # 转换历史记录格式为可哈希的元组
        history_context = None
        # 新增场景一致性检查
        current_scene_name = self.scene_config["name"]
        logging.debug('current_scene_name: %s', current_scene_name)
        if original_purpose != self.scene_name:
            logging.warning(f"场景切换检测：从 {self.scene_name} 切换到 {current_scene_name}")
            # 重置槽位数据（使用新场景的原始模板）
            from aigc_intent_solt.utils.db_utils import save_slot_data
            save_slot_data(f"prev_{session_id}_{self.scene_name}", self.scene_name, self.slot)
            
            # 更新场景配置并获取新意图槽位
            self.scene_config = self.get_updated_scene_config(original_purpose)
            self.scene_name = original_purpose
            self.slot_template = get_raw_slot(self.scene_config["parameters"], session_id)
            
            # 查询新意图的槽位数据（优先使用已保存数据）
            new_slot = get_slot_data(f"prev_{session_id}_{original_purpose}") or self.slot_template
            self.slot = new_slot
            
            # 更新相关配置
            # self.slot_dynamic_example = get_dynamic_example(self.scene_config)
            # self.reset_conversation()
        else:
            # 更新对话上下文
            self.turn_count += 1
            # 从数据库获取最新槽位状态
            latest_slot = get_slot_data(session_id) or []
            # 获取最近一次用户输入（保留原有逻辑作为fallback）
            history_records = get_conversation_history(session_id, limit=1)
            last_db_input = history_records[0]['user_input'] if history_records else user_input

            self.conversation_context.update({
                'current_turn': self.turn_count,
                'last_user_input': last_db_input,  # 从数据库获取最后一次用户输入
                'last_slot_state': latest_slot  # 从数据库获取当前槽位信息
            })
            if context:
                history_context = tuple(tuple(item) for item in context)
        
        message = get_slot_update_message(self.scene_name,
                                        self.slot_dynamic_example,
                                        self.slot_template,
                                        user_input,
                                        session_id) 
        new_info_json_raw = send_message(message, user_input, history_context)
        current_values = extract_json_from_string(new_info_json_raw)
        logging.debug('current_values: %s', current_values)
        logging.debug('slot update before: %s', self.slot)
        # 更新槽位slot参数
        update_slot(current_values, self.slot)
        logging.debug('slot update after: %s', self.slot)
        # 判断槽位参数是否已经全部补完
        if is_slot_fully_filled(self.slot):
            response = self.respond_with_complete_data()
        else:
            response = self.ask_user_for_missing_data(user_input, session_id)
            
        # 记录完整上下文
        self.conversation_context['last_response'] = response
        return response

    def respond_with_complete_data(self):
        # 当所有数据都准备好后的响应
        logging.debug(f'%s ------ 参数已完整，详细参数如下', self.scene_name)
        logging.debug(format_name_value_for_logging(self.slot))
        logging.debug(f'正在请求%sAPI，请稍后……', self.scene_name)
        return format_name_value_for_logging(self.slot) + '\n正在请求{}API，请稍后……'.format(self.scene_name)

    def ask_user_for_missing_data(self, user_input, session_id):
        message = get_slot_query_user_message(self.scene_name, self.slot, user_input, session_id)
        # 进一步流转请求用户填写缺失的数据
        result = send_message(message, user_input, None)  # 传入None作为历史记录
        return result

    def get_conversation_context(self):
        """获取当前会话上下文"""
        return {
            'scene': self.scene_name,
            'turn_count': self.turn_count,
            'current_slots': self.slot,
            **self.conversation_context
        }

    def reset_conversation(self):
        """重置会话状态"""
        self.turn_count = 0
        self.conversation_context = {}
        
        # 强制生成新的原始槽位模板
        raw_slot = get_raw_slot(self.scene_config["parameters"], self.session_id)
        
        # 确保同时更新数据库和内存状态
        from aigc_intent_solt.utils.db_utils import update_slot_data
        update_slot_data(self.session_id, raw_slot)  # 明确保存初始空值
        self.slot = raw_slot  # 必须重新赋值而非直接修改
        
        # 新增调试日志
        logging.debug(f"Session {self.session_id} 槽位已重置: {self.slot}")
