# -*- coding: utf-8 -*-
import hashlib
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "images" / "blog"
BLOG = ROOT / "blog"
slug = "meta-developer-app-and-modern-api-integration-a-business-guide"
urls = [
    "https://images.unsplash.com/photo-1611162616475-46b635cb495f?w=1600&q=80",
    "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=1600&q=80",
    "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=1600&q=80",
    "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1600&q=80",
    "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1600&q=80",
    "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=1600&q=80",
]

used = set()
for p in BLOG.glob("*.html"):
    if p.stem == slug:
        continue
    t = p.read_text(encoding="utf-8")
    m = re.search(r'src="../assets/images/blog/([^"]+)"', t)
    if m:
        f = IMG / m.group(1)
        if f.exists():
            used.add(hashlib.md5(f.read_bytes()).hexdigest())

old = hashlib.md5((IMG / f"{slug}.jpg").read_bytes()).hexdigest()
for url in urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=90).read()
        if len(data) < 80000:
            print("too small", len(data), url[:60])
            continue
        h = hashlib.md5(data).hexdigest()
        if h in used or h == old:
            print("skip")
            continue
        (IMG / f"{slug}.jpg").write_bytes(data)
        print("OK", len(data), h[:8])
        break
    except Exception as e:
        print("err", e)
else:
    print("FAIL")
