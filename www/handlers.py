#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from norm import database, Query
from utils import hash_pwd

__author__ = 'Michael Liao'

' url handlers '

import re

from coroweb import get, post
from apis import Page, APIValueError, APIError

from apps.core.models import User, next_id


def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p


def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'),
                filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)


@post('/login')
async def api_post_login(*, name, password):
    rs = await User.findAll(where='name=? and passwd = ?', args=(name, hash_pwd(password)))
    if rs is not None and len(rs) == 1:
        return 200
    else:
        return 404


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
