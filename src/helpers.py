def nested_set(d: dict, key_path, value):
    for key in key_path[:-1]:
        d = d.setdefault(key, {})
    d[key_path[-1]] = value