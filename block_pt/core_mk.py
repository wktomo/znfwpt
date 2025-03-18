import hashlib
import time
import json
import binascii
from ecdsa import SigningKey, SECP256k1, VerifyingKey
from aihymk import Wallet  # 从文件1导入Wallet类，避免重复定义
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# 区块类
class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        """
        区块初始化
        :param index: 区块索引
        :param transactions: 区块中的交易列表
        :param timestamp: 时间戳
        :param previous_hash: 前一个区块的哈希值
        """
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0  # 工作量证明的随机数
        self.hash = self.compute_hash()

    def compute_hash(self):
        """
        计算区块的哈希值
        """
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def __repr__(self):
        return (f"Block(index={self.index}, transactions={self.transactions}, "
                f"timestamp={self.timestamp}, previous_hash={self.previous_hash}, "
                f"hash={self.hash})")

# 区块链类
class Blockchain:
    def __init__(self, difficulty=4):
        """
        区块链初始化
        :param difficulty: 工作量证明的难度，即哈希值前缀的零数量
        """
        self.chain = []  # 区块链的链
        self.pending_transactions = []  # 待处理的交易
        self.difficulty = difficulty  # 工作量证明的难度
        self.create_genesis_block()  # 创建创世区块

    def create_genesis_block(self):
        """
        创建创世区块
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
        logging.info("Genesis block created.")

    def add_block(self, block):
        """
        添加一个新区块到链中
        :param block: 新区块
        :return: 是否成功添加
        """
        if self.is_valid_block(block):
            self.chain.append(block)
            logging.info(f"Block {block.index} added to the chain.")
            return True
        logging.warning("Invalid block detected. Block not added.")
        return False

    def is_valid_block(self, block):
        """
        验证区块是否有效
        :param block: 新区块
        :return: 验证结果
        """
        # 验证区块哈希是否正确
        if block.hash != block.compute_hash():
            logging.warning("Invalid block hash.")
            return False
        # 验证前一个区块的哈希是否正确
        if block.previous_hash != self.chain[-1].hash:
            logging.warning("Invalid previous block hash.")
            return False
        # 验证工作量证明
        if not block.hash.startswith('0' * self.difficulty):
            logging.warning("Invalid proof of work.")
            return False
        return True

    def mine_pending_transactions(self):
        """
        挖矿：处理待处理的交易并生成新区块
        :return: 是否成功挖矿
        """
        if not self.pending_transactions:
            logging.info("No pending transactions to mine.")
            return False

        last_block = self.chain[-1]
        new_block = Block(len(self.chain), self.pending_transactions.copy(), time.time(), last_block.hash)
        new_block = self.proof_of_work(new_block)
        self.pending_transactions = []  # 清空待处理的交易
        self.add_block(new_block)
        logging.info("Pending transactions mined successfully.")
        return True

    def proof_of_work(self, block):
        """
        工作量证明：找到一个哈希值以指定数量的0开头
        :param block: 新区块
        :return: 完成工作量证明的区块
        """
        while not block.hash.startswith('0' * self.difficulty):
            block.nonce += 1
            block.hash = block.compute_hash()
        logging.info(f"Proof of work completed for block {block.index}.")
        return block

    def add_transaction(self, transaction):
        """
        添加交易到待处理交易列表
        :param transaction: 交易数据
        :return: 是否成功添加
        """
        if self.verify_transaction(transaction):
            self.pending_transactions.append(transaction)
            logging.info("Transaction added to pending list.")
            return True
        logging.warning("Invalid transaction. Transaction not added.")
        return False

    def verify_transaction(self, transaction):
        """
        验证交易的签名
        :param transaction: 交易数据
        :return: 验证结果
        """
        try:
            public_key = transaction['public_key']
            signature = transaction['signature']
            message = json.dumps(transaction['data'], sort_keys=True)
            return Wallet().verify_signature(public_key, signature, message)
        except KeyError:
            logging.error("Transaction missing required fields.")
            return False
        except Exception as e:
            logging.error(f"Error verifying transaction: {e}")
            return False

    def __repr__(self):
        return f"Blockchain(chain={self.chain})"