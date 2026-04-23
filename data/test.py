
class A:
    def get(self, json_path: str, default=None):
        """通过点号路径获取嵌套字段，例如 'data.user.token'"""
        data = self.json()
        keys = json_path.split('.')
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key, default)
            else:
                return default
        return data

    def json(self):
        return  {'data': {'user': {'token': '<PASSWORD>'}}}

a = A()
b = a.get('data.user.token')
print(b)
