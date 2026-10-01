#!/usr/bin/env python3
"""Render content/*.md into the static site in docs/.

    python3 build.py                  -> docs/, linking a shared style.css
    python3 build.py --inline-css     -> docs/, with the CSS inlined per page
    python3 build.py -o /srv/www      -> somewhere else

`docs/` is what GitHub Pages serves (Settings -> Pages -> Deploy from a branch ->
main -> /docs). The output is committed, so a deploy is a `git push`.

Two kinds of page:

    content/*.md         -> docs/*.html         one nav entry each
    content/events/*.md  -> docs/events/*.html  one night each, kept out of the nav

A file whose name starts with `_` is never built — that's how `_template.md`
sits in `content/events/` as a thing to copy rather than a page.

No third-party packages. The markdown subset understood here is deliberately
small — just what these pages use. The conventions are documented in README.md;
the short version:

    ---            frontmatter, key: value pairs
    === name       opens a section with that CSS class
    ^ text         eyebrow above the section heading
    ## text        section heading
    - text         a bullet list; '1. text' for a numbered one
    ::: name       a structured block, closed by a bare ::: (the space is
                   optional — ':::name' is the same directive)
    @ text         inside ::: steps, the aside line for a step
    /x.html        a link to x.html at the site root, from any depth
"""

import argparse
import datetime
import glob
import html
import os
import re
import shutil
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "content")
EVENT_DIR = os.path.join(CONTENT, "events")
DEFAULT_OUT = os.path.join(HERE, os.pardir, "docs")

# --------------------------------------------------------------------------
# per-page render state
#
# Rendering a page needs two things its own markdown doesn't carry: where the
# page sits relative to the site root, so a "/x.html" link resolves from any
# depth, and the list of events, so the schedule and recap blocks can build
# themselves. build() sets both once per page instead of threading them through
# every renderer.
# --------------------------------------------------------------------------

ROOT = ""                       # "" on a top-level page, "../" inside events/
EVENTS = []                     # every event page, oldest night first
TODAY = datetime.date.today()

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
            f'<a href="{html.escape(site_href(m.group(2)), quote=True)}"'
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


def site_href(href):
    """'/x.html' means x.html at the site root, whatever depth the page is at.

    Without this an event page would have to write '../how-it-works.html' and a
    top-level page './how-it-works.html' for the same destination.
    """
    if href.startswith("/"):
        return (ROOT + href.lstrip("/")) or "./"
    return href


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


# What opens a list item — '- text' or '1. text'. Shared by list_items and by
# the bare-list branch of render_body, which has to spot one in a section.
ITEM_RE = re.compile(r"^(-|\d+\.)\s+")


def list_items(lines):
    """Collect '- ' or '1. ' items, joining their wrapped continuation lines."""
    items, current = [], None
    for line in lines:
        stripped = line.strip()
        if ITEM_RE.match(stripped):
            if current is not None:
                items.append(" ".join(current))
            current = [ITEM_RE.sub("", stripped)]
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
                f'<img src="{html.escape(site_href(match.group(2)), quote=True)}" '
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


def render_list(lines, ordered=False):
    """A plain bullet list — the one block that asks nothing of its items.

    `ordered` is for a bare `1.` list written straight into a section. The
    orange bullet `.list` draws would sit where the number belongs, so an
    ordered list stays an unclassed <ol> and takes the fallback list styling.
    """
    rows = [f"<li>{inline(item)}</li>" for item in list_items(lines)]
    if ordered:
        return "<ol>\n" + "\n".join(rows) + "\n</ol>"
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


# ---------------- ::: video ----------------

# Every YouTube URL shape a phone or a browser will hand you, reduced to an id.
YT_HOSTS = ("youtube.com", "m.youtube.com", "youtube-nocookie.com", "youtu.be")
YT_PATHS = ("/embed/", "/shorts/", "/live/", "/v/")
YT_ID_RE = re.compile(r"^[\w-]{11}$")
YT_TIME_RE = re.compile(r"^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$")


def yt_start(value):
    """'90', '1m30s' and '1h02m03s' all mean a number of seconds."""
    if value.isdigit():
        return int(value)
    match = YT_TIME_RE.fullmatch(value)
    if not match or not any(match.groups()):
        return 0
    hours, minutes, seconds = (int(g or 0) for g in match.groups())
    return hours * 3600 + minutes * 60 + seconds


def youtube_embed(url, where):
    """Any YouTube link -> an embed src on the no-cookie host.

    Pasting whatever the share sheet produced should work, so watch?v=, youtu.be,
    /shorts/, /live/ and a playlist link are all accepted. Anything else is a
    typo worth failing the build over rather than shipping a blank frame.
    """
    parts = urllib.parse.urlsplit(url)
    host = parts.netloc.lower()
    host = host[4:] if host.startswith("www.") else host
    path = parts.path.rstrip("/")
    query = urllib.parse.parse_qs(parts.query)

    if host not in YT_HOSTS:
        sys.exit(f"{where}: ::: video — not a YouTube link:\n  {url}")

    video = ""
    if host == "youtu.be":
        video = path.lstrip("/")
    elif path == "/watch":
        video = (query.get("v") or [""])[0]
    else:
        for prefix in YT_PATHS:
            if path.startswith(prefix):
                video = path[len(prefix):]
                break

    playlist = (query.get("list") or [""])[0]
    if video and not YT_ID_RE.match(video):
        sys.exit(f"{where}: ::: video — '{video}' is not an 11-character video id:\n  {url}")
    if not video and not playlist:
        sys.exit(f"{where}: ::: video — no video id or playlist in:\n  {url}")

    embed = "https://www.youtube-nocookie.com/embed/"
    src = embed + (video or "videoseries")
    args = []
    if playlist:
        args.append(("list", playlist))
    start = yt_start((query.get("t") or query.get("start") or [""])[0])
    if start:
        args.append(("start", str(start)))
    if args:
        src += "?" + urllib.parse.urlencode(args)
    return src


def render_video(lines, where):
    """One or more embedded clips, each optionally captioned.

    '- **Caption** — url' captions the clip; a bare '- url' doesn't. Either way
    the caption row carries a plain link out to YouTube, because an embed that
    the viewer's browser blocks should still leave them somewhere to go.
    """
    figures = []
    for item in list_items(lines):
        label, url = "", item.strip()
        if item.lstrip().startswith("**"):
            label, url = split_label(item, "video")
            url = url.strip()
        src = youtube_embed(url, where)
        title = label or "Open jam clip"
        caption = f'<span class="video-label">{inline(label)}</span>' if label else ""
        figures.append(
            '<figure class="video">'
            '<div class="video-frame">'
            f'<iframe src="{html.escape(src, quote=True)}" '
            f'title="{html.escape(title, quote=True)}" loading="lazy" '
            'referrerpolicy="strict-origin-when-cross-origin" '
            'allow="accelerometer; clipboard-write; encrypted-media; picture-in-picture" '
            'allowfullscreen></iframe></div>'
            f'<figcaption>{caption}'
            f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener">'
            'Watch on YouTube</a></figcaption>'
            "</figure>"
        )
    if not figures:
        sys.exit(f"{where}: ::: video — no links in the block")
    return '<div class="videos">\n' + "\n".join(figures) + "\n</div>"


# ---------------- ::: setlist ----------------

# What got played, grouped by whoever played it:
#
#   ### The Turnups — house band
#   - Mustang Sally · Wilson Pickett · C
#
# The '###' row is the act and its kind; each song is up to three fields —
# title, artist, key — separated by '·', or by '|' for anyone whose keyboard
# makes that easier. Artist and key are both optional, because half the time
# nobody wrote them down.
SONG_SEP_RE = re.compile(r"\s*[·|]\s*")
SONG_FIELDS = ("song", "by", "key")


def render_setlist(lines, where):
    """What got played, grouped by whoever played it."""
    sets, current = [], None

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("### "):
            title = stripped[4:].strip()
            kind = ""
            match = re.match(r"^(.*?)\s+[—–]\s+(.*)$", title)
            if match:
                title, kind = match.group(1).strip(), match.group(2).strip()
            current = {"title": title, "kind": kind, "songs": []}
            sets.append(current)
        elif stripped.startswith("- "):
            if current is None:
                sys.exit(
                    f"{where}: ::: setlist — a song needs a '### act' above it:"
                    f"\n  {stripped[:70]}"
                )
            current["songs"].append(stripped[2:].strip())
        elif stripped:
            sys.exit(
                f"{where}: ::: setlist — expected '### act' or '- song':"
                f"\n  {stripped[:70]}"
            )

    if not sets:
        sys.exit(f"{where}: ::: setlist — no '### act' rows in the block")

    out = []
    for act in sets:
        kind = (
            f'<span class="set-kind">{inline(act["kind"])}</span>'
            if act["kind"]
            else ""
        )
        rows = []
        for song in act["songs"]:
            fields = SONG_SEP_RE.split(song)
            cells = [
                f'<span class="song-{name}">{inline(value)}</span>'
                for name, value in zip(SONG_FIELDS, fields)
                if value.strip()
            ]
            rows.append("<li>" + "".join(cells) + "</li>")
        songs = (
            '<ol class="songs">\n' + "\n".join(rows) + "\n</ol>"
            if rows
            else '<p class="empty">Songs not written down.</p>'
        )
        out.append(
            '<div class="set"><div class="set-head">'
            f'<h3>{inline(act["title"])}</h3>{kind}</div>{songs}</div>'
        )
    return '<div class="setlist">\n' + "\n".join(out) + "\n</div>"


# ---------------- ::: schedule and ::: recaps ----------------
#
# The only two blocks that build themselves. They read the event pages rather
# than a hand-kept list, so adding content/events/2026-10-13.md is the whole
# job of putting that night on the home page.


def parse_options(lines, block, allowed, where):
    options = {}
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        match = re.match(r"^(\w+):\s*(.*)$", stripped)
        if match is None or match.group(1) not in allowed:
            sys.exit(
                f"{where}: ::: {block} — takes only "
                f"{', '.join(k + ':' for k in allowed)}, not:\n  {stripped[:70]}"
            )
        options[match.group(1)] = match.group(2).strip()
    return options


def option_limit(options, block, where):
    raw = options.get("limit", "")
    if not raw:
        return None
    if not raw.isdigit() or raw == "0":
        sys.exit(
            f"{where}: ::: {block} — 'limit:' wants a positive whole number, "
            f"got '{raw}'"
        )
    return int(raw)


def listed_events():
    """The events either list may show — a draft is built but never listed."""
    return [e for e in EVENTS if not e["draft"]]


def event_rows(events, note_of, cls):
    rows = []
    for event in events:
        date = event["date"]
        note = note_of(event)
        # The year is noise on this year's dates and necessary on last year's.
        dow = f"{date:%a}" if date.year == TODAY.year else f"{date:%a} {date.year}"
        rows.append(
            f'<li><a href="{html.escape(ROOT + event["href"], quote=True)}">'
            f'<span class="event-date"><b>{date:%b} {date.day}</b>'
            f'<span class="event-dow">{dow}</span></span>'
            f'<span class="event-what"><span class="event-title">'
            f'{inline(event["label"])}</span>'
            + (f'<span class="event-note">{inline(note)}</span>' if note else "")
            + "</span></a></li>"
        )
    return f'<ul class="events {cls}">\n' + "\n".join(rows) + "\n</ul>"


def render_schedule(lines, where):
    """The nights still to come, soonest first."""
    options = parse_options(lines, "schedule", ("limit", "empty"), where)
    limit = option_limit(options, "schedule", where)
    upcoming = [e for e in listed_events() if e["date"] >= TODAY]
    if not upcoming:
        return (
            '<p class="empty">'
            + inline(options.get("empty") or "Next dates going up shortly.")
            + "</p>"
        )
    return event_rows(upcoming[:limit], lambda e: e["meta"].get("note", ""), "upcoming")


def render_recaps(lines, where):
    """The nights already played, most recent first."""
    options = parse_options(lines, "recaps", ("limit", "empty"), where)
    limit = option_limit(options, "recaps", where)
    past = [e for e in reversed(listed_events()) if e["date"] < TODAY]
    if not past:
        return (
            '<p class="empty">'
            + inline(options.get("empty") or "The first recap goes up soon.")
            + "</p>"
        )
    return event_rows(
        past[:limit],
        lambda e: e["meta"].get("summary", "") or "Recap coming soon.",
        "recaps",
    )


BLOCKS = {
    "cards": render_cards,
    "facts": render_facts,
    "callout": render_callout,
    "kicker": render_kicker,
    "list": render_list,
    "numbers": render_numbers,
    "steps": render_steps,
    "video": render_video,
    "setlist": render_setlist,
    "schedule": render_schedule,
    "recaps": render_recaps,
}

# These four need to know which file they came from, to report a bad link or a
# stray line against it; the older blocks can't fail in a way that needs it.
BLOCKS_NEEDING_SOURCE = {"video", "setlist", "schedule", "recaps"}


# The line-based directives, and the name each one carries. The space after the
# marker is optional — ':::list' and '::: list' are the same intent, and a
# missing space used to drop the line into the prose, which shipped a literal
# ':::list' onto the page. A marker that names nothing known now fails the
# build instead of printing itself.
SECTION_RE = re.compile(r"^===\s*(\S.*)$")
EYEBROW_RE = re.compile(r"^\^\s*(\S.*)$")
HEADING_RE = re.compile(r"^##(?!#)\s*(\S.*)$")
BLOCK_RE = re.compile(r"^:::\s*(\S.*)$")


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

        section = SECTION_RE.match(stripped)
        mark = EYEBROW_RE.match(stripped)
        heading = HEADING_RE.match(stripped)
        block = BLOCK_RE.match(stripped)

        if section:
            close_section()
            current = {"cls": section.group(1).strip(), "parts": []}
            eyebrow = None

        elif mark:
            flush_text()
            eyebrow = mark.group(1).strip()

        elif heading:
            flush_text()
            need_section("a '## heading'")
            if eyebrow:
                current["parts"].append(f'<p class="eyebrow">{inline(eyebrow)}</p>')
                eyebrow = None
            current["parts"].append(f"<h2>{inline(heading.group(1).strip())}</h2>")

        elif block:
            flush_text()
            name = block.group(1).strip()
            if name not in BLOCKS:
                sys.exit(f"{where}: unknown block ':::{name}' — known: {', '.join(BLOCKS)}")
            need_section(f"a '::: {name}' block")
            body, i = [], i + 1
            while i < len(lines) and lines[i].strip() != ":::":
                body.append(lines[i])
                i += 1
            if i >= len(lines):
                sys.exit(f"{where}: block '::: {name}' is never closed with a bare ':::'")
            if name in BLOCKS_NEEDING_SOURCE:
                current["parts"].append(BLOCKS[name](body, where))
            else:
                current["parts"].append(BLOCKS[name](body))

        elif ITEM_RE.match(stripped):
            # A list written straight into a section, no '::: list' around it.
            # It runs to the first line that isn't part of it: a blank line with
            # no further item after it, or anything that opens something else.
            flush_text()
            need_section("a list")
            ordered = stripped[0].isdigit()
            body = []
            while i < len(lines):
                item_line = lines[i].strip()
                if not item_line:
                    nxt = i + 1
                    while nxt < len(lines) and not lines[nxt].strip():
                        nxt += 1
                    if nxt >= len(lines) or not ITEM_RE.match(lines[nxt].strip()):
                        break
                    body.append("")  # a gap between items, still one list
                    i = nxt
                    continue
                if item_line.startswith(("=== ", "^ ", "## ", ":::")):
                    break
                body.append(lines[i])
                i += 1
            current["parts"].append(render_list(body, ordered))
            continue  # i already sits on the line after the list

        elif stripped.startswith(("===", ":::")):
            # A marker that named nothing. Either a bare '===', or a ':::'
            # closing a block that was never opened — the block renderers eat
            # their own closing fence, so one reaching here is stray. Letting it
            # through would print the markup onto the page.
            sys.exit(
                f"{where}: '{stripped}' opens nothing and closes nothing — "
                "'=== name' starts a section, ':::name' a block, and a bare "
                "':::' only closes a block already open above it"
            )

        else:
            pending.append(line)

        i += 1

    close_section()
    return "\n\n".join(sections)


def drop_empty(page):
    """Remove masthead/meta spans and paragraphs whose value is blank.

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
    return re.sub(r'<p class="(?:standfirst|eyebrow)">\s*</p>\s*', "", page)


# --------------------------------------------------------------------------
# site
# --------------------------------------------------------------------------


def truthy(value):
    return value.strip().lower() in ("1", "true", "yes", "on")


def source_files(folder):
    """The markdown in a folder, minus the '_' files that are there to copy."""
    return sorted(
        path
        for path in glob.glob(os.path.join(folder, "*.md"))
        if not os.path.basename(path).startswith("_")
    )


def read_page(path, is_event):
    """Turn one markdown file into the page dict the rest of the build uses."""
    where = os.path.relpath(path, HERE)
    name = os.path.splitext(os.path.basename(path))[0]
    with open(path, encoding="utf-8") as f:
        meta, body = split_frontmatter(f.read())

    slug = meta.get("slug", name)
    title = meta.get("title", name)
    folder = "events/" if is_event else ""

    date = None
    if is_event:
        raw = meta.get("date", "")
        try:
            date = datetime.date.fromisoformat(raw)
        except ValueError:
            sys.exit(f"{where}: an event needs 'date: YYYY-MM-DD', not '{raw}'")

    return {
        "meta": meta,
        "body": body,
        "where": where,
        "slug": slug,
        # where the built file goes, and how to reach it from the site root
        "file": f"{folder}{slug}.html",
        "href": "" if slug == "index" else f"{folder}{slug}.html",
        # how to get back to the site root from this page
        "root": "../" if is_event else "",
        "nav": meta.get("nav", title),
        "order": int(meta.get("order", 99)),
        "is_event": is_event,
        "date": date,
        # the short name the schedule and recap lists use
        "label": meta.get("label", title),
        # which nav entry stays lit while this page is open
        "parent": "events" if is_event else meta.get("parent", ""),
        # built, but kept out of the nav and out of both event lists
        "draft": truthy(meta.get("draft", "")),
    }


def load_pages():
    """Read the content into page dicts: the nav pages, then the event pages."""
    paths = source_files(CONTENT)
    if not paths:
        sys.exit(f"no content: {CONTENT}/*.md is empty")

    pages = [read_page(path, False) for path in paths]
    pages.sort(key=lambda p: (p["order"], p["nav"]))

    events = [read_page(path, True) for path in source_files(EVENT_DIR)]
    events.sort(key=lambda p: p["date"])

    seen = {}
    for page in pages + events:
        if page["file"] in seen:
            sys.exit(
                f"two pages both build {page['file']}: "
                f"{seen[page['file']]} and {page['where']}"
            )
        seen[page["file"]] = page["where"]

    return pages, events


def render_nav(pages, current):
    items = []
    for page in pages:
        if page["draft"]:
            continue
        lit = page is current or (current["parent"] and page["slug"] == current["parent"])
        here = ' aria-current="page"' if lit else ""
        href = (current["root"] + page["href"]) or "./"
        items.append(
            f'<a href="{html.escape(href, quote=True)}"{here}>'
            f'{html.escape(page["nav"])}</a>'
        )
    return "\n".join(items)


def build(args):
    global ROOT, EVENTS

    out_dir = os.path.abspath(args.out or DEFAULT_OUT)
    pages, EVENTS = load_pages()

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

    for page in pages + EVENTS:
        meta = page["meta"]
        # Every relative URL on the page — the stylesheet, the nav, a "/x.html"
        # link in the content — is written from here.
        ROOT = page["root"]
        styles = (
            f"<style>\n{css}\n</style>"
            if args.inline_css
            else f'<link rel="stylesheet" href="{ROOT}style.css">'
        )
        fields = {
            "lang": meta.get("lang", "en"),
            "root": ROOT or "./",
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
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_out)
        written.append(path)

    ROOT = ""

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

    if not any(p["slug"] == "index" and not p["is_event"] for p in pages):
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
