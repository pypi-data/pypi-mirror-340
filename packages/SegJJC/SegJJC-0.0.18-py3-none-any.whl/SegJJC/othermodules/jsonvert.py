class CaseInsensitiveDict(dict):
    """
    不区分大小写的字典，支持嵌套结构
    可以使用任意大小写的键访问
    """

    def __init__(self, d=None):
        super().__init__()
        if d is None:
            d = {}
        self._convert_dict(d)

    def _convert_dict(self, d):
        for k, v in d.items():
            if isinstance(v, dict):
                # 递归处理嵌套字典
                self[k] = CaseInsensitiveDict(v)
            elif isinstance(v, list):
                # 处理列表，查找列表中的字典
                self[k] = [CaseInsensitiveDict(x) if isinstance(x, dict) else x for x in v]
            else:
                self[k] = v

    def __getitem__(self, key):
        # 尝试直接获取(优化性能)
        try:
            return super().__getitem__(key)
        except KeyError:
            # 不区分大小写查找
            key_lower = key.lower() if isinstance(key, str) else key
            for k in self.keys():
                if isinstance(k, str) and k.lower() == key_lower:
                    return super().__getitem__(k)
            raise KeyError(key)

    def __contains__(self, key):
        if super().__contains__(key):
            return True
        if isinstance(key, str):
            key_lower = key.lower()
            for k in self.keys():
                if isinstance(k, str) and k.lower() == key_lower:
                    return True
        return False

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default