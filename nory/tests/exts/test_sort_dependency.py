from infras.exts.dependency import sort_app_dependency


def test_sort_dependency():
    """
    A -->G
    A -->D
    A -->G
    B -->C
    D -->B
    D -->E
    F -->E
    G -->F
    B -->G
    :return:
    """
    maps = [('A', 'G'), ('A', 'D'), ('A', 'G'), ('B', 'C'), ('D', 'B'), ('D', 'E'), ('F', 'E'), ('G', 'F'), ('B', 'G')]
    rs = sort_app_dependency(maps)
    print(rs)
    assert rs is not None
    assert len(rs) == 7
