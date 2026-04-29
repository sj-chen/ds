import bcrypt


class Encrypt:
    @staticmethod
    def hash_password( plain_password: str, rounds: int = 10) -> str:
        """
        将明文密码加密为 bcrypt 哈希字符串
        :param plain_password: 明文密码，如 "Test@123456"
        :param rounds: 成本因子，默认 10（迭代 2^10 次），越大越安全但越慢
        :return: bcrypt 哈希字符串，如 "$2a$10$..."
        """
        hashed = bcrypt.hashpw(
            plain_password.encode('utf-8'),    # 明文 → bytes
            bcrypt.gensalt(rounds=rounds)       # 生成随机盐
        )
        return hashed.decode('utf-8')           # bytes → str

    def check_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))