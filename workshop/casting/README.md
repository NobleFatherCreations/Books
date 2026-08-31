# Noble Father Creations

Portfolio site for the hand-poured eco-resin collection.
The gallery lives at **`/statues`** and is built in the same visual
language as [The Portals](https://nfcportals.netlify.app/).

---

## The short version

```bash
npm install                 # once, on your machine

# 1. drop photos into incoming/, ideally in folders named by theme
# 2. process them
npm run ingest

# 3. tell the site what they are
npm run assign -- --range NFC-0001..NFC-0050 --category dragons --label "Dragons"

# 4. see it
npm run serve               # → http://localhost:8080/statues

# 5. publish
git add -A && git commit -m "Add 50 pieces" && git push
```

Netlify redeploys on push. There is no build step.

---

## How the site is put together

```
statues/index.html        the gallery — grid, filters, lightbox
data/statues.json         every piece: the single source of truth
data/categories.json      the category vocabulary (starts empty)
assets/css/theme.css      all colours, fonts and spacing, as CSS variables
assets/css/statues.css    gallery + lightbox layout
assets/js/                store / gallery / lightbox
scripts/                  the ingest and category tools
incoming/                 drop zone for raw photos (never committed)
```

Two rules make the whole thing maintainable:

1. **No category name appears anywhere in the HTML or JavaScript.** The
   filter buttons, the drawer index and the section headings are all
   generated from `categories.json` at page load. Naming a new category
   is a data edit, never a code edit.
2. **Every colour and font lives in `theme.css`** as a CSS variable, copied
   from the portal. Restyling the gallery means editing that one file.

---

## Naming your photos

**One photo per statue is the default, so naming does not matter.** Every
file in `incoming/` becomes its own piece, gets the next id in sequence,
and nothing is grouped or guessed. `IMG_4821.jpg` straight off a phone
works exactly as well as a carefully named file.

Name a file after an existing piece — `NFC-0007.jpg` — and it attaches to
that piece instead of creating a new one. That is how you replace or
improve a photo later.

<details>
<summary>If you ever photograph a piece from several sides</summary>

Pass `--group` and filenames are used to group angles together:

```bash
npm run ingest -- --group
```

```
NFC-0001_front.jpg
NFC-0001_back.jpg     →  one piece, id NFC-0001, three angles
NFC-0001_left.jpg
```

Recognised angle words: `front`, `back`, `left`, `right`, `side`, `top`,
`detail`, `closeup`, `profile` and similar. The gallery already supports
multi-angle pieces — an angle strip appears in the viewer automatically
whenever a piece has more than one photo.

Do **not** use `--group` for one-photo-per-statue work: it would read
`dragon-1.jpg` and `dragon-2.jpg` as two angles of a single statue rather
than two separate statues.
</details>

### Folders become categories

Anything in a subfolder of `incoming/` is filed under that folder's name:

```
incoming/dragons/NFC-0001_front.jpg      →  category "dragons"
incoming/memento-mori/skull_front.jpg    →  category "memento-mori"
```

The category is registered in `categories.json` automatically. **This is
the fastest way to sort a large drop by theme** — make folders in Google
Drive, download, run ingest. Turn it off with `--no-folder-categories`.

---

## Sorting pieces into categories

Everything is `npm run assign -- <options>`. Add `--dry-run` to preview.

```bash
# by id range
npm run assign -- --range NFC-0001..NFC-0050 --category dragons --label "Dragons"

# by specific ids
npm run assign -- --ids NFC-0007,NFC-0012 --category skulls

# by the folder they were ingested from
npm run assign -- --folder dragons --category dragons

# everything not yet filed
npm run assign -- --uncategorized --category new-work

# see where things stand
npm run categories
```

Renaming and describing categories, without touching code:

```bash
npm run assign -- --rename dragons:wyrms
npm run assign -- --label wyrms "Wyrms & Dragons"
npm run assign -- --describe wyrms "Long-necked pieces, poured spring 2026."
npm run assign -- --unassign NFC-0003          # back to New Arrivals
npm run assign -- --clear-review NFC-0001..NFC-0020
```

**Pieces with no category are never hidden.** They collect in a
**New Arrivals** filter, always rendered, always reachable.

---

## Filling in titles and descriptions

Open `data/statues.json` and edit. `title`, `description`, `tags` and
`category` are all safe to change by hand; `id` and `angles` are written by
the ingest script and should be left alone. Then:

```bash
npm run validate
```

which catches duplicate ids, missing image files, categories that don't
exist, and malformed JSON before you push.

---

## Running it again is safe

Every source photo is recorded in `data/.ingest-manifest.json` by content
hash. Re-running `npm run ingest` on the same folder does nothing — even if
you renamed the files in between. Adding a new angle to a piece that
already exists appends the angle rather than creating a second entry. You
can leave photos in `incoming/` indefinitely.

---

## Deploying

Netlify is configured by `netlify.toml`:

- **Build command** — none (`echo`). The gallery reads its JSON in the
  browser; there is nothing to compile.
- **Publish directory** — `.` (the repo root).
- `/statues` and `/statues/NFC-0001` both serve the gallery; the second
  opens that piece straight into full view, so any piece can be linked or
  shared.
- `data/*.json` is served `must-revalidate` so new pieces appear the moment
  you push. Images cache for a year.

`sharp` is only needed to run the ingest script on your own machine.
Netlify never installs it.

Image masters are committed to the repo and resized on request by Netlify's
Image CDN — about 313 MB for 500 pieces. [IMAGES.md](IMAGES.md) has the
full reasoning and the migration path if the collection ever outgrows that.

---

## Viewing a piece

Click or tap any card to open it full-screen.

- **Desktop** — arrow keys or the on-screen arrows move to the next
  *piece*, so you can browse the whole filtered collection without closing
  the viewer. Click the photo to zoom to 2.2x and move the mouse to pan
  around it. `Esc` closes, as does clicking beside the photo.
- **Phone** — swipe left and right between pieces, swipe down to dismiss,
  pinch to zoom the photograph itself.

The viewer shows the grid thumbnail blurred straight away, then fades the
full-resolution photograph in over it, so it never opens on an empty frame.
The browser picks its own image size from the available widths, so a phone
never downloads a 2560px file. On desktop the full-size image starts
downloading on hover, before you click.

Thumbnails are lazy-loaded and the grid pages in as you scroll, so a
collection of several hundred pieces still opens instantly.

## Where images come from

`data/statues.json` stores one master path per photo. Every size the site
requests is built at runtime in `assets/js/images.js`, which means
thumbnail and full-view dimensions can be changed at any time without
re-processing photographs, and moving to a different image host is an edit
to one object in that file.

`npm run serve` emulates Netlify's Image CDN locally using sharp — including
picking AVIF or WebP from the browser's `Accept` header — so the preview
behaves like the deployed site.

**See [IMAGES.md](IMAGES.md)** for the hosting decision, the size
arithmetic, and why Google Drive is the wrong place to serve from.
