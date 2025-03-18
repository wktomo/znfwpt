import logging
import time
import json
import binascii
from aihymk import Wallet  # 从文件1导入Wallet类
from core_mk import Block, Blockchain  # 从文件2导入Block和Blockchain类

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def test_blockchain():
    # 初始化区块链
    blockchain = Blockchain(difficulty=4)
    logging.info("Blockchain initialized.")

    # 测试创世区块
    genesis_block = blockchain.chain[0]
    logging.info(f"Genesis Block: {genesis_block}")

    # 创建钱包
    wallet = Wallet()
    public_key_hex = binascii.hexlify(wallet.public_key.to_string()).decode()
    logging.info(f"Public Key: {public_key_hex}")

    # 创建一个交易
    transaction_data = {
        "sender": "Alice",
        "receiver": "Bob",
        "amount": 10,
        "timestamp": time.time()
    }
    transaction = {
        "data": transaction_data,
        "public_key": public_key_hex,
        "signature": wallet.sign_transaction(json.dumps(transaction_data, sort_keys=True))
    }
    logging.info(f"Transaction created: {transaction}")

    # 添加交易到区块链
    blockchain.add_transaction(transaction)
    logging.info(f"Pending Transactions: {blockchain.pending_transactions}")

    # 挖矿：处理待处理的交易并生成新区块
    blockchain.mine_pending_transactions()
    logging.info(f"Blockchain after mining: {blockchain}")

    # 验证新区块是否正确添加
    last_block = blockchain.chain[-1]
    logging.info(f"Last Block: {last_block}")

    # 验证新区块的有效性
    is_valid = blockchain.is_valid_block(last_block)
    logging.info(f"Is last block valid? {is_valid}")

    # 测试无效区块
    invalid_block = Block(
        index=last_block.index + 1,
        transactions=[{"sender": "Invalid", "receiver": "Invalid", "amount": 100}],
        timestamp=time.time(),
        previous_hash=last_block.hash
    )
    invalid_block.nonce = 0
    invalid_block.hash = invalid_block.compute_hash()
    logging.info(f"Invalid Block: {invalid_block}")

    # 验证无效区块
    is_invalid = blockchain.is_valid_block(invalid_block)
    logging.info(f"Is invalid block valid? {is_invalid}")


if __name__ == "__main__":
    test_blockchain()