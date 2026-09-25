# -*- coding: utf-8 -*-
import hashlib
import re
from collections import defaultdict
from pathlib import Path

IMG = Path("assets/images/blog")
BLOG = Path("blog")
targets = {
    "shopify-plan-guide-how-to-choose-the-right-plan-for-your-online-store",
    "cloud-native-devops-infrastructure-guide",
}
by = defaultdict(list)
for p in BLOG.glob("*.html"):
    t = p.read_text(encoding="utf-8")
    m = re.search(r'src="../assets/images/blog/([^"]+)"', t)
    if not m:
        continue
    f = IMG / m.group(1)
    if f.exists():
        by[hashlib.md5(f.read_bytes()).hexdigest()].append(p.stem)

print("=== target uniqueness ===")
for h, s in by.items():
    if any(x in targets for x in s):
        print(h[:8], len(s), s)

print("=== all dups ===")
dups = {h: s for h, s in by.items() if len(s) > 1}
print("dup groups", len(dups))
for h, s in dups.items():
    print(h[:8], s)

for s in targets:
    f = IMG / f"{s}.jpg"
    print("FILE", s, f.stat().st_size if f.exists() else None, hashlib.md5(f.read_bytes()).hexdigest()[:8] if f.exists() else None)
