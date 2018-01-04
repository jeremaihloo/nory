def get_markdown_h1(content):
    cs = content.split('\n')
    for item in cs:
        if item.startswith('# '):
            return item[1:]
    return "I don't have a Title"
