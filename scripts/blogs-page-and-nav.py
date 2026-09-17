# -*- coding: utf-8 -*-
"""Create blogs.html, update home + posts per latest UX requests."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CARDS = [
    ("custom-enterprise-software-vs-off-the-shelf", "Custom Software", "Custom Enterprise Software vs. Off-the-Shelf: 2026 Strategic Guide", "Compare custom enterprise software development with off-the-shelf platforms. Discover why enterprise leaders choose custom software for scalability and security."),
    ("ai-workflow-automation-enterprise-guide", "AI Automation", "AI Workflow Automation: Scaling Enterprise Efficiency in 2026", "Streamline enterprise operations with custom AI workflow automation solutions, generative AI models, and autonomous AI agents."),
    ("headless-ecommerce-platform-engineering-guide", "E-Commerce", "Headless E-Commerce Engineering: Scaling Enterprise Growth (2026)", "Discover how headless e-commerce engineering and custom web development accelerate load speeds, conversion rates, and global enterprise growth."),
    ("dedicated-software-engineering-teams-staff-augmentation", "Dedicated Teams", "Dedicated Developer Teams: Scaling Engineering Capacity in 2026", "Scale software engineering capacity rapidly with dedicated development teams and IT staff augmentation."),
    ("cloud-native-devops-infrastructure-guide", "Cloud &amp; DevOps", "Cloud-Native Infrastructure &amp; DevOps Best Practices (2026 Guide)", "Modernize enterprise IT with cloud-native DevOps infrastructure, microservices, Docker, Kubernetes, and automated CI/CD pipelines."),
    ("cross-platform-mobile-app-engineering-guide", "Mobile", "Cross-Platform Mobile App Engineering: Flutter &amp; React Native (2026)", "Scale mobile deployment across iOS and Android with cross-platform engineering using Flutter and React Native."),
    ("custom-erp-crm-development-workflow-optimization", "ERP &amp; CRM", "Custom ERP &amp; CRM Systems: Streamlining Enterprise Workflows (2026)", "Streamline operations with custom ERP &amp; CRM software engineering. Eliminate manual data silos for global scale."),
    ("b2b-growth-marketing-seo-tech-platforms", "Growth Marketing", "B2B Growth Marketing &amp; SEO for Enterprise Tech Platforms (2026)", "Drive predictable B2B pipeline growth with SEO, targeted performance marketing, and high-converting content strategies."),
    ("legacy-system-modernization-enterprise-transformation", "Modernization", "Legacy System Modernization: Transforming Enterprise Software (2026)", "Eliminate technical debt and modernize legacy software systems with microservices and cloud infrastructure."),
    ("enterprise-api-engineering-microservices-integration", "API Engineering", "Enterprise API Engineering &amp; Microservices Integration (2026 Guide)", "Connect enterprise software systems with custom API engineering and secure middleware for real-time data flow."),
    ("enterprise-cybersecurity-engineering-compliance-guide", "Cybersecurity", "Enterprise Cybersecurity Engineering &amp; Compliance Standards (2026)", "Safeguard enterprise digital assets with zero-trust security architecture and automated compliance controls."),
    ("enterprise-data-engineering-ai-analytics-guide", "Data &amp; Analytics", "Enterprise Data Engineering &amp; AI Analytics Pipelines (2026)", "Transform raw corporate data into actionable strategic intelligence with data engineering and AI analytics."),
    ("progressive-web-apps-vs-native-mobile-apps-strategy", "PWA Strategy", "Progressive Web Apps (PWAs) vs Native Apps: 2026 Strategy Guide", "Compare Progressive Web Apps and native apps for enterprise expansion and mobile engagement."),
    ("enterprise-headless-cms-architecture-guide", "Headless CMS", "Enterprise Headless CMS Architecture: Multi-Channel Publishing (2026)", "Scale content management with enterprise headless CMS architecture across web, mobile, and digital portals."),
    ("ai-powered-customer-support-enterprise-automation", "Customer Support", "AI Customer Support Automation: Enterprise Scaling in 2026", "Transform customer experience with enterprise AI customer support automation and intelligent ticket routing."),
    ("modern-tech-stack-architecture-enterprise-guide", "Tech Stack", "Modern Tech Stack Architecture for Enterprise Platforms (2026)", "Scale enterprise software with a modern tech stack spanning backend, cloud, AI, and e-commerce integrations."),
]


def card_html(slug, tag, title, desc, prefix=""):
    return f'''<a href="{prefix}blog/{slug}.html" class="group flex flex-col overflow-hidden rounded-[2rem] bg-white border border-gray-100 hover:shadow-card hover:-translate-y-1 transition-all duration-300">
<div class="h-52 overflow-hidden bg-gray-100">
<img src="{prefix}assets/images/blog/{slug}.jpg" alt="{tag}" class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"/>
</div>
<div class="flex flex-col flex-1 p-7 md:p-8">
<span class="text-xs font-bold uppercase tracking-wider text-primary mb-3">{tag}</span>
<h3 class="text-xl font-display font-bold text-[#1c1917] mb-3 leading-snug group-hover:text-primary transition-colors">{title}</h3>
<p class="text-sm text-gray-500 leading-relaxed mb-6 flex-1">{desc}</p>
<span class="inline-flex items-center gap-2 text-sm font-bold text-primary group-hover:gap-3 transition-all">Read article <span class="material-symbols-outlined text-sm">arrow_forward</span></span>
</div>
</a>'''


def create_blogs_page():
    cards = "\n".join(card_html(*c) for c in CARDS)
    html = f'''<!DOCTYPE html>
<html class="light" lang="en">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <meta name="description" content="WebHouse Inc. blogs — enterprise guides on custom software, AI, cloud, e-commerce, and digital growth."/>
    <meta name="keywords" content="webhouse blog, enterprise software, AI automation, cloud devops, digital transformation"/>
    <meta name="author" content="WebHouse Inc."/>
    <meta property="og:title" content="Blogs - WebHouse Inc."/>
    <meta property="og:description" content="Enterprise guides on custom software, AI, cloud, e-commerce, and digital growth."/>
    <meta property="og:type" content="website"/>
    <meta name="twitter:card" content="summary_large_image"/>
    <link rel="canonical" href="https://webhouseinc.co/blogs.html"/>
    <title>Blogs - WebHouse Inc.</title>
    <link rel="preconnect" href="https://fonts.googleapis.com"/>
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <script src="js/tailwind-config.js"></script>
    <link rel="stylesheet" href="css/styles.css"/>
</head>
<body class="bg-background-light text-[#1c1917] selection:bg-primary selection:text-white">
<div class="relative flex h-auto min-h-screen w-full flex-col overflow-x-hidden">
<header class="fixed top-0 z-50 w-full bg-white/80 backdrop-blur-xl border-b border-gray-100 transition-all duration-300 group/header">
<div class="mx-auto flex h-20 max-w-[1400px] items-center justify-between px-6 lg:px-10">
<a href="index.html" class="flex items-center gap-3 group cursor-pointer">
<img src="assets/images/logo.png" alt="WebHouse Inc." class="h-7 w-auto object-contain"/>
</a>
<nav class="hidden md:flex items-center gap-2 rounded-full p-1.5 bg-gray-100/50 border border-gray-200/50 backdrop-blur-md">
    <a class="px-5 py-2 text-sm font-medium rounded-full text-gray-600 hover:text-black hover:bg-white hover:shadow-sm transition-all" href="index.html">Home</a>
    <a class="px-5 py-2 text-sm font-medium rounded-full text-gray-600 hover:text-black hover:bg-white hover:shadow-sm transition-all" href="about.html">Who We Are?</a>
    <a class="px-5 py-2 text-sm font-medium rounded-full text-gray-600 hover:text-black hover:bg-white hover:shadow-sm transition-all" href="how-we-work.html">How We Work?</a>
    <div class="relative" data-mega-menu-trigger="services">
    <a class="px-5 py-2 text-sm font-medium rounded-full text-gray-600 hover:text-black hover:bg-white hover:shadow-sm transition-all inline-block" href="services.html">What We Do?</a>
    </div>
<div class="relative" data-mega-menu-trigger="technologies">
<a class="px-5 py-2 text-sm font-medium rounded-full text-gray-600 hover:text-black hover:bg-white hover:shadow-sm transition-all inline-block" href="technologies.html">Technologies</a>
</div>
<a class="px-5 py-2 text-sm font-medium rounded-full text-gray-600 hover:text-black hover:bg-white hover:shadow-sm transition-all" href="contact_us.html">Contact</a>
</nav>
<div class="flex items-center gap-4">
<a href="contact_us.html" class="hidden sm:flex h-10 items-center justify-center rounded-full bg-transparent px-5 text-sm font-bold text-black hover:text-primary transition-all">Log in</a>
<a href="contact_us.html" class="hidden sm:flex h-10 items-center justify-center rounded-full bg-gradient-to-r from-[#b90606] to-[#c80505] px-5 text-sm font-bold text-white shadow-glow hover:opacity-90 transition-all transform hover:scale-105">Get Started</a>
<button class="md:hidden p-2 text-gray-600 hover:text-primary transition-colors" aria-label="Toggle mobile menu" data-mobile-menu-toggle><span class="material-symbols-outlined">menu</span></button>
</div>
</div>
<div data-mega-menu-panel="services" class="absolute left-0 right-0 top-full pt-0 bg-white border-b border-gray-100 shadow-xl invisible opacity-0 transition-all duration-200 z-40">
<div class="max-w-[1400px] mx-auto px-6 lg:px-10 py-8">
<div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
<div class="lg:col-span-4 pr-8 border-r border-gray-100"><h3 class="font-display text-xl font-bold text-[#1c1917] mb-3">Built to Win</h3><p class="text-sm text-gray-500 leading-relaxed mb-6">Transforming business with our future-ready tech solutions.</p><a href="contact_us.html" class="inline-flex items-center gap-2 text-primary font-bold text-sm hover:gap-3 transition-all">Get In Touch <span class="material-symbols-outlined text-lg">arrow_forward</span></a></div>
<div class="lg:col-span-8 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-x-8 gap-y-6">
<div><a href="services/product-platform-engineering.html" class="block font-bold text-[#1c1917] hover:text-primary mb-3">Product &amp; Platform Engineering</a></div>
<div><a href="services/custom-software-enterprise-systems.html" class="block font-bold text-[#1c1917] hover:text-primary mb-3">Custom Software &amp; Enterprise Systems</a></div>
<div><a href="services/web-ecommerce-engineering.html" class="block font-bold text-[#1c1917] hover:text-primary mb-3">Web &amp; E-Commerce Engineering</a></div>
<div><a href="services/ai-data-intelligent-systems.html" class="block font-bold text-[#1c1917] hover:text-primary mb-3">AI, Data &amp; Intelligent Systems</a></div>
<div><a href="services/cloud-devops-infrastructure.html" class="block font-bold text-[#1c1917] hover:text-primary mb-3">Cloud, DevOps &amp; Infrastructure</a></div>
<div><a href="services/dedicated-teams-staff-augmentation.html" class="block font-bold text-[#1c1917] hover:text-primary mb-3">Dedicated Teams &amp; Staff Augmentation</a></div>
<div><a href="services/growth-marketing-performance.html" class="block font-bold text-[#1c1917] hover:text-primary mb-3">Growth, Marketing &amp; Performance</a></div>
</div>
</div>
</div>
</div>
<div data-mega-menu-panel="technologies" class="absolute left-0 right-0 top-full pt-0 bg-white border-b border-gray-100 shadow-xl invisible opacity-0 transition-all duration-200 z-40">
<div class="max-w-[1400px] mx-auto px-6 lg:px-10 py-8">
<div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
<div class="lg:col-span-4 pr-8 border-r border-gray-100"><h3 class="font-display text-xl font-bold text-[#1c1917] mb-3">Technology Stack</h3><p class="text-sm text-gray-500 leading-relaxed mb-6">We harness revolutionary technologies to create custom solutions.</p><a href="technologies.html" class="inline-flex items-center gap-2 text-primary font-bold text-sm hover:gap-3 transition-all">View Technologies <span class="material-symbols-outlined text-lg">arrow_forward</span></a></div>
<div class="lg:col-span-8 grid grid-cols-1 md:grid-cols-2 gap-8">
<div><a href="technologies.html" class="block font-bold text-[#1c1917] hover:text-primary mb-3">Languages</a><a href="language/dot-net.html" class="block text-gray-500 text-xs mb-1 hover:text-primary">&gt; .NET</a><a href="language/html5.html" class="block text-gray-500 text-xs mb-1 hover:text-primary">&gt; HTML5</a><a href="language/java.html" class="block text-gray-500 text-xs mb-1 hover:text-primary">&gt; Java</a><a href="language/nodejs.html" class="block text-gray-500 text-xs mb-1 hover:text-primary">&gt; Node.js</a><a href="language/php.html" class="block text-gray-500 text-xs mb-1 hover:text-primary">&gt; PHP</a><a href="language/python.html" class="block text-gray-500 text-xs hover:text-primary">&gt; Python</a></div>
<div><a href="technologies.html#platforms" class="block font-bold text-[#1c1917] hover:text-primary mb-3">Platforms</a><a href="platform/azure.html" class="block text-gray-500 text-xs mb-1 hover:text-primary">&gt; Azure</a><a href="platform/gcp.html" class="block text-gray-500 text-xs mb-1 hover:text-primary">&gt; GCP</a><a href="platform/oracle.html" class="block text-gray-500 text-xs mb-1 hover:text-primary">&gt; Oracle</a><a href="platform/sap.html" class="block text-gray-500 text-xs hover:text-primary">&gt; SAP</a></div>
</div>
</div>
</div>
</div>
</header>
<div data-mobile-menu class="fixed inset-0 top-20 z-40 bg-white hidden overflow-y-auto md:hidden">
<nav class="flex flex-col p-6 gap-4">
<a href="index.html" class="px-4 py-3 text-lg font-medium text-gray-600 hover:text-black hover:bg-gray-100 rounded-lg transition-all">Home</a>
<a href="about.html" class="px-4 py-3 text-lg font-medium text-gray-600 hover:text-black hover:bg-gray-100 rounded-lg transition-all">Who We Are?</a>
<a href="how-we-work.html" class="px-4 py-3 text-lg font-medium text-gray-600 hover:text-black hover:bg-gray-100 rounded-lg transition-all">How We Work?</a>
<a href="services.html" class="px-4 py-3 text-lg font-medium text-gray-600 hover:text-black hover:bg-gray-100 rounded-lg transition-all">What We Do?</a>
<a href="technologies.html" class="px-4 py-3 text-lg font-medium text-gray-600 hover:text-black hover:bg-gray-100 rounded-lg transition-all">Technologies</a>
<a href="contact_us.html" class="px-4 py-3 text-lg font-medium text-gray-600 hover:text-black hover:bg-gray-100 rounded-lg transition-all">Contact</a>
<div class="border-t border-gray-100 mt-4 pt-4">
<a href="contact_us.html" class="flex items-center justify-center h-12 rounded-full bg-gradient-to-r from-[#b90606] to-[#c80505] text-white font-bold shadow-glow hover:opacity-90 transition-all">Get Started</a>
</div>
</nav>
</div>

<main class="flex-1">
<section class="bg-white pt-32 pb-12 px-6 lg:px-10">
<div class="mx-auto max-w-[1400px]">
<h1 class="font-display text-4xl md:text-6xl font-extrabold leading-tight tracking-tight text-[#1c1917]">Blogs</h1>
</div>
</section>
<section class="px-6 lg:px-10 pb-24">
<div class="mx-auto max-w-[1400px]">
<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
{cards}
</div>
</div>
</section>
</main>

<footer class="w-full bg-white pt-20 pb-10 border-t border-gray-100">
<div class="mx-auto flex max-w-[1400px] flex-col justify-between gap-16 px-6 lg:px-10">
<div class="grid grid-cols-1 md:grid-cols-12 gap-12">
<div class="col-span-1 md:col-span-4 flex flex-col gap-8">
<div class="flex items-center gap-2"><img src="assets/images/logo.png" alt="WebHouse Inc." class="h-8 w-auto object-contain"/></div>
<p class="text-base leading-relaxed text-gray-500 max-w-sm">Strategic digital execution partner for forward-thinking enterprises. We design, build, and scale technology-driven solutions globally.</p>
</div>
<div class="col-span-1 md:col-span-2">
<h4 class="text-sm font-bold uppercase tracking-wider text-[#1c1917] mb-6">Company</h4>
<div class="flex flex-col gap-4">
<a class="text-sm font-medium text-gray-600 hover:text-primary transition-colors" href="index.html">Home</a>
<a class="text-sm font-medium text-gray-600 hover:text-primary transition-colors" href="about.html">Who We Are?</a>
<a class="text-sm font-medium text-gray-600 hover:text-primary transition-colors" href="how-we-work.html">How We Work?</a>
<a class="text-sm font-medium text-gray-600 hover:text-primary transition-colors" href="technologies.html">Technologies</a>
<a class="text-sm font-medium text-gray-600 hover:text-primary transition-colors" href="blogs.html">Blogs</a>
<a class="text-sm font-medium text-gray-600 hover:text-primary transition-colors" href="contact_us.html">Contact</a>
</div>
</div>
<div class="col-span-1 md:col-span-3">
<h4 class="text-sm font-bold uppercase tracking-wider text-[#1c1917] mb-6">Services</h4>
<div class="flex flex-col gap-4">
<a class="text-sm font-medium text-gray-600 hover:text-primary transition-colors" href="services/product-platform-engineering.html">Product &amp; Platform Engineering</a>
<a class="text-sm font-medium text-gray-600 hover:text-primary transition-colors" href="services/custom-software-enterprise-systems.html">Custom Software &amp; Enterprise Systems</a>
<a class="text-sm font-medium text-gray-600 hover:text-primary transition-colors" href="services/web-ecommerce-engineering.html">Web &amp; E-Commerce Engineering</a>
<a class="text-sm font-medium text-gray-600 hover:text-primary transition-colors" href="services/ai-data-intelligent-systems.html">AI, Data &amp; Intelligent Systems</a>
<a class="text-sm font-medium text-gray-600 hover:text-primary transition-colors" href="services/cloud-devops-infrastructure.html">Cloud, DevOps &amp; Infrastructure</a>
<a class="text-sm font-medium text-gray-600 hover:text-primary transition-colors" href="services/dedicated-teams-staff-augmentation.html">Dedicated Teams &amp; Staff Augmentation</a>
<a class="text-sm font-medium text-gray-600 hover:text-primary transition-colors" href="services/growth-marketing-performance.html">Growth, Marketing &amp; Performance</a>
</div>
</div>
<div class="col-span-1 md:col-span-3">
<h4 class="text-sm font-bold uppercase tracking-wider text-[#1c1917] mb-6">Newsletter</h4>
<p class="text-sm text-gray-500 mb-4">Get insights on technology, digital transformation, and growth strategies.</p>
<form data-newsletter-form class="flex flex-col gap-3">
<input class="w-full rounded-lg border border-gray-200 bg-gray-50 px-4 py-2 text-sm focus:border-primary focus:ring-primary outline-none transition" placeholder="Your email address" type="email" required/>
<button type="submit" class="w-full bg-black text-white px-4 py-2 rounded-lg text-sm font-bold hover:bg-gradient-to-r hover:from-[#b90606] hover:to-[#c80505] transition-all">Subscribe</button>
</form>
</div>
</div>
<div class="flex flex-col md:flex-row justify-between items-center gap-6 border-t border-gray-100 pt-8">
<p class="text-xs text-gray-400">&copy; 2026 WebHouse Inc. All rights reserved.</p>
<div class="flex gap-8">
<a class="text-xs font-medium text-gray-500 hover:text-black transition-colors" href="mailto:connect@webhouseinc.co?subject=Privacy%20Policy%20Inquiry">Privacy Policy</a>
<a class="text-xs font-medium text-gray-500 hover:text-black transition-colors" href="mailto:connect@webhouseinc.co?subject=Terms%20of%20Service%20Inquiry">Terms of Service</a>
</div>
</div>
</div>
</footer>
</div>
<script src="js/form-config.js"></script>
<script src="js/main.js"></script>
<script src="js/mega-menu.js"></script>
</body>
</html>
'''
    (ROOT / "blogs.html").write_text(html, encoding="utf-8")
    print("created blogs.html")


def update_index():
    path = ROOT / "index.html"
    html = path.read_text(encoding="utf-8")

    # Remove Blogs from desktop nav
    html = html.replace(
        '\n<a class="px-5 py-2 text-sm font-medium rounded-full text-gray-600 hover:text-black hover:bg-white hover:shadow-sm transition-all" href="#blogs">Blogs</a>',
        "",
    )
    # Remove Blogs from mobile nav
    html = html.replace(
        '\n        <a href="#blogs" class="px-4 py-3 text-lg font-medium text-gray-600 hover:text-black hover:bg-gray-100 rounded-lg transition-all">Blogs</a>',
        "",
    )
    # Footer blogs -> blogs.html
    html = html.replace('href="#blogs">Blogs</a>', 'href="blogs.html">Blogs</a>')

    # Replace blog section grid: only first 4 + View more link
    first4 = "\n".join(card_html(*c) for c in CARDS[:4])
    new_section = f'''<section class="w-full py-24 bg-white border-t border-gray-100" id="blogs">
<div class="mx-auto max-w-[1400px] px-6 lg:px-10">
<div class="flex flex-col gap-4 max-w-2xl mb-16">
<h2 class="text-4xl font-bold tracking-tight text-[#1c1917] sm:text-5xl leading-tight font-display">
Blogs
</h2>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
{first4}
</div>
<div class="flex justify-center mt-12">
<a href="blogs.html" class="inline-flex h-14 items-center justify-center gap-2 rounded-full border border-gray-200 bg-white px-8 text-sm font-bold text-[#1c1917] hover:border-primary hover:text-primary transition-all shadow-sm">
View more
<span class="material-symbols-outlined text-base">arrow_forward</span>
</a>
</div>
</div>
</section>'''

    html, n = re.subn(
        r'<section class="w-full py-24 bg-white border-t border-gray-100" id="blogs"[^>]*>.*?</section>\s*(?=<section class="w-full py-24 bg-white  relative overflow-hidden">)',
        new_section + "\n",
        html,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit("failed to replace home blog section")
    path.write_text(html, encoding="utf-8")
    print("updated index.html")


def update_blog_posts():
    for path in sorted((ROOT / "blog").glob("*.html")):
        html = path.read_text(encoding="utf-8")

        # Remove Blogs from desktop/mobile nav (highlighted or normal)
        html = re.sub(
            r'\n<a class="px-5 py-2 text-sm font-medium rounded-full[^>]*href="\.\./index\.html#blogs">Blogs</a>',
            "",
            html,
        )
        html = re.sub(
            r'\n\s*<a href="\.\./index\.html#blogs" class="px-4 py-3 text-lg font-medium[^>]*>Blogs</a>',
            "",
            html,
        )

        # Footer + back links -> blogs.html
        html = html.replace("../index.html#blogs", "../blogs.html")

        # Center heading block vertically + horizontally inside image
        html = html.replace(
            "relative z-10 mx-auto flex min-h-[420px] md:min-h-[520px] max-w-[1000px] flex-col justify-end items-center text-center px-6 lg:px-10 pb-12 md:pb-16 pt-28",
            "relative z-10 mx-auto flex min-h-[420px] md:min-h-[520px] max-w-[1000px] flex-col justify-center items-center text-center px-6 lg:px-10 py-16",
        )

        # Soften nav highlight if Blogs was the active item — Contact should not be wrong
        # Fix primary highlight that was on Blogs; leave Contact normal

        path.write_text(html, encoding="utf-8")
        print(f"updated {path.name}")


def update_main_js():
    path = ROOT / "js" / "main.js"
    js = path.read_text(encoding="utf-8")
    js = re.sub(
        r"\n\s*// Homepage blog section:.*?\n\s*function initBlogLoadMore\(\) \{.*?\n\s*\}\n",
        "\n",
        js,
        count=1,
        flags=re.S,
    )
    js = js.replace("\n        initBlogLoadMore();", "")
    path.write_text(js, encoding="utf-8")
    print("updated main.js")


def main():
    create_blogs_page()
    update_index()
    update_blog_posts()
    update_main_js()


if __name__ == "__main__":
    main()
