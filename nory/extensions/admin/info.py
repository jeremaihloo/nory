__author__ = 'jeremaihloo'

__version__ = '0.0.1'

__description__ = 'plugin manager'

__home_page__ = 'https://github.com/jeremaihloo/ncms-plugin-manager'

INDEXS = [
    'handlers',
    'message'
]

static = {
    'static':'static',
    'adminify/static':'adminify/dist/static'
}

dependency = [
    'welcome',
    'rbacm',
    'auth_cookie'
]