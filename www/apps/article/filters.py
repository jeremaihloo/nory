import time
import datetime
import events
import markdown

from app_cores import feature


@feature(events.__FEATURE_TEMPLATE_FILTER__, 'datetime', 'datetime friendly filter')
def filter_datetime(t: datetime.datetime):
    delta = (datetime.datetime.now() - t).seconds
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)


@feature(events.__FEATURE_TEMPLATE_FILTER__, 'md', 'markdown it')
def filter_md(t):
    return markdown.markdown(t, ['markdown.extensions.tables',
                                 'pymdownx.magiclink',
                                 'pymdownx.betterem',
                                 'pymdownx.tilde',
                                 'pymdownx.emoji',
                                 'pymdownx.tasklist',
                                 'pymdownx.superfences'])
