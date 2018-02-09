import logging

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


def sort_app_info_by_dependency(app_infos):
    maps = []
    for item in app_infos:
        for dep in item.dependency:
            maps.append((item, dep))
    logging.info('dependency mappings:{}'.format(maps))
    sorted_deps = sort_app_dependency(maps)

    def get_info_by_name(name):
        for item in app_infos:
            if name == item.name:
                return item
        return None

    not_need_to_sorted = list(filter(lambda x: x.name not in sorted_deps, app_infos))
    sorted_app_info = [get_info_by_name(x) for x in sorted_deps]
    not_need_to_sorted.extend(sorted_app_info)
    return [x for x in not_need_to_sorted if x is not None]
