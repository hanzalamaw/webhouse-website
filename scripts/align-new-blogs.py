# -*- coding: utf-8 -*-
"""Rename numbered blogs/images, fix refs, rebuild blogs.html."""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "blog"
IMG_DIR = ROOT / "assets" / "images" / "blog"

# Numbered image filename by blog number (as currently on disk)
NUMBERED_IMG_EXT = {
    1: ".webp",
    2: ".webp",
    3: ".avif",
    4: ".webp",
    5: ".jfif",
    6: ".jpg",
    7: ".jfif",
    8: ".jpg",
    9: ".webp",
    10: ".jfif",
    11: ".jfif",
    12: ".jfif",
    13: ".jfif",
    14: ".webp",
    15: ".avif",
    16: ".jpg",
    17: ".jfif",
    18: ".jfif",
    19: ".jfif",
    20: ".jfif",
}

# Images whose current name does not match the blog HTML stem
IMAGE_RENAMES = {
    # current_stem: target_blog_stem
    "enterprise-cloud-native-architecture-devops-pipeline": "enterprise-cloud-native-architecture-devops-guide",
    "enterprise-dedicated-teams-staff-augmentation-collaboration": "enterprise-dedicated-teams-staff-augmentation-guide",
    "enterprise-generative-ai-intelligent-systems-workflow": "enterprise-generative-ai-intelligent-systems-guide",
    "enterprise-growth-marketing-performance-analytics-dashboard": "enterprise-growth-marketing-technical-seo-guide",
    "enterprise-seo-strategy-technical-growth-dashboard": "enterprise-seo-strategy-technical-growth-guide",
    "enterprise-ui-ux-design-product-experience-prototyping": "enterprise-ui-ux-design-product-experience-guide",
    "cross-platform-mobile-app-development-flutter-react-native": "cross-platform-mobile-app-development-strategy-guide",
}


def strip_number_prefix(name: str):
    m = re.match(r"^(\d{2})-(.+)$", name)
    if not m:
        return None, None
    return int(m.group(1)), m.group(2)


def rename_numbered_blogs():
    mapping = {}  # old_stem -> new_stem
    for path in sorted(BLOG_DIR.glob("*.html")):
        num, rest = strip_number_prefix(path.stem)
        if num is None:
            continue
        new_path = BLOG_DIR / f"{rest}.html"
        if new_path.exists() and new_path.resolve() != path.resolve():
            print(f"SKIP rename blog (target exists): {path.name} -> {new_path.name}")
            continue
        print(f"RENAME blog {path.name} -> {new_path.name}")
        path.rename(new_path)
        mapping[path.stem] = rest

        # rename matching numbered image
        ext = NUMBERED_IMG_EXT.get(num)
        if not ext:
            continue
        # try both "01" and "1" styles; files are 1.webp not 01.webp
        candidates = [
            IMG_DIR / f"{num}{ext}",
            IMG_DIR / f"{num:02d}{ext}",
        ]
        for img in candidates:
            if img.exists():
                dest = IMG_DIR / f"{rest}{ext}"
                if dest.exists() and dest.resolve() != img.resolve():
                    print(f"  SKIP image target exists: {dest.name}")
                else:
                    print(f"  RENAME image {img.name} -> {dest.name}")
                    img.rename(dest)
                break
        else:
            print(f"  WARN no numbered image for {num}")
    return mapping


def rename_mismatched_images():
    for old_stem, new_stem in IMAGE_RENAMES.items():
        matches = list(IMG_DIR.glob(f"{old_stem}.*"))
        if not matches:
            print(f"SKIP missing image stem {old_stem}")
            continue
        for img in matches:
            dest = IMG_DIR / f"{new_stem}{img.suffix}"
            if dest.exists() and dest.resolve() != img.resolve():
                print(f"SKIP image exists {dest.name}")
                continue
            print(f"RENAME image {img.name} -> {dest.name}")
            img.rename(dest)


def find_image_for_slug(slug: str):
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".avif", ".jfif", ".gif"):
        p = IMG_DIR / f"{slug}{ext}"
        if p.exists():
            return p.name
    return None


def update_blog_file_refs(path: Path, old_stem: str | None = None):
    """Point hero/og image to assets/images/blog/{slug}.{ext}."""
    html = path.read_text(encoding="utf-8")
    slug = path.stem
    img_name = find_image_for_slug(slug)
    if not img_name:
        print(f"WARN no image for {slug}")
        return

    local_path = f"../assets/images/blog/{img_name}"
    abs_url = f"https://webhouseinc.co/assets/images/blog/{img_name}"

    # Fix wrong blogs/ folder and any previous image path in hero
    html = html.replace("../assets/images/blogs/", "../assets/images/blog/")
    html = re.sub(
        r'(<img src=")[^"]*(" alt="[^"]*" class="absolute inset-0 h-full w-full object-cover")',
        rf'\1{local_path}\2',
        html,
        count=1,
    )
    # og:image
    if 'property="og:image"' in html:
        html = re.sub(
            r'<meta property="og:image" content="[^"]*"/>',
            f'<meta property="og:image" content="{abs_url}"/>',
            html,
            count=1,
        )
    else:
        html = html.replace(
            '<meta property="og:type" content="article"/>',
            f'<meta property="og:type" content="article"/>\n    <meta property="og:image" content="{abs_url}"/>',
        )

    # Fix numbered URLs in canonical/og if present with old stem
    if old_stem and old_stem != slug:
        html = html.replace(f"/blog/{old_stem}.html", f"/blog/{slug}.html")
        html = html.replace(f"blog/{old_stem}.html", f"blog/{slug}.html")

    # Also ensure canonical uses current slug
    html = re.sub(
        r'(href="https://webhouseinc\.co/blog/)[^"]+(\.html")',
        rf"\1{slug}\2",
        html,
    )
    html = re.sub(
        r'(content="https://webhouseinc\.co/blog/)[^"]+(\.html")',
        rf"\1{slug}\2",
        html,
    )

    path.write_text(html, encoding="utf-8")
    print(f"UPDATED refs {path.name} -> {img_name}")


def extract_meta(path: Path):
    html = path.read_text(encoding="utf-8")
    title_m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    title = title_m.group(1).strip() if title_m else path.stem
    title = re.sub(r"\s*-\s*WebHouse Inc\.?\s*$", "", title, flags=re.I)

    desc_m = re.search(
        r'<meta\s+name="description"\s+content="([^"]*)"',
        html,
        re.I,
    )
    desc = desc_m.group(1).strip() if desc_m else ""

    # Prefer H1 from hero if available (cleaner)
    h1_m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if h1_m:
        h1 = re.sub(r"<[^>]+>", "", h1_m.group(1)).strip()
        if h1:
            title = h1

    # Category tag from page if present
    tag_m = re.search(
        r'font-mono text-xs tracking-widest uppercase font-bold[^>]*>(.*?)</span>',
        html,
        re.S,
    )
    tag = re.sub(r"<[^>]+>", "", tag_m.group(1)).strip() if tag_m else "Blog"
    if not tag or tag.lower() in ("insights", "blogs", "blog"):
        # derive short tag from title words
        words = re.findall(r"[A-Za-z0-9&]+", title)
        tag = " ".join(words[:3]) if words else "Blog"

    return title, desc, tag


def card_html(slug, title, desc, tag, img_name, prefix=""):
    return f'''<a href="{prefix}blog/{slug}.html" class="group flex flex-col overflow-hidden rounded-[2rem] bg-white border border-gray-100 hover:shadow-card hover:-translate-y-1 transition-all duration-300">
<div class="h-52 overflow-hidden bg-gray-100">
<img src="{prefix}assets/images/blog/{img_name}" alt="{tag}" class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"/>
</div>
<div class="flex flex-col flex-1 p-7 md:p-8">
<span class="text-xs font-bold uppercase tracking-wider text-primary mb-3">{tag}</span>
<h3 class="text-xl font-display font-bold text-[#1c1917] mb-3 leading-snug group-hover:text-primary transition-colors">{title}</h3>
<p class="text-sm text-gray-500 leading-relaxed mb-6 flex-1">{desc}</p>
<span class="inline-flex items-center gap-2 text-sm font-bold text-primary group-hover:gap-3 transition-all">Read article <span class="material-symbols-outlined text-sm">arrow_forward</span></span>
</div>
</a>'''


def collect_blogs():
    blogs = []
    for path in sorted(BLOG_DIR.glob("*.html"), key=lambda p: p.stat().st_mtime, reverse=True):
        slug = path.stem
        img = find_image_for_slug(slug)
        if not img:
            print(f"LIST WARN no image: {slug}")
            continue
        title, desc, tag = extract_meta(path)
        # escape for HTML attribute/text already mostly escaped in sources
        blogs.append((slug, title, desc, tag, img))
    return blogs


def rebuild_blogs_html(blogs):
    # Keep shell of existing blogs.html if present, else build minimal
    existing = ROOT / "blogs.html"
    if existing.exists():
        base = existing.read_text(encoding="utf-8")
    else:
        raise SystemExit("blogs.html missing")

    cards = "\n".join(card_html(*b) for b in blogs)
    grid = f'<div class="grid grid-cols-1 md:grid-cols-2 gap-8">\n{cards}\n</div>'
    updated, n = re.subn(
        r'<div class="grid grid-cols-1 md:grid-cols-2 gap-8">.*?</div>\s*</div>\s*</section>',
        grid + "\n</div>\n</section>",
        base,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit("failed to rebuild blogs.html grid")
    existing.write_text(updated, encoding="utf-8")
    print(f"rebuilt blogs.html with {len(blogs)} posts")


def update_homepage(blogs):
    """Keep first 4 newest on homepage; preserve View more button design."""
    path = ROOT / "index.html"
    html = path.read_text(encoding="utf-8")
    cards = "\n".join(card_html(*b) for b in blogs[:4])
    grid = f'<div class="grid grid-cols-1 md:grid-cols-2 gap-8">\n{cards}\n</div>'
    html2, n = re.subn(
        r'(<section class="w-full py-24 bg-white border-t border-gray-100" id="blogs"[^>]*>.*?)'
        r'<div class="grid grid-cols-1 md:grid-cols-2 gap-8">.*?</div>'
        r'(\s*<div class="flex justify-center mt-12">)',
        rf"\1{grid}\2",
        html,
        count=1,
        flags=re.S,
    )
    if n != 1:
        print("WARN homepage cards replace failed (View more left untouched)")
        return
    path.write_text(html2, encoding="utf-8")
    print("updated homepage first 4 blogs (preserved View more button)")


def fix_all_blog_refs(old_to_new: dict):
    # reverse map new->old for numbered
    new_to_old = {v: k for k, v in old_to_new.items()}
    for path in sorted(BLOG_DIR.glob("*.html")):
        update_blog_file_refs(path, old_stem=new_to_old.get(path.stem))


def main():
    mapping = rename_numbered_blogs()
    rename_mismatched_images()
    fix_all_blog_refs(mapping)
    blogs = collect_blogs()
    rebuild_blogs_html(blogs)
    update_homepage(blogs)
    print(f"DONE total blogs with images: {len(blogs)}")


if __name__ == "__main__":
    main()
