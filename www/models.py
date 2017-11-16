#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Models for user, blog, comment.
'''

__author__ = 'Michael Liao'

import time, uuid

from orm import Model, StringField, BooleanField, FloatField, TextField, execute, select


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class User(Model):
    """Users"""
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    name = StringField(ddl='varchar(50)')
    created_at = FloatField(default=time.time)


class UserProfile(Model):
    __table__ = 'user_profiles'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    nick_name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    phone = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)


class ContentType(Model):
    """Content Type"""
    __table__ = 'content_types'

    name = StringField(primary_key=True, ddl='varchar(50)')
    title = StringField(ddl='varchar(50)')
    created_at = FloatField(default=time.time)


class ContentField(Model):
    """Content Field"""
    __table__ = 'content_fields'

    name = StringField(primary_key=True, ddl='varchar(50)')
    title = StringField(ddl='varchar(50)')
    content_type = StringField(ddl='varchar(50)')
    created_at = FloatField(default=time.time)


class ContentModel(Model):
    """Content Model"""
    __table__ = 'content_models'

    name = StringField(primary_key=True, ddl='varchar(50)')
    title = StringField(ddl='varchar(50)')
    created_at = FloatField(default=time.time)


class ContentModelField(Model):
    """Content Field"""
    __table__ = 'content_model_fields'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    model = StringField(ddl='varchar(50)')
    content_field = StringField(ddl='varchar(50)')
    created_at = FloatField(default=time.time)


class Content(Model):
    """Content"""
    __table__ = 'contents'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    created_at = FloatField(default=time.time)


class ContentItem(Model):
    """Content"""
    __table__ = 'content_items'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    model = StringField(ddl='varchar(50)')
    model_field_id = StringField(ddl='varchar(50)')
    content_id = StringField(ddl='varchar(50)')
    value = TextField()
    created_at = FloatField(default=time.time)


class Settings(Model):
    """Site"""
    __table__ = 'settings'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    key = StringField(ddl='varchar(50)')
    value = TextField()
    created_at = FloatField(default=time.time)

    def get(self, key):
        settings = Settings.query().all()