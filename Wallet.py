import base64
import binascii
from hashlib import sha256
# 导入椭圆曲线算法
from ecdsa import SigningKey, SECP256k1, VerifyingKey


class Wallet:
    """
        钱包
    """

    def __init__(self):
        """
            钱包初始化时基于椭圆曲线生成一个唯一的秘钥对，代表区块链上一个唯一的账户
        """
        # 生成私钥
        self._private_key = SigningKey.generate(curve=SECP256k1)
        # 基于私钥生成公钥
        self._public_key = self._private_key.get_verifying_key()

    @property
    def address(self):
        """
            这里通过公钥生成地址
        """
        h = sha256(self._public_key.to_pem())
        # 地址先由公钥进行哈希算法，再进行 Base64 计算而成
        return base64.b64encode(h.digest())

    @property
    def pubkey(self):
        """
            返回公钥字符串
        """
        return self._public_key.to_pem()

    def sign(self, message):
        """
            生成数字签名
        """
        h = sha256(message.encode('utf8'))
        # 利用私钥生成签名
        # 签名生成的是一串二进制字符串，为了便于查看，这里转换为 ASCII 字符串进行输出
        return binascii.hexlify(self._private_key.sign(h.digest()))


def verify_sign(pubkey, message, signature):
    """
        验证签名
    """
    verifier = VerifyingKey.from_pem(pubkey)
    h = sha256(message.encode('utf8'))
    return verifier.verify(binascii.unhexlify(signature), h.digest())