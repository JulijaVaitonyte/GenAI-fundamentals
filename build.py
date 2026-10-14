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
            action = resource.get('action', 'Watch video' if resource['type'] == 'Video' else 'Open PDF')
            caption = f'<p class="resource-caption">{text(resource["caption"])}</p>' if resource.get('caption') else ''
            cards.append(f'''<div class="resource-item">{caption}<a class="resource" href="{text(url)}" target="_blank" rel="noopener noreferrer" aria-label="{text(action)}: {text(resource['title'])} (opens in a new tab)">{text(action)} <span aria-hidden="true">↗</span></a></div>''')
        sections.append(f'''<details id="{text(sid)}"><summary><span class="number">0{number}</span><h2>{text(section['title'])}</h2><span class="plus" aria-hidden="true">+</span></summary>
        <div class="content"><p class="intro">{text(section['intro'])}</p><div class="resources">{''.join(cards)}</div></div></details>''')
    template = (ROOT / 'template.html').read_text(encoding='utf-8')
    for key, value in {'TITLE':text(data['title']).replace('generative AI', '<span class="keep-together">generative AI</span>'), 'SUBTITLE':text(data['subtitle']), 'NAV':''.join(nav), 'SECTIONS':''.join(sections)}.items():
        template = template.replace('{{'+key+'}}', value)
    (ROOT / 'index.html').write_text(template, encoding='utf-8')
    (ROOT / '.nojekyll').touch()
    print(f'Built {ROOT / "index.html"}')

if __name__ == '__main__':
    build()
