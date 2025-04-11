import base64
import random
import time


class XORException(Exception):
    pass


Expired = XORException("Token Expired")
Invalid = XORException("Token Invalid")


class SimpleXOR:
    def __init__(self, secret_key=None):
        """
        初始化Token管理器
        :param secret_key: 密钥，用于加密解密
        """
        if secret_key is None:
            secret_key = random.getrandbits(128)
        self.secret_key = secret_key

    def _xor_encrypt(self, data):
        """
        使用异或加密算法对数据进行加密/解密
        :param data: 输入的整数数据
        :return: 加密后的整数数据
        """
        encrypted = data ^ self.secret_key  # 将数据与密钥进行异或运算
        return encrypted

    def generate(self, expire_date):
        """
        :param expire_date: 过期日期（格式：YYYY-MM-DD HH:MM:SS）
        :return: 生成的Token
        """
        # 将日期转换为时间戳（秒级）
        time_struct = time.strptime(expire_date, "%Y-%m-%d %H:%M:%S")
        timestamp = int(time.mktime(time_struct))

        # 使用异或加密时间戳
        encrypted_timestamp = self._xor_encrypt(timestamp)

        # 将加密后的数据转换为16位的Base64字符串
        token = base64.urlsafe_b64encode(encrypted_timestamp.to_bytes(16, byteorder="big")).decode("utf-8")
        return token

    def validate(self, token):
        """
        验证Token是否有效
        :param token: 需要验证的Token
        :return: 是否有效（布尔值）以及过期日期
        """

        padded_token = token + "=="  # Base64解码时需要补齐=号
        encrypted_timestamp = int.from_bytes(base64.urlsafe_b64decode(padded_token), byteorder="big")

        # 使用异或解密获取原始时间戳
        original_timestamp = self._xor_encrypt(encrypted_timestamp)

        try:
            # 获取Date对应的时间戳
            expire_date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(original_timestamp))
        except OverflowError:
            return False, Invalid

        # 检查当前时间是否超过过期时间
        current_timestamp = time.time()
        if current_timestamp > original_timestamp:
            return False, Expired
        return True, expire_date
