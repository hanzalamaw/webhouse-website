# -*- coding: utf-8 -*-
"""Change ONLY Shopify Plan + Enterprise Resilience images — unique + relevant."""
import hashlib
import re
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "images" / "blog"
BLOG = ROOT / "blog"

# Fresh Unsplash IDs (avoid ones reused earlier in this project)
JOBS = {
    "cloud-native-devops-infrastructure-guide": (
        [
            # data center / kubernetes / infrastructure
            "https://images.unsplash.com/photo-1605745341112-85968b19386b?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1597852074816-d933c7bf97f9?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1544197150-b99a580bb7a2?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&w=1600&q=80",
        ],
        "Cloud-native infrastructure and DevOps data center",
    ),
    "shopify-plan-guide-how-to-choose-the-right-plan-for-your-online-store": (
        [
            # ecommerce / online shopping / store
            "https://images.unsplash.com/photo-1556740758-90de374c12ad?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1607083206869-4c7672e72a8a?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1607082349566-187342175e2f?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1472851294608-062f824d29cc?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1441984904996-e0b14cb33adb?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=1600&q=80",
        ],
        "Shopify online store and ecommerce plan selection",
    ),
}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = resp.read()
    if len(data) < 50000:
        raise RuntimeError(f"too small ({len(data)})")
    return data


def md5_bytes(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def file_md5(path: Path) -> str:
    return md5_bytes(path.read_bytes())


def update_html(slug: str, alt: str) -> None:
    path = BLOG / f"{slug}.html"
    html = path.read_text(encoding="utf-8")
    html2 = re.sub(
        rf'(src="../assets/images/blog/{re.escape(slug)}\.jpg" alt=")[^"]*(")',
        rf"\1{alt}\2",
        html,
        count=1,
    )
    absu = f"https://webhouseinc.co/assets/images/blog/{slug}.jpg"
    html2 = re.sub(
        r'<meta property="og:image" content="[^"]*"/>',
        f'<meta property="og:image" content="{absu}"/>',
        html2,
        count=1,
    )
    if html2 != html:
        path.write_text(html2, encoding="utf-8")


def main():
    used = set()
    old = {}
    for p in BLOG.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        m = re.search(r'src="../assets/images/blog/([^"]+)"', t)
        if not m:
            continue
        f = IMG / m.group(1)
        if not f.exists():
            continue
        h = file_md5(f)
        if p.stem in JOBS:
            old[p.stem] = h
        else:
            used.add(h)

    for slug, (urls, alt) in JOBS.items():
        dest = IMG / f"{slug}.jpg"
        ok = False
        for url in urls:
            try:
                data = fetch(url)
            except Exception as e:
                print(f"err {slug}: {e}")
                continue
            h = md5_bytes(data)
            if h in used or h == old.get(slug):
                print(f"skip used/same {slug}")
                continue
            dest.write_bytes(data)
            used.add(h)
            update_html(slug, alt)
            print(f"OK {slug} {len(data)} {h[:8]}")
            ok = True
            break
        if not ok:
            print(f"FAIL {slug}")

    # verify no dups involving these two
    by = {}
    for p in BLOG.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        m = re.search(r'src="../assets/images/blog/([^"]+)"', t)
        if not m:
            continue
        f = IMG / m.group(1)
        if f.exists():
            by.setdefault(file_md5(f), []).append(p.stem)
    dups = [s for h, s in by.items() if len(s) > 1]
    print("dup groups", len(dups))
    if dups:
        for s in dups:
            print(s)


if __name__ == "__main__":
    main()
