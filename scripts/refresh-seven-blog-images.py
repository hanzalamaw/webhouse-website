# -*- coding: utf-8 -*-
import hashlib
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "images" / "blog"
BLOG = ROOT / "blog"

JOBS = {
    "shopify-plan-guide-how-to-choose-the-right-plan-for-your-online-store": (
        [
            "https://images.unsplash.com/photo-1556742031-c6961e8560b0?w=1600&q=80",
            "https://images.unsplash.com/photo-1556742111-a301053dbe2e?w=1600&q=80",
            "https://images.unsplash.com/photo-1607083206869-4c7672e72a8a?w=1600&q=80",
        ],
        "Shopify plan guide for online store teams",
    ),
    "oracle-sql-developer-vs-full-stack-developer-understanding-modern-engineering-roles": (
        [
            "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1600&q=80",
            "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=1600&q=80",
            "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1600&q=80",
        ],
        "Oracle SQL developer versus full-stack engineering roles",
    ),
    "meta-developer-app-and-modern-api-integration-a-business-guide": (
        [
            "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=1600&q=80",
            "https://images.unsplash.com/photo-1611162616305-c69b3fa7fbe0?w=1600&q=80",
            "https://images.unsplash.com/photo-1611162618071-b39a2ec055fb?w=1600&q=80",
        ],
        "Meta developer app and modern API integration",
    ),
    "cloud-native-devops-infrastructure-guide": (
        [
            "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=1600&q=80",
            "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1600&q=80",
            "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1600&q=80",
        ],
        "Cloud-native infrastructure with DevOps precision",
    ),
    "ai-workflow-automation-enterprise-guide": (
        [
            "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1600&q=80",
            "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1600&q=80",
            "https://images.unsplash.com/photo-1535378917041-10a22c95931a?w=1600&q=80",
        ],
        "Enterprise AI workflow automation and intelligent systems",
    ),
    "b2b-growth-marketing-seo-tech-platforms": (
        [
            "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1600&q=80",
            "https://images.unsplash.com/photo-1432888498266-38ffec3f093e?w=1600&q=80",
            "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1600&q=80",
        ],
        "B2B SEO and performance marketing growth engine",
    ),
    "native-vs-cross-platform-app-development-2026": (
        [
            "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=1600&q=80",
            "https://images.unsplash.com/photo-1551650975-87deedd944c3?w=1600&q=80",
            "https://images.unsplash.com/photo-1607252650355-f7fd0460ccdb?w=1600&q=80",
        ],
        "Native versus cross-platform app development decision",
    ),
}

EXTRA = [
    "https://images.unsplash.com/photo-1557800636-894a64c1696f?w=1600&q=80",
    "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=1600&q=80",
    "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1600&q=80",
    "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=1600&q=80",
    "https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?w=1600&q=80",
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
    "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=1600&q=80",
    "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1600&q=80",
    "https://images.unsplash.com/photo-1544197150-b99a580bb7a2?w=1600&q=80",
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


def update_html(slug: str, alt: str) -> None:
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
    if html2 != html:
        path.write_text(html2, encoding="utf-8")


def main():
    used = set()
    for p in BLOG.glob("*.html"):
        if p.stem in JOBS:
            continue
        t = p.read_text(encoding="utf-8")
        m = re.search(r'src="../assets/images/blog/([^"]+)"', t)
        if not m:
            continue
        f = IMG / m.group(1)
        if f.exists():
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
                update_html(slug, alt)
                print("OK", slug, len(data))
                ok = True
                break
            except Exception as e:
                print("err", slug, e)
        if not ok:
            print("FAIL", slug)

    # verify uniqueness across all blogs
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
    print("remaining dups", len(dups))
    for h, s in dups.items():
        print(h[:8], s)


if __name__ == "__main__":
    main()
