# The site

The public pages for the open jam, built from Markdown so the words can be
edited without touching the design.

```text
content/        the words             <- edit these
  about.md        -> docs/index.html
  how-it-works.md -> docs/how-it-works.html
style.css       the design            <- and this, to retune the look
template.html   the page skeleton     <- nav, footer, <head>
build.py        the renderer          <- no dependencies, stdlib only
```

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
`content/songlist.md` builds `docs/songlist.html`.

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
| `site` | The site name in the header, footer and `<title>`. Set once, on any page |

Exactly one page should carry `slug: index`, or the site root 404s. Today that's
`about.md` — the about page *is* the front door. If a separate landing page ever
makes sense, move `slug: index` to it and give `about.md` its own slug.

## Writing in content files

Normal Markdown for paragraphs, `**bold**`, `*italic*`, `[links](url)` and
`` `code` ``. Off-site links get `target="_blank"` automatically. On top of that
there are four conventions, all line-based.

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

Closed by a bare `:::`. Each one renders a specific layout:

| Block | Takes | Renders |
|---|---|---|
| `facts` | list of `- **Label** — text` | the when/where strip with the orange rule |
| `cards` | list of `- **Label** — text`, each optionally led by `![alt](pics/x.jpg)` | the bordered card grid, picture across the top |
| `callout` | a paragraph | the tinted box with the orange rule |
| `list` | a list of `- text` | a plain bullet list with orange bullets |
| `numbers` | a numbered list | `01/02/03` rows |
| `steps` | `###` headings, each with an optional `@ aside` line and optional `####` sub-steps | the numbered rows with asides, sub-steps bulleted beneath their step |
| `kicker` | a paragraph | the italic closing line |

Numbering in `steps` and `numbers` is generated — write the items in order and
don't hand-number them, or you'll get `01 1.`.

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
