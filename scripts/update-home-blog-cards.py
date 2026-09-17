# -*- coding: utf-8 -*-
from pathlib import Path
import re

index = Path("index.html")
html = index.read_text(encoding="utf-8")

cards = [
    ("custom-enterprise-software-vs-off-the-shelf", "Custom Software", "Custom Enterprise Software vs. Off-the-Shelf: 2026 Strategic Guide", "Compare custom enterprise software development with off-the-shelf platforms. Discover why enterprise leaders choose custom software for scalability and security.", False),
    ("ai-workflow-automation-enterprise-guide", "AI Automation", "AI Workflow Automation: Scaling Enterprise Efficiency in 2026", "Streamline enterprise operations with custom AI workflow automation solutions, generative AI models, and autonomous AI agents.", False),
    ("headless-ecommerce-platform-engineering-guide", "E-Commerce", "Headless E-Commerce Engineering: Scaling Enterprise Growth (2026)", "Discover how headless e-commerce engineering and custom web development accelerate load speeds, conversion rates, and global enterprise growth.", False),
    ("dedicated-software-engineering-teams-staff-augmentation", "Dedicated Teams", "Dedicated Developer Teams: Scaling Engineering Capacity in 2026", "Scale software engineering capacity rapidly with dedicated development teams and IT staff augmentation.", False),
    ("cloud-native-devops-infrastructure-guide", "Cloud &amp; DevOps", "Cloud-Native Infrastructure &amp; DevOps Best Practices (2026 Guide)", "Modernize enterprise IT with cloud-native DevOps infrastructure, microservices, Docker, Kubernetes, and automated CI/CD pipelines.", True),
    ("cross-platform-mobile-app-engineering-guide", "Mobile", "Cross-Platform Mobile App Engineering: Flutter &amp; React Native (2026)", "Scale mobile deployment across iOS and Android with cross-platform engineering using Flutter and React Native.", True),
    ("custom-erp-crm-development-workflow-optimization", "ERP &amp; CRM", "Custom ERP &amp; CRM Systems: Streamlining Enterprise Workflows (2026)", "Streamline operations with custom ERP &amp; CRM software engineering. Eliminate manual data silos for global scale.", True),
    ("b2b-growth-marketing-seo-tech-platforms", "Growth Marketing", "B2B Growth Marketing &amp; SEO for Enterprise Tech Platforms (2026)", "Drive predictable B2B pipeline growth with SEO, targeted performance marketing, and high-converting content strategies.", True),
    ("legacy-system-modernization-enterprise-transformation", "Modernization", "Legacy System Modernization: Transforming Enterprise Software (2026)", "Eliminate technical debt and modernize legacy software systems with microservices and cloud infrastructure.", True),
    ("enterprise-api-engineering-microservices-integration", "API Engineering", "Enterprise API Engineering &amp; Microservices Integration (2026 Guide)", "Connect enterprise software systems with custom API engineering and secure middleware for real-time data flow.", True),
    ("enterprise-cybersecurity-engineering-compliance-guide", "Cybersecurity", "Enterprise Cybersecurity Engineering &amp; Compliance Standards (2026)", "Safeguard enterprise digital assets with zero-trust security architecture and automated compliance controls.", True),
    ("enterprise-data-engineering-ai-analytics-guide", "Data &amp; Analytics", "Enterprise Data Engineering &amp; AI Analytics Pipelines (2026)", "Transform raw corporate data into actionable strategic intelligence with data engineering and AI analytics.", True),
    ("progressive-web-apps-vs-native-mobile-apps-strategy", "PWA Strategy", "Progressive Web Apps (PWAs) vs Native Apps: 2026 Strategy Guide", "Compare Progressive Web Apps and native apps for enterprise expansion and mobile engagement.", True),
    ("enterprise-headless-cms-architecture-guide", "Headless CMS", "Enterprise Headless CMS Architecture: Multi-Channel Publishing (2026)", "Scale content management with enterprise headless CMS architecture across web, mobile, and digital portals.", True),
    ("ai-powered-customer-support-enterprise-automation", "Customer Support", "AI Customer Support Automation: Enterprise Scaling in 2026", "Transform customer experience with enterprise AI customer support automation and intelligent ticket routing.", True),
    ("modern-tech-stack-architecture-enterprise-guide", "Tech Stack", "Modern Tech Stack Architecture for Enterprise Platforms (2026)", "Scale enterprise software with a modern tech stack spanning backend, cloud, AI, and e-commerce integrations.", True),
]

parts = ['<div class="grid grid-cols-1 md:grid-cols-2 gap-8" data-blog-grid>']
for slug, tag, title, desc, more in cards:
    hidden = " hidden" if more else ""
    more_attr = " data-blog-more" if more else ""
    parts.append(
        f'''<a href="blog/{slug}.html" class="group flex flex-col overflow-hidden rounded-[2rem] bg-white border border-gray-100 hover:shadow-card hover:-translate-y-1 transition-all duration-300{hidden}" data-blog-card{more_attr}>
<div class="h-52 overflow-hidden bg-gray-100">
<img src="assets/images/blog/{slug}.jpg" alt="{tag}" class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"/>
</div>
<div class="flex flex-col flex-1 p-7 md:p-8">
<span class="text-xs font-bold uppercase tracking-wider text-primary mb-3">{tag}</span>
<h3 class="text-xl font-display font-bold text-[#1c1917] mb-3 leading-snug group-hover:text-primary transition-colors">{title}</h3>
<p class="text-sm text-gray-500 leading-relaxed mb-6 flex-1">{desc}</p>
<span class="inline-flex items-center gap-2 text-sm font-bold text-primary group-hover:gap-3 transition-all">Read article <span class="material-symbols-outlined text-sm">arrow_forward</span></span>
</div>
</a>'''
    )
parts.append("</div>")
new_grid = "\n".join(parts)

html2, n = re.subn(
    r'<div class="grid grid-cols-1 md:grid-cols-2 gap-6" data-blog-grid>.*?</div>\s*<div class="flex justify-center mt-12">',
    new_grid + '\n<div class="flex justify-center mt-12">',
    html,
    count=1,
    flags=re.S,
)
print("replacements", n)
if n == 1:
    index.write_text(html2, encoding="utf-8")
    print("homepage cards updated")
else:
    raise SystemExit("FAILED to update homepage")
