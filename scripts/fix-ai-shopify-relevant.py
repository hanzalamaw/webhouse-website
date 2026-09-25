# -*- coding: utf-8 -*-
import hashlib
import re
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "images" / "blog"
BLOG = ROOT / "blog"

# Fix AI + Shopify with more unique relevant URLs
JOBS = {
    "ai-workflow-automation-enterprise-guide": (
        [
            "https://images.unsplash.com/photo-1535378917041-10a22c95931a?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1697577418970-95d99b5a55cf?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1717501218370-b0f0c8d0c0c0?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1555255707-c07966088b7b?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1507146426996-ef05306b995a?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1527430253228-e93688616381?auto=format&fit=crop&w=1600&q=80",
        ],
        "Enterprise AI workflow automation and intelligent systems",
    ),
    "shopify-plan-guide-how-to-choose-the-right-plan-for-your-online-store": (
        [
            "https://images.unsplash.com/photo-1556740758-90de374c12ad?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1472851294608-062f824d29cc?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1441984904996-e0b14cb33adb?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1607083206869-4c7672e72a8a?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1607082349566-187342175e2f?auto=format&fit=crop&w=1600&q=80",
        ],
        "Shopify online store plan and ecommerce setup",
    ),
}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = resp.read()
    if len(data) < 40000:
        raise RuntimeError(f"too small ({len(data)})")
    return data


def file_md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


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
            h = hashlib.md5(data).hexdigest()
            if h in used or h == old.get(slug):
                print(f"skip {slug}")
                continue
            dest.write_bytes(data)
            used.add(h)
            update_html(slug, alt)
            print(f"OK {slug} {len(data)}")
            ok = True
            break
        if not ok:
            print(f"FAIL {slug}")


if __name__ == "__main__":
    main()
