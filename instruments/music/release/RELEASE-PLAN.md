# The Listening Room → Streaming: Release Operations Plan

Prepared 2026-10-08 from the actual catalog, not a hypothetical one.

**What the catalog actually is.** The audio comes from the Drive folder *MP3 music*
(`14TecSqJSZOlYlT7bHPsKqBdHsGdUC0ea`, plus its `dad` and `New` subfolders) and is
already catalogued in `instruments/music/MANIFEST.json`. That manifest is the data
behind the Listening Room page on the website.

| Fact | Number | Source |
|---|---|---|
| Files in Drive today | 272 audio (274 entries incl. 2 folders) | public folder listing, today |
| Distinct recordings | **177** (176 in manifest + *The Fourth Position*, added 2026-09-17) | Suno IDs in ID3 tags |
| Distinct *songs* after collapsing takes/versions | **~155** (139 single-take + 16 songs with 2–3 takes each) | `MASTER-RELEASE-SHEET.csv` |
| Total runtime | 14 h 50 m; median 4:43; shortest 2:01; 11 tracks over 8 min | ffprobe |
| Created in Suno | 2026-06-30 → 2026-08-08 (152 of them in July) | ID3 comment |
| Audio format | MP3, ~175–220 kbps VBR, 48 kHz stereo | measured |
| Loudness (12-track sample, 2 per shelf) | **−12.0 to −14.5 LUFS integrated** | ffmpeg ebur128 |
| True peak (same sample) | −2.7 to **−0.2 dBTP**; 4 of 12 above −1.0 | ffmpeg ebur128 |

The Listening Room already sorts the songs into six **shelves**. Each one works as a
ready-made album concept: The Reckoning (39), The Descent (23), The Frequency (38),
The Dragon Cycle (10), The Festival Floor (52), The Tender Room (14).

Files in this folder:
- `MASTER-RELEASE-SHEET.csv`: all 177 recordings, pre-filled, with flags
- `build-release-sheet.py`: regenerates the sheet from the manifest
- `qc.sh`: free loudness and true-peak QC for any folder of masters, before or after Mixea

---

## 0. Before anything is uploaded: three gates

These carry more risk than any rollout question. Clear all three first.

**Gate 1: commercial rights to each Suno song.** Suno grants commercial rights only
for songs generated *while you held a paid plan* (Pro/Premier). A free-tier song
stays non-commercial even if you upgrade later. Your songs were made between
2026-06-30 and 2026-08-08. Check your Suno billing history against those dates, and
fill in the `Suno Plan At Creation (verify)` column. Suno's terms have also been
changing since its 2025 label settlements, so re-read the current terms on the day
you start. Distributing a song you don't hold rights to is the fastest way to have
an account terminated, and termination takes the whole catalog down with it.

**Gate 2: get WAVs, not MP3s.** Every file in Drive is an MP3. The biggest quality
upgrade you can make is free: re-download each keeper from Suno as **WAV** (paid
plans offer it). Mastering cannot restore what MP3 encoding already threw away, and
the stores re-encode whatever you send them. MP3 → AAC/Ogg is lossy on top of lossy.
WAV → AAC is one generation. The `Suno ID` column gives you the exact song to find
in your Suno library.

**Gate 3: one artist name, decided once.** Before release 1, search the name on
Spotify, Apple Music and YouTube. If another artist already uses it, your songs will
be mis-mapped to their profile, which is the most common new-artist disaster. The
name you upload with on day 1 is the name every later release must match exactly,
character for character.

---

## 1. Rollout strategy for ~155 songs

### What actually triggers spam flags

Distributors and DSPs don't penalise volume as such. They flag *patterns*:
- many near-identical tracks
- the same song under multiple titles
- very short tracks built to farm streams
- keyword-stuffed titles
- artist names that imitate real artists
- huge dumps with no listening behind them

Spotify's 2025 AI policy added a spam filter for exactly these patterns, plus an
impersonation ban and AI-credit disclosures. Your catalog has two real risks here:

1. **Multiple takes of the same song.** There are 16 groups, such as *Going Pink
   Fishin* v1 and v2, *Wizard … Potter* three ways, and *Goose Juice Groove* three
   ways. Releasing several takes as separate tracks is the textbook duplicate-content
   flag. **Release one take per song.** The sheet marks these with `Duplicate Group`
   and `multiple takes - choose one`. Listen, then set `Keeper` to Y on exactly one
   per group.
2. **Volume with no audience yet.** Since 2024, Spotify pays nothing on a track with
   fewer than 1,000 streams in 12 months. 155 songs released at once means ~155
   tracks each splitting a tiny audience, with most of them earning $0. Concentrating
   attention is a revenue decision, not just a marketing one.

### The three formats compared

The Spotify/Apple format rules decide what counts as what:
- **Single:** 1–3 tracks, each under 10 min.
- **EP:** 4–6 tracks totalling under 30 min (or 1–3 tracks with one over 10 min).
- **Album:** 7+ tracks or 30+ min.

Most of your songs run ~4–5 min, so a "4-track EP" lands around 18–20 min and still
counts as an EP.

| | 10-track thematic LP | 4-track EP | Single-a-week waterfall |
|---|---|---|---|
| Fits your catalog | ✅ Shelves are already albums (Dragon Cycle = exactly 10) | ✅ Good for the 14-song Tender Room or Descent sub-themes | ⚠️ 155 weeks ≈ 3 years |
| Algorithmic reach | One Release Radar push for 10 songs; deep cuts get little | Moderate | ✅ Every release = new Release Radar + editorial pitch slot |
| Editorial pitch | 1 pitch per LP | 1 per EP | 1 per single |
| Spam risk | Low | Low | Low *if* the songs are distinct. Weekly cadence is normal |
| Workload | Low (art + metadata once) | Medium | High (weekly art, promo, pitching) |
| Stream concentration | Diluted across 10 | Better | ✅ Best |
| Audience fatigue | Low | Low | Higher for a small audience |

### Recommendation: a "chapter" waterfall, one shelf at a time

Each shelf becomes a chapter:
1. Release single A, 2 weeks later single B, 2 weeks later single C.
2. Two weeks after that, release the full shelf album. It **includes A, B and C with
   their original ISRCs**, so their streams, saves and playlist adds carry over
   instead of resetting.
3. Rest 2 weeks, then start the next chapter.

That gives you something new every two weeks, with three editorial pitches and one
album moment per chapter. Each chapter takes about 10 weeks, so all six run about 60
weeks.

Big shelves split into volumes of no more than ~15 tracks (a 39-track album buries
everything):
- The Reckoning → Vol. 1 / Vol. 2 (39 songs)
- The Frequency → Vol. 1 / Vol. 2 (38 songs)
- The Festival Floor → Vol. 1 / 2 / 3 (52 songs)

Run the chapters in this order:
1. **The Dragon Cycle** (10). Most cohesive, already album-sized, lowest
   explicit/trademark risk. It's the right first impression.
2. **The Tender Room** (14). Broadest appeal.
3. **The Descent** (23 → one LP of the best 12–15).
4. **The Frequency** Vol. 1.
5. **The Reckoning** Vol. 1.
6. **The Festival Floor** Vol. 1. Last, because it has the most explicit and
   trademark flags to clean up first.

**Curate ruthlessly.** Release your best ~100 in year one and keep the rest in the
Listening Room on your site as a "vault" exclusive. A smaller catalog of songs that
each pass 1,000 streams earns more than a large one that mostly doesn't.

**Waterfall mechanics in DistroKid.** When you build the album, add the
already-released single by entering its **existing ISRC** in that track's ISRC field.
Use the same audio file and the exact same title, or the stores treat it as a new
recording.

### How DistroKid maps to each platform

DistroKid sends every release to every store you tick. Each store builds its own
artist profile from the **artist name you type** plus the **store artist ID**
DistroKid asks you to confirm. Getting that ID right on release 2 is what keeps the
catalog unified.

| Platform | What DistroKid delivers | Your artist presence | How to claim it |
|---|---|---|---|
| **Spotify** | Release + ISRCs; profile created on first ingest | Artist profile | Spotify for Artists. DistroKid offers instant access under *Special Access / Spotify for Artists* once the release is delivered, often before release day |
| **Apple Music / iTunes** | Release, Apple ID per artist | Artist page | Apple Music for Artists (artists.apple.com) → *Request artist access* → search your name → pick the profile with your release → verify. DistroKid's Special Access page may also offer a direct link |
| **Amazon Music** | Release | Artist page | Amazon Music for Artists app → *Claim artist* → verify via the distributor/email flow |
| **YouTube Music** | Audio as "Art Tracks" on an auto-made **Topic channel** (*Artist – Topic*) | Topic channel | See OAC below |
| **TikTok / CapCut / Instagram & Facebook (Meta)** | Songs into the sound libraries | Sound pages | TikTok Artist Account: switch to a Creator account, then request the artist tag / *TikTok for Artists* access. Link your official sound |
| Deezer, Tidal, Pandora, etc. | Release | Profiles | Each has its own "for Artists" claim flow; do these after the big three |

**YouTube Official Artist Channel (OAC), first-time setup.** The OAC merges your
Topic channel and your own channel into one verified channel with a ♪ badge.
Eligibility:
1. A YouTube channel you own, with no Community Guidelines strikes. Use the artist
   name as the channel name.
2. **At least 3 official releases** delivered to YouTube by a distributor. The Topic
   channel has to exist first, usually 1–3 weeks after release 1 goes live.
3. Request it **through your distributor**. In DistroKid that's the YouTube OAC
   request under *Special Access* / the YouTube section: give your channel URL and
   the Topic channel URL.

YouTube reviews it, usually within a few weeks. Under the chapter plan you become
eligible right after single 3 of chapter 1.

**Do not enable YouTube Content ID** for these tracks. Content ID requires exclusive
rights, which AI-generated audio may not cleanly give you. Suno outputs can also
resemble other material, and false claims against other uploaders are a fast way to
lose the feature, or the account.

---

## 2. File architecture

### Local directory blueprint

```
NobleFather-Music/
├── 00_ADMIN/
│   ├── MASTER-RELEASE-SHEET.csv        ← the one ledger; nothing ships that isn't a row here
│   ├── rights/                         ← Suno billing receipts covering 2026-06-30 → 2026-08-08
│   └── qc-reports/                     ← qc.sh output per batch, dated
├── 01_SOURCE_MP3/                      ← untouched Drive downloads, never edited
│   └── <shelf>/<slug>.mp3
├── 02_SOURCE_WAV/                      ← Suno WAV re-downloads (the real masters' input)
│   └── <shelf>/<slug>.wav
├── 03_MASTERED/                        ← Mixea output, one subfolder per release
│   └── <YYYY-MM-DD>_<release-slug>/
│       └── <NN>_<slug>_MASTER.wav
├── 04_ARTWORK/
│   └── <release-slug>/cover_3000.jpg   ← 3000×3000 RGB JPG/PNG
├── 05_RELEASES/                        ← exactly what was uploaded, frozen after upload
│   └── <YYYY-MM-DD>_<SINGLE|EP|LP>_<release-slug>/
│       ├── audio/  artwork/  metadata.txt (title, ISRC, UPC, credits, lyrics)
├── 06_VAULT/                           ← takes not chosen, website-only songs
└── 07_PROMO/<release-slug>/            ← 9:16 clips, canvas loops, captions
```

Naming rules:
- Lowercase slugs, hyphens, no spaces or emoji. Use the manifest `slug`, which
  already follows these.
- Prefix ISO dates (`2026-11-06_`) so folders sort chronologically.
- Prefix track numbers (`03_`) inside releases.
- Never rename a file in `05_RELEASES` after upload. That folder is your proof of
  what went out.

### Master Release Metadata Sheet

`MASTER-RELEASE-SHEET.csv` is already generated and pre-filled for all 177
recordings. Open it in Google Sheets or Excel. Its columns:

```
System File Name, Drive ID, Library Title (as-is), Commercial Track Title, Version Field,
Duplicate Group, Keeper (Y/N), Shelf, Proposed Release, Release Format (Single/EP/LP),
Track #, Primary Genre, Secondary Genre, Explicit (Y/N), Flags, Duration (m:ss),
Suno Created, Suno ID, Suno Plan At Creation (verify), WAV Re-download,
Mixea Master Status, Integrated LUFS, True Peak dBTP, Lyricist, AI Disclosure,
ISRC, UPC, Distribution Date, Release Date, DistroKid Status, Notes
```

Status vocabularies (use these exact words so you can filter on them):
- **Mixea Master Status:** `Not started` → `Mastered` → `QC pass` / `QC fail`
- **DistroKid Status:** `Not uploaded` → `Uploaded` → `Delivered` → `Live` / `Rejected`
- **ISRC:** leave blank and let DistroKid assign it on upload, then paste it back here
  the same day. An ISRC belongs to one recording forever; reuse it only for that exact
  audio.
- **Distribution Date** = the day you uploaded. **Release Date** = the street date.

What's already filled in for you:
- Proposed store-safe commercial titles
- Duplicate groups
- Explicit guesses (`Y?` = title suggests it; `listen` = check the lyrics)
- Proposed genres per shelf: edit these, they're a starting point
- The 71 rows that need a decision are flagged:

| Flag | Rows |
|---|---|
| Multiple takes, choose one | 38 |
| "Remastered" in the title | 26 |
| Version suffix | 19 |
| Over 8 min | 11 |
| Emoji in the title | 9 |
| Trademark/IP risk | 7 |

### Title guidelines

1. **Title case, no styling.**
   - Use standard title case: *Ember in the Marrow*, not *EMBER IN THE MARROW* or
     *ember in the marrow*. The exception is a stylisation your brand really owns and
     uses everywhere.
   - No emoji (9 titles have them).
   - No decorative glyphs. `Sw^ng` → *Swing*, `🎵 The Still Valley…` → *The Still
     Valley & the Certain Fire*.
2. **Never use generic titles.** *Track 12*, *Untitled*, *Song 3* and *Intro* on its
   own get rejected or buried. None of yours are generic, which is good.
3. **Version info goes in DistroKid's version field, not the title.**
   - Use the field for *Remix*, *Extended Mix*, *Acoustic* and similar.
   - **"Remastered" is only allowed when an earlier version was commercially
     released.** None of yours were, so Suno's "(Remastered)" re-generations are just
     *the song*. Drop the word.
   - Drop `· Version 2` entirely: it means "the take I chose," not a version.
4. **No other artists' names, and no franchise IP or trademarks.**
   - Seven titles reference Jedi, Hufflepuff, Potter or Chuck E. Cheese:
     - *Djedi Remembers*
     - *Capital D Precedes Jedi*
     - *Hufflepuffin' Puff Pass*
     - three *Wizard … Potter* titles
     - *Pay to Play (Chuckee Cheesin Mix)*
   - Stores reject these, or rights holders take them down later. Retitle them, or
     keep them website-only in the vault.
   - Never put "feat." or "in the style of" someone you didn't work with.
5. **Mark explicit honestly.** Tick *Explicit* for any song with explicit lyrics,
   whatever the title says. A wrong "clean" flag is a takedown reason. Many Festival
   Floor tracks will need it.
6. **Avoid parenthetical stacks.** *The Loose & Smooth Goose Juice Groove (Goose
   Troop Remix) (Remastered) · Version 2* → title *The Loose & Smooth Goose Juice
   Groove*, version *Goose Troop Remix*.
7. **Credit AI use truthfully, and in the right place.**
   - Answer DistroKid's AI question on the upload form truthfully if it asks one.
   - Spotify now displays standardised AI disclosures (DDEX) in credits.
   - Credit yourself as **songwriter/lyricist** for lyrics you wrote: that's your
     copyrightable contribution, and what PRO registration is based on.
   - Never list Suno, or any real artist, as a performer.
   - Keep the AI disclosure in credits. It doesn't belong in the title.
8. **Cover art.**
   - 3000×3000 px, RGB.
   - No URLs, social handles, store logos, "new single" text or blur.
   - Any text on it must match the artist name and title exactly.

---

## 3. Native Suno MP3 vs. the Mixea upgrade

### What the measurements say

Measured on 12 tracks, two from every shelf:

```
track                                  LUFS   TruePk
contact-high-ll-anthem               -14.5   -1.7
cozy-dragon-dance                    -13.3   -1.1
djedi-remembers                      -12.7   -1.7
dragon-nobility                      -12.0   -0.2  ← hot
first-of-her-name                    -13.7   -0.5  ← hot
god-in-the-mask-banger               -13.5   -1.3
never-doubt-your-visions             -13.4   -2.0
oddmelon-s-verdict…                  -13.7   -2.7
portal-potty-wonderland-orgy…        -13.1   -0.2  ← hot
shoalfish                            -13.1   -0.2  ← hot
so-below-las-above-flex              -13.5   -2.4
the-density-of-divinity              -14.5   -1.9
```

**Loudness is already fine.** Every sampled track sits between −12 and −14.5 LUFS,
inside the −14 to −10 streaming window you named. No store rejects on loudness
anyway:
- Spotify turns songs down to about −14 LUFS by default.
- Apple Sound Check normalises to about −16.
- YouTube normalises to about −14.

So **Mixea is not a requirement** for loudness, and not a requirement to pass Apple
or Spotify ingestion.

**The real technical issues:**
1. **True peaks.** A third of the sample peaks above −1 dBTP, as hot as −0.2. When
   the stores re-encode to AAC/Ogg, those peaks can overshoot into audible clipping.
   Spotify and Apple both recommend −1 dBTP or lower.
2. **The source is MP3.** It's lossy, and Gate 2 above (get WAVs) is the fix.
   DistroKid accepts MP3 uploads but recommends WAV/FLAC; check the current upload
   page. Mixea cannot fix this. Mastering an MP3 gives you a WAV *of an MP3*.
3. **Consistency inside an album.** Tracks range from −12 to −14.5 LUFS and have
   different tonal balance. On an LP played in order that's noticeable, even with
   normalisation on.

### Verdict

Buy Mixea, but **after** the WAV re-downloads, and as polish:
- **True-peak control.** Mixea's output is limited for streaming, which fixes the hot
  peaks.
- **Album consistency.** Running every track of a chapter through the same settings
  evens out level and tone.
- **Cost.** At $99/yr across ~100–155 songs it's well under $1 a track. If it A/Bs
  better on your ears, that's the cheapest real improvement available.

If you skip Mixea, the free minimum is a true-peak limiter at −1 dBTP. That's a
one-line `ffmpeg … -af alimiter`/`loudnorm` pass, and I can write the batch script.
It fixes peaks, not tone.

### How to use Mixea in this pipeline

1. **Subscribe** from your DistroKid dashboard (Mixea is DistroKid's own service, so
   it uses the same login).
2. **Input:** the **WAV** from `02_SOURCE_WAV/`. Use the MP3 only if a WAV truly
   can't be had.
3. **Start with the three lead singles.** Before committing settings to a whole
   chapter:
   1. Try the available loudness/character options on each single.
   2. A/B every option against the original **at matched volume**. Louder always
      sounds "better" for a few seconds, so turn the master down to the original's
      level before judging.
   3. Listen on earbuds, on a phone speaker and in a car.
4. **Choose one setting per chapter** and apply it to every track in that album, for
   consistency.
5. **Download the WAV master** (24-bit if offered) into `03_MASTERED/<release>/`.
6. **Run QC:** `./qc.sh 03_MASTERED/<release>`. Every row should read
   `OK` (−16 to −9 LUFS, true peak ≤ −1.0 dBTP).
   - Re-master any `TRUE-PEAK-HOT` file at a gentler setting.
   - Avoid masters louder than about −9 LUFS: streaming turns them down anyway, and
     all you keep is the distortion.
7. **Upload the mastered WAV to DistroKid.** Mark `Mixea Master Status` = `QC pass`
   and paste the measured LUFS/TP into the sheet.

---

## 4. Account and release chronology (real dates)

The schedule assumes a start date of **Thu 2026-10-08**. "Week" means weeks from
today. Store timings are typical, not guaranteed: DistroKid's minimum is days, but
leave weeks so you can pitch.

| Week | Date | Action | System identifiers created |
|---|---|---|---|
| 0 | Oct 8–14 | Gates 1–3: rights, WAVs, artist name. Choose takes in the sheet. Make chapter-1 cover art. Create or upgrade the DistroKid account. Subscribe to Mixea and A/B the 3 Dragon Cycle singles | — |
| 1 | by Oct 15 | **Upload Single 1** with a release date of **Fri Nov 6** (3 weeks' lead). Enter the artist name exactly and choose **"new artist"** on every store (correct only for this first release). Turn on a HyperFollow pre-save page and put it on the website | ISRC (at upload), UPC, DistroKid release ID |
| 1–2 | Oct 16–22 | Release delivered (typically 2–7 days). Spotify creates the artist profile and URI at ingest. **Claim Spotify for Artists** via DistroKid Special Access. Fill the profile: bio, photo, links to noblefathercreations.com. **Pitch Single 1** to Spotify editorial (it must be unreleased and pitched at least 7 days before release, so aim for 2+ weeks) | Spotify artist URI (`spotify:artist:…`), track URIs |
| 2 | by Oct 22 | **Upload Single 2** with a release date of Fri Nov 20. On every store, **select your existing artist profile, not "new"**. Paste the Spotify URI/ID if asked. This step is what keeps everything on one profile | ISRC #2 |
| 4 | Fri Nov 6 | Single 1 goes live. **Claim Apple Music for Artists** and **Amazon Music for Artists** (the profiles exist now). Make the YouTube channel if you haven't yet | Apple artist ID, Amazon artist page |
| 4–6 | Nov 6–20 | The YouTube **Topic channel** appears. Upload Single 3 (release Dec 4) and pitch it | Topic channel |
| 6 | Fri Nov 20 | Single 2 live. Set up the TikTok Artist Account / claim the official sound | — |
| 8 | Fri Dec 4 | Single 3 live → **3 releases delivered → request a YouTube OAC** through DistroKid | — |
| 8 | by Dec 4 | Upload **The Dragon Cycle (LP)** with a release date of **Fri Jan 8 2027**. Holiday weeks are a bad time to launch, which is why there's a 5-week lead. Enter the 3 singles' **existing ISRCs** so their streams carry over | UPC (album), ISRC ×7 new |
| 13 | Jan 8 2027 | Chapter 1 complete. Chapter 2 (Tender Room) single 1 goes out Jan 22. Repeat every ~10 weeks | — |

**Check after every release.** Open your Spotify for Artists, Apple and YouTube
catalogs and confirm the new release appears *under your profile*. If it lands on a
stranger's profile, or on a duplicate "you" profile, open a DistroKid support ticket
**immediately** ("release mapped to wrong artist page"). It's easy to fix in the
first days and painful after.

---

## 5. Getting the most out of it: reach and money

**Revenue streams.** DistroKid only collects one of these. The other three are
free to set up and easy to leave on the table:

| Revenue stream | Who collects | What you do |
|---|---|---|
| Master royalties (streams/downloads) | DistroKid → you (100%) | Done by uploading. Note: a track pays **$0 on Spotify under 1,000 streams per 12 months** |
| Performance royalties (songwriter) | A PRO, e.g. BMI (free to join in the US) | Register as a songwriter and register each song's lyrics/composition |
| Mechanical royalties (US streams) | The MLC (free) | Self-administer: register your works with the MLC |
| Digital performance (Pandora, SiriusXM, web radio) | SoundExchange (free) | Register as featured artist + rights owner |

Notes:
- The registrations above are where the *lyrics you wrote* earn money independently
  of the AI audio.
- DistroKid takes releases down if your subscription lapses, unless you pay for its
  "Leave a Legacy" add-on. Budget for the plan every year.

**Using the website.** The Listening Room on the noblemusic site, generated from
`MANIFEST.json`, is a real asset here:
- **Vault and funnel.** It holds all 176 songs, while stores get the curated ~100.
  "Hear the whole vault at noblefathercreations.com" gives your stores bio and social
  posts a reason to click through.
- **Store links per song.** As each song goes live, add its Spotify/Apple URL to that
  track in `MANIFEST.json`. The page builder can then show "Stream it" next to the
  in-browser player, which turns site visits into the streams that clear the
  1,000-stream threshold. This is a planned page change, not done yet.
- **HyperFollow.** Put the current pre-save link on the site's music section during
  every pre-release window.
- **Housekeeping.** *The Fourth Position* (Drive, 2026-09-17) isn't in the manifest
  yet. Add it when the Listening Room next gets a pass.

**Editorial and algorithmic reach:**
1. **Pitch every single** in Spotify for Artists:
   - Use accurate genre and mood tags.
   - Write a real story, e.g. "the dragon songs began as a lullaby for…".
   - Leave at least 2 weeks of lead time.
2. **Add Canvas loops and an artist pick** on Spotify, and **Apple Music artwork
   motion** where offered.
3. **Clip pipeline.** Use the CLAUDE.md pipeline to cut 15–30s 9:16 hooks from each
   single for TikTok/Reels/Shorts. Post them using the TikTok *official sound* so
   uses count toward the track.
4. **One release every two weeks, without fail.** Regular releases are what feed
   Release Radar and the algorithms.

---

## Next three actions

1. Check the Suno billing history for 2026-06-30 → 2026-08-08 and fill
   `Suno Plan At Creation`.
2. In the sheet:
   1. Filter `Duplicate Group` and pick the keepers.
   2. Fix the 7 trademark titles and the 9 emoji titles.
   3. Mark the 10 Dragon Cycle songs and choose 3 singles.
3. Re-download those 10 as WAV, run `qc.sh`, trial Mixea on the 3 singles, and
   upload Single 1 by **Oct 15**.
