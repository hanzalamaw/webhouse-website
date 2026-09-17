# -*- coding: utf-8 -*-
"""Update blog layout: title on hero, darker image, wider centered body."""
import re
from pathlib import Path

BLOG_DIR = Path(__file__).resolve().parent.parent / "blog"


def update_file(path: Path):
    html = path.read_text(encoding="utf-8")

    # Extract tag, title, body, cta from current structure
    tag_m = re.search(
        r'<span class="text-primary font-mono text-xs tracking-widest uppercase font-bold">(.*?)</span>',
        html,
        re.S,
    )
    title_m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    img_m = re.search(
        r'<img src="(\.\./assets/images/blog/[^"]+)" alt="([^"]*)"[^,]*>',
        html,
    )
    if not img_m:
        img_m = re.search(
            r'<img src="(\.\./assets/images/blog/[^"]+)" alt="([^"]*)"[^>]*>',
            html,
        )

    prose_m = re.search(
        r'<div class="blog-prose[^"]*"[^>]*>(.*?)</div>',
        html,
        re.S,
    )
    cta_m = re.search(
        r'<div class="mt-20 rounded-\[2rem\] bg-\[#1c1917\][^"]*"[^>]*>(.*?)</div>\s*</div>\s*</section>',
        html,
        re.S,
    )
    if not cta_m:
        cta_m = re.search(
            r'<div class="mt-20 rounded-\[2rem\].*?</div>\s*</div>\s*</section>',
            html,
            re.S,
        )

    if not all([tag_m, title_m, img_m, prose_m]):
        print(f"skip extract fail: {path.name}")
        return

    tag = tag_m.group(1).strip()
    title = title_m.group(1).strip()
    img_src = img_m.group(1)
    img_alt = img_m.group(2)
    body = prose_m.group(1).strip()

    cta_title = "Talk to WebHouse Inc."
    cta_text = "Let's discuss how we can help your enterprise scale."
    if cta_m:
        block = cta_m.group(0)
        ct = re.search(r"<h2[^>]*>(.*?)</h2>", block, re.S)
        cp = re.search(r"<p[^>]*>(.*?)</p>", block, re.S)
        if ct:
            cta_title = ct.group(1).strip()
        if cp:
            cta_text = cp.group(1).strip()

    new_main = f'''<main>
<article>
<!-- Hero with title overlay -->
<section class="relative w-full pt-20">
<div class="relative min-h-[420px] md:min-h-[520px] w-full overflow-hidden bg-gray-900">
<img src="{img_src}" alt="{img_alt}" class="absolute inset-0 h-full w-full object-cover"/>
<div class="absolute inset-0 bg-black/60"></div>
<div class="relative z-10 mx-auto flex min-h-[420px] md:min-h-[520px] max-w-[1000px] flex-col justify-end px-6 lg:px-10 pb-12 md:pb-16 pt-28">
<a href="../index.html#blogs" class="inline-flex items-center gap-2 text-sm font-medium text-white/70 hover:text-white transition-colors mb-6 w-fit">
<span class="material-symbols-outlined text-base">arrow_back</span>
Back to Blogs
</a>
<span class="text-primary-light font-mono text-xs tracking-widest uppercase font-bold">{tag}</span>
<h1 class="mt-4 font-display text-3xl md:text-5xl font-extrabold leading-tight tracking-tight text-white max-w-4xl">{title}</h1>
</div>
</div>
</section>

<!-- Body — centered, wider -->
<section class="bg-white py-16 md:py-24">
<div class="mx-auto max-w-[920px] px-6 lg:px-10">
<div class="blog-prose text-lg text-gray-600 leading-[1.85]">
{body}
</div>

<div class="mt-20 rounded-[2rem] bg-[#1c1917] p-10 md:p-14 text-center">
<h2 class="font-display text-2xl md:text-3xl font-bold text-white mb-4 leading-snug">{cta_title}</h2>
<p class="text-gray-400 text-base leading-relaxed mb-8 max-w-xl mx-auto">{cta_text}</p>
<a href="../contact_us.html" class="inline-flex h-12 items-center justify-center rounded-full bg-gradient-to-r from-[#b90606] to-[#c80505] px-8 text-sm font-bold text-white shadow-glow hover:opacity-90 transition-all">Get Started</a>
</div>
</div>
</section>
</article>
</main>'''

    updated, n = re.subn(r"<main>.*?</main>", new_main, html, count=1, flags=re.S)
    if n != 1:
        print(f"replace fail: {path.name}")
        return
    path.write_text(updated, encoding="utf-8")
    print(f"ok {path.name}")


def main():
    for path in sorted(BLOG_DIR.glob("*.html")):
        update_file(path)


if __name__ == "__main__":
    main()
