#!/usr/bin/env python3
"""Render content/*.md into the static site in docs/.

    python3 build.py                  -> docs/, linking a shared style.css
    python3 build.py --inline-css     -> docs/, with the CSS inlined per page
    python3 build.py -o /srv/www      -> somewhere else

`docs/` is what GitHub Pages serves (Settings -> Pages -> Deploy from a branch ->
main -> /docs). The output is committed, so a deploy is a `git push`.

No third-party packages. The markdown subset understood here is deliberately
small — just what these pages use. The conventions are documented in README.md;
the short version:

    ---            frontmatter, key: value pairs
    === name       opens a section with that CSS class
    ^ text         eyebrow above the section heading
    ## text        section heading
    ::: name       a structured block, closed by a bare :::
    @ text         inside ::: steps, the aside line for a step
"""

import argparse
import datetime
import glob
import html
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "content")
DEFAULT_OUT = os.path.join(HERE, os.pardir, "docs")

# --------------------------------------------------------------------------
# inline markdown
# --------------------------------------------------------------------------

CODE_RE = re.compile(r"`([^`]+)`")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*", re.S)
ITAL_RE = re.compile(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", re.S)


def inline(text):
    """Escape HTML, then apply the handful of inline marks these pages use."""
    out = html.escape(text, quote=False)
    stash = []

    def keep(fragment):
        stash.append(fragment)
        return f"\x00{len(stash) - 1}\x00"

    out = CODE_RE.sub(lambda m: keep(f"<code>{m.group(1)}</code>"), out)
    out = LINK_RE.sub(
        lambda m: keep(
            f'<a href="{html.escape(m.group(2), quote=True)}"'
            f'{external(m.group(2))}>{m.group(1)}</a>'
        ),
        out,
    )
    out = BOLD_RE.sub(r"<b>\1</b>", out)
    out = ITAL_RE.sub(r"<em>\1</em>", out)

    for i, fragment in enumerate(stash):
        out = out.replace(f"\x00{i}\x00", fragment)
    return out.strip()


def external(href):
    """Off-site links open in a new tab; internal ones don't."""
    if href.startswith(("http://", "https://")):
        return ' target="_blank" rel="noopener"'
    return ""


# --------------------------------------------------------------------------
# parsing
# --------------------------------------------------------------------------


def split_frontmatter(src):
    if not src.startswith("---"):
        return {}, src
    _, fm, rest = src.split("---", 2)
    meta = {}
    for line in fm.strip().splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, rest


def paragraphs(lines):
    """Group consecutive non-blank lines into unwrapped paragraphs."""
    buf, out = [], []
    for line in lines:
        if line.strip():
            buf.append(line.strip())
        elif buf:
            out.append(" ".join(buf))
            buf = []
    if buf:
        out.append(" ".join(buf))
    return out


def list_items(lines):
    """Collect '- ' or '1. ' items, joining their wrapped continuation lines."""
    items, current = [], None
    for line in lines:
        stripped = line.strip()
        if re.match(r"^(-|\d+\.)\s+", stripped):
            if current is not None:
                items.append(" ".join(current))
            current = [re.sub(r"^(-|\d+\.)\s+", "", stripped)]
        elif stripped and current is not None:
            current.append(stripped)
        elif not stripped and current is not None:
            items.append(" ".join(current))
            current = None
    if current is not None:
        items.append(" ".join(current))
    return items


def split_label(item, block):
    """Pull '**Label** — text' apart, the shape every labelled block uses."""
    match = re.match(r"^\*\*(.+?)\*\*\s*[—–-]\s*(.*)$", item, re.S)
    if not match:
        sys.exit(f"::: {block} — item needs '**Label** — text':\n  {item[:70]}")
    return match.group(1), match.group(2)


# --------------------------------------------------------------------------
# block renderers
# --------------------------------------------------------------------------


# A card may lead with a picture: '- ![alt](pics/name.jpg) **Label** — text'.
CARD_IMG_RE = re.compile(r"^!\[([^\]]*)\]\(([^)\s]+)\)\s*")


def render_cards(lines):
    cards = []
    for item in list_items(lines):
        portrait = ""
        match = CARD_IMG_RE.match(item)
        if match:
            item = item[match.end():]
            portrait = (
                f'<img src="{html.escape(match.group(2), quote=True)}" '
                f'alt="{html.escape(match.group(1), quote=True)}" loading="lazy">'
            )
        label, text = split_label(item, "cards")
        cards.append(
            f'<div class="card">{portrait}<span>{inline(label)}</span>'
            f"<p>{inline(text)}</p></div>"
        )
    return '<div class="cards">\n' + "\n".join(cards) + "\n</div>"


def render_facts(lines):
    """The key/value strip — what a visitor scanning for 'when and where' wants."""
    rows = []
    for item in list_items(lines):
        label, text = split_label(item, "facts")
        rows.append(f"<dt>{inline(label)}</dt><dd>{inline(text)}</dd>")
    return '<dl class="facts">\n' + "\n".join(rows) + "\n</dl>"


def render_callout(lines):
    return f'<p class="callout">{inline(" ".join(paragraphs(lines)))}</p>'


def render_kicker(lines):
    return f'<p class="kicker">{inline(" ".join(paragraphs(lines)))}</p>'


def render_list(lines):
    """A plain bullet list — the one block that asks nothing of its items."""
    rows = [f"<li>{inline(item)}</li>" for item in list_items(lines)]
    return '<ul class="list">\n' + "\n".join(rows) + "\n</ul>"


def render_numbers(lines):
    rows = []
    for n, item in enumerate(list_items(lines), 1):
        rows.append(f'<li><span>{n:02d}</span><div>{inline(item)}</div></li>')
    return '<ul class="numbers">\n' + "\n".join(rows) + "\n</ul>"


def step_content(step, heading):
    """A step's heading, its prose if it has any, then its aside if it has one."""
    out = f"<{heading}>{inline(step['title'])}</{heading}>"
    body = " ".join(paragraphs(step["body"]))
    if body:
        out += f"<p>{inline(body)}</p>"
    if step["aside"]:
        out += f'<span class="aside">{inline(step["aside"])}</span>'
    return out


def render_steps(lines):
    """'### ' rows, each of which may hold '#### ' sub-rows nested under it."""
    steps, current, sub = [], None, None

    def start(title):
        return {"title": title, "aside": "", "body": [], "subs": []}

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#### "):
            if current is None:
                sys.exit("::: steps — a '#### ' sub-step needs a '### ' step above it")
            sub = start(stripped[5:].strip())
            current["subs"].append(sub)
        elif stripped.startswith("### "):
            current, sub = start(stripped[4:].strip()), None
            steps.append(current)
        elif stripped.startswith("@ ") and current is not None:
            (sub or current)["aside"] = stripped[2:].strip()
        elif current is not None:
            (sub or current)["body"].append(line)

    out = []
    for n, step in enumerate(steps, 1):
        subs = ""
        if step["subs"]:
            rows = [
                '<div class="substep"><div class="substep-mark" aria-hidden="true">'
                f'&bull;</div><div>{step_content(s, "h4")}</div></div>'
                for s in step["subs"]
            ]
            subs = '<div class="substeps">\n' + "\n".join(rows) + "\n</div>"
        out.append(
            f'<div class="step"><div class="step-num">{n:02d}</div>'
            f'<div>{step_content(step, "h3")}{subs}</div></div>'
        )
    return '<div class="steps">\n' + "\n".join(out) + "\n</div>"


BLOCKS = {
    "cards": render_cards,
    "facts": render_facts,
    "callout": render_callout,
    "kicker": render_kicker,
    "list": render_list,
    "numbers": render_numbers,
    "steps": render_steps,
}


# --------------------------------------------------------------------------
# document
# --------------------------------------------------------------------------


def render_body(src, where):
    sections = []
    current = None  # {"cls": str, "parts": [html, ...]}
    pending = []  # plain lines awaiting a paragraph flush
    eyebrow = None

    def flush_text():
        nonlocal pending
        if current is not None:
            for para in paragraphs(pending):
                current["parts"].append(f"<p>{inline(para)}</p>")
        pending = []

    def close_section():
        flush_text()
        if current is not None:
            sections.append(
                f'<section class="{current["cls"]}">\n'
                + "\n".join(current["parts"])
                + "\n</section>"
            )

    def need_section(what):
        if current is None:
            sys.exit(f"{where}: {what} before any '=== section'")

    lines = src.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("=== "):
            close_section()
            current = {"cls": stripped[4:].strip(), "parts": []}
            eyebrow = None

        elif stripped.startswith("^ "):
            flush_text()
            eyebrow = stripped[2:].strip()

        elif stripped.startswith("## "):
            flush_text()
            need_section("a '## heading'")
            if eyebrow:
                current["parts"].append(f'<p class="eyebrow">{inline(eyebrow)}</p>')
                eyebrow = None
            current["parts"].append(f"<h2>{inline(stripped[3:].strip())}</h2>")

        elif stripped.startswith("::: "):
            flush_text()
            name = stripped[4:].strip()
            if name not in BLOCKS:
                sys.exit(f"{where}: unknown block '::: {name}' — known: {', '.join(BLOCKS)}")
            need_section(f"a '::: {name}' block")
            body, i = [], i + 1
            while i < len(lines) and lines[i].strip() != ":::":
                body.append(lines[i])
                i += 1
            if i >= len(lines):
                sys.exit(f"{where}: block '::: {name}' is never closed with a bare ':::'")
            current["parts"].append(BLOCKS[name](body))

        else:
            pending.append(line)

        i += 1

    close_section()
    return "\n\n".join(sections)


def drop_empty(page):
    """Remove masthead/meta spans whose value is blank.

    Leaving a key out of the frontmatter should make that item disappear, not
    leave an empty <span> behind widening the flex gap.
    """

    def keep(match):
        inner = match.group(1)
        bold = re.search(r"<b>(.*?)</b>", inner, re.S)
        if bold is not None:
            return "" if not bold.group(1).strip() else match.group(0)
        return "" if not re.sub(r"<[^>]+>", "", inner).strip() else match.group(0)

    page = re.sub(r"<span>(.*?)</span>\s*", keep, page, flags=re.S)
    return re.sub(r'<p class="standfirst">\s*</p>\s*', "", page)


# --------------------------------------------------------------------------
# site
# --------------------------------------------------------------------------


def load_pages():
    """Read every content/*.md into a page dict, ordered for the nav."""
    paths = sorted(glob.glob(os.path.join(CONTENT, "*.md")))
    if not paths:
        sys.exit(f"no content: {CONTENT}/*.md is empty")

    pages = []
    for path in paths:
        name = os.path.splitext(os.path.basename(path))[0]
        with open(path, encoding="utf-8") as f:
            meta, body = split_frontmatter(f.read())
        slug = meta.get("slug", name)
        pages.append(
            {
                "meta": meta,
                "body": body,
                "where": os.path.relpath(path, HERE),
                "slug": slug,
                "file": f"{slug}.html",
                "href": "./" if slug == "index" else f"./{slug}.html",
                "nav": meta.get("nav", meta.get("title", name)),
                "order": int(meta.get("order", 99)),
            }
        )

    seen = {}
    for page in pages:
        if page["slug"] in seen:
            sys.exit(
                f"two pages both build {page['file']}: "
                f"{seen[page['slug']]} and {page['where']}"
            )
        seen[page["slug"]] = page["where"]

    pages.sort(key=lambda p: (p["order"], p["nav"]))
    return pages


def render_nav(pages, current):
    items = []
    for page in pages:
        here = ' aria-current="page"' if page is current else ""
        items.append(f'<a href="{page["href"]}"{here}>{html.escape(page["nav"])}</a>')
    return "\n".join(items)


def build(args):
    out_dir = os.path.abspath(args.out or DEFAULT_OUT)
    pages = load_pages()

    with open(os.path.join(HERE, "style.css"), encoding="utf-8") as f:
        css = f.read()
    with open(os.path.join(HERE, "template.html"), encoding="utf-8") as f:
        template = f.read()

    site_title = next(
        (p["meta"]["site"] for p in pages if p["meta"].get("site")),
        "Shoreline Brewery Open Jam",
    )
    year = str(datetime.date.today().year)

    os.makedirs(out_dir, exist_ok=True)
    written = []

    for page in pages:
        meta = page["meta"]
        styles = (
            f"<style>\n{css}\n</style>"
            if args.inline_css
            else '<link rel="stylesheet" href="./style.css">'
        )
        fields = {
            "lang": meta.get("lang", "en"),
            "title": html.escape(meta.get("title", site_title)),
            "site": html.escape(site_title),
            "description": html.escape(meta.get("description", "")),
            "standfirst": inline(meta.get("standfirst", "")),
            "eyebrow": inline(meta.get("eyebrow", "")),
            "nav": render_nav(pages, page),
            "styles": styles,
            "content": render_body(page["body"], page["where"]),
            "year": year,
        }

        html_out = template
        for key, value in fields.items():
            html_out = html_out.replace("{{" + key + "}}", value)
        html_out = drop_empty(html_out)

        leftover = set(re.findall(r"\{\{(\w+)\}\}", html_out))
        if leftover:
            print(f"warning: {page['file']}: unreplaced placeholders: {', '.join(leftover)}")

        path = os.path.join(out_dir, page["file"])
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_out)
        written.append(path)

    if not args.inline_css:
        path = os.path.join(out_dir, "style.css")
        shutil.copyfile(os.path.join(HERE, "style.css"), path)
        written.append(path)

    # Pictures live beside the markdown that names them; ship the folder as-is.
    pics = os.path.join(CONTENT, "pics")
    if os.path.isdir(pics):
        dest = os.path.join(out_dir, "pics")
        shutil.copytree(pics, dest, dirs_exist_ok=True)
        written.extend(sorted(glob.glob(os.path.join(dest, "*"))))

    # Tell GitHub Pages to serve these files as-is rather than run Jekyll over them.
    nojekyll = os.path.join(out_dir, ".nojekyll")
    if not os.path.exists(nojekyll):
        open(nojekyll, "w").close()
        written.append(nojekyll)

    if not any(p["slug"] == "index" for p in pages):
        print("warning: no page has slug 'index' — GitHub Pages will 404 at the site root")

    for path in written:
        shown = os.path.relpath(path, os.getcwd())
        if shown.startswith(".." + os.sep + ".."):
            shown = path  # a distant output directory reads better absolute
        print(f"wrote {shown}  ({os.path.getsize(path):,} bytes)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-o", "--out", help="output directory (default: ../docs)")
    parser.add_argument(
        "--inline-css",
        action="store_true",
        help="inline the CSS into every page instead of linking a shared style.css",
    )
    build(parser.parse_args())
