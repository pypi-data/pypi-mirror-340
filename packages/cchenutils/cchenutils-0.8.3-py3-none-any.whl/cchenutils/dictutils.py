import json


class Dict(dict):
    def __init__(self, iterable, **kwargs):
        if isinstance(iterable, list):
            iterable = {str(i): value for i, value in enumerate(iterable)}
        super().__init__(iterable, **kwargs)

    def path(self, key, default=None):
        # nested get
        if '/' in key:
            k1, k2 = key.split('/', 1)
            return self.__class__(self[k1]).path(k2, default) if k1 in self else None
        else:
            return self.__class__(self[key]) if isinstance(self.get(key), (dict, Dict)) else self.get(key, default)

    def gets(self, keys, default=None):
        # nested gets
        if default is None:
            default = {}
        return [json.dumps(val)
                if isinstance(val := self.path(k, default.get(k)), (dict, list, Dict))
                else val
                for k in keys]

    # @property
    # def __class__(self):
    #     return super().__class__()
