#!/usr/bin/env python3
"""Run: python3 -m pip install -r scripts/requirements.txt; python3 scripts/build_posts.py.

Commit generated blog/*.html and sitemap.xml so the site needs no server build.
Only listed posts are published. Markdown is trusted, repository-authored content.
"""

import datetime
import html
import json
from pathlib import Path
import re

import markdown

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://hunter-liles.com"


def build():
    template = (ROOT / "blog/post.html").read_text()
    posts = json.loads((ROOT / "blog/posts.json").read_text())
    urls = [f"{ORIGIN}/", f"{ORIGIN}/blog.html"]
    seen = set()
    for post in posts:
        slug = post["slug"]
        if (not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug)
                or slug in seen or slug == "post"):
            raise ValueError(f"Invalid or duplicate slug: {slug}")
        seen.add(slug)
        date = datetime.date.fromisoformat(post["date"])
        title = html.escape(post["title"], quote=True)
        description = html.escape(post.get("excerpt") or post["title"], quote=True)
        url = f"{ORIGIN}/blog/{slug}.html"
        content = markdown.markdown(
            (ROOT / f"blog/posts/{slug}.md").read_text(),
            extensions=["fenced_code", "tables"],
        )
        page = template.replace("<title>Post — Hunter Liles</title>",
                                f"<title>{title} — Hunter Liles</title>")
        page = page.replace('<meta name="description" content="Technical notes by Hunter Liles." />',
                            f'<meta name="description" content="{description}" />')
        metadata = f'''<link rel="canonical" href="{url}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:type" content="article" />
    <meta property="og:site_name" content="Hunter Liles" />
    <meta property="og:title" content="{title} — Hunter Liles" />
    <meta property="og:description" content="{description}" />
    <meta property="og:image" content="{ORIGIN}/assets/images/headshot.webp" />
    <meta property="og:image:width" content="720" />
    <meta property="og:image:height" content="480" />
    <meta property="og:image:alt" content="Hunter Liles" />
    <meta property="article:published_time" content="{date.isoformat()}" />
    <meta property="article:author" content="{ORIGIN}/" />
    <meta name="twitter:card" content="summary_large_image" />'''
        page = page.replace('<meta name="robots" content="noindex, follow" />', metadata)
        page = re.sub(r'    <script\s+src="https://cdn.jsdelivr.net/npm/marked[^>]+></script>\n', '', page)
        page = page.replace('<script src="../blog.js" defer></script>',
                            '<script src="post.js" defer></script>')
        page = page.replace('<h1 id="post-title">Loading…</h1>', f'<h1 id="post-title">{title}</h1>')
        meta = f'<time datetime="{date.isoformat()}">{date.strftime("%B")} {date.day}, {date.year}</time>'
        if post.get("readTime"):
            meta += f'<span class="dot" aria-hidden="true">·</span><span>{html.escape(post["readTime"])}</span>'
        page = page.replace('<p class="writing-meta" id="post-meta"></p>',
                            f'<p class="writing-meta" id="post-meta">{meta}</p>')
        page = re.sub(r'<div class="prose" id="post-body".*?</div>',
                      lambda _: f'<div class="prose" id="post-body" data-state="ready">\n{content}\n          </div>',
                      page, count=1, flags=re.S)
        page = re.sub(r'\s*<noscript>.*?</noscript>', '', page, flags=re.S)
        (ROOT / f"blog/{slug}.html").write_text(page)
        urls.append(url)
    entries = "\n".join(f"  <url><loc>{html.escape(url)}</loc></url>" for url in urls)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'{entries}\n</urlset>\n'
    )


if __name__ == "__main__":
    build()
