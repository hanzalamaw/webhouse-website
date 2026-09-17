# -*- coding: utf-8 -*-
"""Redesign blog pages: spacious layout + hero images."""
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "blog"
IMG_DIR = ROOT / "assets" / "images" / "blog"
IMG_DIR.mkdir(parents=True, exist_ok=True)

# Topic-relevant Unsplash images (stable photo IDs)
BLOGS = {
    "custom-enterprise-software-vs-off-the-shelf": {
        "tag": "Custom Software",
        "img": "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=1600&q=80",
        "alt": "Enterprise software engineering workspace",
    },
    "ai-workflow-automation-enterprise-guide": {
        "tag": "AI Automation",
        "img": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1600&q=80",
        "alt": "Artificial intelligence and automation technology",
    },
    "headless-ecommerce-platform-engineering-guide": {
        "tag": "E-Commerce",
        "img": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=1600&q=80",
        "alt": "Modern e-commerce shopping experience",
    },
    "dedicated-software-engineering-teams-staff-augmentation": {
        "tag": "Dedicated Teams",
        "img": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1600&q=80",
        "alt": "Software engineering team collaboration",
    },
    "cloud-native-devops-infrastructure-guide": {
        "tag": "Cloud & DevOps",
        "img": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1600&q=80",
        "alt": "Cloud infrastructure and global network",
    },
    "cross-platform-mobile-app-engineering-guide": {
        "tag": "Mobile",
        "img": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=1600&q=80",
        "alt": "Cross-platform mobile application design",
    },
    "custom-erp-crm-development-workflow-optimization": {
        "tag": "ERP & CRM",
        "img": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1600&q=80",
        "alt": "Business analytics and workflow dashboards",
    },
    "b2b-growth-marketing-seo-tech-platforms": {
        "tag": "Growth Marketing",
        "img": "https://images.unsplash.com/photo-1432888622747-4eb9a8efeb07?w=1600&q=80",
        "alt": "Digital growth marketing and strategy",
    },
    "legacy-system-modernization-enterprise-transformation": {
        "tag": "Modernization",
        "img": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1600&q=80",
        "alt": "Technology modernization and circuit systems",
    },
    "enterprise-api-engineering-microservices-integration": {
        "tag": "API Engineering",
        "img": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1600&q=80",
        "alt": "Server infrastructure and API systems",
    },
    "enterprise-cybersecurity-engineering-compliance-guide": {
        "tag": "Cybersecurity",
        "img": "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=1600&q=80",
        "alt": "Cybersecurity and digital protection",
    },
    "enterprise-data-engineering-ai-analytics-guide": {
        "tag": "Data & Analytics",
        "img": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1600&q=80",
        "alt": "Data analytics and business intelligence dashboards",
    },
    "progressive-web-apps-vs-native-mobile-apps-strategy": {
        "tag": "PWA Strategy",
        "img": "https://images.unsplash.com/photo-1551650975-87deedd944c3?w=1600&q=80",
        "alt": "Progressive web app on mobile devices",
    },
    "enterprise-headless-cms-architecture-guide": {
        "tag": "Headless CMS",
        "img": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=1600&q=80",
        "alt": "Content creation and publishing workspace",
    },
    "ai-powered-customer-support-enterprise-automation": {
        "tag": "Customer Support",
        "img": "https://images.unsplash.com/photo-1556745757-8d76bdb6984b?w=1600&q=80",
        "alt": "Customer support and service communication",
    },
    "modern-tech-stack-architecture-enterprise-guide": {
        "tag": "Tech Stack",
        "img": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1600&q=80",
        "alt": "Modern software development tech stack",
    },
}


def download_images():
    for slug, meta in BLOGS.items():
        dest = IMG_DIR / f"{slug}.jpg"
        if dest.exists() and dest.stat().st_size > 10000:
            print(f"skip {slug}")
            continue
        print(f"download {slug}")
        req = urllib.request.Request(
            meta["img"],
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            dest.write_bytes(resp.read())


def extract_article_parts(html: str):
    """Pull title, body prose, and CTA from existing article."""
    title_m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    title = title_m.group(1).strip() if title_m else "Blog"

    prose_m = re.search(
        r'<div class="prose-blog[^"]*"[^>]*>(.*?)</div>\s*<div class="mt-16',
        html,
        re.S,
    )
    if not prose_m:
        prose_m = re.search(
            r'<div class="prose-blog[^"]*"[^>]*>(.*?)</div>',
            html,
            re.S,
        )
    body = prose_m.group(1).strip() if prose_m else ""

    cta_m = re.search(
        r'<div class="mt-16 rounded-3xl.*?">(.*?)</div>\s*</div>\s*</article>',
        html,
        re.S,
    )
    cta_title = "Talk to WebHouse Inc."
    cta_text = "Let's discuss how we can help your enterprise scale."
    if cta_m:
        ct = re.search(r"<h2[^>]*>(.*?)</h2>", cta_m.group(1), re.S)
        cp = re.search(r"<p[^>]*>(.*?)</p>", cta_m.group(1), re.S)
        if ct:
            cta_title = ct.group(1).strip()
        if cp:
            cta_text = cp.group(1).strip()

    return title, body, cta_title, cta_text


def build_article(slug, meta, title, body, cta_title, cta_text):
    img = f"../assets/images/blog/{slug}.jpg"
    return f'''
<main>
<article>
<!-- Hero -->
<section class="relative w-full pt-20">
<div class="relative h-[42vh] min-h-[280px] max-h-[480px] w-full overflow-hidden bg-gray-200">
<img src="{img}" alt="{meta["alt"]}" class="h-full w-full object-cover"/>
<div class="absolute inset-0 bg-gradient-to-t from-black/55 via-black/15 to-transparent"></div>
</div>
</section>

<!-- Header -->
<section class="bg-white">
<div class="mx-auto max-w-[760px] px-6 lg:px-10 pt-12 md:pt-16 pb-6">
<a href="../index.html#blogs" class="inline-flex items-center gap-2 text-sm font-medium text-gray-500 hover:text-primary transition-colors mb-8">
<span class="material-symbols-outlined text-base">arrow_back</span>
Back to Blogs
</a>
<span class="text-primary font-mono text-xs tracking-widest uppercase font-bold">{meta["tag"]}</span>
<h1 class="mt-4 font-display text-3xl md:text-5xl font-extrabold leading-tight tracking-tight text-[#1c1917]">{title}</h1>
</div>
</section>

<!-- Body -->
<section class="bg-white pb-20">
<div class="mx-auto max-w-[760px] px-6 lg:px-10">
<div class="blog-prose text-lg text-gray-600 leading-[1.85]">
{body}
</div>

<div class="mt-20 rounded-[2rem] bg-[#1c1917] p-10 md:p-14">
<h2 class="font-display text-2xl md:text-3xl font-bold text-white mb-4 leading-snug">{cta_title}</h2>
<p class="text-gray-400 text-base leading-relaxed mb-8 max-w-xl">{cta_text}</p>
<a href="../contact_us.html" class="inline-flex h-12 items-center justify-center rounded-full bg-gradient-to-r from-[#b90606] to-[#c80505] px-8 text-sm font-bold text-white shadow-glow hover:opacity-90 transition-all">Get Started</a>
</div>
</div>
</section>
</article>
</main>
'''


def redesign_file(path: Path):
    slug = path.stem
    if slug not in BLOGS:
        print(f"unknown {slug}")
        return
    meta = BLOGS[slug]
    html = path.read_text(encoding="utf-8")
    title, body, cta_title, cta_text = extract_article_parts(html)
    if not body:
        print(f"no body {slug}")
        return

    new_article = build_article(slug, meta, title, body, cta_title, cta_text)
    updated, n = re.subn(
        r"<main>.*?</main>",
        new_article.strip(),
        html,
        count=1,
        flags=re.S,
    )
    if n != 1:
        print(f"replace failed {slug}")
        return

    # Add og:image if missing
    og_img = f'    <meta property="og:image" content="https://webhouseinc.co/assets/images/blog/{slug}.jpg"/>\n'
    if "og:image" not in updated:
        updated = updated.replace(
            '<meta property="og:type" content="article"/>',
            '<meta property="og:type" content="article"/>\n' + og_img,
        )

    path.write_text(updated, encoding="utf-8")
    print(f"redesigned {slug}")


def main():
    download_images()
    for path in sorted(BLOG_DIR.glob("*.html")):
        redesign_file(path)


if __name__ == "__main__":
    main()
