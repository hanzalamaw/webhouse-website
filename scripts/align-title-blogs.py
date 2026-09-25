# -*- coding: utf-8 -*-
"""Align newly added title-named blogs: slugify filenames, rename images, rebuild listing."""
import html as html_lib
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "blog"
IMG_DIR = ROOT / "assets" / "images" / "blog"


def slugify(name: str) -> str:
    # Decode HTML entities in filename like &amp;
    name = html_lib.unescape(name)
    name = name.replace(".html", "")
    name = re.sub(r"\(2026\)", "", name, flags=re.I)
    name = name.replace("&", " and ")
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "-", name)
    name = re.sub(r"-+", "-", name).strip("-")
    return name


def is_title_style(filename: str) -> bool:
    # Spaces, HTML entities, parentheses, or Title Case with spaces
    return bool(re.search(r"[\s(&]|amp;", filename))


def extract_img_ref(html: str):
    m = re.search(
        r'src="\.\./assets/images/blog/([^"]+)"\s+[^>]*class="absolute inset-0',
        html,
    )
    if m:
        return m.group(1)
    m = re.search(r'src="\.\./assets/images/blog/([^"]+)"', html)
    return m.group(1) if m else None


def find_image_file(name: str):
    """Find image by exact name; also try URL-decoded / unescaped variants."""
    candidates = [
        IMG_DIR / name,
        IMG_DIR / html_lib.unescape(name),
    ]
    for c in candidates:
        if c.exists():
            return c
    # Fuzzy: try matching by stem ignoring spaces/case
    stem = Path(html_lib.unescape(name)).stem
    for p in IMG_DIR.iterdir():
        if not p.is_file():
            continue
        if p.stem.lower().replace(" ", "-") == stem.lower().replace(" ", "-"):
            return p
        if p.name.lower() == name.lower():
            return p
    return None


def find_image_for_slug(slug: str):
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".avif", ".jfif", ".gif"):
        p = IMG_DIR / f"{slug}{ext}"
        if p.exists():
            return p.name
    # also handle double extensions like .png.jfif already renamed to .jfif
    return None


def rename_title_blogs():
    mapping = []  # (old_path, new_path, old_img_name, new_img_name)
    for path in list(BLOG_DIR.glob("*.html")):
        if not is_title_style(path.name):
            continue
        slug = slugify(path.name)
        new_path = BLOG_DIR / f"{slug}.html"
        if new_path.exists() and new_path.resolve() != path.resolve():
            print(f"SKIP target exists: {new_path.name}")
            continue

        html = path.read_text(encoding="utf-8")
        old_img_name = extract_img_ref(html)
        old_img = find_image_file(old_img_name) if old_img_name else None

        print(f"RENAME blog: {path.name}")
        print(f"      -> {new_path.name}")
        path.rename(new_path)

        new_img_name = None
        if old_img and old_img.exists():
            # normalize weird .png.jfif -> .jfif
            ext = old_img.suffix.lower()
            if old_img.name.lower().endswith(".png.jfif"):
                ext = ".jfif"
            dest = IMG_DIR / f"{slug}{ext}"
            if dest.exists() and dest.resolve() != old_img.resolve():
                print(f"  SKIP image exists {dest.name}, keep existing")
                new_img_name = dest.name
            else:
                print(f"  RENAME image: {old_img.name} -> {dest.name}")
                old_img.rename(dest)
                new_img_name = dest.name
        else:
            print(f"  WARN image not found: {old_img_name}")

        mapping.append((new_path, old_img_name, new_img_name, slug))
    return mapping


def update_blog_refs(path: Path, slug: str, img_name: str | None):
    html = path.read_text(encoding="utf-8")
    if not img_name:
        img_name = find_image_for_slug(slug)
    if not img_name:
        print(f"WARN no image for {slug}")
        return

    local = f"../assets/images/blog/{img_name}"
    abs_url = f"https://webhouseinc.co/assets/images/blog/{img_name}"

    html = html.replace("../assets/images/blogs/", "../assets/images/blog/")
    html = re.sub(
        r'(<img src=")[^"]*(" alt="[^"]*" class="absolute inset-0 h-full w-full object-cover")',
        rf"\1{local}\2",
        html,
        count=1,
    )
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
    print(f"UPDATED {path.name} -> {img_name}")


def extract_meta(path: Path):
    html = path.read_text(encoding="utf-8")
    title_m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    title = title_m.group(1).strip() if title_m else path.stem
    title = re.sub(r"\s*-\s*WebHouse Inc\.?\s*$", "", title, flags=re.I)
    h1_m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if h1_m:
        h1 = re.sub(r"<[^>]+>", "", h1_m.group(1)).strip()
        if h1:
            title = h1
    desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html, re.I)
    desc = desc_m.group(1).strip() if desc_m else ""
    tag_m = re.search(
        r'font-mono text-xs tracking-widest uppercase font-bold[^>]*>(.*?)</span>',
        html,
        re.S,
    )
    tag = re.sub(r"<[^>]+>", "", tag_m.group(1)).strip() if tag_m else "Blog"
    if not tag or tag.lower() in ("insights", "blogs", "blog"):
        words = re.findall(r"[A-Za-z0-9&]+", title)
        tag = " ".join(words[:3]) if words else "Blog"
    return title, desc, tag


def card_html(slug, title, desc, tag, img_name):
    # Escape title/desc if they contain unescaped < — usually already fine
    return f'''<a href="blog/{slug}.html" class="group flex flex-col overflow-hidden rounded-[2rem] bg-white border border-gray-100 hover:shadow-card hover:-translate-y-1 transition-all duration-300">
<div class="h-52 overflow-hidden bg-gray-100">
<img src="assets/images/blog/{img_name}" alt="{tag}" class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"/>
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
        if is_title_style(path.name):
            print(f"WARN still title-style: {path.name}")
            continue
        slug = path.stem
        img = find_image_for_slug(slug)
        if not img:
            print(f"LIST WARN no image: {slug}")
            continue
        title, desc, tag = extract_meta(path)
        blogs.append((slug, title, desc, tag, img))
    return blogs


def rebuild_blogs_html(blogs):
    existing = ROOT / "blogs.html"
    base = existing.read_text(encoding="utf-8")
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
        raise SystemExit("failed to rebuild blogs.html")
    existing.write_text(updated, encoding="utf-8")
    print(f"rebuilt blogs.html with {len(blogs)} posts")


def update_homepage(blogs):
    """Update only the blog cards grid; preserve View more button design."""
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
    print("updated homepage first 4 (preserved View more button)")


def main():
    mapping = rename_title_blogs()
    for new_path, _old_img, new_img, slug in mapping:
        update_blog_refs(new_path, slug, new_img)

    # Also refresh refs for any slug blogs missing correct image path
    for path in BLOG_DIR.glob("*.html"):
        if is_title_style(path.name):
            continue
        img = find_image_for_slug(path.stem)
        if img:
            # cheap check: does html already point to this file?
            html = path.read_text(encoding="utf-8")
            if f"assets/images/blog/{img}" not in html:
                update_blog_refs(path, path.stem, img)

    blogs = collect_blogs()
    rebuild_blogs_html(blogs)
    update_homepage(blogs)
    print(f"DONE total: {len(blogs)}")


if __name__ == "__main__":
    main()
