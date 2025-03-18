import hashlib
import json
from datetime import datetime
from Transactions import Transaction, TransactionEncoder


class Block:
    """
        区块结构
            prev_hash:      父区块哈希值
            transactions:   交易对
            timestamp:      区块创建时间
            hash:           区块哈希值
            Nonce:          随机数
    """

    def __init__(self, transactions, prev_hash):
        # 将传入的父哈希值和数据保存到类变量中
        self.prev_hash = prev_hash
        # 交易列表
        self.transactions = transactions
        # 获取当前时间
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 设置Nonce和哈希的初始值为None
        self.nonce = None
        self.hash = None

    # 类的 __repr__() 方法定义了实例化对象的输出信息
    def __repr__(self):
        return f"区块内容：{self.transactions}\n区块哈希值：{self.hash}"


class ProofOfWork:
    """
        工作量证明
            block：          区块
            difficulty：     难度值
    """

    def __init__(self, block, miner, difficult=5):
        self.block = block
        self.miner = miner

        # 定义工作量难度，默认为5，表示有效的哈希值以5个“0”开头
        self.difficulty = difficult

        # 添加挖矿奖励
        self.reward_amount = 1

    def mine(self):

        i = 0
        prefix = '0' * self.difficulty

        # 设置挖矿自动生成交易信息，添加挖矿奖励
        t = Transaction(
            sender="",
            recipient=self.miner.address,
            amount=self.reward_amount,
        )
        sig = self.miner.sign(json.dumps(t, cls=TransactionEncoder))
        t.set_sign(sig, self.miner.pubkey)
        self.block.transactions.append(t)

        while True:
            message = hashlib.sha256()
            message.update(str(self.block.prev_hash).encode('utf-8'))
            # 更新区块中的交易数据
            # message.update(str(self.block.data).encode('utf-8'))
            message.update(str(self.block.transactions).encode('utf-8'))
            message.update(str(self.block.timestamp).encode('utf-8'))
            message.update(str(i).encode("utf-8"))
            digest = message.hexdigest()
            if digest.startswith(prefix):
                self.block.nonce = i
                self.block.hash = digest
                return self.block
            i += 1

    def validate(self):
        """
            验证有效性
        """
        message = hashlib.sha256()
        message.update(str(self.block.prev_hash).encode('utf-8'))
        # 更新区块中的交易数据
        # message.update(str(self.block.data).encode('utf-8'))
        message.update(json.dumps(self.block.transactions).encode('utf-8'))
        message.update(str(self.block.timestamp).encode('utf-8'))
        message.update(str(self.block.nonce).encode('utf-8'))
        digest = message.hexdigest()

        prefix = '0' * self.difficulty
        return digest.startswith(prefix)
