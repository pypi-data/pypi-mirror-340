# -*- coding:utf-8 -*-

import glob
import json
import re
from aigc_intent_solt import config
import logging

from functools import lru_cache
from aigc_intent_solt.utils.send_llm import send_local_qwen_message
from aigc_intent_solt.utils.send_llm import send_chatgpt_message
from aigc_intent_solt.utils.send_llm import send_glm4_message
from aigc_intent_solt.utils.db_utils import get_slot_data, update_slot_data

send_llm_req = {
    "Qwen": send_local_qwen_message,
    "chatGPT": send_chatgpt_message,
    "GLM": send_glm4_message
}


def filename_to_classname(filename):
    """
    Convert a snake_case filename to a CamelCase class name.

    Args:
    filename (str): The filename in snake_case, without the .py extension.

    Returns:
    str: The converted CamelCase class name.
    """
    parts = filename.split('_')
    class_name = ''.join(part.capitalize() for part in parts)
    return class_name


def load_scene_templates(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_all_scene_configs():
    # 用于存储所有场景配置的字典
    all_scene_configs = {}

    # 搜索目录下的所有json文件
    for file_path in glob.glob("scene_config/**/*.json", recursive=True):
        current_config = load_scene_templates(file_path)
        
        # 新格式为数组，遍历每个function定义
        for func_def in current_config:
            function_config = func_def["function"]
            # 使用function.name作为唯一标识
            key = function_config["name"]
            
            # 只有当键不存在时，才添加到all_scene_configs中
            if key not in all_scene_configs:
                all_scene_configs[key] = function_config

    return all_scene_configs


@lru_cache(maxsize=100)
def send_message(message, user_input, history):
    """
    请求LLM函数
    """
    # 默认调用 GLM-4
    logging.debug(f'message: %s', message)
    logging.debug(f'user_input: %s', user_input)
    logging.debug(f'history: %s', history)
    return send_llm_req.get(config.USE_MODEL, send_glm4_message)(message, history)


def is_slot_fully_filled(json_data):
    """
    检查槽位是否完整填充
    """
    # 遍历JSON数据中的每个元素
    for item in json_data:
        # 检查value字段是否为空字符串
        if item.get('value') == '':
            return False  # 如果发现空字符串，返回False
    return True  # 如果所有value字段都非空，返回True


def get_raw_slot(parameters, session_id=None):
    """生成会话关联的原始槽位模板"""
    # 尝试获取已有会话数据
    if session_id:
        from aigc_intent_solt.utils.db_utils import get_slot_data
        existing = get_slot_data(session_id)
        if existing:
            return existing
    
    # 创建带会话ID的新槽位数据
    output_data = []
    for item in parameters:
        new_item = {
            "name": item["name"],
            "description": item.get("description", item.get("desc", "")),  # 兼容新旧字段
            "type": item["type"],
            "value": "",
            "session_id": session_id  # 新增会话关联字段
        }
        output_data.append(new_item)
    return output_data


def get_dynamic_example(scene_config):
    # 创建新的JSON对象
    if 'example' in scene_config:
        return scene_config['example']
    else:
        return '答：{"name":"xx","value":"xx"}'


def get_slot_update_json(slot, session_id):
    # 从数据库获取已有槽位数据
    existing_data = get_slot_data(session_id) or []
    
    # 创建合并后的数据（以新传入的slot为准）
    merged_data = {item['name']: item for item in existing_data}
    # 修复循环逻辑：直接遍历传入的slot参数
    for item in slot:
        merged_data[item['name']] = {
            "name": item["name"],
            "description": item.get("description", item.get("desc", "")),  # 兼容新旧字段
            "value": item["value"]
        }

    output_data = list(merged_data.values())
    
    # 保存更新后的数据
    update_slot_data(session_id, output_data)
    
    return output_data

def get_slot_query_user_json(slot, session_id):
    # 从数据库获取完整槽位数据
    existing_data = get_slot_data(session_id) or []
    
    # 创建名称映射表（以数据库数据为准）
    slot_map = {item['name']: item for item in existing_data}
    
    # 合并新传入的slot数据
    for item in slot:
        if item['name'] in slot_map:
            slot_map[item['name']]['value'] = item['value']
        else:
            slot_map[item['name']] = item
    
    # 过滤出需要用户补充的字段
    output_data = []
    for item in slot_map.values():
        if not item.get('value'):
            output_data.append({
                "name": item["name"],
                "description": item.get("description", item.get("desc", "")),  # 兼容新旧字段
                "value": item.get("value", "")
            })
    
    return output_data


def update_slot(json_data, dict_target):
    """
    更新槽位slot参数
    """
    # 遍历JSON数据中的每个元素
    for item in json_data:
        # 修复点：增加None检查和安全访问
        if item is not None and item.get('value', '') != '':  # 使用get方法避免KeyError
            for target in dict_target:
                if target['name'] == item.get('name'):
                    target['value'] = item.get('value')
                    break


def format_name_value_for_logging(json_data):
    """
    抽取参数名称和value值
    """
    log_strings = []
    for item in json_data:
        name = item.get('name', 'Unknown name')  # 获取name，如果不存在则使用'Unknown name'
        value = item.get('value', 'N/A')  # 获取value，如果不存在则使用'N/A'
        log_string = f"name: {name}, Value: {value}"
        log_strings.append(log_string)
    return '\n'.join(log_strings)


def extract_json_from_string(input_string):
    """
    JSON抽取函数
    返回包含JSON对象的列表
    """
    try:
        # 正则表达式假设JSON对象由花括号括起来
        matches = re.findall(r'\{.*?\}', input_string, re.DOTALL)

        # 验证找到的每个匹配项是否为有效的JSON
        valid_jsons = []
        for match in matches:
            try:
                json_obj = json.loads(match)
                valid_jsons.append(json_obj)
            except json.JSONDecodeError:
                try:
                    valid_jsons.append(fix_json(match))
                except json.JSONDecodeError:
                    continue  # 如果不是有效的JSON，跳过该匹配项
                continue  # 如果不是有效的JSON，跳过该匹配项

        return valid_jsons
    except Exception as e:
        print(f"Error occurred: {e}")
        return []


def fix_json(bad_json):
    # 首先，用双引号替换掉所有的单引号
    fixed_json = bad_json.replace("'", '"')
    try:
        # 然后尝试解析
        return json.loads(fixed_json)
    except json.JSONDecodeError:
        # 如果解析失败，打印错误信息，但不会崩溃
        print("给定的字符串不是有效的 JSON 格式。")
