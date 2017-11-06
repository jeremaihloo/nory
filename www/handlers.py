#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

' url handlers '

import re, time, json, logging, hashlib, base64, asyncio

import markdown2

from aiohttp import web

from coroweb import get, post
from apis import Page, APIValueError, APIResourceNotFoundError, APIPermissionError, APIError

from models import User, next_id, ContentField, ContentModel, ContentType, ContentItem, ContentModelField, Content
from config import configs


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
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')


@post('/api/users')
async def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    users = await User.findAll('email=?', [email])
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid,
                name=name.strip(),
                email=email,
                passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(),
                image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    await user.save()

    user.passwd = '******'

    return user


@post('/api/content-type')
async def api_create_content_type(*, name, title):
    fc = await ContentType.find(name)
    if fc is not None:
        raise APIError(None, name, 'ContentType {} existed !'.format(name))
    field_type = ContentType()
    field_type.name = name
    field_type.title = title
    await field_type.save()
    return field_type


@post('/api/fields')
async def api_create_content_field(*, name, title, field_type):
    field = ContentField()
    field.name = name
    field.title = title
    field.content_type = field_type
    await field.save()
    return field


@post('/api/models')
async def api_create_content_model(*, name, title, fields):
    m = ContentModel()
    m.name = name
    m.title = title
    await m.save()

    for item in fields:
        f = ContentModelField()
        f.model = m.name
        f.content_field = item
        await f.save()
    return m


@post('/api/contents/{model_name}')
async def api_create_content(*, model_name, data):
    m = list(await ContentModel.find(model_name))
    if m is None or len(m) == 0:
        raise Exception('model not found ! model name : {}'.format(model_name))

    m = m[0]
    content = Content()
    content.model = model_name
    await content.save()

    for field_type, field_value in data.items():
        """
        data = 
            {
                'content':'hello world !'
            }
        """
        f = list(
            await ContentModelField.findAll(where='model = ? and content_field = ?', args=(model_name, field_type)))
        if f is None or len(f) == 0:
            raise Exception('field not found ! field name : {}'.format(field_type))
        f = f[0]

        item = ContentItem()
        item.content_id = content.id
        item.value = field_value
        item.model_field_id = f.id
        item.model = model_name
        await item.save()

    return m


@get('/api/contents/{model_name}/{page_size}/{page_index}')
async def api_get_contents(*, model_name, page_index=1, page_size=15):
    contents = await ContentItem.findAll(where='model = ?', args=(model_name,))
    results = {}
    for line in contents:
        if results.get(line.content_id, None) is None:
            results[line.content_id] = {}
        content_model_field = await ContentModelField.find(line['model_field_id'])
        results[line.content_id][content_model_field.content_field] = line['value']
    return results
