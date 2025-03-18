import json


class Transaction:
    """
        交易的结构
    """

    def __init__(self, sender, recipient, amount):
        """
            初始化交易，设置交易的发送方、接收方和交易数量
        """
        # 交易发送者的公钥
        self.pubkey = None
        # 交易的数字签名
        self.signature = None

        if isinstance(sender, bytes):
            sender = sender.decode('utf-8')
        self.sender = sender  # 发送方
        if isinstance(recipient, bytes):
            recipient = recipient.decode('utf-8')
        self.recipient = recipient  # 接收方
        self.amount = amount  # 交易数量

    def set_sign(self, signature, pubkey):
        """
            为了便于验证这个交易的可靠性，需要发送方输入他的公钥和签名
        """
        self.signature = signature  # 签名
        self.pubkey = pubkey  # 发送方公钥

    def __repr__(self):
        """
            交易大致可分为两种，一是挖矿所得，而是转账交易
            挖矿所得无发送方，以此进行区分显示不同内容
        """
        if self.sender:
            s = f"从{self.sender}转自{self.recipient}{self.amount}个加密货币"
        elif self.recipient:
            s = f"{self.recipient}挖矿所得{self.amount}个加密货币"
        else:
            s = "error"
        return s


class TransactionEncoder(json.JSONEncoder):
    """
        定义Json的编码类，用来序列化Transaction
    """

    def default(self, obj):
        if isinstance(obj, Transaction):
            return obj.__dict__
        else:
            return json.JSONEncoder.default(self, obj)
            # return super(TransactionEncoder, self).default(obj)