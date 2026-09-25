# -*- coding: utf-8 -*-
"""Fix broken blog image refs and convert .jfif to .jpg for browser support."""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "blog"
IMG_DIR = ROOT / "assets" / "images" / "blog"
BLOGS_HTML = ROOT / "blogs.html"
INDEX_HTML = ROOT / "index.html"


def find_image_for_slug(slug: str):
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".avif", ".jfif", ".gif"):
        p = IMG_DIR / f"{slug}{ext}"
        if p.exists():
            return p
    return None


def convert_jfif_to_jpg():
    converted = []
    for jfif in list(IMG_DIR.glob("*.jfif")):
        dest = jfif.with_suffix(".jpg")
        if dest.exists():
            # keep jpg, remove jfif duplicate if same slug
            print(f"REMOVE duplicate jfif (jpg exists): {jfif.name}")
            jfif.unlink()
            converted.append((jfif.name, dest.name))
            continue
        print(f"CONVERT {jfif.name} -> {dest.name}")
        jfif.rename(dest)
        converted.append((jfif.name, dest.name))
    return converted


def update_file_image_refs(path: Path, replacements: dict):
    """replacements: old_filename -> new_filename"""
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in replacements.items():
        text = text.replace(old, new)
    # also fix any remaining .jfif to .jpg when jpg exists for that stem
    text = re.sub(r"(assets/images/blog/[^\"'\s]+)\.jfif", r"\1.jpg", text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def fix_blog_hero_to_slug_image(path: Path):
    slug = path.stem
    img = find_image_for_slug(slug)
    if not img:
        print(f"WARN no image for {slug}")
        return False
    html = path.read_text(encoding="utf-8")
    local = f"../assets/images/blog/{img.name}"
    abs_url = f"https://webhouseinc.co/assets/images/blog/{img.name}"

    new_html, n = re.subn(
        r'(<img src=")[^"]*(" alt="[^"]*" class="absolute inset-0 h-full w-full object-cover")',
        rf"\1{local}\2",
        html,
        count=1,
    )
    if n == 0:
        # broader replace first blog image after hero
        new_html, n = re.subn(
            r'(src=")(\.\./assets/images/blog/)[^"]+(")',
            rf"\1{local}\3",
            html,
            count=1,
        )
    if 'property="og:image"' in new_html:
        new_html = re.sub(
            r'<meta property="og:image" content="[^"]*"/>',
            f'<meta property="og:image" content="{abs_url}"/>',
            new_html,
            count=1,
        )
    if new_html != html:
        path.write_text(new_html, encoding="utf-8")
        print(f"FIXED {path.name} -> {img.name}")
        return True
    return False


def rebuild_listing_img_ext():
    # Ensure blogs.html / index use .jpg where files are jpg
    for page in (BLOGS_HTML, INDEX_HTML):
        if not page.exists():
            continue
        text = page.read_text(encoding="utf-8")
        original = text

        def repl(m):
            stem = m.group(1)
            jpg = IMG_DIR / f"{stem}.jpg"
            if jpg.exists():
                return f'assets/images/blog/{stem}.jpg'
            # keep original if no jpg
            return m.group(0)

        text = re.sub(
            r'assets/images/blog/([A-Za-z0-9_\-]+)\.jfif',
            lambda m: f'assets/images/blog/{m.group(1)}.jpg'
            if (IMG_DIR / f"{m.group(1)}.jpg").exists()
            else m.group(0),
            text,
        )
        if text != original:
            page.write_text(text, encoding="utf-8")
            print(f"updated listing paths in {page.name}")


def main():
    converted = convert_jfif_to_jpg()
    print(f"converted {len(converted)} jfif files")

    fixed = 0
    for path in sorted(BLOG_DIR.glob("*.html")):
        if fix_blog_hero_to_slug_image(path):
            fixed += 1
    print(f"fixed blog pages: {fixed}")

    rebuild_listing_img_ext()

    # final verify
    missing = []
    for path in sorted(BLOG_DIR.glob("*.html")):
        t = path.read_text(encoding="utf-8")
        m = re.search(
            r'src="(\.\./assets/images/blog/[^"]+)"[^>]*class="absolute inset-0',
            t,
        )
        if not m:
            m = re.search(r'src="(\.\./assets/images/blog/[^"]+)"', t)
        if not m:
            missing.append((path.name, "NO_TAG"))
            continue
        name = m.group(1).split("/")[-1]
        if not (IMG_DIR / name).exists():
            missing.append((path.name, name))
    print(f"still missing: {len(missing)}")
    for item in missing:
        print(item)


if __name__ == "__main__":
    main()
