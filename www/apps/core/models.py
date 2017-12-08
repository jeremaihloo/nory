#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Models for user, blog, comment.
"""
from datetime import datetime
from uuid import uuid4
from dbs import BaseModel
from peewee import CharField, TextField, ForeignKeyField, UUIDField, DateTimeField


class User(BaseModel):
    """Users"""
    id = UUIDField(primary_key=True, default=uuid4)
    password = CharField()
    name = CharField()
    created_at = DateTimeField(default=datetime.now)


class UserProfile(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    user = ForeignKeyField(User, related_name='profile')
    email = CharField()
    nick_name = CharField()
    image = CharField()
    phone = CharField()
    created_at = DateTimeField(default=datetime.now)


class Settings(BaseModel):
    """Site"""
    id = UUIDField(primary_key=True, default=uuid4)
    key = CharField()
    value = TextField()
    created_at = DateTimeField(default=datetime.now)


class Article(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    user = ForeignKeyField(User, related_name='articles')
    title = TextField()
    content = TextField()
    created_at = DateTimeField(default=datetime.now)


class Tag(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    content = CharField()
    created_at = DateTimeField(default=datetime.now)


class ArticleTagMapping(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    article = ForeignKeyField(Article, related_name='tags')
    tag = ForeignKeyField(Tag, related_name='tag')
    created_at = DateTimeField(default=datetime.now)
