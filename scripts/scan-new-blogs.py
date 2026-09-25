# -*- coding: utf-8 -*-
from pathlib import Path
import re
import hashlib
from collections import defaultdict

BLOG = Path("blog")
IMG = Path("assets/images/blog")
blogs = sorted(BLOG.glob("*.html"))
print("blog count", len(blogs))

bh = Path("blogs.html").read_text(encoding="utf-8") if Path("blogs.html").exists() else ""
not_listed = []
missing = []
no_ref = []
by_hash = defaultdict(list)

for p in blogs:
    t = p.read_text(encoding="utf-8")
    m = re.search(r'src="../assets/images/blog/([^"]+)"', t)
    title_m = re.search(r"<title>(.*?)</title>", t, re.I | re.S)
    title = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else p.stem
    if f"blog/{p.stem}.html" not in bh:
        not_listed.append((p.stem, title))
    if not m:
        no_ref.append((p.stem, title))
        continue
    f = IMG / m.group(1)
    if not f.exists():
        missing.append((p.stem, m.group(1), title))
    else:
        by_hash[hashlib.md5(f.read_bytes()).hexdigest()].append(p.stem)

print("not in blogs.html", len(not_listed))
for s, title in not_listed:
    print(" NEW", s)
    print("  ", title)

print("missing image files", len(missing))
for x in missing:
    print(" MISS", x)
print("no img ref", len(no_ref))
for x in no_ref:
    print(" NOREF", x)
dups = {h: s for h, s in by_hash.items() if len(s) > 1}
print("dup groups among existing", len(dups))
