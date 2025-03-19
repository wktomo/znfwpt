from sql_mk import init_db, save_block, fetch_block, get_db_connection
from core_mk import Block
import time
import sqlite3
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 初始化数据库
init_db()

# 获取当前最大的区块索引
def get_max_block_index():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(block_index) FROM blockchain")
            result = cursor.fetchone()
            return result[0] if result else 0
    except sqlite3.Error as e:
        logging.error(f"Error fetching max block index: {e}")
        return 0

# 获取当前最大的区块索引
max_index = get_max_block_index()

# 创建一个示例区块，索引为 max_index + 1
sample_block = Block(
    index=max_index + 1,
    transactions=[{"sender": "Alice", "receiver": "Bob", "amount": 10}],
    timestamp=time.time(),
    previous_hash="0"
)

# 计算区块的哈希值
sample_block.hash = sample_block.compute_hash()

# 保存区块到数据库
try:
    save_block(sample_block)
    logging.info(f"Block {sample_block.index} saved successfully.")
except sqlite3.Error as e:
    logging.error(f"Error saving block: {e}")