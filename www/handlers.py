#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from utils import hash_pwd

__author__ = 'Michael Liao'

' url handlers '

import re

from coroweb import get, post
from apis import Page, APIValueError, APIError

from apps.core.models import User


@post('/login')
async def api_post_login(*, name, password):
    user = User.select().where(User.name == name, User.password == password)
    if user.exists():
        user = user.get()
    return user


@get('/api/users')
async def api_get_users(*, page='1'):
    page_index = get_page_index(page)
    num = await User.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, users=())
    users = await User.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    for u in users:
        u.passwd = '******'
    return dict(page=p, users=users)


_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')


@post('/api/users')
async def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd:
        raise APIValueError('passwd')
    users = await User.findAll('email=?', [email])
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()

    user = User(id=uid,
                name=name.strip(),
                email=email,
                passwd=hash_pwd(passwd))
    async with await database.atomic() as db:
        db.create(user)

    user.passwd = '******'

    return user


async def api_login(*, name, passwd):
    q = Query().select(User).where(User.name == name & User.passwd == passwd).one()
    async with await database.atomic() as db:
        user = db.select(q)
    return 200 if user else 404
