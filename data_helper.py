# For dictionaries that have lists as values. Prevent invalid index access error.
def initialize_dict(keys, value):
    res = dict({})
    n = len(keys)
    for i in range(n):
        if isinstance(value, list):
            res[keys[i]] = value.copy()
        else:
            res[keys[i]] = value
    return res

def powerset(L):
	res = []
	n = len(L)
	for i in range(1 << n):
		res.append([L[j] for j in range(n) if (i & (1 << j))])
	res.sort()
	return res
    