import redis
from common.file import load_setting

setting = load_setting()

class RedisClient:
    def __init__(self):
        r = redis.Redis(
            host= setting['redis']['HOST'],      # 测试环境 Redis 地址
            port=setting['redis']['PORT'],
            password=setting['redis']['PASSWORD'], # 测试专用密码
            decode_responses=True
        )
        self.redis = r

    def getAuth(self, telephone):
        authcode = self.redis.get(f"mall:ums:authCode:{telephone}")
        return authcode.strip().strip('"').strip("'")

    def close(self):
        self.redis.close()