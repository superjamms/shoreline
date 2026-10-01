# The site

The public pages for the open jam, built from Markdown so the words can be
edited without touching the design.

```text
content/          the words                 <- edit these
  home.md           -> docs/index.html        the dashboard
  events.md         -> docs/events.html       dates and recaps
  how-it-works.md   -> docs/how-it-works.html
  people.md         -> docs/people.html
  about.md          -> docs/about.html
  events/           one file per night      <- add one a week
    template.md       -> docs/events/template.html   (draft: copy this)
    2026-10-06.md     -> docs/events/2026-10-06.html
style.css         the design                <- and this, to retune the look
template.html     the page skeleton         <- nav, footer, <head>
build.py          the renderer              <- no dependencies, stdlib only
```

Top-level pages each get a nav entry. Event pages don't — they're reached from
the home page and from `events.html`, both of which build their lists from the
files in `content/events/`.

Output goes to **`../docs/`**, which is what GitHub Pages serves. It is generated
— don't edit it — but it *is* committed, because Pages serves the committed files.

## Build

```sh
cd site
python3 build.py                # writes ../docs/
python3 build.py --inline-css   # same, but each page carries its own CSS
python3 build.py -o /tmp/preview
```

No install step and no network access needed to build. Anything with Python 3
can run it.

To look at the result before pushing:

```sh
python3 -m http.server -d ../docs 8000   # then open http://localhost:8000
```

Opening `docs/index.html` straight off disk mostly works too, but the `./` link
on the wordmark needs a server to resolve.

The one external request a page makes is to Google Fonts. To make the pages
fetch nothing at all, delete the three `<link>` tags from `template.html`; the
fallback stacks in `style.css` take over.

## Publishing to GitHub Pages

One-time, in the repo on github.com:

**Settings → Pages → Build and deployment → Deploy from a branch → `main` / `/docs`**

After that a deploy is just:

```sh
cd site && python3 build.py
git add -A && git commit -m "site: update" && git push
```

The site appears at `https://<user>.github.io/shoreline/`. Everything is linked
relatively, so the subdirectory is fine and so is a custom domain later.

**For a custom domain** (PLAYBOOK.md argues for one — something like
`shorelineopenjam.com`): add the domain under Settings → Pages, which writes a
`CNAME` file. Put a copy at `site/CNAME`-adjacent — simplest is to commit
`docs/CNAME` once; `build.py` only overwrites the files it generates, so it
survives rebuilds.

`docs/.nojekyll` is generated too. It tells Pages to serve these files as-is
instead of running Jekyll over them.

## Adding a page

Drop a new file in `content/`. The filename becomes the URL, so
`content/songlist.md` builds `docs/songlist.html`. A file whose name starts with
`_` is skipped, so a scratch draft can sit in the folder without shipping.

Frontmatter drives everything outside the body:

| Key | Does |
|---|---|
| `title` | The `<h1>`, the `<title>`, and the default nav label |
| `nav` | Nav label, if it should differ from the title |
| `order` | Position in the nav. Lower is further left. Default 99 |
| `slug` | Output filename without `.html`. `slug: index` makes it the home page |
| `eyebrow` | The small orange line above the `<h1>` |
| `standfirst` | The larger intro paragraph under the `<h1>` |
| `description` | Meta description and social-preview text |
| `draft` | `true` builds the page but keeps it out of the nav and both event lists |
| `site` | The site name in the header, footer and `<title>`. Set once, on any page |

Exactly one page should carry `slug: index`, or the site root 404s. That's
`home.md` — the dashboard.

## Adding an event

One file per Tuesday, in `content/events/`. Name it for the date and the URL
follows: `content/events/2026-10-13.md` builds `docs/events/2026-10-13.html`.

```sh
cp content/events/template.md content/events/2026-10-13.md
```

Then edit the frontmatter — set `date`, `title`, `label` and `note`, and delete
the `slug` and `draft` lines the template carries. That's the whole job of
putting the night on the home page: `::: schedule` and `::: recaps` read the
folder, so nothing else needs touching.

| Key | Does |
|---|---|
| `date` | `YYYY-MM-DD`. **Required.** Decides upcoming vs. recap, and the sort order |
| `title` | The `<h1>` on the event page |
| `label` | The short name in both lists. Defaults to `title` |
| `note` | The second line in the **upcoming** list. Usually the timing |
| `summary` | The second line in the **recaps** list. One sentence about the night |

Plus `eyebrow`, `standfirst`, `description` and `draft`, which mean what they do
on any other page. Before the night a page needs only `date`, `title` and `note`;
the recap, the clips and the setlist go in the next morning.

`content/events/template.md` is a live page — `docs/events/template.html` — that
documents all of this and shows every block rendered. It carries `draft: true`,
so it builds but is linked from nowhere.

## Writing in content files

Normal Markdown for paragraphs, `**bold**`, `*italic*`, `[links](url)`, `` `code` ``
and bullet or numbered lists. Off-site links get `target="_blank"` automatically.
There are no fenced code blocks — inline `` `code` `` only. Lists don't nest.

**Link to other pages with a leading slash**: `[how it works](/how-it-works.html)`
means "how-it-works.html at the site root" and resolves from any depth, so the
same line works on a top-level page and on an event page one folder down.

**Lists need no wrapper.** Write one straight under a heading:

```markdown
## Mach 11

- Core
- Everlong
```

A list runs until a blank line with nothing more after it, or until the next
`===`, `^`, `##` or `:::`; a blank line *between* two items keeps them in one
list. A `- ` list gets the orange bullets, a `1. ` list gets plain numbers.
`::: list` renders the same `- ` list as a block, which only matters if you want
the fence for clarity in a long file.

On top of that there are four conventions, all line-based.

### `=== name` starts a section

Everything after it, until the next `===`, renders inside `<section class="name">`.
Three exist: `block` (a normal section), `panel` (the navy panel), `footer`
(the quiet closing note).

### `^ text` is the eyebrow

The small orange line above a heading. Put it directly before the `##`.

```markdown
^ The running order

## What happens, roughly in this order
```

### `## text` is a section heading

Renders as the condensed uppercase `<h2>`.

### `::: name` opens a structured block

Closed by a bare `:::`. The space after the marker is optional, so `:::list` and
`::: list` are the same directive — that goes for `=== name`, `^ text` and
`## text` too. A marker that names nothing known **fails the build**, rather
than printing a stray `:::` onto the page.

Each block renders a specific layout:

| Block | Takes | Renders |
|---|---|---|
| `facts` | list of `- **Label** — text` | the when/where strip with the orange rule |
| `cards` | list of `- **Label** — text`, each optionally led by `![alt](pics/x.jpg)` | the bordered card grid, picture across the top |
| `callout` | a paragraph | the tinted box with the orange rule |
| `list` | a list of `- text` | a plain bullet list with orange bullets |
| `numbers` | a numbered list | `01/02/03` rows |
| `steps` | `###` headings, each with an optional `@ aside` line and optional `####` sub-steps | the numbered rows with asides, sub-steps bulleted beneath their step |
| `kicker` | a paragraph | the italic closing line |
| `video` | a list of `- **Caption** — youtube-url`, caption optional | embedded clips, two up, each with a link out to YouTube |
| `setlist` | `### Act — kind` rows, each followed by `- Song · Artist · Key` items | the night's setlist, grouped by act |
| `schedule` | `limit:` and `empty:` options | the upcoming nights, soonest first — built from `content/events/` |
| `recaps` | `limit:` and `empty:` options | the past nights, most recent first — built from `content/events/` |

Numbering in `steps`, `numbers` and `setlist` is generated — write the items in
order and don't hand-number them, or you'll get `01 1.`.

### `::: video`

Any YouTube URL shape works — `watch?v=`, a `youtu.be` share link, `/shorts/`,
`/live/`, or a playlist. A `?t=90` or `?t=1m30s` becomes the start time. Embeds
go to `youtube-nocookie.com` and load lazily. A link that isn't YouTube, or that
carries no video id, **fails the build** rather than shipping a blank frame.

### `::: setlist`

```text
### The Turnups — house band
- Mustang Sally · Wilson Pickett · C
- Cissy Strut · The Meters · C

### A Soloist — solo, backing track
- Song title · Artist
```

The text after the em dash on a `###` row is the kind of act — *house band*,
*guest band*, *solo*, *open jam*, or anything else — and becomes the tag beside
the name. Each song is up to three `·`-separated fields: title, artist, key
(`|` works as a separator too, if that's easier to type). Artist and key are
optional; leave the middle field empty (`Song ·  · A`) to give a key without an
artist.

### `::: schedule` and `::: recaps`

The only two blocks that build themselves. They read `content/events/`, so the
lists are never edited by hand. Both take options, one per line:

```text
::: schedule
limit: 4
empty: The next dates go up here as they're set.
:::
```

`limit:` caps the number of rows; leave it out for all of them. `empty:` is the
line shown when there's nothing to list. An event with `draft: true` is skipped
by both.

## Retuning the design

Everything visual is a custom property at the top of `style.css`. The rules
below that block never hard-code a colour, so changing the tokens moves both
pages.

- **Palette** — `--orange: #FC5000` and `--navy: #13216A` are sampled straight
  off the Shoreline bowtie logo. `--orange-ink` is the same orange darkened
  enough to be readable as text on white; use it for type, `--orange` for rules
  and marks.
- **Type** — the brewery's own site runs on Adobe Fonts, which needs a paid kit
  tied to a domain, so each face is matched to its closest free Google Fonts
  equivalent: Adobe Garamond Pro → **EB Garamond** (`--font-display`), Bebas Neue
  → **Bebas Neue** (`--font-label`, same face), DIN Condensed → **Oswald**
  (`--font-meta`), Proxima Nova → **Montserrat** (`--font-body`). Swapping a face
  means updating the Google Fonts URL in `template.html` too.
- **Measure** — `--measure: 36rem` keeps running text near 68 characters.

Dark mode is defined three times on purpose: `:root` carries the light palette,
the `prefers-color-scheme` block covers viewers whose OS asks for dark, and
`:root[data-theme="dark"]` lets an explicit toggle win. If you add a theme
switch, stamp `data-theme` on `<html>` and it works with no other change.

`@media print` is tuned too — the navy panel inverts to bordered white.

## Still to fill in

Marked `TODO` in the content, all of them waiting on decisions in
[PLAYBOOK.md](../PLAYBOOK.md):

- **The start time.** `about.md` says 7:00 pm because the Facebook bio does, but
  other listings say 7:30 and the brewery's own page says 9:30. One of them wins
  and then it goes everywhere.
- **The signup form URL** (PLAYBOOK §4), linked from `how-it-works.md`.
- **The songlist URL** (PLAYBOOK §5), linked from the callout in `how-it-works.md`.
- **The first real recap.** `content/events/` has the next six Tuesdays as
  upcoming dates and `template.md` as the shape a recap takes; no night has been
  written up yet, so both recap lists are showing their `empty:` line.
