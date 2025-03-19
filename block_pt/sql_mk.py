import sqlite3
import json
import logging
import os
import unittest
from contextlib import contextmanager
from typing import NamedTuple, Optional

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 数据库配置
CONFIG_FILE = "config.json"
DEFAULT_DB_FILE = "blockchain.db"

# 加载配置
def load_config(config_file: str = CONFIG_FILE) -> dict:
    """从配置文件加载配置"""
    logging.info(f"尝试加载配置文件: {config_file}")
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
            logging.info(f"配置文件加载成功: {config}")
            return config
    except FileNotFoundError:
        logging.warning(f"配置文件 {config_file} 未找到，使用默认配置。")
        return {"db_file": DEFAULT_DB_FILE}
    except json.JSONDecodeError:
        logging.error(f"配置文件 {config_file} 格式错误，使用默认配置。")
        return {"db_file": DEFAULT_DB_FILE}

# 加载数据库文件名
config = load_config()
DATABASE_FILE = config.get("db_file", DEFAULT_DB_FILE)


# 定义区块数据结构
class Block(NamedTuple):
    block_index: int
    hash: str
    previous_hash: str
    timestamp: float
    transactions: list


# 数据库连接上下文管理器
@contextmanager
def get_db_connection():
    """上下文管理器：获取数据库连接"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        yield conn
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {e}")
        raise
    finally:
        conn.close()


# 初始化数据库
def init_db():
    """初始化数据库并创建区块链表"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS blockchain (
                    block_index INTEGER PRIMARY KEY,
                    hash TEXT NOT NULL,
                    previous_hash TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    transactions TEXT NOT NULL
                )
            ''')
            conn.commit()
        logging.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error initializing database: {e}")


# 保存区块
def save_block(block: Block):
    """将区块保存到数据库中"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO blockchain (block_index, hash, previous_hash, timestamp, transactions) VALUES (?, ?, ?, ?, ?)",
                (block.index, block.hash, block.previous_hash, block.timestamp, json.dumps(block.transactions))
            )
            conn.commit()
        logging.info(f"Block {block.index} saved successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error saving block: {e}")
        conn.rollback()
# 查询区块
def fetch_block(block_index: int) -> Optional[Block]:
    """从数据库中获取指定索引的区块"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM blockchain WHERE block_index = ?", (block_index,))
            row = cursor.fetchone()
            if row:
                return Block(
                    block_index=row[0],
                    hash=row[1],
                    previous_hash=row[2],
                    timestamp=row[3],
                    transactions=json.loads(row[4])
                )
            return None
    except sqlite3.Error as e:
        logging.error(f"Error fetching block: {e}")
        return None


# 示例用法
if __name__ == "__main__":
    # 初始化数据库
    init_db()

    # 创建一个示例区块
    sample_block = Block(
        block_index=1,
        hash="abc123",
        previous_hash="def456",
        timestamp=1680000000.0,
        transactions=[{"sender": "Alice", "receiver": "Bob", "amount": 10}]
    )

    # 保存区块
    save_block(sample_block)

    # 查询区块
    fetched_block = fetch_block(1)
    if fetched_block:
        logging.info(f"Fetched block: {fetched_block}")
    else:
        logging.warning("Block not found.")