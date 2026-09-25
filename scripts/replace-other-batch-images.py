# -*- coding: utf-8 -*-
"""Replace remaining blog-batch images with topic-relevant Unsplash photos."""
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "assets" / "images" / "blog"
BLOG_DIR = ROOT / "blog"

REPLACEMENTS = {
    "ai-agent-workflow-automation-enterprise-guide": (
        "https://images.unsplash.com/photo-1676299080920-bfbc1c8c8b8a?w=1600&q=80",
        "AI agents and enterprise workflow automation",
    ),
    "ai-developer-guide-how-businesses-can-build-useful-ai-products": (
        "https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=1600&q=80",
        "AI product development for business teams",
    ),
    "apple-developer-and-ios-engineering-planning-apps-for-the-apple-ecosystem": (
        "https://images.unsplash.com/photo-1512499617640-c74ae3a79d37?w=1600&q=80",
        "Apple iOS app engineering and mobile devices",
    ),
    "cloud-native-architecture-devops-enterprise-scaling": (
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1600&q=80",
        "Cloud-native architecture and global infrastructure",
    ),
    "complaint-management-system-turning-customer-feedback-into-digital-workflows": (
        "https://images.unsplash.com/photo-1556745757-8d76bdb6984b?w=1600&q=80",
        "Customer feedback and complaint management workflows",
    ),
    "cross-platform-mobile-app-development-strategy-guide": (
        "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=1600&q=80",
        "Cross-platform mobile app development",
    ),
    "custom-erp-crm-vs-off-the-shelf-software": (
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1600&q=80",
        "Custom ERP and CRM business software dashboards",
    ),
    "custom-software-development-scaling-enterprises": (
        "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=1600&q=80",
        "Custom enterprise software development and coding",
    ),
    "cybersecurity-software-and-cybersecurity-engineers-building-safer-digital-systems": (
        "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1600&q=80",
        "Cybersecurity engineering and digital protection",
    ),
    "dedicated-software-engineering-teams-scale": (
        "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1600&q=80",
        "Dedicated software engineering team collaboration",
    ),
    "digital-system-design-and-figma-from-product-idea-to-scalable-interface": (
        "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=1600&q=80",
        "Digital product design and Figma interface work",
    ),
    "enterprise-cloud-native-architecture-devops-guide": (
        "https://images.unsplash.com/photo-1544197150-b99a580bb7a2?w=1600&q=80",
        "Enterprise cloud DevOps and data center systems",
    ),
    "enterprise-dedicated-teams-staff-augmentation-guide": (
        "https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=1600&q=80",
        "Dedicated teams and staff augmentation collaboration",
    ),
    "enterprise-generative-ai-intelligent-systems-guide": (
        "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1600&q=80",
        "Generative AI and intelligent enterprise systems",
    ),
    "enterprise-growth-marketing-technical-seo-guide": (
        "https://images.unsplash.com/photo-1432888622747-4eb9a8efeb07?w=1600&q=80",
        "Growth marketing and technical SEO strategy",
    ),
    "enterprise-seo-strategy-technical-growth-guide": (
        "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=1600&q=80",
        "Enterprise SEO strategy and growth analytics",
    ),
    "enterprise-ui-ux-design-product-experience-guide": (
        "https://images.unsplash.com/photo-1586717791821-3f44a563fa4c?w=1600&q=80",
        "Enterprise UI/UX product experience design",
    ),
    "event-management-website-features-design-and-development-checklist": (
        "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=1600&q=80",
        "Event management website and live events",
    ),
    "full-stack-web-development-mern-react-and-cloud-in-one-architecture": (
        "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1600&q=80",
        "Full-stack web development with modern frameworks",
    ),
    "future-of-web-development-ai-cloud-ux-and-search-in-the-next-era": (
        "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=1600&q=80",
        "Future of web development AI cloud and UX",
    ),
    "generative-ai-enterprise-workflow-automation-2026": (
        "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1600&q=80",
        "Generative AI enterprise workflow automation",
    ),
    "google-ads-and-seo-services-how-paid-and-organic-search-work-together": (
        "https://images.unsplash.com/photo-1557838923-2985c318be48?w=1600&q=80",
        "Google Ads and SEO search marketing",
    ),
    "headless-commerce-nextjs-shopify-scaling": (
        "https://images.unsplash.com/photo-1472851294608-062f824d29cc?w=1600&q=80",
        "Headless commerce Shopify and Next.js scaling",
    ),
    "hostinger-hosting-website-builders-and-when-to-move-to-custom-infrastructure": (
        "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1600&q=80",
        "Web hosting infrastructure and servers",
    ),
    "how-to-choose-a-shopify-developer-or-shopify-partner-for-a-growing-brand": (
        "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=1600&q=80",
        "Choosing a Shopify developer for growing brands",
    ),
    "meta-developer-app-and-modern-api-integration-a-business-guide": (
        "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=1600&q=80",
        "Meta developer apps and modern API integration",
    ),
    "mobile-app-development-in-2026-android-ios-and-react-native-explained": (
        "https://images.unsplash.com/photo-1551650975-87deedd944c3?w=1600&q=80",
        "Mobile app development for Android iOS and React Native",
    ),
    "native-vs-cross-platform-app-development-2026": (
        "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=1600&q=80",
        "Native versus cross-platform mobile app development",
    ),
    "oracle-aws-and-azure-connecting-enterprise-development-with-modern-cloud": (
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1600&q=80",
        "Oracle AWS and Azure enterprise cloud platforms",
    ),
    "oracle-sql-developer-vs-full-stack-developer-understanding-modern-engineering-roles": (
        "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1600&q=80",
        "Software engineering roles and full-stack development",
    ),
    "shopify-admin-and-shopify-dev-docs-a-practical-guide-for-store-teams": (
        "https://images.unsplash.com/photo-1556740738-b6a63e27c4df?w=1600&q=80",
        "Shopify admin and store operations for teams",
    ),
    "shopify-plan-guide-how-to-choose-the-right-plan-for-your-online-store": (
        "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1600&q=80",
        "Shopify plan guide for online stores",
    ),
    "shopify-themes-vs-custom-development-what-should-your-store-use": (
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1600&q=80",
        "Shopify themes versus custom store development",
    ),
    "web-development-company-vs-web-development-agency-how-to-choose-a-team": (
        "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1600&q=80",
        "Choosing a web development company or agency team",
    ),
    "web-development-services-in-lahore-pakistan-and-major-global-cities": (
        "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=1600&q=80",
        "Web development services and global digital teams",
    ),
}

# fallbacks if primary 404s
FALLBACKS = {
    "ai-agent-workflow-automation-enterprise-guide": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1600&q=80",
    "ai-developer-guide-how-businesses-can-build-useful-ai-products": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1600&q=80",
    "apple-developer-and-ios-engineering-planning-apps-for-the-apple-ecosystem": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=1600&q=80",
    "enterprise-cloud-native-architecture-devops-guide": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1600&q=80",
    "enterprise-seo-strategy-technical-growth-guide": "https://images.unsplash.com/photo-1432888622747-4eb9a8efeb07?w=1600&q=80",
    "enterprise-ui-ux-design-product-experience-guide": "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=1600&q=80",
    "google-ads-and-seo-services-how-paid-and-organic-search-work-together": "https://images.unsplash.com/photo-1432888622747-4eb9a8efeb07?w=1600&q=80",
    "meta-developer-app-and-modern-api-integration-a-business-guide": "https://images.unsplash.com/photo-1611162616305-c69b3fa7fbe0?w=1600&q=80",
    "shopify-admin-and-shopify-dev-docs-a-practical-guide-for-store-teams": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=1600&q=80",
}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        return resp.read()


def download(slug: str, url: str, alt: str):
    dest = IMG_DIR / f"{slug}.jpg"
    try:
        data = fetch(url)
    except Exception as e:
        fb = FALLBACKS.get(slug)
        if not fb:
            raise
        print(f"  retry fallback after {e}")
        data = fetch(fb)
    if len(data) < 5000:
        raise RuntimeError("too small")
    dest.write_bytes(data)

    path = BLOG_DIR / f"{slug}.html"
    if path.exists():
        html = path.read_text(encoding="utf-8")
        html2 = re.sub(
            rf'(src="../assets/images/blog/{re.escape(slug)}\.(?:jpg|jpeg|png|webp|avif|jfif)" alt=")[^"]*(")',
            rf"\1{alt}\2",
            html,
            count=1,
        )
        # also normalize extension in src to .jpg
        html2 = re.sub(
            rf'src="../assets/images/blog/{re.escape(slug)}\.(?:jpg|jpeg|png|webp|avif|jfif)"',
            f'src="../assets/images/blog/{slug}.jpg"',
            html2,
        )
        if html2 != html:
            path.write_text(html2, encoding="utf-8")


def cleanup_unused():
    used = set()
    for p in list(BLOG_DIR.glob("*.html")) + [ROOT / "blogs.html", ROOT / "index.html"]:
        if not p.exists():
            continue
        used |= set(re.findall(r"assets/images/blog/([^\"'\s>]+)", p.read_text(encoding="utf-8")))
    deleted = []
    for f in IMG_DIR.iterdir():
        if f.is_file() and f.name not in used:
            if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".avif", ".jfif", ".gif", ".pdf"}:
                print(f"DELETE {f.name}")
                f.unlink()
                deleted.append(f.name)
    print(f"deleted {len(deleted)} unused")


def main():
    ok = fail = 0
    for slug, (url, alt) in REPLACEMENTS.items():
        print(f"download {slug}")
        try:
            download(slug, url, alt)
            size = (IMG_DIR / f"{slug}.jpg").stat().st_size
            print(f"  OK {size}")
            ok += 1
        except Exception as e:
            print(f"  FAIL {e}")
            fail += 1
    # update listings that may still point to old extensions
    for page in (ROOT / "blogs.html", ROOT / "index.html"):
        if not page.exists():
            continue
        text = page.read_text(encoding="utf-8")
        text2 = text
        for slug in REPLACEMENTS:
            text2 = re.sub(
                rf'(assets/images/blog/{re.escape(slug)})\.(?:jfif|png|webp|avif|jpeg)',
                rf"\1.jpg",
                text2,
            )
        if text2 != text:
            page.write_text(text2, encoding="utf-8")
            print(f"updated extensions in {page.name}")
    cleanup_unused()
    print(f"DONE ok={ok} fail={fail}")


if __name__ == "__main__":
    main()
