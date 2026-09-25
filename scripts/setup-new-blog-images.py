# -*- coding: utf-8 -*-
"""Add unique local images for 20 new blogs + list them on blogs.html."""
import hashlib
import html as html_lib
import re
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
BLOG = ROOT / "blog"
IMG = ROOT / "assets" / "images" / "blog"
BLOGS_HTML = ROOT / "blogs.html"

# Topic-relevant Unsplash pools — prefer IDs not used in prior batches
IMAGE_POOLS = {
    "cloud-migration-playbook-moving-legacy-apps-to-aws": [
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1544197150-b99a580bb7a2?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1605745341112-85968b19386b?auto=format&fit=crop&w=1600&q=80",
    ],
    "conversion-focused-website-redesign-strategy-before-design": [
        "https://images.unsplash.com/photo-1586717791821-3f44a563fa4c?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=1600&q=80",
    ],
    "design-systems-that-convert-scalable-ui-ux-foundations": [
        "https://images.unsplash.com/photo-1581291518633-83b4ebd1d83e?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1558655146-9f40138edfeb?auto=format&fit=crop&w=1600&q=80",
    ],
    "fintech-software-engineering-security-compliance-essentials": [
        "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1553729459-efe14ef6055d?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1600&q=80",
    ],
    "flutter-app-engineering-for-business-and-consumer-products": [
        "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1556652037-9a88e09c5d0f?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1526498460520-4c246339dccb?auto=format&fit=crop&w=1600&q=80",
    ],
    "generative-engine-optimization-geo-ranking-in-ai-search": [
        "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=1600&q=80",
    ],
    "graphql-vs-rest-apis-for-modern-enterprise-integration": [
        "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1600&q=80",
    ],
    "hipaa-compliant-healthcare-software-development-guide": [
        "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1584982751601-97dcc096659c?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=1600&q=80",
    ],
    "inventory-order-management-systems-for-growing-retailers": [
        "https://images.unsplash.com/photo-1553413077-190dd305871c?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?auto=format&fit=crop&w=1600&q=80",
    ],
    "magento-vs-shopify-plus-enterprise-commerce-platform-guide": [
        "https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1472851294608-062f824d29cc?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?auto=format&fit=crop&w=1600&q=80",
    ],
    "marketing-automation-lifecycle-funnels-for-tech-brands": [
        "https://images.unsplash.com/photo-1533750349088-cd871a92f312?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1432888498266-38ffec3f093e?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=1600&q=80",
    ],
    "microservices-observability-monitoring-distributed-systems": [
        "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1600&q=80",
    ],
    "multi-tenant-saas-architecture-patterns-that-scale": [
        "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1504639725590-34d0984388bd?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1518773553398-650c184e0bb3?auto=format&fit=crop&w=1600&q=80",
    ],
    "nextjs-enterprise-web-apps-performance-seo-guide": [
        "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1542831371-29b0f74f9713?auto=format&fit=crop&w=1600&q=80",
    ],
    "react-native-performance-tuning-for-production-apps": [
        "https://images.unsplash.com/photo-1607252650355-f7fd0460ccdb?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=1600&q=80",
    ],
    "real-time-bi-dashboards-operations-data-into-decisions": [
        "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?auto=format&fit=crop&w=1600&q=85",
    ],
    "saas-mvp-to-scale-product-engineering-roadmap-for-startups": [
        "https://images.unsplash.com/photo-1559136555-9303baea8ebd?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1553877522-43269d4ea984?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=1600&q=80",
    ],
    "social-media-growth-systems-for-ecommerce-brands": [
        "https://images.unsplash.com/photo-1611162616475-46b635cb495f?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1611162616305-c69b3fa7fbe0?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1432888622747-4eb9a8f2c1a9?auto=format&fit=crop&w=1600&q=80",
    ],
    "staff-augmentation-vs-managed-delivery-choosing-the-right-model": [
        "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1600880292203-757bb62b4baf?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1600&q=80",
    ],
    "woocommerce-customization-vs-custom-storefront-engineering": [
        "https://images.unsplash.com/photo-1556740738-b6a63e27c4df?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=1600&q=80",
        "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=1600&q=80",
    ],
}

# Extra unique fallbacks (must not collide with used hashes)
EXTRA = [
    "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1516321497487-e288fb19713f?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1573164713985-8667cf75090f?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1531297484001-80022131f5a1?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1633356122544-f134324a6cee?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1639322537504-6427a16b0a28?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1557800636-894a64c1696f?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1556742111-a301053dbe2e?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1441984904996-e0b14cb33adb?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1607083206869-4c7672e72a8a?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1607082349566-187342175e2f?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1553729459-efe14ef6055d?auto=format&fit=crop&w=1600&q=85",
    "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=1600&q=85",
    "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1553413077-190dd305871c?auto=format&fit=crop&w=1600&q=85",
    "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=1600&q=85",
    "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1600&q=85",
    "https://images.unsplash.com/photo-1558655146-d09347e92766?auto=format&fit=crop&w=1600&q=80",
]


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = resp.read()
    if len(data) < 20000:
        raise RuntimeError(f"too small {len(data)}")
    return data


def md5(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def blog_meta(slug: str):
    path = BLOG / f"{slug}.html"
    t = path.read_text(encoding="utf-8")
    h1 = re.search(r'itemprop="headline">(.*?)</h1>', t, re.S)
    name = html_lib.unescape(re.sub(r"\s+", " ", h1.group(1)).strip()) if h1 else slug
    cat_m = re.search(
        r'<span class="text-primary-light[^"]*"[^>]*>(.*?)</span>', t, re.S
    )
    cat = html_lib.unescape(re.sub(r"<[^>]+>", "", cat_m.group(1)).strip()) if cat_m else "Insights"
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', t)
    desc = html_lib.unescape(desc_m.group(1).strip()) if desc_m else ""
    if len(desc) > 180:
        desc = desc[:177].rsplit(" ", 1)[0] + "..."
    return name, cat, desc, path, t


def update_blog_html(slug: str, name: str, path: Path, text: str) -> None:
    alt = html_lib.escape(name, quote=True)
    local = f"https://webhouseinc.co/assets/images/blog/{slug}.jpg"

    # hero img alt
    text2 = re.sub(
        rf'(src="../assets/images/blog/{re.escape(slug)}\.jpg" alt=")[^"]*(")',
        rf"\1{alt}\2",
        text,
        count=1,
    )
    # og/twitter images -> local
    for prop in (
        'property="og:image"',
        'property="og:image:secure_url"',
        'name="twitter:image"',
    ):
        text2 = re.sub(
            rf'(<meta {prop} content=")[^"]*("/>)',
            rf"\1{local}\2",
            text2,
            count=1,
        )
    text2 = re.sub(
        r'(<meta property="og:image:alt" content=")[^"]*("/>)',
        rf"\1{alt}\2",
        text2,
        count=1,
    )
    text2 = re.sub(
        r'(<meta name="twitter:image:alt" content=")[^"]*("/>)',
        rf"\1{alt}\2",
        text2,
        count=1,
    )
    if text2 != text:
        path.write_text(text2, encoding="utf-8")


def card_html(slug: str, name: str, cat: str, desc: str) -> str:
    e_name = html_lib.escape(name)
    e_cat = html_lib.escape(cat)
    e_desc = html_lib.escape(desc)
    return f'''<a href="blog/{slug}.html" class="group flex flex-col overflow-hidden rounded-[2rem] bg-white border border-gray-100 hover:shadow-card hover:-translate-y-1 transition-all duration-300">
<div class="h-52 overflow-hidden bg-gray-100">
<img src="assets/images/blog/{slug}.jpg" alt="{e_name}" class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"/>
</div>
<div class="flex flex-col flex-1 p-7 md:p-8">
<span class="text-xs font-bold uppercase tracking-wider text-primary mb-3">{e_cat}</span>
<h3 class="text-xl font-display font-bold text-[#1c1917] mb-3 leading-snug group-hover:text-primary transition-colors">{e_name}</h3>
<p class="text-sm text-gray-500 leading-relaxed mb-6 flex-1">{e_desc}</p>
<span class="inline-flex items-center gap-2 text-sm font-bold text-primary group-hover:gap-3 transition-all">Read article <span class="material-symbols-outlined text-sm">arrow_forward</span></span>
</div>
</a>
'''


def main():
    # hashes already used by existing blog image files
    used = set()
    for f in IMG.glob("*"):
        if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".avif"} and f.is_file():
            # only count if referenced by a non-new blog OR any existing file
            used.add(md5(f.read_bytes()))

    # also hash any currently referenced images from OLD blogs only
    new_slugs = set(IMAGE_POOLS.keys())
    used = set()
    for p in BLOG.glob("*.html"):
        if p.stem in new_slugs:
            continue
        t = p.read_text(encoding="utf-8")
        m = re.search(r'src="../assets/images/blog/([^"]+)"', t)
        if not m:
            continue
        f = IMG / m.group(1)
        if f.exists():
            used.add(md5(f.read_bytes()))

    print(f"existing unique hashes reserved: {len(used)}")
    cards = []
    ok = fail = 0

    for slug, urls in IMAGE_POOLS.items():
        name, cat, desc, path, text = blog_meta(slug)
        dest = IMG / f"{slug}.jpg"
        candidates = list(urls) + EXTRA
        got = False
        for url in candidates:
            try:
                data = fetch(url)
            except Exception as e:
                print(f"  err {slug}: {e}")
                continue
            h = md5(data)
            if h in used:
                print(f"  skip dup hash {slug}")
                continue
            dest.write_bytes(data)
            used.add(h)
            update_blog_html(slug, name, path, path.read_text(encoding="utf-8"))
            print(f"OK {slug} ({len(data)} bytes) -> {name[:50]}")
            cards.append(card_html(slug, name, cat, desc))
            ok += 1
            got = True
            break
        if not got:
            print(f"FAIL {slug}")
            fail += 1

    # prepend cards to blogs.html grid
    if cards:
        listing = BLOGS_HTML.read_text(encoding="utf-8")
        # remove any existing cards for these slugs first
        for slug in IMAGE_POOLS:
            listing = re.sub(
                rf'<a href="blog/{re.escape(slug)}\.html"[\s\S]*?</a>\s*',
                "",
                listing,
                count=1,
            )
        marker = '<div class="grid grid-cols-1 md:grid-cols-2 gap-8">\n'
        if marker not in listing:
            raise SystemExit("grid marker not found")
        insert = marker + "".join(cards)
        listing = listing.replace(marker, insert, 1)
        BLOGS_HTML.write_text(listing, encoding="utf-8")
        print(f"blogs.html updated with {len(cards)} cards")

    # final uniqueness check
    by = {}
    for p in BLOG.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        m = re.search(r'src="../assets/images/blog/([^"]+)"', t)
        if not m:
            continue
        f = IMG / m.group(1)
        if f.exists():
            by.setdefault(md5(f.read_bytes()), []).append(p.stem)
    dups = {h: s for h, s in by.items() if len(s) > 1}
    print(f"DONE ok={ok} fail={fail} dup_groups={len(dups)}")
    for h, s in dups.items():
        print(" DUP", s)


if __name__ == "__main__":
    main()
