#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Models for user, blog, comment.
'''

__author__ = 'Michael Liao'

import time, uuid

from orm import Model, StringField, BooleanField, FloatField, TextField


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class User(Model):
    """Users"""
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)


class ContentField(Model):
    """Content Field"""
    __table__ = 'content_fields'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    content_model_id = StringField(ddl='varchar(50)')
    name = StringField(ddl='varchar(50)')
    title = StringField(ddl='varchar(50)')
    field_type = StringField(ddl='varchar(50)')
    created_at = FloatField(default=time.time)


class ContentModel(Model):
    """Content MOdel"""
    __table__ = 'content_models'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    name = StringField(ddl='varchar(50)')
    title = StringField(ddl='varchar(50)')
    created_at = FloatField(default=time.time)


class Content(Model):
    """Content"""
    __table__ = 'contents'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    field_id = StringField(ddl='varchar(50)')
    model_id = StringField(ddl='varchar(50)')
    value = TextField()
    created_at = FloatField(default=time.time)

class ContentType(Model):
    __table__ = 'content_types'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    name = StringField(ddl='varchar(50)')
    title = StringField(ddl='varchar(50)')
    created_at = FloatField(default=time.time)