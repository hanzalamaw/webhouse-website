# -*- coding: utf-8 -*-
"""Set every blog image alt attribute to the blog title/name."""
import html as html_lib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "blog"


def escape_attr(text: str) -> str:
    # Match existing HTML entity style used in listings (&amp; etc.)
    return html_lib.escape(text, quote=True)


def update_blog_pages() -> int:
    updated = 0
    for path in sorted(BLOG_DIR.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        m_title = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
        if not m_title:
            print(f"no title: {path.name}")
            continue
        title = re.sub(r"\s+", " ", m_title.group(1)).strip()
        # strip any HTML entities already decoded by reading as text — keep as plain
        title = html_lib.unescape(title)
        alt = escape_attr(title)

        def repl_img(match: re.Match) -> str:
            before, after = match.group(1), match.group(2)
            # replace existing alt or insert if missing
            if re.search(r'\balt="', before + after):
                return re.sub(r'\balt="[^"]*"', f'alt="{alt}"', match.group(0), count=1)
            # insert alt before class or at end of opening tag bits
            return f'{before} alt="{alt}"{after}'

        new_text, n = re.subn(
            r'(<img\b[^>]*src="\.\./assets/images/blog/[^"]+"[^>]*?)(/?>)',
            repl_img,
            text,
            flags=re.I,
        )
        # Also handle if alt comes before src
        if n == 0:
            new_text, n = re.subn(
                r'(<img\b[^>]*?)(src="\.\./assets/images/blog/[^"]+"[^>]*?/?>)',
                lambda m: re.sub(r'\balt="[^"]*"', f'alt="{alt}"', m.group(0), count=1)
                if re.search(r'\balt="', m.group(0))
                else f'{m.group(1)}alt="{alt}" {m.group(2)}',
                text,
                flags=re.I,
            )

        # Simpler reliable approach: find blog image tags and rebuild alt
        def fix_tag(m: re.Match) -> str:
            tag = m.group(0)
            if re.search(r'\balt="', tag):
                return re.sub(r'\balt="[^"]*"', f'alt="{alt}"', tag, count=1)
            return tag.replace("<img ", f'<img alt="{alt}" ', 1)

        new_text, n = re.subn(
            r'<img\b[^>]*src="\.\./assets/images/blog/[^"]+"[^>]*>',
            fix_tag,
            text,
            flags=re.I,
        )
        if n and new_text != text:
            path.write_text(new_text, encoding="utf-8")
            updated += 1
        elif n == 0:
            print(f"no blog img: {path.name}")
    return updated


def update_listing(path: Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    # Card pattern: <a href="blog/SLUG.html" ...> ... <img ... alt="..."> ... <h3>...</h3>
    pattern = re.compile(
        r'(<a href="blog/([^"]+)\.html"[^>]*>[\s\S]*?'
        r'<img src="assets/images/blog/[^"]+"\s+alt=")([^"]*)("[\s\S]*?'
        r'<h3[^>]*>)([\s\S]*?)(</h3>)',
        re.I,
    )

    def repl(m: re.Match) -> str:
        h3_inner = m.group(5)
        title = re.sub(r"<[^>]+>", "", h3_inner)
        title = html_lib.unescape(re.sub(r"\s+", " ", title).strip())
        alt = escape_attr(title)
        return f"{m.group(1)}{alt}{m.group(4)}{h3_inner}{m.group(6)}"

    new_text, n = pattern.subn(repl, text)
    if n and new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return n


def main():
    blog_n = update_blog_pages()
    blogs_n = update_listing(ROOT / "blogs.html")
    index_n = update_listing(ROOT / "index.html")
    print(f"blog pages updated: {blog_n}")
    print(f"blogs.html cards: {blogs_n}")
    print(f"index.html cards: {index_n}")


if __name__ == "__main__":
    main()
