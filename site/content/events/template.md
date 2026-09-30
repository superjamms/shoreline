---
date: 2026-09-29
slug: template
draft: true
title: Recap template
label: Recap template
eyebrow: Copy this file · not linked from anywhere
standfirst: This page is the shape every recap takes. Everything below is placeholder text — copy this file to content/events/YYYY-MM-DD.md, set the frontmatter, and replace the words.
description: The template a Shoreline Brewery open jam recap is built from — frontmatter, clips, and the setlist blocks for bands, soloists and the open jam.
---

=== block

::: callout
**This is a template, not a night.** It carries `draft: true`, so it builds but
stays out of the nav and out of both event lists. Nothing on it happened.
:::

::: facts
- **Copy it** — `cp content/events/template.md content/events/2026-10-13.md`
- **Then** — set `date`, `title`, `label`, `summary`; delete `draft` and `slug`
- **Slug** — leave it out and the filename becomes the URL, so the date is the URL
- **Rebuild** — `python3 build.py`
:::

=== block

^ The recap

## How the night went

Two or three paragraphs, written the morning after while it's still fresh. Who
turned up, what the room was like, anything worth remembering — a first-timer who
got up and shouldn't have been nervous, a song nobody expected to work.

Name people and bands here. The recap is also the thank-you, so the names matter
more than the prose does.

::: kicker
One line to close on — the moment from the night you'd tell someone about.
:::

=== block

^ Clips

## On video

::: video
- **Placeholder clip — replace with the night's video** — https://www.youtube.com/watch?v=jNQXAC9IVRw
- **A second clip sits beside the first** — https://youtu.be/jNQXAC9IVRw
:::

Any YouTube link works — `watch?v=`, a `youtu.be` share link, a `/shorts/` or
`/live/` URL, or a playlist. A `?t=90` or `?t=1m30s` in the link becomes the
start time. The caption is optional, so a line in a `::: video` block is either:

::: list
- `- **The Turn Ups — Mustang Sally** — https://youtu.be/VIDEOID` — captioned
- `- https://youtu.be/VIDEOID` — no caption, just the clip
:::

A link that isn't YouTube, or that carries no video id, fails the build rather
than shipping a blank frame.

=== block

^ What got played

## The setlist

::: setlist
### The Turn Ups — house band
- Mustang Sally · Wilson Pickett · C
- Ain't No Sunshine · Bill Withers · Am
- Cissy Strut · The Meters · C

### Example Guest Band — guest band
- Their own material
- A cover nobody saw coming · Some Artist · G

### A Soloist — solo, backing track
- Song title · Artist

### Another Soloist — solo, backed by the house band
- Song title · Artist · E

### The open jam — open jam
- Folsom Prison Blues · Johnny Cash · E
- Green Onions · Booker T. & the M.G.'s · F
- Something in a blues in A · · A
:::

One `###` row per act. The part after the em dash is the kind of act — *house
band*, *guest band*, *solo*, *open jam*, or anything else that describes it — and
it becomes the tag beside the name. Each song is up to three fields — title,
artist, key — separated by `·`:

::: list
- `- Song title · Artist · Key` — all three
- `- Song title · Artist` — no key
- `- Song title` — just the title
- `- Song title ·  · Key` — a key but no artist: leave the middle field empty
:::

Artist and key are both optional, because half the time nobody wrote them down.

=== panel

^ Frontmatter

## What each key does

::: facts
- **date** — `YYYY-MM-DD`. Required. Decides upcoming vs. recap, and the sort order
- **title** — the `<h1>` on the page
- **label** — the short name in the schedule and recap lists. Defaults to `title`
- **note** — the second line in the *upcoming* list. Usually the timing
- **summary** — the second line in the *recaps* list. One sentence about the night
- **eyebrow** — the small orange line above the `<h1>`
- **standfirst** — the intro paragraph under the `<h1>`
- **description** — meta description and social-preview text
- **draft** — `true` builds the page but hides it from the nav and both lists
:::

Before the night, a page needs only `date`, `title` and `note`. The recap, the
clips and the setlist get added the next morning.

=== footer

Back to [all dates and recaps](/events.html).
