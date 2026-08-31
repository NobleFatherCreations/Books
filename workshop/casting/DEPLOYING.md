# Deploying — and moving this site anywhere

The site is plain static files: HTML, CSS, JavaScript and images. There is
no build step, no server, no database, and **no dependency on any
particular host**. Whatever you copy, works.

That is deliberate. An earlier version generated image URLs through
Netlify's image-transform endpoint (`/.netlify/images?url=…`), which is a
slightly nicer pipeline but silently ties the site to one provider — every
photograph 404s the moment it is hosted anywhere else. Every size is now a
real file on disk, referenced by an ordinary path.

## What actually has to be uploaded

Everything except the working folders:

```
statues/          the gallery + one folder per piece
assets/           css, js, and all images
data/             the JSON the gallery reads
sitemap.xml
robots.txt
index.html        (whatever else lives at the site root)
```

Not needed on the server: `incoming/`, `scripts/`, `node_modules/`,
`package.json`. Those are the workshop, not the shop.

## Moving it to another account or host

Nothing has to change in the code. Pick whichever suits you:

| Host | What to do |
|---|---|
| **Netlify** (any account) | Connect the repo, or drag the folder into the deploys page. Build command empty, publish directory `.` |
| **Cloudflare Pages** | Connect the repo. Build command empty, output directory `/` |
| **GitHub Pages** | Push to the repo, enable Pages on the branch root. See the note below |
| **Vercel** | Import the repo, framework preset "Other", no build command |
| **Plain web server / S3** | Upload the folders above. Any server that serves files will do |

The only thing worth checking after a move is `data/site.json` — the `url`
there is used to build absolute `og:image` URLs for link previews. Change
it to the new domain and run `npm run pages` to regenerate.

### If the site is not at the domain root

Everything is referenced with root-relative paths (`/assets/…`,
`/data/…`), which assumes the site lives at `example.com/`, not at
`example.com/some-folder/`. GitHub Project Pages serve from a subfolder by
default, so either use a custom domain, use a User/Org Pages repo, or
serve from the root.

## Netlify specifics

`netlify.toml` only sets caching headers and pretty URLs. It is
**optional** — delete it and the site still works, you just lose the cache
tuning. Nothing in it is required for images to render.

## Regenerating after any change

```bash
npm run ingest     # process new photos from incoming/
npm run pages      # rebuild per-piece pages, social cards, sitemap
npm run validate   # check nothing is broken before pushing
```

Then commit and push. Whatever host is watching the repo redeploys, or you
re-upload the folder by hand.

## Image weight

Three WebP renditions per piece (600 / 1200 / 2000px), roughly 1.3 MB per
statue in total. At 150 pieces that is about 200 MB, at 500 pieces about
650 MB — comfortable for git, since these files are written once and never
edited. If it ever does become a problem, move `assets/images/` to object
storage and rewrite the paths in `data/statues.json`; nothing else in the
site needs to know.
