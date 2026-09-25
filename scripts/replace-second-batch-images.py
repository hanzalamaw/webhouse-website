# -*- coding: utf-8 -*-
"""Replace second-batch blog images with topic-relevant Unsplash photos; delete unused assets."""
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "assets" / "images" / "blog"
BLOG_DIR = ROOT / "blog"

# Second batch blogs + relevant Unsplash photo URLs
REPLACEMENTS = {
    "ai-workflow-automation-and-rpa-for-enterprise-platforms": {
        "url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1600&q=80",
        "alt": "AI workflow automation and intelligent systems",
    },
    "cloud-native-microservices-architecture-strategy-guide": {
        "url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1600&q=80",
        "alt": "Cloud-native microservices and global infrastructure",
    },
    "custom-e-commerce-checkout-optimization-strategy": {
        "url": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=1600&q=80",
        "alt": "E-commerce checkout and online shopping experience",
    },
    "custom-shopify-app-development-and-api-integration": {
        "url": "https://images.unsplash.com/photo-1556740758-90de7981ce55?w=1600&q=80",
        "alt": "Custom Shopify app and API commerce development",
    },
    "custom-shopify-theme-development-liquid-and-tailwind-guide": {
        "url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1600&q=80",
        "alt": "Shopify theme design and storefront analytics",
    },
    "enterprise-llm-integration-prompt-engineering-guide": {
        "url": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1600&q=80",
        "alt": "Enterprise LLM integration and prompt engineering",
    },
    "enterprise-shopify-store-development-and-setup-services": {
        "url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1600&q=80",
        "alt": "Enterprise Shopify store setup and online retail",
    },
    "fintech-software-engineering-and-payment-integrations": {
        "url": "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=1600&q=80",
        "alt": "FinTech payments and secure digital transactions",
    },
    "graphql-vs-rest-apis-enterprise-architecture-strategy-guide": {
        "url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1600&q=80",
        "alt": "Enterprise API architecture and server infrastructure",
    },
    "headless-e-commerce-architecture-shopify-plus-and-next-js": {
        "url": "https://images.unsplash.com/photo-1556742111-a301553dbe2e?w=1600&q=80",
        "alt": "Headless e-commerce storefront and shopping experience",
    },
    "headless-shopify-architecture-next-js-and-storefront-api": {
        "url": "https://images.unsplash.com/photo-1472851294608-062f824d29cc?w=1600&q=80",
        "alt": "Headless Shopify commerce and modern storefronts",
    },
    "micro-frontends-architecture-for-enterprise-apps": {
        "url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1600&q=80",
        "alt": "Micro frontends and modular web application code",
    },
    "progressive-web-apps-pwas-vs-native-apps-guide": {
        "url": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=1600&q=80",
        "alt": "Progressive web apps and mobile devices",
    },
    "real-time-event-driven-architecture-websockets": {
        "url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1600&q=80",
        "alt": "Real-time event-driven systems and live dashboards",
    },
    "saas-multi-tenant-architecture-data-isolation": {
        "url": "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=1600&q=80",
        "alt": "SaaS multi-tenant software architecture and engineering",
    },
    "serverless-vs-containerization-enterprise-cloud-guide": {
        "url": "https://images.unsplash.com/photo-1544197150-b99a580bb7a2?w=1600&q=80",
        "alt": "Serverless and container cloud infrastructure",
    },
    "shopify-b2b-and-wholesale-portal-development-guide": {
        "url": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1600&q=80",
        "alt": "B2B wholesale commerce and retail operations",
    },
    "shopify-speed-optimization-and-core-web-vitals-engineering": {
        "url": "https://images.unsplash.com/photo-1432888622747-4eb9a8efeb07?w=1600&q=80",
        "alt": "Website speed optimization and performance metrics",
    },
    "software-testing-automation-and-cicd-pipeline-strategy": {
        "url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1600&q=80",
        "alt": "Software testing automation and CI/CD engineering",
    },
    "uiux-design-engineering-for-enterprise-conversions": {
        "url": "https://images.unsplash.com/photo-1581291518633-83b4ebd1d83b?w=1600&q=80",
        "alt": "UI/UX design engineering and product interfaces",
    },
    "zero-trust-cyber-security-architecture-for-enterprise-cloud": {
        "url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1600&q=80",
        "alt": "Zero trust cybersecurity and enterprise cloud protection",
    },
}


def download(url: str, dest: Path):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = resp.read()
    dest.write_bytes(data)
    if dest.stat().st_size < 5000:
        raise RuntimeError(f"download too small: {dest}")


def update_alt(slug: str, alt: str):
    path = BLOG_DIR / f"{slug}.html"
    if not path.exists():
        return
    html = path.read_text(encoding="utf-8")
    html2 = re.sub(
        rf'(src="../assets/images/blog/{re.escape(slug)}\.jpg" alt=")[^"]*(")',
        rf"\1{alt}\2",
        html,
        count=1,
    )
    if html2 != html:
        path.write_text(html2, encoding="utf-8")


def used_image_names():
    used = set()
    for html_path in list(BLOG_DIR.glob("*.html")) + [ROOT / "blogs.html", ROOT / "index.html"]:
        if not html_path.exists():
            continue
        text = html_path.read_text(encoding="utf-8")
        for m in re.finditer(r"assets/images/blog/([^\"'\s>]+)", text):
            used.add(m.group(1))
    return used


def main():
    for slug, meta in REPLACEMENTS.items():
        dest = IMG_DIR / f"{slug}.jpg"
        print(f"download {slug}")
        try:
            download(meta["url"], dest)
            update_alt(slug, meta["alt"])
            print(f"  OK {dest.stat().st_size} bytes")
        except Exception as e:
            print(f"  FAIL {e}")

    used = used_image_names()
    print(f"\nused images referenced: {len(used)}")
    deleted = []
    for f in IMG_DIR.iterdir():
        if not f.is_file():
            continue
        # keep only image-like; delete unused images + junk pdfs
        if f.name in used:
            continue
        if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".avif", ".jfif", ".gif", ".pdf"}:
            print(f"DELETE unused {f.name}")
            f.unlink()
            deleted.append(f.name)
    print(f"deleted {len(deleted)} unused files")


if __name__ == "__main__":
    main()
