#!/usr/bin/env python3
"""Static build for atlr.pro (Atelier Superintelligence).

  python3 build.py --base "" --origin https://atlr.pro --cname atlr.pro --out docs
      production: the custom domain, indexable

  python3 build.py --base /atlr-staging --origin https://atlr-frge.github.io --staging --out ../atlr-staging
      staging: GitHub Pages project path, noindex + robots Disallow

Reads src/, writes --out. Follows the aiimaginelabs build.py conventions:
layout.html + src/pages/*.html with a <!--meta {...}--> header, a JSON-LD
graph on every page, sitemap, robots, llms.txt, cache stamp on css/js.
"""
import argparse, datetime, hashlib, html, json, os, re, shutil, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'src')

ap = argparse.ArgumentParser()
ap.add_argument('--base', default=None, help='URL path prefix, "" for a custom domain')
ap.add_argument('--origin', default=None, help='scheme + host, no trailing slash')
ap.add_argument('--cname', default='', help='write a CNAME file with this host')
ap.add_argument('--out', default=None, help='output directory')
ap.add_argument('--staging', action='store_true', help='noindex every page and disallow robots')
args = ap.parse_args()
if args.base is None or args.origin is None or args.out is None:
    ap.error('pass --base, --origin and --out explicitly (see the docstring); there is no safe default')

BASE = args.base.rstrip('/')
ORIGIN = args.origin.rstrip('/')
OUT = os.path.abspath(os.path.join(ROOT, args.out))
SITE = ORIGIN + BASE
YEAR = str(datetime.date.today().year)
CSS = open(os.path.join(SRC, 'css', 'site.css'), 'rb').read()
JS = open(os.path.join(SRC, 'js', 'site.js'), 'rb').read()
V = hashlib.md5(CSS + JS).hexdigest()[:8]

ORG_NAME = 'Atelier Superintelligence'
POSITIONING = 'Bespoke agentic systems. Deep context. Real integrations. Results that compound.'
EMAIL = 'hello@atlr.pro'
LINKEDIN_MICHAEL = 'https://www.linkedin.com/in/chasemichael/'
LINKEDIN_SEAN = 'https://www.linkedin.com/in/seanthomasevans/'
MATERIALITY_URL = 'https://www.aiimaginelabs.com/materiality/'

layout = open(os.path.join(SRC, 'layout.html'), encoding='utf-8').read()

def ids():
    return {'org': SITE + '/#organization', 'site': SITE + '/#website',
            'michael': SITE + '/team/#michael', 'sean': SITE + '/team/#sean'}

def base_graph():
    i = ids()
    return [
        {'@type': 'Organization', '@id': i['org'], 'name': ORG_NAME, 'url': SITE + '/',
         'email': EMAIL, 'description': POSITIONING,
         'logo': {'@type': 'ImageObject', 'url': SITE + '/assets/img/og-default.jpg', 'width': 1200, 'height': 630},
         'address': {'@type': 'PostalAddress', 'addressLocality': 'Toronto', 'addressRegion': 'ON', 'addressCountry': 'CA'},
         'founder': [{'@id': i['michael']}, {'@id': i['sean']}],
         'contactPoint': {'@type': 'ContactPoint', 'email': EMAIL, 'contactType': 'sales', 'availableLanguage': 'en'},
         'knowsAbout': ['agentic systems', 'AI agents', 'financial crime compliance', 'media pipelines', 'generative production']},
        {'@type': 'WebSite', '@id': i['site'], 'url': SITE + '/', 'name': ORG_NAME, 'publisher': {'@id': i['org']}, 'inLanguage': 'en'},
        {'@type': 'Person', '@id': i['michael'], 'name': 'Michael Chase', 'jobTitle': 'Co-founder, strategy and adoption',
         'worksFor': {'@id': i['org']}, 'sameAs': [LINKEDIN_MICHAEL, 'https://www.aiimaginelabs.com/about/'],
         'url': SITE + '/team/#michael'},
        {'@type': 'Person', '@id': i['sean'], 'name': 'Sean Evans', 'jobTitle': 'Co-founder, engineering and production',
         'worksFor': {'@id': i['org']}, 'sameAs': [LINKEDIN_SEAN], 'url': SITE + '/team/#sean'},
    ]

def graph_for(meta, canonical):
    g = base_graph()
    page = {'@type': meta.get('schema_type', 'WebPage'), '@id': canonical + '#webpage', 'url': canonical,
            'name': meta['title'], 'description': meta['desc'], 'isPartOf': {'@id': ids()['site']},
            'about': {'@id': ids()['org']}, 'inLanguage': 'en'}
    g.append(page)
    if meta['path'] != '/':
        g.append({'@type': 'BreadcrumbList', '@id': canonical + '#breadcrumb', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': meta.get('crumb', meta['title'].split('|')[0].strip()), 'item': canonical}]})
    for extra in meta.get('jsonld_extra', []):
        g.append(extra)
    return {'@context': 'https://schema.org', '@graph': g}

def page_lastmod(src_file):
    try:
        out = subprocess.check_output(['git', 'log', '-1', '--format=%cs', '--', src_file], cwd=ROOT, text=True).strip()
        if out:
            return out
    except Exception:
        pass
    return datetime.date.today().isoformat()

def render(body, meta):
    path = meta['path']
    canonical = SITE + (path if path.endswith('/') or path.endswith('.html') else path + '/')
    og_image = SITE + meta.get('og_image', '/assets/img/og-default.jpg')
    head_extra = ''
    if meta.get('noindex') or args.staging:
        head_extra += '<meta name="robots" content="noindex">\n'
    for pl in meta.get('preload', []):
        head_extra += '<link rel="preload" as="image" href="%s%s" fetchpriority="high"%s>\n' % (BASE, pl['href'], (' media="%s"' % pl['media']) if pl.get('media') else '')
    if meta.get('jsonld', True):
        head_extra += '<script type="application/ld+json">%s</script>\n' % json.dumps(graph_for(meta, canonical), ensure_ascii=False, separators=(',', ':'))
    out = layout
    out = out.replace('{{TITLE}}', html.escape(meta['title'], quote=True))
    out = out.replace('{{DESC}}', html.escape(meta['desc'], quote=True))
    out = out.replace('{{CANONICAL}}', canonical if not meta.get('no_canonical') else '')
    out = out.replace('{{OG_IMAGE}}', og_image)
    out = out.replace('{{OG_TYPE}}', meta.get('og_type', 'website'))
    out = out.replace('{{HEAD_EXTRA}}', head_extra)
    out = out.replace('{{BODY_CLASS}}', meta.get('body_class', ''))
    out = out.replace('{{BODY}}', body)
    for nav in ['home', 'work', 'method', 'team', 'materiality', 'contact']:
        out = out.replace('{{ACTIVE_%s}}' % nav, 'aria-current="page"' if meta.get('nav') == nav else '')
    out = out.replace('{{ORIGIN}}', ORIGIN).replace('{{BASE}}', BASE).replace('{{V}}', V).replace('{{YEAR}}', YEAR)
    if meta.get('no_canonical'):
        out = out.replace('<link rel="canonical" href="">\n', '').replace('<meta property="og:url" content="">\n', '')
    return out

def write(rel, content):
    fp = os.path.join(OUT, rel.lstrip('/'))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    mode = 'wb' if isinstance(content, bytes) else 'w'
    with open(fp, mode, encoding=None if mode == 'wb' else 'utf-8') as f:
        f.write(content)

def parse_page(fp):
    raw = open(fp, encoding='utf-8').read()
    m = re.match(r'\s*<!--meta\s+(\{.*?\})\s*-->\s*', raw, re.S)
    if not m:
        raise SystemExit('missing <!--meta {...}--> header in ' + fp)
    return json.loads(m.group(1)), raw[m.end():]

# ---------- clean output (keep the .git of a sibling staging checkout) ----------
os.makedirs(OUT, exist_ok=True)
for name in os.listdir(OUT):
    if name == '.git':
        continue
    p = os.path.join(OUT, name)
    shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)

# ---------- assets + static ----------
shutil.copytree(os.path.join(SRC, 'assets'), os.path.join(OUT, 'assets'))
os.makedirs(os.path.join(OUT, 'assets', 'css'), exist_ok=True)
os.makedirs(os.path.join(OUT, 'assets', 'js'), exist_ok=True)
write('/assets/css/site.css', CSS)
write('/assets/js/site.js', JS)
if os.path.isdir(os.path.join(SRC, 'static')):
    for name in os.listdir(os.path.join(SRC, 'static')):
        s = os.path.join(SRC, 'static', name); d = os.path.join(OUT, name)
        shutil.copytree(s, d) if os.path.isdir(s) else shutil.copy2(s, d)
write('/.nojekyll', '')
if args.cname:
    write('/CNAME', args.cname + '\n')

# ---------- pages ----------
pages = []
for fn in sorted(os.listdir(os.path.join(SRC, 'pages'))):
    if not fn.endswith('.html'):
        continue
    fp = os.path.join(SRC, 'pages', fn)
    meta, body = parse_page(fp)
    body = body.replace('{{BASE}}', BASE).replace('{{ORIGIN}}', ORIGIN)
    out_rel = meta['path'] if meta['path'].endswith('.html') else meta['path'].rstrip('/') + '/index.html'
    write(out_rel, render(body, meta))
    if not meta.get('noindex') and not meta['path'].endswith('.html'):
        pages.append({'loc': SITE + meta['path'], 'lastmod': page_lastmod(fp), 'priority': meta.get('priority', '0.7')})
    print('  wrote', out_rel)

# ---------- sitemap + robots ----------
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in sorted(pages, key=lambda x: (x['loc'] != SITE + '/', x['loc'])):
    sm.append('  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>' % (p['loc'], p['lastmod'], p['priority']))
sm.append('</urlset>\n')
write('/sitemap.xml', '\n'.join(sm))
if args.staging:
    write('/robots.txt', 'User-agent: *\nDisallow: /\n')
else:
    write('/robots.txt', 'User-agent: *\nAllow: /\n\nUser-agent: GPTBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % SITE)

# ---------- llms.txt ----------
llms = f"""# {ORG_NAME}

> {POSITIONING}

Atelier Superintelligence is a Toronto workshop that builds agentic systems inside a client's own cloud: agents that reason, keep memory and carry skills, working with autonomy under human oversight, with the points where people step in designed from the start. Founded by Michael Chase (strategy and adoption) and Sean Evans (engineering and production). Method: FORGE (Learn, Build, Prove, Stay). Contact: {EMAIL}.

## Pages
- Home: {SITE}/
- Work: {SITE}/work/ (selected systems 2024 to 2026 and the controls on every job)
- Method: {SITE}/method/ (the Forge Sprint and the four moves)
- Team: {SITE}/team/
- Materiality: {SITE}/materiality/ (the weekly series on AI with Verma Private Wealth at Canaccord Genuity, hosted by Michael Chase)
- Contact: {SITE}/contact/

## Facts
- Domains of work: financial crime, network television, music, film, a projection venue, a weekly series on AI.
- Five controls on every build: validation before use, human approval, an audit record, release control, data protection.
- Michael Chase hosts Materiality ({MATERIALITY_URL}) and writes the Monday Morning Mashup (https://www.aiimaginelabs.com/blog/).
"""
write('/llms.txt', llms)
print('built %d pages -> %s (base=%r origin=%s staging=%s v=%s)' % (len(pages), OUT, BASE, ORIGIN, args.staging, V))
