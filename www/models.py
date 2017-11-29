#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Models for user, blog, comment.
"""

__author__ = 'Michael Liao'

import time, uuid

from orm import Model, StringField, FloatField, TextField


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class User(Model):
    """Users"""
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    name = StringField(ddl='varchar(50)', unique=True)
    created_at = FloatField(default=time.time)


class UserProfile(Model):
    __table__ = 'user_profiles'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    email = StringField(ddl='varchar(50)', unique=True)
    nick_name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    phone = StringField(ddl='varchar(500)', unique=True)
    created_at = FloatField(default=time.time)


class Settings(Model):
    """Site"""
    __table__ = 'settings'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    key = StringField(ddl='varchar(50)', unique=True)
    value = TextField()
    created_at = FloatField(default=time.time)

    def get(self, key):
        settings = Settings.query().all()