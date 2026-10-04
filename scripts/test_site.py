"""Run python3 scripts/test_site.py after building posts."""

import html.parser
import json
from pathlib import Path
import unittest
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://hunter-liles.com"


class Page(html.parser.HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.metas = {}
        self.canonicals = []
        self.refs = []
        self.ids = set()
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta":
            key = attrs.get("property") or attrs.get("name")
            if key:
                self.metas[key] = attrs.get("content")
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append(attrs["href"])
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        for attr in ("src", "href"):
            if attrs.get(attr):
                self.refs.append(attrs[attr])


class SiteTests(unittest.TestCase):
    def test_metadata_and_sitemap(self):
        posts = json.loads((ROOT / "blog/posts.json").read_text())
        pages = {"index.html": f"{ORIGIN}/", "blog.html": f"{ORIGIN}/blog.html"}
        pages.update({f'blog/{p["slug"]}.html': f'{ORIGIN}/blog/{p["slug"]}.html' for p in posts})
        for name, url in pages.items():
            with self.subTest(page=name):
                page = Page(ROOT / name)
                self.assertEqual(page.canonicals, [url])
                self.assertEqual(page.metas["og:url"], url)
                self.assertTrue(page.metas["description"])
                self.assertTrue(page.metas["og:title"])
                self.assertTrue(page.metas["og:description"])
                self.assertEqual(page.metas["og:image"], f"{ORIGIN}/assets/images/headshot.webp")
                self.assertEqual(page.metas["twitter:card"], "summary_large_image")
                self.assertNotIn("robots", page.metas)
        sitemap = ET.parse(ROOT / "sitemap.xml")
        self.assertEqual(set(pages.values()), {el.text for el in sitemap.findall(".//{*}loc")})
        self.assertIn(f"Sitemap: {ORIGIN}/sitemap.xml", (ROOT / "robots.txt").read_text())
        self.assertEqual(Page(ROOT / "blog/post.html").metas["robots"], "noindex, follow")

    def test_local_assets_and_anchors(self):
        for path in ROOT.glob("**/*.html"):
            page = Page(path)
            for ref in page.refs:
                parsed = urlsplit(ref)
                if parsed.scheme or parsed.netloc:
                    continue
                target = (ROOT / unquote(parsed.path.lstrip("/")) if parsed.path.startswith("/")
                          else path.parent / unquote(parsed.path)) if parsed.path else path
                if target.is_dir():
                    target = target / "index.html"
                with self.subTest(page=str(path.relative_to(ROOT)), reference=ref):
                    self.assertTrue(target.is_file(), f"Missing: {target}")
                    if parsed.fragment and target.suffix == ".html":
                        self.assertIn(unquote(parsed.fragment), Page(target).ids)

    def test_removed_content(self):
        for path in [ROOT / "index.html", ROOT / "blog.html", *ROOT.glob("blog/*.html"),
                     ROOT / "assets/documents/resume.tex"]:
            source = path.read_text()
            for stale in ["hunterliles06@gmail.com", "hunter-liles-128145332", "tui-3d-renderer",
                          "<!-- more here:", "All handwritten.", "trading-heading"]:
                self.assertNotIn(stale, source)


if __name__ == "__main__":
    unittest.main()
