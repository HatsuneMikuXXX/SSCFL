def initialize_dict(keys, value):
    res = dict({})
    n = len(keys)
    for i in range(n):
        if isinstance(value, list):
            res[keys[i]] = value.copy()
        else:
            res[keys[i]] = value
    return res
    