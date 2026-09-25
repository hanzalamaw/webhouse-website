# -*- coding: utf-8 -*-
"""Replace 5 blog images with topic-relevant Unsplash photos."""
import hashlib
import re
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "images" / "blog"
BLOG = ROOT / "blog"

JOBS = {
    "cloud-native-devops-infrastructure-guide": (
        [
            "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1544197150-b99a580bb7a2?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1597852074816-d933c7bf97f9?auto=format&fit=crop&w=1600&q=80",
        ],
        "Cloud-native infrastructure and DevOps server environment",
    ),
    "custom-software-development-scaling-enterprises": (
        [
            "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1587620962725-abab7fe55159?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1542831371-29b0f74f9713?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1484417894907-623942c8ee41?auto=format&fit=crop&w=1600&q=80",
        ],
        "Custom software development and enterprise engineering",
    ),
    "oracle-sql-developer-vs-full-stack-developer-understanding-modern-engineering-roles": (
        [
            "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1571171637578-41bc2dd41cd2?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1633356122544-f134324a6cee?auto=format&fit=crop&w=1600&q=80",
        ],
        "SQL database development versus full-stack engineering",
    ),
    "shopify-plan-guide-how-to-choose-the-right-plan-for-your-online-store": (
        [
            "https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1556742111-a301053dbe2e?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=1600&q=80",
        ],
        "Shopify online store plan and ecommerce setup",
    ),
    "ai-workflow-automation-enterprise-guide": (
        [
            "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1531746790731-6d275e0ebb14?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1677756119517-756a188d2d94?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1655720828018-edd2fcaf484d?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=1600&q=80",
        ],
        "Enterprise AI workflow automation and intelligent systems",
    ),
}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = resp.read()
    if len(data) < 20000:
        raise RuntimeError(f"too small ({len(data)})")
    return data


def file_md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def update_html(slug: str, alt: str) -> None:
    path = BLOG / f"{slug}.html"
    if not path.exists():
        return
    html = path.read_text(encoding="utf-8")
    html2 = re.sub(
        rf'src="../assets/images/blog/{re.escape(slug)}\.(?:jpg|jpeg|png|webp|avif|jfif)"',
        f'src="../assets/images/blog/{slug}.jpg"',
        html,
    )
    html2 = re.sub(
        rf'(src="../assets/images/blog/{re.escape(slug)}\.jpg" alt=")[^"]*(")',
        rf"\1{alt}\2",
        html2,
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
    old_hashes = {}
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
            old_hashes[p.stem] = h
        else:
            used.add(h)

    for slug, (urls, alt) in JOBS.items():
        dest = IMG / f"{slug}.jpg"
        ok = False
        for url in urls:
            try:
                data = fetch(url)
            except Exception as e:
                print(f"err fetch {slug}: {e}")
                continue
            h = hashlib.md5(data).hexdigest()
            if h in used or h == old_hashes.get(slug):
                print(f"skip used {slug}")
                continue
            dest.write_bytes(data)
            used.add(h)
            update_html(slug, alt)
            print(f"OK {slug} {len(data)} bytes")
            ok = True
            break
        if not ok:
            print(f"FAIL {slug}")

    by = {}
    for p in BLOG.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        m = re.search(r'src="../assets/images/blog/([^"]+)"', t)
        if not m:
            continue
        f = IMG / m.group(1)
        if f.exists():
            by.setdefault(file_md5(f), []).append(p.stem)
    dups = {h: s for h, s in by.items() if len(s) > 1}
    print(f"dups {len(dups)}")
    for slug in JOBS:
        f = IMG / f"{slug}.jpg"
        print(f"  {file_md5(f)[:8]} {f.stat().st_size:7d} {slug}")


if __name__ == "__main__":
    main()
