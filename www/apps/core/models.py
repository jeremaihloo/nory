#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Models for user, blog, comment.
"""

__author__ = 'Michael Liao'

import time, uuid
from utils import next_id
from norm import Model, StringField, FloatField, TextField, OneField, ForeignField


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


class Blog(Model):
    __table__ = 'blog'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user = StringField(ddl='varchar(50)')
    created_at = FloatField(default=time.time)


class PostRecord(Model):
    __table__ = 'post_record'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    content = TextField()
    created_at = FloatField(default=time.time)


class Tag(Model):
    __table__ = 'tags'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    content = TextField()
    created_at = FloatField(default=time.time)


class BlogTagMapping(Model):
    __table__ = 'blog_tag_mappings'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(ddl='varchar(50)')
    tag_id = StringField(ddl='varchar(50)')
    created_at = FloatField(default=time.time)
