"""Check rendered pages, internal resources, and the publication artifact."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import xml.etree.ElementTree as ET

ROOT = Path("_site").resolve()
assert ROOT.is_dir(), "Build the site first"
errors = []

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.ids, self.links = path, [], []
        self.h1 = 0
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "html" and a.get("lang") != "en":
            errors.append(f"{self.path}: missing English language")
        if tag == "img" and not a.get("alt"):
            errors.append(f"{self.path}: image needs alternative text")
        for key in ("href", "src"):
            if key in a:
                self.links.append(a[key])
        if tag == "a" and not a.get("href"):
            errors.append(f"{self.path}: empty link")

pages = {p.resolve(): Page(p) for p in ROOT.rglob("*.html")}
assert ROOT / "index.html" in pages, "Homepage is missing"
for path, page in pages.items():
    if page.h1 != 1:
        errors.append(f"{path}: expected one h1")
    if any(n > 1 for n in Counter(page.ids).values()):
        errors.append(f"{path}: duplicate IDs")
    if "{{" in path.read_text() or "{%" in path.read_text():
        errors.append(f"{path}: unrendered Liquid")
    for link in page.links:
        parts = urlsplit(link)
        if parts.scheme in ("https", "mailto") or parts.netloc:
            continue
        if parts.scheme:
            errors.append(f"{path}: unsupported URL scheme: {link}")
            continue
        target = ROOT / unquote(parts.path).lstrip("/") if parts.path.startswith("/") else path.parent / unquote(parts.path)
        if not parts.path:
            target = path
        elif target.is_dir() or parts.path.endswith("/"):
            target = target / "index.html"
        target = target.resolve()
        if not target.is_relative_to(ROOT) or not target.is_file():
            errors.append(f"{path}: missing internal resource {link}")
        elif parts.fragment and target in pages and unquote(parts.fragment) not in pages[target].ids:
            errors.append(f"{path}: missing anchor {link}")

research = json.loads(Path("_data/research.yaml").read_text())
assert [r["id"] for r in research] == ["models", "enzymes", "sweet-modulators"]
for area in research:
    assert area["status"], "Research status must be explicit"
    if area.get("figure"):
        assert area.get("figure_alt") and area.get("caption")
        ET.parse(ROOT / area["figure"].lstrip("/"))

allowed = {
    "index.html", "404.html", "robots.txt", "sitemap.xml",
    "static/site.css", "static/favicon.svg", "static/saisai-ding.jpg",
    "static/research-models.svg", "static/research-enzymes.svg",
    "static/research-sweet.svg",
}
actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file()}
if actual - allowed:
    errors.append(f"Unexpected published files: {sorted(actual - allowed)}")
if allowed - actual:
    errors.append(f"Missing published files: {sorted(allowed - actual)}")
ET.parse(ROOT / "sitemap.xml")
if errors:
    raise SystemExit("\n".join(errors))
print(f"PASS: {len(pages)} pages; internal links, anchors, images, SVG/XML, and artifact allowlist.")
