# -*- coding: utf-8 -*-
import hashlib
import re
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "images" / "blog"
BLOG = ROOT / "blog"

JOBS = {
    "enterprise-api-engineering-microservices-integration": (
        [
            "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1600&q=80",
            "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1600&q=80",
            "https://images.unsplash.com/photo-1639322537504-6427a16b0a28?w=1600&q=80",
        ],
        "Enterprise API engineering and microservices integration",
    ),
    "zero-trust-cyber-security-architecture-for-enterprise-cloud": (
        [
            "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=1600&q=80",
            "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=1600&q=80",
            "https://images.unsplash.com/photo-1526374870839-e155464bb9b2?w=1600&q=80",
        ],
        "Zero trust cybersecurity architecture for enterprise cloud",
    ),
    "shopify-speed-optimization-and-core-web-vitals-engineering": (
        [
            "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=1600&q=80",
            "https://images.unsplash.com/photo-1557800636-894a64c1696f?w=1600&q=80",
            "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=1600&q=80",
        ],
        "Shopify speed optimization and Core Web Vitals engineering",
    ),
    "shopify-themes-vs-custom-development-what-should-your-store-use": (
        [
            "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=1600&q=80",
            "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=1600&q=80",
            "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=1600&q=80",
        ],
        "Shopify themes versus custom store development",
    ),
    "software-testing-automation-and-cicd-pipeline-strategy": (
        [
            "https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=1600&q=80",
            "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1600&q=80",
            "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=1600&q=80",
        ],
        "Software testing automation and CI/CD pipeline strategy",
    ),
    "shopify-plan-guide-how-to-choose-the-right-plan-for-your-online-store": (
        [
            "https://images.unsplash.com/photo-1556740758-90de374c12ad?w=1600&q=80",
            "https://images.unsplash.com/photo-1474631245212-32dc3c8310c6?w=1600&q=80",
            "https://images.unsplash.com/photo-1441984904996-e0b14cb33adb?w=1600&q=80",
        ],
        "Shopify plan guide for choosing the right online store plan",
    ),
}

EXTRA = [
    "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=1600&q=80",
    "https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?w=1600&q=80",
    "https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=1600&q=80",
    "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=1600&q=80",
    "https://images.unsplash.com/photo-1573164713985-8667cf75090f?w=1600&q=80",
    "https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=1600&q=80",
    "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=1600&q=80",
    "https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?w=1600&q=80",
    "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1600&q=80",
    "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1600&q=80",
    "https://images.unsplash.com/photo-1553877522-43269d4ea984?w=1600&q=80",
    "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=1600&q=80",
    "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1600&q=80",
]


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = resp.read()
    if len(data) < 5000:
        raise RuntimeError("too small")
    return data


def file_md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def main():
    used = set()
    for p in BLOG.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        m = re.search(r'src="../assets/images/blog/([^"]+)"', t)
        if not m:
            continue
        f = IMG / m.group(1)
        if f.exists() and p.stem not in JOBS:
            used.add(file_md5(f))

    for slug, (urls, alt) in JOBS.items():
        candidates = list(urls) + EXTRA
        dest = IMG / f"{slug}.jpg"
        ok = False
        for url in candidates:
            try:
                data = fetch(url)
                h = hashlib.md5(data).hexdigest()
                if h in used:
                    print("skip dup", slug)
                    continue
                dest.write_bytes(data)
                used.add(h)
                path = BLOG / f"{slug}.html"
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
                path.write_text(html2, encoding="utf-8")
                print("OK", slug, len(data))
                ok = True
                break
            except Exception as e:
                print("err", slug, e)
        if not ok:
            print("FAIL", slug)

    by = defaultdict(list)
    for p in BLOG.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        m = re.search(r'src="../assets/images/blog/([^"]+)"', t)
        if not m:
            continue
        f = IMG / m.group(1)
        if f.exists():
            by[file_md5(f)].append(p.stem)

    dups = {h: s for h, s in by.items() if len(s) > 1}
    print("remaining dups", len(dups))
    for h, s in dups.items():
        print(h[:8], s)
    print("total blogs", len(list(BLOG.glob("*.html"))), "unique hashes", len(by))


if __name__ == "__main__":
    main()
