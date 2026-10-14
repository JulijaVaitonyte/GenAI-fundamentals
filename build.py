#!/usr/bin/env python3
"""Generate the GitHub Pages site. Python 3.9+; no packages required."""
import json
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent

def text(value):
    return escape(str(value), quote=True)

def build():
    data = json.loads((ROOT / 'resources.json').read_text(encoding='utf-8'))
    sections = []
    nav = []
    seen = set()
    for number, section in enumerate(data['sections'], 1):
        sid = section['id']
        if not sid or not all(c.isalnum() or c == '-' for c in sid) or sid in seen:
            raise ValueError('Section IDs must be unique letters, numbers or hyphens')
        seen.add(sid)
        nav.append(f'<a href="#{text(sid)}"><span>0{number}</span>{text(section["title"])}<b aria-hidden="true">↗</b></a>')
        cards = []
        for resource in section['resources']:
            url = resource['url']
            parsed = urlsplit(url)
            if parsed.scheme != 'https':
                if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith('/'):
                    raise ValueError(f'Unsupported URL: {url}')
                local = (ROOT / parsed.path).resolve()
                if ROOT not in local.parents or not local.is_file():
                    raise ValueError(f'Missing or unsafe local resource: {url}')
            cards.append(f'''<a class="resource" href="{text(url)}" target="_blank" rel="noopener noreferrer">
            <span class="type">{text(resource['type'])}</span><div><p class="meta">{text(resource['meta'])}</p>
            <h3>{text(resource['title'])}</h3><p>{text(resource['description'])}</p>
            <span class="action">{'Watch video' if resource['type']=='Video' else 'Open PDF'} <span aria-hidden="true">↗</span><span class="sr"> (opens in a new tab)</span></span></div></a>''')
        sections.append(f'''<details id="{text(sid)}"><summary><span class="number">0{number}</span><span><small>{text(section['label'])}</small><h2>{text(section['title'])}</h2></span><span class="plus" aria-hidden="true">+</span></summary>
        <div class="content"><p class="intro">{text(section['intro'])}</p><div class="resources">{''.join(cards)}</div>
        <aside><strong>Think about it</strong><p>{text(section['question'])}</p></aside></div></details>''')
    template = (ROOT / 'template.html').read_text(encoding='utf-8')
    for key, value in {'TITLE':text(data['title']), 'SUBTITLE':text(data['subtitle']), 'NAV':''.join(nav), 'SECTIONS':''.join(sections)}.items():
        template = template.replace('{{'+key+'}}', value)
    (ROOT / 'index.html').write_text(template, encoding='utf-8')
    (ROOT / '.nojekyll').touch()
    print(f'Built {ROOT / "index.html"}')

if __name__ == '__main__':
    build()
