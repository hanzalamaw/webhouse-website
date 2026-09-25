# -*- coding: utf-8 -*-
from pathlib import Path
import re
import html as H

blog_dir = Path("blog")
img_dir = Path("assets/images/blog")
broken = []
ok = 0

for p in sorted(blog_dir.glob("*.html")):
    t = p.read_text(encoding="utf-8")
    m = re.search(
        r'src="(\.\./assets/images/blog/[^"]+)"[^>]*class="absolute inset-0',
        t,
    )
    if not m:
        m = re.search(r'src="(\.\./assets/images/blog/[^"]+)"', t)
    if not m:
        broken.append((p.name, "NO_IMG_TAG", ""))
        continue
    rel = m.group(1)
    name = rel.split("/")[-1]
    name_u = H.unescape(name)
    path = img_dir / name_u
    path2 = img_dir / name
    if path.exists() or path2.exists():
        ok += 1
        continue
    found = None
    for f in img_dir.iterdir():
        if f.name.lower() == name_u.lower() or f.name.lower() == name.lower():
            found = f.name
            break
    broken.append((p.name, rel, found or "MISSING"))

print(f"OK: {ok}")
print(f"Broken: {len(broken)}")
for b in broken:
    print("---")
    print("blog:", b[0])
    print("ref:", b[1])
    print("disk:", b[2])
