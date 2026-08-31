# incoming/

Drop raw photographs here, then run `npm run ingest`.

Nothing in this folder is committed to git — it is your working drop zone,
and the originals stay on your machine and in Google Drive.

## Sorting by theme

Put photos in subfolders and the folder name becomes the category:

```
incoming/
  dragons/          → category "dragons"
    NFC-0001_front.jpg
    NFC-0001_back.jpg
  memento-mori/     → category "memento-mori"
    raven-skull_front.jpg
    raven-skull_detail.jpg
  IMG_4821.jpg      → no folder, lands in New Arrivals
```

## Naming photos

**Naming does not matter.** One photo per statue is the default, so every
file becomes its own piece with the next id in sequence. `IMG_4821.jpg`
off a phone is fine.

The one case where the name is meaningful: call a file after an existing
piece — `NFC-0007.jpg` — and it attaches to that piece rather than creating
a new one. That is how you swap in a better photo later.

To photograph a piece from several sides instead, see `--group` in the main
README.

Accepted formats: jpg, jpeg, png, webp, tif, tiff, heic, heif, avif.

Once ingested, photos can stay here — re-running is safe and will not
duplicate anything.
