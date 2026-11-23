# "Who made this" on every page: easy to find wherever someone lands

**The aim.** A reader can land on any page of any book (usually from Google or a Facebook share, deep inside a chapter) and find out who made this in **one tap**. It never pushes, never pops up, and never gets in the way of someone in crisis.

**One source.**
- The text lives in `content/about.md` (the full page and the short version).
- The one-liner and the link live in `site_manifest.json`.
- Every builder reads them, so the wording is identical everywhere, and one edit updates all sites at the next rebuild.

---

## The seven touchpoints (from most to least visible)

### 1. The `/about` page itself (one home)
- **URL:** `noblefathercreations.com/about`. Add the aliases `/who-made-this` and `/author` as 301s in `hub/catalogue-redesign._redirects`.
- **Built by** `scripts/seo/build_about.py` from `content/about.md`. Ships with the homepage.
- **Design:**
  - The brand header as the hero.
  - The wordmark image in the signature.
  - Type: Gloock display, Newsreader body, Space Mono labels, all self-hosted.
  - Phone-first and AA. The Leave button stays.
- **Ends with:**
  - "My only ask": a native share button, plus copy-link.
  - "Tell me how it helped": the feedback box (03 B1) or the owner's social links.
- **Schema:** `AboutPage` + `Person` (Shae Stovell, `sameAs` = TikTok plus Facebook and Instagram once sent) + `Organization` (Noble Father Creations).

### 2. The seal menu (Catalogue drawer): on every page of every site already
- Add one row at the top or bottom of the drawer: the small figure mark, then "Who made this" → `/about`.
- The drawer is already on every page, so this is the single change that reaches everywhere.
- **Built by** `scripts/nf-catalogue-sweep.py`.
- **Deploy caution (02, incident 1):** it touches every site. List them and ask the owner site by site, or ride along with each book's next real deploy.

### 3. The byline under every chapter title
- **Today** chapters show "Last reviewed …". Make it: **"By Shae Stovell · Last reviewed 23 Nov 2026"**, with the name linking to `/about`.
- This is where search readers' eyes already are, and Google reads a visible byline as experience and authorship.
- **Safety books** (Long After, Silence, Repair, Slow Take, Feminine, At Will): text only, no photo or figure, so it stays discreet on a shared screen.

### 4. The end-of-chapter author strip (the colophon line)
- After the chapter's last section and the handoff line, one quiet line: **"Made by Shae Stovell, a father who needed this map and couldn't find one. [Who made this →]"**.
- On books with room (Festie, Fractal, Feminine, the Decoder About page), use the 90-word short version from `content/about.md` with the small figure mark.
- Next to it, the share line from "My only ask": **"Know someone who needs this? [Share]"** (`navigator.share`, nothing stored).

### 5. Each book's own About or colophon section
- Every book has an About, colophon or updates section (CLAUDE.md patch notes). Put the short version there in full, with the wordmark and the link.
- **Playground Protectors:** a version for parents only, in the parents' notes, not in the kids' pages.

### 6. The homepage
- The short version as a calm section near the end ("Someone once studied the way I love…" → Read why).
- Plus "Who made this" in the footer.
- Built through `build_home.py`. Deploy on "deploy the homepage".

### 7. Machines: search, AI and share previews
- **JSON-LD:** every Book and Chapter gets `author: {"@type":"Person","name":"Shae Stovell","url":".../about"}`. The hub carries the full Person and Organization with `sameAs`.
- **llms.txt** (hub and Decoder): a "Who made this" line plus the `/about` link.
- **Share cards** already carry "Shae Stovell · Noble Father Creations" and the brand figure.
- **Result:** "who made the Pattern Decoder" and "who is Shae Stovell" get the right answer in Google and AI tools, and it builds toward a Knowledge Panel.

---

## The rules for every touchpoint
- **One tap from anywhere:** the drawer row, the byline name and the end strip all go to `/about`.
- **Never in the way.** No pop-ups, no sticky banners, nothing above the chapter text except the byline. Crisis pages (`if-youre-not-safe-right-now` and the like) show only the byline.
- **No helplines in the bio.** They stay where they belong, in the books.
- **Nothing stored and no tracking.** The share button and the feedback box keep that promise.
- **The wordmark image, never a font imitation.**
- **The same words everywhere,** from the manifest. Never retyped per book.

## Build order (cheapest reach first)
1. `/about` page, plus the footer link and homepage section. One homepage deploy.
2. JSON-LD `author` and llms.txt lines. These ride with each book's next deploy.
3. The drawer row (one sweep). Deploy site by site **with the owner's yes for each**, or batch it with the next real deploy of each book.
4. Byline and end-of-chapter strip: added to the shared book shell, first in The Long After v6, then The Silence, then each book as it gets its round.
