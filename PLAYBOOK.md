# Open Jam Playbook

A plan for the Shoreline Brewery Open Jam's online presence: weekly events,
signups, setlist tracking, and the partnerships around them.

Prepared 19 Sept 2026, revised 21 Sept 2026. For the page, the host, and the bar.

> The nights themselves are a lot of fun, and each one is run well. What's thin is
> everything between them — almost nothing online, and nothing left behind
> afterwards.

Every fix in here does one job: leave something behind after last call.

**Two problems, not one.** The README names both, and they need different answers:

- **The online presence is almost non-existent.** One Facebook page with a stale
  follower list, a four-sentence bio, no events, no songlist, and no record of any
  night that has ever happened. The venue's own site doesn't list the jam at all.
- **The partnerships are real, but nothing online says so.** They already exist
  informally: Shoreline as the host venue, the Turn Ups coordinating and hosting
  every week, **Roxy Music** — where the band members work and teach, and where
  some guest bands arrive from via the student programs — and returning guest
  bands like New Groove and Catalyst. None of that is visible from any page. So
  this isn't a cold-call problem, it's an undeclared-relationship problem, which
  is a far cheaper one to fix. §1 and §3.

**Start from what's already true.** Planning is not absent. Per the README, there's
discussion between the coordinator and house band members ahead of a night — who's
coming, who's sitting in, whether a guest band is booked. The gap isn't effort,
it's that none of it is transparent: it lives with whoever was in the thread, and
it's gone by the following week.

So the fix has two halves, and neither works alone. A *routine* — a standing prompt
at the same point each week — is what keeps it from decaying back into ad hoc. A
*record* is what makes it visible to everyone who wasn't in the conversation, and
what lets one week build on the last instead of starting the same questions over.

The good news is in what this isn't. Nothing below asks anyone to start
coordinating from nothing — the instinct is demonstrably there. It asks that the
coordination which already happens gets a fixed time and a place to land. That's a
much smaller request than it looks, and it's why this is realistic rather than
aspirational.

**A record also surfaces the weeks that got skipped.** This is the part that's easy
to miss. Written-down planning isn't only an archive for the good weeks; it's what
makes a thin week legible while there's still time to act. An empty sheet on Sunday
is itself the signal — and no amount of private conversation can produce that signal,
because the absence of a conversation looks exactly like nothing at all.

What genuinely doesn't exist yet is the *published* layer. No event means no
reminder and no attendance signal, so nobody outside the conversation knows whether
the room will be empty or stacked. No songlist means a first-timer has no way to
prepare, so they watch instead of play. Those two gaps produce the rest of what's
in the README — the idle nights, the packed nights that waste an hour on logistics,
the stale follower list.

---

## What was checked before writing this

**The Page itself is public; the tooling couldn't read it.** Worth stating
precisely, because the two are different things. The Page and its bio are
viewable anonymously — no account needed, no login wall. What failed was
*automated* retrieval: fetching `facebook.com/shorelineopenjam` returns only the
document title, "Shoreline Brewery Open Jam | Michigan City IN," because Facebook
serves a script shell to non-browser clients. So everything below about
followers, posts, and bio is taken from the README rather than a direct look —
a limit of how this was checked, not a limit on who can see the page.

**Events and RSVPs are the part that does need a login.** That asymmetry has a
consequence worth designing around, in §2 and §6: anything published only inside
an event is invisible to someone without an account, while the bio and a pinned
post are not. So the essentials — start time, backline, how a night runs, and the
songlist and signup links — belong in the bio and the pinned post, with the event
carrying the week-specific detail. It's also a second argument for keeping the
signup and songlist on Google rather than anywhere inside Facebook: those open
for anyone, logged in or not.

**Confirmed — it's a Page, with no Group alongside it.** The Page is the only
surface, which settles the question this plan was hedging on and makes everything
below load-bearing rather than provisional. It also fixes the shape of the
problem: on a Page, followers can't post: all content originates from the Page
itself. There is no members' wall that might fill itself in. Whatever the one
named owner posts is the entire output, which is exactly why §6's three-posts-a-
week rhythm has to be small enough to actually survive.

**Found — the venue's own calendar doesn't list the jam.**
`shorelinebrewery.com/events` has Jazz Night, bocce, and the Sunday music series.
The Tuesday jam isn't there. Their dedicated open mic page is a single stale
event dated **20 Feb 2018**, 9:30 PM, hosted by Eric Norman and Nate Miller.
That's free exposure sitting unused on a site the brewery already maintains.

**Found — the start time disagrees across every source.** This README says
**7:00 PM**. Other listings say **7:30 PM**. The venue's stale page says
**9:30 PM**. Worth fixing first — it's cheap, and no amount of promotion helps if
people arrive at the wrong hour.

---

## Where the jam is visible today

Every surface the jam is currently advertised on, in one place. It's a short list,
and two of the five entries are the same website failing to mention Tuesday.

| What | URL |
|---|---|
| Open Jam Facebook page | https://www.facebook.com/shorelineopenjam |
| Shoreline Brewery website | https://www.shorelinebrewery.com/ |
| Shoreline Brewery events calendar | https://www.shorelinebrewery.com/events |
| Shoreline Brewery open mic page (stale — 20 Feb 2018) | https://www.shorelinebrewery.com/events/openmic |
| Venue | 208 W. Wabash St, Michigan City, IN |

Six links this plan needs and doesn't have. Two of them exist and just haven't
been tracked down; four get created along the way. Every `[link]` placeholder in
the templates below points at one of them:

| What | Status |
|---|---|
| Shoreline Brewery main Facebook page (the Page, not a group) | URL unconfirmed — needed for the co-host step in §1 |
| Roxy Music page | URL unconfirmed — needed for partner credits and tags (§1, §6) |
| **The jam's own page** — one owned URL, the canonical explainer | To be stood up in Phase 2 (§1, *The detail needs a URL the Page can point at*) |
| Signup form (Google Form → Sheet) | To be built in Phase 2 |
| Songlist + setlist log (published Sheet) | To be built in Phase 3 |
| Pinned post permalink | Exists the moment the post does — copy it at publish time (§1) |

Fill these in as they're made, and keep this table as the single place they're
copied from — the bio, every event description, and the pinned post all quote the
same URLs, and they only stay consistent if there's one source for them.

---

## 1. Fix the front door

Before adding anything new, make the existing page correct and complete — then
borrow the audiences that are already standing next to it. The corrections are an
afternoon of work and they're the highest ratio of effect to effort on the list;
the partnerships are conversations, not projects.

### Settle on one time, then publish it everywhere

Pick the real start time and push it to the Page bio, every event, the venue's
website, and any directory listing reachable. One canonical number.

### Rewrite the bio

The current bio is four sentences that say when and what. It doesn't answer the
question an actual newcomer has, which is *what happens if I show up and I've
never done this*. Something closer to this:

```
Open Jam at Shoreline Brewery — every Tuesday, 7:00 PM.
Hosted by Nate Miller & the Turn Ups.

Full backline provided: guitar and bass amps, keys, drums,
mics, mixer, DI, and the house PA. Bring your instrument —
that's genuinely all you need. Prefer your own pedalboard or
amp? Bring it, we'll make room.

How the night runs: the house band opens, then we work
through the signup list. Play a solo set, sit in with the
Turn Ups, bring your whole group, or just tell us you want
to jam and we'll put you with people. Backing tracks are
fine — bring your phone, the cable and the adapters are
already at the board.

First time? Say so at the bar and we'll put you somewhere
comfortable. You don't need a band, a set, or gear.

Hosted at Shoreline Brewery. Players and student bands from
Roxy Music always welcome.

How it works, songlist and signup → [jam page link]
208 W. Wabash St, Michigan City, IN
```

**One link, and make it the jam's own page.** The bio has room for exactly one
URL, so it can't be the form *and* the sheet — it has to be the page that carries
both, for the reasons in *The detail needs a URL the Page can point at* below. Use
the venue's events page in the interim if the jam page isn't up yet; don't leave
the line reading `[link]`.

**Don't bury the backline.** The gear list reads like housekeeping and isn't —
it's the single most persuasive fact the page has. A full backline with keys, DI
and a house PA means a keys player can turn up carrying nothing at all, and a
guitarist needs one hand free. "Bring your instrument, that's it" removes the
actual reason most people who think about coming don't, which is the logistics of
hauling gear to a bar on a work night for a slot they aren't sure they'll get.
The line about welcoming your own pedalboard matters for the opposite reason: it
tells a gigging player that showing up properly equipped won't be treated as a
nuisance. And the board takes a backing track, which quietly extends the same
promise to solo acts: a singer with tracks on their phone is a complete act on
that stage without carrying anything either.

**And be clear about whose it is.** The PA is the venue's. Everything else on
that stage — amps, keys, drums, mics, mixer, DI — belongs to the house band, in
practice to the coordinator and the bass player personally. That matters twice
over. It's a substantial contribution from both parties that nothing online
mentions, which makes it exactly the sort of thing the partner credits in the
next section exist to say out loud. And it means every decision about how that
rig gets set up — the backing-track channel in §3 included — is the band's own
call, requiring nobody's permission and no one else's budget.

It also comes in and out of the building every week. The backline is hauled in,
set up, torn down and hauled back out every Tuesday by those same two people,
which has two consequences worth holding onto. The first is a credit: that is a
substantial standing effort, donated weekly, that nothing online records — and
it's the most concrete answer available to anyone who wonders what the house band
contributes beyond playing. The second is a constraint that applies to every
suggestion in this document: **nothing can be permanently installed.** Anything
settled about the setup has to survive being packed into a car and rebuilt from
scratch the following week, which makes the useful unit of change a line in the
setup routine rather than a piece of gear left in place.

**One standing coordination item comes with the split.** The venue runs separate
indoor and outdoor PA systems for seasonal use. Which one a given Tuesday lands
on doesn't matter to anybody attending and shouldn't appear in public copy, but
it has to be settled between the venue coordinator and the band's coordinator
beforehand, because it changes where the mixer patches in and how long setup
takes. It's noted here so it joins the agenda of the same conversation as the
calendar entry, instead of being discovered at load-in.

### The partners already exist — the page just doesn't say so

This is the README's second headline problem, and it's worth stating the way the
README now does: the partnerships aren't missing. They're *implicit*. Four
relationships are already doing real work every Tuesday, and not one of them is
visible to anybody who wasn't there.

| Partner | The relationship today | What declaring it is worth | Where it's built |
|---|---|---|---|
| **Shoreline Brewery** | Lead partner — hosts the night, owns the room, provides the PA, and has a following and an events calendar the jam doesn't appear on | A filled Tuesday, and people who eat and drink while they watch; the jam inherits their reach | Co-host + calendar entry, below |
| **The Turn Ups** (house band) | The other visible partner — coordinate and host every week, haul in, set up and tear down the entire backline out of their own gear every week, and bring their own gigging followings | Their names, their other bands and their dates in front of the page's audience every week | Recaps in §6; bio in §1 |
| **Roxy Music** | Band members work and teach there, and some guest bands arrive through its student programs. A genuine pipeline, invisible online | A named partner credit both ways, and the best-targeted audience within reach — people who play and have never sat in anywhere | Below |
| **Guest bands** (New Groove, Catalyst, others) | Turn up with their own material and often their own following, some through Roxy, then leave no trace | Tagged, linked and clipped afterwards, so a visit compounds instead of evaporating | §3 cross-promotion |

The striking thing about that table is that none of it needs negotiating. Three of
the four are people already in the room every Tuesday, and the fourth employs half
the house band. What's missing is the *declaration* — a line in the bio, a co-host
slot on the event, a credit in the weekly post. That's the cheapest work in this
plan and it's most of the answer to the README's second problem.

**Name the partners in public, everywhere.** Concretely, in Phase 1: the bio and
pinned post say who hosts and who backs the night; every event carries Shoreline as
co-host and, if they'll take it, Roxy; the Wednesday recap credits Roxy by name
whenever a student-program act played. An implicit partnership that gets said out
loud every week is what turns into an explicit one — and if a sponsor arrangement
ever happens (below), this is the machinery it plugs into.

### Borrow the brewery's audience

The main **Shoreline Brewery** page reaches far more people than the jam page
does. Two moves follow from that, and together they're the real answer to a stale
follower list:

- Add the brewery page as a **co-host** on every weekly event. A co-hosted event
  shows up on both pages' calendars and in both audiences' feeds — you inherit
  their reach without asking anyone to post anything.
- Get the jam onto `shorelinebrewery.com/events` as a recurring entry, and
  replace that 2018 open mic page. The venue coordinator works the bar and works
  with the house band, so this is one conversation, not a negotiation.

Go into that conversation with the business case rather than a favor to ask. The
jam fills a Tuesday — historically the deadest night a bar has — in a venue whose
food and service are genuinely good. They already put the PA behind it, so this
isn't a request to start supporting the night; it's a request to get credit for
support they're already giving, on surfaces they already own. Every person who comes to play brings the
people who came to watch them, and those people eat. Framed that way, co-hosting
and a calendar entry cost the brewery nothing and protect an evening that already
earns.

### Borrow Roxy Music's audience too

Members of the house band work and teach at **Roxy Music**, and some guest bands
already reach the jam through its student programs. That's a second audience, and a
better-targeted one than the brewery's: a music school's student list is made almost
entirely of people who play a bit, have never sat in anywhere, and would come if
someone they trusted told them it was safe to.

That's the exact person the rewritten bio is written for, and the introduction is
already there — it doesn't need a marketing relationship, just a flyer by the
register and teachers who mention it. Worth asking whether Roxy will take a co-host
slot on the event as well; a music store and a brewery promoting the same Tuesday is
a wider net than either alone.

The student-program pipeline is the part to protect deliberately. A student band
playing its first room outside a recital is the best possible use of this night, and
it's already happening — it just isn't named anywhere. Crediting Roxy in the recap
every time one of those acts plays costs one sentence and gives the store something
to share with the next class of students, which is how a pipeline that currently
depends on individual teachers becomes something the store itself promotes.

### What a sponsor looks like here, and what to ask for

"Sponsor" reads bigger than it is. The realistic version is a local business that
wants to be in front of people who play — Roxy Music first, since the relationship
already exists, but a gear shop, a repair tech, a recording studio or a print shop
all qualify —
and the thing they get is a named line on the weekly posts, the event, and the
pinned post. That's real placement in front of a targeted audience, and it costs
the jam nothing but a sentence.

Two rules keep this from turning into a thing nobody wants to run:

- **Ask for goods and reach, not cash.** A gift card for a raffle, a set of strings
  for a first-timer prize, a stack of flyers by a register, a share from their page.
  In-kind is an easy yes, and it doesn't create an invoice or an expectation of
  reporting.
- **Don't sell an audience you can't yet describe.** The follower count is stale and
  there's no record of any night. This is the second reason the setlist log in §5
  matters: after a season it's the only evidence that this is a continuous,
  well-attended thing, and that's what makes the sponsor conversation easy. So
  treat sponsors as a Phase 3 move, not a Phase 1 one — with the single exception
  of Roxy Music, where the relationship already exists and only needs saying out
  loud.

### What the Page can hold, and what it can't

Worth being concrete about this before writing anything, because it decides where
each piece of the plan lands. A Facebook Page has **no page-within-a-page** — Notes
was removed years ago, and the new Pages Experience took the custom tabs with it.
What's left is a handful of fixed slots, and none of them is a good home for
detail:

| Surface | What it's for | Linkable | The limit |
|---|---|---|---|
| **Intro / bio** | The one-sentence hook | `/shorelineopenjam`, `/about` | Around 100 characters visible before it truncates. Not a place for anything |
| **About** — additional info, hours, address, website and social links | Start time, venue, the canonical link list | `/about` | Almost nobody reads it; search engines and Maps do. Keep it correct, not persuasive |
| **Action button** (*Sign Up*, *Learn More*) | One high-intent click | n/a | You get **one**. It goes to the signup form once §4 exists, and to the jam's own page until then |
| **Pinned post** | The "how a night works" explainer | **Yes — posts have permalinks** | One pinned at a time; ~250 characters before *See more*; no headings, no tables, no clickable anchor text (bare URLs auto-link) |
| **Weekly event** | Week-specific detail, co-hosting, RSVPs | Yes | Needs a login to view — so nothing essential can live only here (see *What was checked*) |
| **Photo album + captions** | The backline, with pictures | Yes | A supplement. Captions are not where anyone looks for logistics |

Two caveats on that table. Facebook renames these controls regularly, and what a
given Page exposes depends on its category and whether it's been migrated to the
new Pages Experience — so find them under *Edit Page info* and the professional
dashboard rather than expecting the labels above verbatim. And the character
limits move; treat them as "shorter than you want," which is the part that never
changes.

The conclusion to carry into the next two sections: **the Page is a router, not a
home.** Every slot above is either too short or too structureless to hold how the
night actually works, which means the detail lives somewhere else and the Page
points at it.

### Pin one post that explains the night

A single pinned post — how a night runs, the slot shape, the songlist link, the
signup link. It's what every "how does this work?" comment gets pointed at for
the next year.

It carries more weight than it looks like it should, because the Page is readable
without an account and events aren't. For anyone who isn't on Facebook — or who
simply isn't logged in when they go looking — the bio and this one post are the
*entire* public face of the jam. Write it so that a person who reads only those
two things still knows the day, the time, the address, what gear is there, and
what happens if they walk in cold.

**Pinning and linking are two different jobs, and this post does both.** Pinning
is discovery — it puts the post at the top for someone who lands cold. The
*permalink* (`facebook.com/shorelineopenjam/posts/<id>`) is the half worth
keeping: copy it the moment the post goes up, put it in the links table above, and
paste it into every event description and every "how does this work?" reply from
then on. It keeps working after the post is unpinned, which makes it the closest
thing this Page has to a static page.

Three mechanics that follow from that:

- **Editing keeps the permalink.** So the explainer is maintained, not replaced —
  which also means it doesn't have to wait for the songlist and signup links. Put
  it up early with the links missing and edit them in.
- **The date doesn't update when you edit.** An explainer still stamped 2026 a
  year from now reads as abandoned, so plan on re-posting and re-pinning roughly
  annually, or whenever the backline or the slot shape changes materially.
- **Pin a comment for anything time-boxed.** "Signups for the 30th are open"
  belongs in a pinned comment on this post, not in its body, so the body stays
  evergreen.

Put the one link that matters on its own line in the first two lines, so it
survives the *See more* truncation.

### The detail needs a URL the Page can point at

Everything above says the same thing from a different angle: there is nowhere on
the Page to put the full version. So one URL has to exist off Facebook, and
everything else quotes it.

**A Google Doc isn't it.** It's the obvious shortcut and it's the wrong one — an
opaque URL nobody can say out loud, a layout that reads as a document rather than
a page, poor on a phone, no branding, no analytics, and it signals *internal* to
exactly the person it's trying to convince. A musician deciding whether to turn up
on Tuesday should not be reading a Google Doc.

**Google keeps the two jobs it's actually good at**, both of them already in this
plan: the **signup form** (§4) and the **published songlist and setlist sheet**
(§5). Those are tabular, edited weekly, and open for logged-out visitors. What
Google loses is the prose job.

**Before provisioning anything, borrow.** The brewery's site already exists and
already has a dead 2018 page carrying this event's name — getting Tuesday onto
`shorelinebrewery.com/events` is free, is the best-placed local link available, and
doubles as the partner declaration. That's the *Borrow the brewery's audience* step
above, and it should happen regardless. It just can't be the canonical URL, because
the CMS, the publishing latency and the willingness to update a changed start time
all belong to somebody else.

So: one page, one owned URL. Not a site.

| Option | Ease of publishing | Flexibility / branding | Cost | The catch |
|---|---|---|---|---|
| **GitHub Pages** off the existing repo | `git push` | Total — it's your own HTML and CSS | Free | Needs git. Hostile handoff to a non-technical successor |
| **Cloudflare Pages** | Git push *or* drag a folder in | Total | Free | One more account |
| **Netlify** | Same, plus form handling | Total | Free tier | The forms tempt you into rebuilding the Google Form |
| **Google Sites** | WYSIWYG, no build step | Low ceiling, but not embarrassing | Free | Sits beside the form and sheet and can embed both inline. Anyone can edit it |
| **Linktree / Beacons** | Instant | None | Free | A link hub, not a page — holds no prose. Stopgap only |
| **Squarespace / Wix / Bandzoogle** | Easy | High | ~$10–25/mo | A monthly bill for a weekly jam with nothing to sell |

**The recommendation: GitHub Pages, and it now exists.** `site/` renders
Markdown into styled pages with no dependencies, and writes them into `docs/`,
which is the folder GitHub Pages serves off `main`. Two pages are up — *About*
and *How it works* — and a deploy is `python3 build.py` followed by a push. The
styling is borrowed from the brewery's own site so the two don't read as
strangers: the orange and navy are sampled off the bowtie logo, and each of
their Adobe Fonts faces is matched to a free equivalent. See
[site/README.md](site/README.md) for how to edit the words and add a page.

**Register a domain either way.** Something like `shorelineopenjam.com`, roughly
$10–15 a year, pointed at whichever host wins. It's the largest branding return
for the least money, and it buys two things a `github.io` address doesn't: it can
be *said from the stage*, and it's portable — when the host changes, or the whole
thing gets handed on, every link already posted keeps working. Settle whose name
it's registered in now rather than later; if this is really a venue-and-band
arrangement, a personal registration is a future ownership conversation.

**It's also the only surface that gets indexed.** Facebook Pages rank poorly in
search now. A real page on a real domain can turn up for "open jam michigan city,"
which is precisely the cold-discovery path the README says is missing. Add
Cloudflare Web Analytics or Plausible while setting it up — free, no cookie banner
— and the question of whether anyone ever clicks the link in the bio stops being
unanswerable.

**The one thing that would change the answer** is the same thing that decides the
rest of this document: can whoever inherits this fix a changed start time without
the person who built it? GitHub Pages fails that as written. Two ways out — keep
every editable word in one Markdown file so the change is one line in the GitHub
web editor, which a semi-technical successor can manage, or take Google Sites and
trade the design ceiling for the fact that anyone can edit it. If a handoff inside
the year is a real prospect, take Google Sites and don't feel bad about it.

---

## 2. Put the weekly event back

This is the spine everything else hangs off. An event isn't just a listing — it's
a reminder that fires on its own, a discussion thread nobody has to moderate,
and, most usefully, a **demand forecast**.

### Create it as a repeating series

Set up the Tuesday event as a weekly recurrence. Facebook has reshuffled
recurring-event support more than once, so if the option isn't where expected,
the fallback works fine: sit down once a quarter and batch-create twelve weeks of
events in about half an hour. Either way you're covered months out.

### Use the RSVPs to fix idle nights *before* they happen

This is the part that solves the README's biggest complaint. On Sunday, look at
who's marked Going:

- **Two or three names?** That's the signal to text the regulars and pull in a
  band — two days early, while it can still change the outcome. The regulars are
  the asset that makes this work: they're already there most weeks, they know
  each other, and a thin Tuesday is exactly the night they can fill.
  This is the move the coordinator and the band are already making, just earlier
  and with a number behind it instead of a hunch.
- **Twenty names?** Publish the slot times in the event so the room knows roughly
  when each act goes on, and the night doesn't burn its first hour on
  coordination.

Neither is possible at 7 PM on Tuesday. The event is what buys the two days.

Once signups are running, read the **mix** and not just the count — twelve people
who want to jam is a completely different night from three booked bands, and only
one of those needs slot times published. §3 is the breakdown.

> **The event thread is the only place followers can talk back.** Since the
> presence is a Page with no Group, the Page's own posts are one-directional by
> design — the event discussion area is the single surface where people can post
> to each other rather than just react. That makes it more valuable here than it
> would be otherwise, and worth actively seeding: ask a question in it on Sunday
> rather than leaving it empty.
>
> It's also a group without the work. It resets clean every week, and nobody has
> to moderate a standing community. If a Group ever comes up, let the event
> threads visibly outgrow themselves first — a Group is a permanent moderation
> obligation, and this plan already depends on one person's twenty minutes.

### Reusable event description

```
Open Jam — every Tuesday, 7:00 PM. Free.
Hosted by Nate Miller & the Turn Ups at Shoreline Brewery.

Backline provided: guitar and bass amps, keys, drums, mics,
mixer, DI, PA. Show up with your instrument and nothing else.
Own pedalboard or amp? Bring it.
Playing to a backing track? Bring your phone — the cable and
the adapters are already at the board.

TONIGHT'S SHAPE
7:00  House band opens
7:40  Solo slots and sit-ins, 15-20 min each
9:00  Band slots

Play your own set, sit in with the Turn Ups, or tell us you're
looking to jam and we'll put you with people.

SIGN UP (optional, walk-ins always welcome) → [form link]
WHAT WE KNOW HOW TO BACK → [songlist link]
EVERYTHING ELSE → [jam page link]

First time? Just come. Tell us at the bar.
```

---

## 3. Four kinds of act

Everything above treats "a performer" as one thing. On an actual Tuesday it's
four things, and they want different enough outcomes that one signup field and
one slot length can't serve all of them.

| Act | What they bring | What they need | Slot |
|---|---|---|---|
| **House band opens** | A set worked out in advance | Nothing — they self-organize a ~30 min set | ~30 min, fixed |
| **Guest bands sit in** (one or more) | Covers or own material, often own following | A clean changeover — backline prep or swaps between sets | Short set |
| **Soloist showcasing** | Own material | A stage — and often a backing track, or the house band behind them | 1–2 songs |
| **Someone who wants to jam** | Willingness to play with anyone | To know what the room can cover, and who else is up | Variable |

Three things follow from that table, and each one changes something concrete
later in this plan.

The categories leak, and the leak is worth designing for. A showcasing soloist
may arrive self-contained with a backing track, or may ask the house band to
cover them — same act type, opposite requirement, and the host can't tell which
until they ask. So the question that matters isn't really *what kind of act are
you*, it's **what do you need behind you**: nothing, a track through the PA, or
the band. Ask that one directly and the other four-way distinctions mostly sort
themselves out.

### There's a cross-promotion trade sitting unused

This is the guest-band row of §1's partnership table, and it's the one that comes
back around every single week. Some of these acts are already repeat visitors —
New Groove, Catalyst, players from both — and some arrive through Roxy Music's
student programs, which makes each one a partner touch as well as an act.

Guest bands and showcasing soloists arrive with their own material and often some
of their own following. Why they come isn't knowable from here and doesn't need
to be — by all accounts the nights are a good time, and guessing at anyone's
motives would be a poor foundation for a plan anyway.

What *is* visible from the coordinator's chair is an unused quid pro quo. They
bring people through the door; the page can put them in front of its audience
afterwards. Both sides gain and neither has to have planned it that way, which is
what makes it worth building into the routine rather than leaving to whoever
remembers.

In practice that's one habit and one form field. Collect a link to each act's own
page on the signup form, and make sure the Wednesday recap tags them, spells the
name right, and links back. An act that got tagged, linked, and clipped has a
reason to come back and bring people; an act that played to a room and vanished
doesn't. That's the difference the recap is actually making.

### Backing tracks are a decision, not a purchase

"Sometimes they play to a backing track" sounds like a gear problem and isn't —
the board already takes a cable, Bluetooth or USB, and there's a venue PA behind
it. Nothing needs buying. The friction is that the track lives on the performer's
own device, which has to be connected for their slot and disconnected again for
the next one. Every act carrying a track is its own handoff, done on stage, while
the room waits.

None of it needs anyone's approval either: the board belongs to the house band,
so this is a decision they can simply make and then publish.

**Make the cable the standing answer.** Bluetooth has to drop the previous
performer's phone before it will take the next one, and that renegotiation is the
part that happens in front of the room. A cable doesn't: it's the same two
seconds for everyone, and it can be sitting there before the player is. Either
3.5mm into a TRS line channel, or 3.5mm into the DI and out on XLR — whichever
channel gets picked, it stays that channel every week.

Three details decide whether this actually works.

**Make it a line in the setup routine, not an installation.** The whole backline
goes home at the end of the night, so there is no taping a cable down once and
forgetting it. What there is instead is a setup that already happens every
Tuesday and can absorb one more item — the cable goes in when the mixer does, on
the same channel it had last week.

**Bag the cable and its adapters as one thing.** Most phones no longer have a
headphone jack, and a performer who brought a track but not a dongle is exactly
the stall this is meant to prevent. A USB-C and a Lightning adapter taped to that
cable means the three travel as a single unit and can't be separately forgotten
at 5pm on a Tuesday.

**Keep Bluetooth as the stated fallback**, because some device will refuse the
wired path.

One thing that helps here: the channel is on the band's own mixer, not the
room's. It survives the teardown, and it stays the same answer whichever of the
venue's two PA systems the night is running through.

Then the part that actually pays: write it into the bio and the event
description, along with what the performer does at their end — track downloaded
rather than streamed, notifications off, device volume up. A soloist who can see
in advance that their track will play is a soloist who signs up instead of
wondering. Ask on the form whether an act is bringing one, so the connection gets
made during the previous act instead of after it.

### The jammers are the group nothing currently serves

The other three types arrive self-contained — the house band has its set, the
guest band has its material, the soloist has their own songs. The fourth type
arrives wanting to be combined with other people, and there is currently no
mechanism for that at all beyond whoever happens to be standing nearby.

This is the group the **songlist** exists for, and the reason the form should ask
what someone plays rather than only what they want to play. If three people sign
up wanting to jam and one of them is a drummer, that's a band — but only if
somebody notices in advance. That noticing is a job, and it belongs to whoever
owns the list.

---

## 4. Signups

> **One expectation to reset first.** The README lists "Facebook integration
> (songlists/signup lists)" as a goal. Facebook has no native signup-sheet or
> setlist feature, and building one against their API isn't worth it: posting to a
> Page programmatically requires app review plus business verification, and with
> no Group in the picture that Page path is the only one there is. That's weeks
> of paperwork to automate three posts a week. **Link out to a tool instead** — the friction is a
> single tap and you keep full control.

### Start with a form and a sheet

A Google Form feeding a Sheet is free, needs no account from the person signing
up, and works on a phone in a loud room. The sheet *is* the running order — the
host sorts it and works down the list. Publish it read-only and link it from the
event.

Think of the sheet as the existing conversation with a memory. Most of what goes
in it is already being said somewhere — in a text thread, at the bar, between sets.
The form just gives that information one place to land where it outlives the
conversation and where someone who wasn't in the thread can read it. Which also
means the sheet shouldn't replace the talking: that's how a jam gets organised, and
it should carry on exactly as it does. The sheet is the write-down, not the
substitute.

The fields that actually matter:

- Name or act name
- **What do you need behind you?** — nothing, I'm self-contained · a backing
  track through the PA · the house band · put me with other players. This is the
  field that does the most work, and it's a better question than "what kind of
  act are you," because a soloist can answer any of the four
- What you play (instrument / voice) — needed to match up the jammers
- How many players
- Anything you need beyond the standard backline, and whether you're bringing
  your own amp or pedalboard (so there's room and a channel for it)
- **Playing to a backing track?** If so, what it plays from — phone, laptop —
  and whether it has a headphone jack or needs an adapter. Default answer is the
  house cable; Bluetooth on request
- Two or three songs you'd like to play — **with keys**
- **A link to your page**, if you have one, so the recap can tag you properly
- First time here? (yes / no)
- Roughly when you'll arrive

> **Protect the walk-ins.** A jam that requires a form stops being a jam. Hold
> roughly half the slots for people who wander in — the form is there to *reduce*
> uncertainty, not to become a gate. If a regular ever feels they need a phone to
> play, the tool has started working against the night.
>
> **And protect the on-the-fly part.** Working out what to play in the moment
> isn't friction to be engineered away — it's a good part of what people come
> for. So a signed-up act's three songs are a starting point, not a contract, and
> nobody owes the sheet a performance of what they wrote down on Sunday. What the
> form removes is uncertainty about *whether and when you play*. What happens
> once you're up there should stay improvised.

### Print the slot shape

The README's sharpest observation is that guests have no idea when they'd play.
That's answered by publishing a rough structure, not by scheduling to the minute.
Even an approximate shape in the event description — house band opens, then 15–20
minute slots, bands later — tells someone whether to order another beer or go
home and come back.

---

## 5. Setlist tracking, split in two

"Setlist tracking" is really two different artifacts, and conflating them is the
usual reason neither one ever gets built. They have different audiences,
different update rhythms, and different value.

### The Songlist — what the house band can back you on

This is the single most valuable thing on the list, and it's the direct fix for
"newcomers have no idea what is typically played." It's a standing document, not
a log: the repertoire the Turn Ups can drop into behind a stranger. Fifty to a
hundred songs is plenty.

It answers a more specific question than "what gets played here," and that's the
question worth designing around: **can you back me on this?** A newcomer arrives
with a song in mind and currently has no way to find out whether the house band
knows it until they're standing at the mic asking. The songlist turns that into
something they can check from the parking lot.

The answer is useful to them whichever way it comes out, and that's the part
worth noticing. A soloist who finds their material on the list can leave the
tracks at home and be backed by a band. One who doesn't find it knows to bring
the track and the device — a decision far better made on Sunday than at the mic.
Paired with the form's *what do you need behind you*, the whole question of what
stands behind an act is settled before anybody arrives, which is the same ten
minutes of stage time §3 was trying to buy back.

Note which of the four acts it's for. A guest band and a showcasing soloist
arrive with their own material and will never open it. It's built for the sit-ins
and the jammers — which is precisely the group that currently has the least to go
on, so the narrow audience is the point rather than a limitation.

| Song | Artist | Key | Feel | Backing | Notes |
|---|---|---|---|---|---|
| Mustang Sally | Wilson Pickett | C | Shuffle | Full band | Everyone knows it. Good first-timer song. |
| Ain't No Sunshine | Bill Withers | Am | Slow soul | Full band | Works for a solo singer too. |
| Folsom Prison Blues | Johnny Cash | E | Train beat | Guitar + drums | Easy sit-in. |

*Illustrative rows — the real content has to come from the house band. The schema
is the point.*

**Key is the field that decides whether a sit-in works.** A singer who knows the
song is in C and the band plays it in C walks up confident; without it, everyone
finds out on stage. The **Backing** column matters nearly as much — it tells a
newcomer whether they get a full band, a rhythm section, or just a stage.

**Say plainly that the list is a floor, not a ceiling.** This band reads and uses
functional theory and adapts to whoever is in front of them, which means their
real range is much wider than any fifty rows — give them a key, a feel and a form
and they can follow a song nobody wrote down. If the list is published without
saying so, it quietly becomes a *restriction*: a newcomer scans it, doesn't find
their song, and concludes the answer is no.

So publish it with one line at the top — *this is what we can drop into cold; if
your song isn't here, ask anyway, just bring the key and the changes* — and the
same document that reassures the cautious stops turning away the rest. That
sentence costs nothing and prevents the most likely way this artifact backfires.

**Let the regulars add to it, too.** The house band isn't the only thing backing
people up — the regulars who sit in cover plenty between them, and that goes
unrecorded. Giving the sheet a "who can play this" column, or simply letting
regulars append rows, makes the list describe what the *room* can cover rather
than just what the Turn Ups can. It also costs nothing: the people who'd fill it
in are there every Tuesday anyway.

They're the right people to own it for a second reason. The regulars are what
makes the night feel continuous — same faces, established rapport, the
good-natured needling that tells a newcomer this is a room with a history. A
songlist maintained by the people who actually show up every week stays current
in a way that one maintained by whoever set up the spreadsheet does not.

### The Setlist Log — what actually got played

Date, song, who played it. One tab in the same sheet. It does three jobs: it
writes the Wednesday recap post for you, it shows a prospective player what the
room actually sounds like, and after a year it's the evidence that this is a
real, continuous thing rather than an open mic that happens sometimes.

The capture method decides whether this survives, so keep it to five minutes. The
host or coordinator types into the sheet between acts, or photographs the paper
signup sheet and types it up Wednesday morning. Consistency beats tooling here by
a wide margin — a log that's always a day late is infinitely more useful than a
beautiful system nobody fills in.

---

## 6. The weekly rhythm

Three posts a week, each one tied to the event. That's the whole content engine —
small enough to survive a busy month, which is the only test that matters.

Facebook is where the week-to-week rhythm lives, but it isn't the whole presence.
The brewery's calendar entry (§1) is the other standing surface, and it's the one
that reaches people who will never look at a Facebook page — so when the start time
or the format changes, it changes in both places on the same day.

| When | What |
|---|---|
| **Sunday** | **Reminder, and read the room.** Post the reminder, then check the RSVP count. Thin? Start texting regulars now. Heavy? Draft the slot times. |
| **Tue PM** | **Day-of post.** Signup link, tonight's shape, anything special — a visiting band, a theme, a birthday. |
| **During** | **One photo, one clip, the songs.** A 30–60 second clip is enough. Jot song titles as they go by; that's the log. |
| **Wednesday** | **Recap — and tag everyone.** The clip, the night's setlist, and every performer tagged by name and linked to their own page. Tag the partners too: Shoreline every week, and Roxy Music whenever one of their student-program acts played. Tagging is the growth engine: it puts the jam in front of each player's friends, which is exactly the audience a stale follower list is missing. It's also the page's half of the cross-promotion trade (§3) — the reason an act comes back and brings people. |

---

## 7. Rollout

Doing all of this at once is how it stalls. Each phase should be running on its
own before the next one starts.

**Phase 1 · This week — make it correct**

- Settle the start time
- Rewrite the bio — lead with the full backline, "bring your instrument, that's it"
- Settle how a backing track gets connected, and say so publicly
- Name the partners in the bio and pinned post — Shoreline, the Turn Ups, Roxy Music
- Ask Roxy Music about a flyer, a mention from the teachers, and a co-host slot
- Create 12 weeks of events
- Add the brewery as co-host
- Get on the venue calendar, and replace the 2018 open mic page

**Phase 2 · Weeks 2–3 — open signups**

- Register the domain and publish the one-page explainer (§1)
- Point the bio, the pinned post, the action button and every event at it
- Build the form and sheet, with the four act types as the first question
- Link it in every event
- Announce it from the stage — twice a night, every night
- Keep walk-in slots open
- Start pairing up the people who signed up wanting to jam

**Phase 3 · Week 4+ — build the record**

- Publish the songlist
- Start the setlist log
- Wednesday recaps with tags and links back to each act's own page
- Re-pin the "how it works" post with the links filled in — the permalink
  survives the edit, so it can go up in Phase 1 without them
- Once there's a season of log to point at, open the sponsor conversations (§1)

---

## The thing that actually decides this

None of the above is hard. It's roughly twenty minutes a week once it's set up.
But it needs **one named person** who owns the cycle — posts Sunday, posts
Tuesday, posts Wednesday, keeps the sheet current.

Split across three well-meaning people, this fails within a month; that's the
actual failure mode here, not the tooling. Before building anything, settle who
that person is. If the answer is nobody, then the honest version of this plan is
just Phase 1 — fix the bio, fix the time, batch the events, get co-hosted — and
stop there. Phase 1 alone still meaningfully improves the page, and it doesn't
need a weekly owner.

One encouraging note to end on. Somebody is *already* doing an unrecorded version
of this job every week — the planning behind a Tuesday doesn't happen by itself. So
the question isn't whether anyone here will do weekly coordination; that's settled,
and the answer is yes. It's only whether the writing-down gets attached to the
person already doing it, or handed to someone else who then needs looping in. The
first is a small change to an existing habit. The second is a new habit, and new
habits are what fail.
