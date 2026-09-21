"""Check source integrity and all generated HTML's local links and images."""
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parents[1]
SITE = HERE/'build/_site'


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.refs = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for key in ('src','href'):
            if key in attrs:
                self.refs.append(attrs[key])


def main():
    manifest = json.loads((HERE/'build/manifest.json').read_text(encoding='utf-8'))
    errors = []
    for entry in manifest['pages']:
        source = HERE.parent/entry['source']
        if hashlib.sha256(source.read_bytes()).hexdigest() != entry['sha256']:
            errors.append(f'Source changed since generation: {source}')
        if not (SITE/Path(entry['page']).with_suffix('.html')).is_file():
            errors.append(f'Page missing: {entry["page"]}')
    pages = {p.resolve():Page(p.read_text(encoding='utf-8')) for p in SITE.rglob('*.html')}
    refs = 0
    for path, page in pages.items():
        for ref in page.refs:
            parsed = urlsplit(ref)
            if parsed.scheme or parsed.netloc:
                continue
            target = (path.parent/unquote(parsed.path)).resolve() if parsed.path else path
            if parsed.path.startswith('/'):
                target = (SITE/unquote(parsed.path).removeprefix('/csapp-zh-markdown/').lstrip('/')).resolve()
            if target.is_dir():
                target = target/'index.html'
            refs += 1
            if not target.exists():
                errors.append(f'{path.relative_to(SITE)}: missing {ref}')
            elif parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
                errors.append(f'{path.relative_to(SITE)}: missing anchor {ref}')
    for source, asset in manifest['assets'].items():
        target = SITE/asset
        if not target.is_file() or hashlib.sha256(target.read_bytes()).digest() != hashlib.sha256((HERE.parent/source).read_bytes()).digest():
            errors.append(f'Asset missing or changed: {asset}')
    (HERE/'build/check-report.json').write_text(json.dumps({'pages':len(pages),'references':refs,'errors':errors},ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{len(pages)} HTML pages, {refs} local references, {len(errors)} errors')
    for error in errors[:30]:
        print(error)
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
