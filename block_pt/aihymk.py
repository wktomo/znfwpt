from ecdsa import SigningKey, SECP256k1, VerifyingKey
import binascii
import json

class Wallet:
    def __init__(self):
        """
        初始化钱包，生成私钥和公钥。
        """
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()

    def sign_transaction(self, transaction):
        """
        使用私钥对交易数据进行签名。
        :param transaction: 交易数据，必须是可编码为字节的字符串。
        :return: 签名的十六进制字符串。
        """
        transaction_bytes = json.dumps(transaction, sort_keys=True).encode()
        signature = self.private_key.sign(transaction_bytes)
        return binascii.hexlify(signature).decode()

    def verify_signature(self, public_key_hex, signature_hex, transaction):
        """
        使用公钥验证签名的有效性。
        :param public_key_hex: 公钥的十六进制字符串。
        :param signature_hex: 签名的十六进制字符串。
        :param transaction: 交易数据，必须是可编码为字节的字符串。
        :return: 验证结果，布尔值。
        """
        try:
            public_key_bytes = binascii.unhexlify(public_key_hex)
            signature_bytes = binascii.unhexlify(signature_hex)
            transaction_bytes = json.dumps(transaction, sort_keys=True).encode()
            vk = VerifyingKey.from_string(public_key_bytes, curve=SECP256k1)
            return vk.verify(signature_bytes, transaction_bytes)
        except Exception as e:
            print(f"Error verifying signature: {e}")
            return False

    def get_public_key_hex(self):
        """
        获取公钥的十六进制字符串表示。
        :return: 公钥的十六进制字符串。
        """
        return binascii.hexlify(self.public_key.to_string()).decode()