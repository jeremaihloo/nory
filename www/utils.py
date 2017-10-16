import os


def get_ncms_path():
    cwd = os.getcwd()
    cwd = os.path.abspath(cwd)
    cwd = cwd[:cwd.find('ncms/www') + 8]
    return cwd

class DictClass(dict):

    def __getattr__(self, item):
        if self.get(item, None) is None:
            raise KeyError('{} key not exist !'.format(item))
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value