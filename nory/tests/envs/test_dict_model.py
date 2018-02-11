class Dict(dict):
    '''
    Simple dict but support access as x.y style.
    '''
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value



def test_setting_value_from_dict():

    d = Dict()
    d['url'] == '111'
    print(d)
    assert d.url == '111'

def test_setting_value_from_attr():
    d = Dict()
    d.url = '111'
    assert d.url == '111'
    assert d['url'] == '111'