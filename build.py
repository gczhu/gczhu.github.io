#!/usr/bin/env python3
"""Generate a dependency-free static academic homepage from content/*.json."""
import argparse
from pathlib import Path
import html, json, shutil

ROOT = Path(__file__).resolve().parent
esc = lambda value: html.escape(str(value), quote=True)

def link(text, url, **attrs):
    if not url:
        return esc(text)
    assert url.startswith(('https://', 'mailto:')), f'Unsafe URL: {url}'
    extra = ''.join(f' {esc(k)}="{esc(v)}"' for k, v in attrs.items())
    return f'<a href="{esc(url)}"{extra}>{esc(text)}</a>'

def render(profile, papers):
    if len({p['id'] for p in papers}) != len(papers):
        raise ValueError('Duplicate publication IDs')
    rows = []
    for p in papers:
        if profile['name'] not in p['authors']:
            raise ValueError(f'Author missing from {p["id"]}')
        authors = []
        for author in p['authors']:
            name = esc(author)
            if author == profile['name']:
                name = f'<strong>{name}</strong>'
            if author in p.get('equal_contributors', []):
                name += '<sup title="Equal contribution">*</sup>'
            authors.append(name)
        authors_html = ', '.join(authors)
        if len(authors) > 16:
            visible = ', '.join(authors[:8])
            authors_html = f'{visible}, et al. <details class="author-list"><summary>All authors</summary><p>{authors_html}</p></details>'
        actions = ''.join(link(a['label'], a['url']) for a in p['links'])
        rows.append(f'''<article class="paper" id="{esc(p['id'])}" data-selected="{str(p['selected']).lower()}">
          <div class="paper-content">
            <p class="venue">{esc(p['venue'])} {p['year']}</p>
            <h3>{link(p['title'], p['links'][0]['url'])}</h3>
            <div class="authors">{authors_html}</div>
            <div class="paper-actions">{actions}
              <details class="citation"><summary>bibtex</summary>
                <div class="citation-body"><pre id="bib-{esc(p['id'])}">{esc(p['bibtex'])}</pre>
                  <div class="citation-controls"><button type="button" class="copy-citation" data-copy="bib-{esc(p['id'])}" hidden>Copy citation</button><a href="citations/{esc(p['id'])}.bib" download>Download .bib</a></div>
                </div>
              </details>
            </div>
          </div>
        </article>''')
    advisers = ' and '.join(link(x['name'], x['url']) for x in profile['advisors'])
    if profile.get('portrait'):
        portrait = f'<img class="portrait" src="{esc(profile["portrait"])}" alt="{esc(profile.get("portrait_alt", profile["name"]))}" width="220" height="265">'
    else:
        portrait = '<div class="portrait monogram" role="img" aria-label="Guangcheng Zhu, initials GZ"><span>GZ</span></div>'
    social = [link('Email', 'mailto:' + profile['email'])]
    if profile.get('scholar'):
        social.append(link('Google Scholar', profile['scholar']))
    social.append(link('GitHub', profile['github']))
    education = ''.join(f'''<li><span class="education-date">{esc(e['period'])}</span><div><h3>{esc(e['institution'])}</h3><p>{esc(e['degree'])} · {esc(e['department'])}</p></div></li>''' for e in profile['education'])
    research_html = esc(profile['research'])
    for phrase in profile['research_highlights']:
        research_html = research_html.replace(esc(phrase), f'<strong>{esc(phrase)}</strong>')
    jsonld = json.dumps({'@context':'https://schema.org','@type':'Person','name':profile['name'],'alternateName':profile['name_zh'],'url':profile['url'],'email':profile['email'],'jobTitle':profile['role'],'affiliation':{'@type':'CollegeOrUniversity','name':profile['institution']},'sameAs':[url for url in (profile['github'], profile.get('scholar')) if url], 'knowsAbout':['Large language models', *profile['research_highlights']]},ensure_ascii=False).replace('<','\\u003c')
    return f'''<!doctype html>
<html lang="en" data-view="selected">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(profile['name'])} | {esc(profile['name_zh'])}</title>
  <meta name="description" content="Guangcheng Zhu (祝广程), a master’s student at Zhejiang University, working on large language models and data-efficient post-training.">
  <meta name="color-scheme" content="light">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Guangcheng Zhu | 祝广程">
  <meta property="og:description" content="Large language models · Data-efficient post-training · Zhejiang University">
  <meta property="og:url" content="{esc(profile['url'])}">
  <link rel="canonical" href="{esc(profile['url'])}">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/style.css">
  <script>document.documentElement.classList.add('js');</script>
  <script src="assets/site.js" defer></script>
  <script type="application/ld+json">{jsonld}</script>
</head>
<body>
  <a class="skip-link" href="#about">Skip to main content</a>
  <header class="topbar page">
    <a class="site-name" href="#top">{esc(profile['name'])}</a>
    <nav aria-label="Page navigation"><a href="#about">About</a><a href="#publications">Publications</a><a href="#education">Education</a></nav>
  </header>
  <main class="page" id="top">
    <section class="profile" id="about" aria-labelledby="profile-heading">
      <div class="portrait-wrap">{portrait}</div>
      <div class="profile-heading">
        <h1 id="profile-heading">{esc(profile['name'])} <span lang="zh-CN">{esc(profile['name_zh'])}</span></h1>
        <p class="affiliation">{esc(profile['department'])}<br>{esc(profile['institution'])}</p>
      </div>
      <div class="profile-bio">
        <p class="bio">I am a {esc(profile['role'].lower())} at {esc(profile['institution'])}, jointly advised by {advisers}. {research_html}</p>
        <div class="social-links">{''.join(social)}</div>
      </div>
    </section>

    <section class="content-section" id="publications" aria-labelledby="publications-heading">
      <div class="section-heading"><h2 id="publications-heading">Publications</h2>
        <div class="view-switch" role="group" aria-label="Publications to display" hidden>
          <button type="button" data-view-button="selected" aria-pressed="true">Selected</button><span aria-hidden="true">/</span><button type="button" data-view-button="all" aria-pressed="false">Full list ({len(papers)})</button>
        </div>
      </div>
      <p class="publication-note"><sup>*</sup> Equal contribution</p>
      <p class="sr-only" id="view-status" aria-live="polite"></p>
      <div class="publications">{''.join(rows)}</div>
    </section>

    <section class="content-section education" id="education" aria-labelledby="education-heading">
      <h2 id="education-heading">Education</h2>
      <ul>{education}</ul>
    </section>

  </main>
  <footer class="page site-footer"><span>© 2026 {esc(profile['name'])}</span><span>Last updated {esc(profile['updated'])}</span></footer>
</body>
</html>
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='.', help='Output directory, relative to the project root')
    args = parser.parse_args()
    out = (ROOT / args.output).resolve()
    out.mkdir(parents=True,exist_ok=True)
    profile = json.loads((ROOT/'content/profile.json').read_text())
    papers = json.loads((ROOT/'content/publications.json').read_text())
    papers.sort(key=lambda p: p.get('sort_date', str(p['year'])), reverse=True)
    if out != ROOT:
        shutil.copytree(ROOT/'assets',out/'assets',dirs_exist_ok=True)
    (out/'citations').mkdir(exist_ok=True)
    for p in papers:
        (out/'citations'/f'{p["id"]}.bib').write_text(p['bibtex'])
    (out/'publications.bib').write_text('\n'.join(p['bibtex'] for p in papers))
    (out/'index.html').write_text(render(profile,papers))
    (out/'.nojekyll').touch()
    (out/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+profile['url']+'sitemap.xml\n')
    (out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>'+esc(profile['url'])+'</loc></url></urlset>\n')
    print(f'Built {out}/index.html ({len(papers)} publications, {sum(p["selected"] for p in papers)} selected)')

if __name__ == '__main__':
    main()
