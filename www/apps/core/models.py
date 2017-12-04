#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Models for user, blog, comment.
"""
from datetime import datetime

from dbs import BaseModel

__author__ = 'Michael Liao'

from peewee import CharField, TextField, ForeignKeyField, FloatField, UUIDField, DateTimeField


class User(BaseModel):
    """Users"""
    id = UUIDField(primary_key=True)
    password = CharField()
    name = CharField()
    created_at = DateTimeField(default=datetime.now)


class UserProfile(BaseModel):
    id = UUIDField(primary_key=True)
    user = ForeignKeyField(User, related_name='user')
    email = CharField()
    nick_name = CharField()
    image = CharField()
    phone = CharField()
    created_at = DateTimeField(default=datetime.now)


class Settings(BaseModel):
    """Site"""
    id = UUIDField(primary_key=True)
    key = CharField()
    value = TextField()
    created_at = DateTimeField(default=datetime.now)


class Article(BaseModel):
    id = UUIDField(primary_key=True)
    user = ForeignKeyField(User, related_name='articles')
    created_at = DateTimeField(default=datetime.now)


class PostRecord(BaseModel):
    id = UUIDField(primary_key=True)
    article = ForeignKeyField(Article, related_name='posts')
    content = TextField()
    created_at = DateTimeField(default=datetime.now)


class Tag(BaseModel):
    id = UUIDField(primary_key=True)
    content = TextField()
    created_at = DateTimeField(default=datetime.now)


class ArticleTagMapping(BaseModel):
    id = UUIDField(primary_key=True)
    blog = ForeignKeyField(Article)
    tag = ForeignKeyField(Tag)
    created_at = DateTimeField(default=datetime.now)
