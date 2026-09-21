"""Generate a Quarto site from the canonical book Markdown without editing it."""
import hashlib
import html
import importlib.util
import json
import os
import re
import shutil
from pathlib import Path
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parent
OUT = HERE / 'build'
spec = importlib.util.spec_from_file_location('chapters', ROOT / '维护工具/tools/build_chapters.py')
chapters = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chapters)


def title(path):
    match = re.search(r'^#{1,6}\s+(.+)$', path.read_text(encoding='utf-8-sig'), re.M)
    if not match:
        raise ValueError(f'Missing title: {path}')
    return match[1].strip()


def generate():
    dirs = [ROOT/'前言', *sorted(ROOT.glob('第*章-*')), ROOT/'附录A-错误处理', ROOT/'实验']
    names = {d.name: ('preface' if d.name == '前言' else 'appendix' if d.name.startswith('附录') else 'labs' if d.name == '实验' else 'chapter-'+d.name[1:3]) for d in dirs}
    sources = sorted([p for d in dirs for p in d.rglob('*.md')] + [ROOT/'README.md', ROOT/'参考文献.md', ROOT/'答案编校说明.md'])
    opening = ROOT/'第01章-计算机系统漫游/1.1/1.0-chapter-opening.md'
    mapping = {}
    for p in sources:
        rel = p.relative_to(ROOT)
        if p == opening:
            target = Path('index.qmd')
        elif len(rel.parts) == 1:
            target = Path({'README.md':'guide.qmd','参考文献.md':'bibliography.qmd','答案编校说明.md':'editorial.qmd'}[p.name])
        else:
            target = Path(names[rel.parts[0]], *rel.parts[1:]).with_suffix('.qmd')
            if p.name in ('README.md','练习题答案.md'):
                target = target.with_name('index.qmd' if p.name == 'README.md' else 'answers.qmd')
        mapping[p.resolve()] = target
    if OUT.exists():
        if OUT.resolve().parent != HERE:
            raise ValueError('Unexpected output directory')
        shutil.rmtree(OUT)
    OUT.mkdir()
    assets = {}
    manifest = []
    for source, dest in mapping.items():
        text = source.read_text(encoding='utf-8-sig')
        seen = {}

        def transform(line):
            def link(match):
                raw = match[2].strip('<>')
                u = urlsplit(raw)
                if u.scheme or u.netloc or not u.path:
                    return match[0]
                resolved = (source.parent/unquote(u.path)).resolve()
                resolved.relative_to(ROOT)
                if resolved in mapping:
                    target = mapping[resolved]
                elif resolved.is_file():
                    target = Path('assets')/resolved.relative_to(ROOT)
                    assets[resolved] = target
                else:
                    raise ValueError(f'Unresolved link {source}: {raw}')
                url = Path(os.path.relpath(target, dest.parent)).as_posix()
                if u.fragment:
                    url += '#'+unquote(u.fragment)
                if match[1].startswith('!'):
                    # Raw images preserve alt text without Quarto inventing captions.
                    alt = match[1][2:-2]
                    return f'<img src="{html.escape(url, quote=True)}" alt="{html.escape(alt, quote=True)}">'
                return match[1]+'<'+url+'>'+match[3]
            line = chapters.LINK.sub(link, line)
            h = re.match(r'^(#{1,6})\s+(.+?)\s*$', line)
            if h:
                slug = chapters.heading_slug(h[2])
                count = seen.get(slug, 0)
                seen[slug] = count+1
                ident = slug if count == 0 else f'{slug}-{count}'
                line = f'{h[1]} {h[2]} {{#{ident}}}\n'
            return line

        first_heading = re.search(r'^(#{1,6})\s+', text, re.M)
        text = chapters.shift_headings(text, 1-len(first_heading[1]))
        body = chapters.outside_fences(text, transform)
        meta = {'title':title(source),'execute':{'enabled':False}}
        if source.name == 'chapter.md':
            meta.update({'search':False,'page-navigation':False})
        page = OUT/dest
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text('---\n'+json.dumps(meta, ensure_ascii=False)+'\n---\n\n'+body, encoding='utf-8')
        manifest.append({'source':source.relative_to(ROOT).as_posix(),'page':dest.as_posix(),'sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
    for source, dest in assets.items():
        (OUT/dest).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, OUT/dest)

    def entry(p, label=None):
        return {'href':mapping[p.resolve()].as_posix(),'text':label or title(p)}
    contents = []
    for d in dirs:
        index = d/'README.md'
        if d.name == '实验':
            refs = [p for p in sorted(d.rglob('*.md')) if p != index]
        else:
            refs = [(d/unquote(urlsplit(r).path)).resolve() for r in chapters.section_links(index.read_text(encoding='utf-8-sig'))]
            if (d/'练习题答案.md').exists():
                refs.append(d/'练习题答案.md')
        contents.append({'section':title(index),'href':mapping[index.resolve()].as_posix(),'contents':[entry(p) for p in refs]})
    contents.extend([entry(ROOT/'参考文献.md'),entry(ROOT/'答案编校说明.md')])
    config = {
        'project':{'type':'website','output-dir':'_site','resources':['assets/**']},
        'lang':'zh', 'from':'markdown-smart-implicit_figures', 'execute':{'enabled':False},
        'website':{
            'title':'CSAPP 中文阅读',
            'site-url':'https://sunnymaria.github.io/csapp-zh-markdown/',
            'page-navigation':True,
            'search':{'location':'navbar','type':'overlay'},
            'navbar':{'title':'CSAPP 中文阅读','left':[{'text':'正文','href':'index.qmd'}, {'text':'实验','href':'labs/index.qmd'}, {'text':'关于','href':'guide.qmd'}], 'right':[{'icon':'github','href':'https://github.com/SunnyMaria/csapp-zh-markdown','aria-label':'GitHub 仓库'}]},
            'sidebar':{'style':'docked','collapse-level':1,'contents':contents},
            'page-footer':{'left':'深入理解计算机系统 · 第三版', 'right':[{'text':'GitHub','href':'https://github.com/SunnyMaria/csapp-zh-markdown'}]},
        },
        'format':{'html':{'theme':{'light':'cosmo','dark':'darkly'},'css':'styles.css','toc':True,'toc-title':'本页目录','toc-depth':3,'number-sections':False,'code-copy':True,'code-overflow':'scroll','anchor-sections':True,'smooth-scroll':True,'link-external-newwindow':True}},
    }
    (OUT/'_quarto.yml').write_text(json.dumps(config,ensure_ascii=False,indent=2),encoding='utf-8')
    shutil.copy2(HERE/'styles/reader.css',OUT/'styles.css')
    (OUT/'manifest.json').write_text(json.dumps({'pages':manifest,'assets':{p.relative_to(ROOT).as_posix():v.as_posix() for p,v in assets.items()}},ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Generated {len(mapping)} pages and copied {len(assets)} assets; book sources unchanged.')


if __name__ == '__main__':
    generate()
