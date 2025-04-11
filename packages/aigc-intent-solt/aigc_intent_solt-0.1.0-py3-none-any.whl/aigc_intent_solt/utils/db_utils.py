import json
import sqlite3
from datetime import datetime
from pathlib import Path
import os

DB_PATH = Path(__file__).parent.parent / 'data' / 'conversations.db'

def init_db():
    os.makedirs(Path(DB_PATH).parent, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversations (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        user_input TEXT NOT NULL,
        bot_response TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    ''')
    # 新增会话场景表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS session_scenes (
        session_id TEXT PRIMARY KEY,
        current_purpose TEXT NOT NULL,
        slot_data TEXT, 
        updated_at TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def save_current_scene(session_id, purpose):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
        INSERT OR REPLACE INTO session_scenes (session_id, current_purpose, updated_at)
        VALUES (?, ?, ?)
        ''', (session_id, purpose, datetime.now().isoformat()))
        conn.commit()

def get_current_purpose(session_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute('''
        SELECT current_purpose FROM session_scenes WHERE session_id = ?
        ''', (session_id,))
        result = cursor.fetchone()
        return result[0] if result else ''

def update_slot_data(session_id, slot_data):
    """保存槽位数据到session_scenes表"""
    with sqlite3.connect(DB_PATH) as conn:
        # 使用UPDATE语句仅更新slot_data字段
        conn.execute('''
        UPDATE session_scenes 
        SET slot_data = ?, updated_at = ?
        WHERE session_id = ?
        ''', (json.dumps(slot_data), datetime.now().isoformat(), session_id))
        conn.commit()

def save_slot_data(session_id, current_purpose, slot_data):
    """保存槽位数据到session_scenes表"""
    with sqlite3.connect(DB_PATH) as conn:
        # 使用UPDATE语句仅更新slot_data字段
        conn.execute('''
        INSERT INTO session_scenes 
        (session_id, current_purpose, slot_data, updated_at)
        VALUES  (?, ?, ?, ?)
        ''', (session_id, current_purpose, json.dumps(slot_data), datetime.now().isoformat()))
        conn.commit()

def get_slot_data(session_id):
    """从数据库获取槽位数据"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute('''
        SELECT slot_data FROM session_scenes WHERE session_id = ?
        ''', (session_id,))
        result = cursor.fetchone()
        if result and result[0]:
            return json.loads(result[0])
        return None

# Initialize database when module is imported
init_db()

def save_conversation(session_id, user_input, bot_response):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
        INSERT INTO conversations (id, session_id, user_input, bot_response, created_at)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            f"{session_id}_{datetime.now().timestamp()}",
            session_id,
            user_input,
            bot_response,
            datetime.now().isoformat()
        ))
        conn.commit()

def get_conversation_history(session_id: str, limit: int = 10) -> list:
    """根据session_id查询历史对话记录（返回字典格式）
    :param limit: 返回记录条数限制，默认10条
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row  # 关键配置：启用行字典格式
        cursor = conn.execute(
            '''SELECT user_input, bot_response, created_at 
            FROM conversations 
            WHERE session_id = ? 
            ORDER BY created_at DESC
            LIMIT ?''',  # 改为参数化查询
            (session_id, limit)  # 传入两个参数
        )
        return [dict(row) for row in cursor.fetchall()]  # 转换为字典列表