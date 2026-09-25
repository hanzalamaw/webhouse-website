# -*- coding: utf-8 -*-
"""Ensure every blog has a unique image; refresh specifically requested posts."""
import hashlib
import re
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "assets" / "images" / "blog"
BLOG_DIR = ROOT / "blog"

# Force-refresh these (user-requested)
FORCE = {
    "web-development-company-vs-web-development-agency-how-to-choose-a-team": (
        "https://images.unsplash.com/photo-1552664730-d307ca884978?w=1600&q=80",
        "Choosing between a web development company and agency team",
    ),
    "native-vs-cross-platform-app-development-2026": (
        "https://images.unsplash.com/photo-1607252650355-f7fd0460ccdb?w=1600&q=80",
        "Native versus cross-platform mobile engineering decision",
    ),
    "generative-ai-enterprise-workflow-automation-2026": (
        "https://images.unsplash.com/photo-1677756119517-756a188d2d94?w=1600&q=80",
        "Generative AI and autonomous agents transforming enterprise workflows",
    ),
    "enterprise-seo-strategy-technical-growth-guide": (
        "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1600&q=80",
        "Enterprise technical SEO architecture and organic growth",
    ),
    "enterprise-generative-ai-intelligent-systems-guide": (
        "https://images.unsplash.com/photo-1655720828018-edd2fcaf484d?w=1600&q=80",
        "Enterprise AI transformation with autonomous agents",
    ),
    "dedicated-software-engineering-teams-scale": (
        "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=1600&q=80",
        "Dedicated software development teams for scale-ups",
    ),
    "custom-erp-crm-vs-off-the-shelf-software": (
        "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=1600&q=80",
        "Custom ERP CRM versus off-the-shelf enterprise software",
    ),
    "ai-agent-workflow-automation-enterprise-guide": (
        "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=1600&q=80",
        "Autonomous AI agents and intelligent automation for enterprises",
    ),
}

# Unique replacements for remaining duplicates (slug -> url, alt)
DEDUP = {
    # keep ai-workflow-automation-enterprise-guide / original AI if unique; replace siblings
    "ai-workflow-automation-and-rpa-for-enterprise-platforms": (
        "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=1600&q=80",
        "AI workflow automation and RPA for enterprise platforms",
    ),
    # cloud group - keep cloud-native-devops-infrastructure-guide if unique; replace extras
    "cloud-native-architecture-devops-enterprise-scaling": (
        "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1600&q=80",
        "Cloud-native architecture DevOps enterprise scaling",
    ),
    "cloud-native-microservices-architecture-strategy-guide": (
        "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1600&q=80",
        "Cloud-native microservices architecture strategy",
    ),
    "enterprise-cloud-native-architecture-devops-guide": (
        "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=1600&q=80",
        "Enterprise cloud-native architecture and DevOps",
    ),
    "oracle-aws-and-azure-connecting-enterprise-development-with-modern-cloud": (
        "https://images.unsplash.com/photo-1544197150-b99a580bb7a2?w=1600&q=80",
        "Oracle AWS and Azure enterprise cloud platforms",
    ),
    "serverless-vs-containerization-enterprise-cloud-guide": (
        "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=1600&q=80",
        "Serverless versus containerization enterprise cloud",
    ),
    # mobile group
    "cross-platform-mobile-app-development-strategy-guide": (
        "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=1600&q=80",
        "Cross-platform mobile app development strategy",
    ),
    "progressive-web-apps-pwas-vs-native-apps-guide": (
        "https://images.unsplash.com/photo-1551650975-87deedd944c3?w=1600&q=80",
        "Progressive web apps versus native mobile apps",
    ),
    # ecommerce/shopify dups
    "how-to-choose-a-shopify-developer-or-shopify-partner-for-a-growing-brand": (
        "https://images.unsplash.com/photo-1556740738-b6a63e27c4df?w=1600&q=80",
        "Choosing a Shopify developer or partner",
    ),
    "custom-shopify-theme-development-liquid-and-tailwind-guide": (
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1600&q=80",
        "Custom Shopify theme Liquid and Tailwind development",
    ),
    "shopify-themes-vs-custom-development-what-should-your-store-use": (
        "https://images.unsplash.com/photo-1472851294608-062f824d29cc?w=1600&q=80",
        "Shopify themes versus custom store development",
    ),
    # software / saas
    "saas-multi-tenant-architecture-data-isolation": (
        "https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?w=1600&q=80",
        "SaaS multi-tenant architecture and data isolation",
    ),
    # security
    "zero-trust-cyber-security-architecture-for-enterprise-cloud": (
        "https://images.unsplash.com/photo-1563986768494-4dee2763ff36?w=1600&q=80",
        "Zero trust cybersecurity for enterprise cloud",
    ),
    # design
    "uiux-design-engineering-for-enterprise-conversions": (
        "https://images.unsplash.com/photo-1586717799252-bd134ad00e26?w=1600&q=80",
        "UI/UX design engineering for enterprise conversions",
    ),
    # APIs / hosting
    "graphql-vs-rest-apis-enterprise-architecture-strategy-guide": (
        "https://images.unsplash.com/photo-1516321165247-4aa89a64be82?w=1600&q=80",
        "GraphQL versus REST enterprise API architecture",
    ),
    "hostinger-hosting-website-builders-and-when-to-move-to-custom-infrastructure": (
        "https://images.unsplash.com/photo-1597852074816-d933c7bf97f9?w=1600&q=80",
        "Hosting website builders and custom infrastructure",
    ),
    # marketing/speed
    "shopify-speed-optimization-and-core-web-vitals-engineering": (
        "https://images.unsplash.com/photo-1432888498266-38ffec0f0d2e?w=1600&q=80",
        "Shopify speed optimization and Core Web Vitals",
    ),
    # headless
    "headless-shopify-architecture-next-js-and-storefront-api": (
        "https://images.unsplash.com/photo-1556742111-a301053dbe2e?w=1600&q=80",
        "Headless Shopify Next.js Storefront API architecture",
    ),
    # engineering roles / testing / micro frontends
    "oracle-sql-developer-vs-full-stack-developer-understanding-modern-engineering-roles": (
        "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=1600&q=80",
        "Oracle SQL developer versus full-stack engineering roles",
    ),
    "software-testing-automation-and-cicd-pipeline-strategy": (
        "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1600&q=80",
        "Software testing automation and CI/CD pipelines",
    ),
    "micro-frontends-architecture-for-enterprise-apps": (
        "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1600&q=80",
        "Micro frontends architecture for enterprise apps",
    ),
    # shopify plan / b2b
    "shopify-plan-guide-how-to-choose-the-right-plan-for-your-online-store": (
        "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1600&q=80",
        "Shopify plan guide for online stores",
    ),
    # modern tech stack sibling
    "modern-tech-stack-architecture-enterprise-guide": (
        "https://images.unsplash.com/photo-1518773553398-650c184e0bb3?w=1600&q=80",
        "Modern enterprise tech stack architecture",
    ),
}

FALLBACK_POOL = [
    "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=1600&q=80",
    "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1600&q=80",
    "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1600&q=80",
    "https://images.unsplash.com/photo-1553877522-43269d4ea984?w=1600&q=80",
    "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=1600&q=80",
    "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1600&q=80",
    "https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=1600&q=80",
    "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=1600&q=80",
    "https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?w=1600&q=80",
    "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1600&q=80",
    "https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?w=1600&q=80",
    "https://images.unsplash.com/photo-1487058792273-3bb4e8d7f0d1?w=1600&q=80",
    "https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=1600&q=80",
    "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=1600&q=80",
    "https://images.unsplash.com/photo-1573164713985-8667cf75090f?w=1600&q=80",
]


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = resp.read()
    if len(data) < 5000:
        raise RuntimeError("too small")
    return data


def file_hash(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def update_html(slug: str, alt: str):
    path = BLOG_DIR / f"{slug}.html"
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
    abs_url = f"https://webhouseinc.co/assets/images/blog/{slug}.jpg"
    if 'property="og:image"' in html2:
        html2 = re.sub(
            r'<meta property="og:image" content="[^"]*"/>',
            f'<meta property="og:image" content="{abs_url}"/>',
            html2,
            count=1,
        )
    if html2 != html:
        path.write_text(html2, encoding="utf-8")


def download_unique(slug: str, url: str, alt: str, used_hashes: set, fallback_idx: list):
    dest = IMG_DIR / f"{slug}.jpg"
    urls = [url] + FALLBACK_POOL
    last_err = None
    for candidate in urls:
        try:
            data = fetch(candidate)
            h = hashlib.md5(data).hexdigest()
            if h in used_hashes:
                print(f"  skip duplicate hash for {slug}")
                continue
            dest.write_bytes(data)
            used_hashes.add(h)
            update_html(slug, alt)
            print(f"  OK {slug} ({len(data)} bytes)")
            return True
        except Exception as e:
            last_err = e
            continue
    print(f"  FAIL {slug}: {last_err}")
    return False


def main():
    # current hashes in use
    used_hashes = set()
    slug_to_file = {}
    for p in BLOG_DIR.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        m = re.search(r'src="\.\./assets/images/blog/([^"]+)"', t)
        if not m:
            continue
        f = IMG_DIR / m.group(1)
        slug_to_file[p.stem] = f
        if f.exists():
            used_hashes.add(file_hash(f))

    # find duplicates; keep first slug, replace others
    by_hash = defaultdict(list)
    for slug, f in slug_to_file.items():
        if f.exists():
            by_hash[file_hash(f)].append(slug)

    to_replace = set(FORCE.keys())
    for h, slugs in by_hash.items():
        if len(slugs) > 1:
            # keep first alphabetically unless it's in FORCE
            keep = None
            for s in sorted(slugs):
                if s not in FORCE:
                    keep = s
                    break
            if keep is None:
                keep = sorted(slugs)[0]
            for s in slugs:
                if s != keep:
                    to_replace.add(s)

    # merge FORCE + DEDUP targets
    jobs = {}
    jobs.update(DEDUP)
    jobs.update(FORCE)  # force overrides

    # only process needed + any still-duplicate not covered
    for slug in sorted(to_replace):
        if slug not in jobs:
            # assign from fallback pool via DEDUP-less entry
            jobs[slug] = (
                FALLBACK_POOL[len(jobs) % len(FALLBACK_POOL)],
                slug.replace("-", " "),
            )

    print(f"replacing {len(to_replace)} blogs for uniqueness")
    # remove old hashes for targets so we can re-add new ones
    for slug in to_replace:
        f = slug_to_file.get(slug)
        if f and f.exists():
            try:
                used_hashes.discard(file_hash(f))
            except Exception:
                pass

    fallback_idx = [0]
    ok = fail = 0
    for slug in sorted(to_replace):
        url, alt = jobs[slug]
        print(f"download {slug}")
        if download_unique(slug, url, alt, used_hashes, fallback_idx):
            ok += 1
        else:
            fail += 1

    # final uniqueness verification
    by_hash = defaultdict(list)
    for p in BLOG_DIR.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        m = re.search(r'src="\.\./assets/images/blog/([^"]+)"', t)
        if not m:
            continue
        f = IMG_DIR / m.group(1)
        if f.exists():
            by_hash[file_hash(f)].append(p.stem)
    remaining = {h: s for h, s in by_hash.items() if len(s) > 1}
    print(f"DONE ok={ok} fail={fail}")
    print(f"remaining duplicate groups: {len(remaining)}")
    for h, slugs in remaining.items():
        print(h[:8], slugs)

    # cleanup unused
    used_names = set()
    for p in list(BLOG_DIR.glob("*.html")) + [ROOT / "blogs.html", ROOT / "index.html"]:
        if p.exists():
            used_names |= set(
                re.findall(r"assets/images/blog/([^\"'\s>]+)", p.read_text(encoding="utf-8"))
            )
    deleted = 0
    for f in IMG_DIR.iterdir():
        if f.is_file() and f.name not in used_names and f.suffix.lower() in {
            ".jpg", ".jpeg", ".png", ".webp", ".avif", ".jfif", ".gif", ".pdf"
        }:
            print("DELETE", f.name)
            f.unlink()
            deleted += 1
    print(f"deleted unused: {deleted}")


if __name__ == "__main__":
    main()
