__all_keys = []


def sort_app_dependency(maps: list, rs=[], min_set=set()):

    if len(maps) == 0:
        return rs

    maps = [(k, v) for k, v in maps if k not in min_set]

    keys = [x[0] for x in maps]
    keys.extend([x[1] for x in maps])
    keys = set(keys)

    global __all_keys
    if len(__all_keys) == 0:
        __all_keys = keys

    deps = set([x[1] for x in maps])
    min_set = set(__all_keys) - set(rs) - deps

    rs.extend(min_set)

    return sort_app_dependency(maps, rs, min_set)
