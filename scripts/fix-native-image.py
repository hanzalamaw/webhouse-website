# -*- coding: utf-8 -*-
import hashlib
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "images" / "blog"
BLOG = ROOT / "blog"
slug = "native-vs-cross-platform-app-development-2026"
urls = [
    "https://images.unsplash.com/photo-1556652037-9a88e09c5d0f?w=1600&q=80",
    "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=1600&q=80",
    "https://images.unsplash.com/photo-1526498460520-4c246339dccb?w=1600&q=80",
    "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=1600&q=80",
    "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=1600&q=80",
    "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=1600&q=80",
    "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=1600&q=80",
    "https://images.unsplash.com/photo-1574949802264-57073e9f2a2d?w=1600&q=80",
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
        if len(data) < 5000:
            continue
        h = hashlib.md5(data).hexdigest()
        if h in used or h == old:
            print("skip", url[:70])
            continue
        (IMG / f"{slug}.jpg").write_bytes(data)
        print("OK", len(data), h[:8])
        break
    except Exception as e:
        print("err", e)
else:
    print("FAIL")
