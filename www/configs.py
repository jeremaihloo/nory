#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Configuration
'''
import json

__author__ = 'jeremaihloo'


class Config(object):
    def to_dict(self):
        return dict((name, getattr(self, name)) for name in dir(self) if not name.startswith('__'))


class MySqlConfig(Config):
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    password = 'root'
    db = 'ncms'


class NcmsConfig(Config):
    version = 1
    home_page = 'http://github.com/jeremaihloo/ncms'
    debug = False
    session = {'secret': 'Awesome'}
    db = MySqlConfig()


options = NcmsConfig()


def option_the_model(model: Config, configs: dict):
    attrs = list(filter(lambda x: not x.startswith('_'), dir(model)))
    for key in attrs:
        val = getattr(model, key, None)
        if isinstance(val, Config):
            setattr(model, key, option_the_model(val, configs[key]))
        else:
            setattr(model, key, val if configs.get(key, None) is None else configs[key])
    return model


def load_configs(config_path=None):
    with open(config_path) as f:
        obj = json.load(f)
        option_the_model(options, obj)
    return obj


def merge(defaults, override):
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r
