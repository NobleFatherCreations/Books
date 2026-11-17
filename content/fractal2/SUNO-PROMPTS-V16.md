# Suno prompts for the Fractal² film, script v16 (2026-11-17)

Replaces the prompts in section 7 of `SUNO-VOCAL-SPEC.md`, which were written for the old 12:48 cut. Recording notes and what to send in that file still hold. Times come from the film's own clock (`design/fractal2/film/cues.json`), so they match the picture as built.

Film: 18:40, 150 BPM half-time (feels like 75), one bar = 1.6 s, 700 bars. D minor, lifting to F major at the window.

## How to set up every cue

- Model: **v6**. Mode: **Custom**. **Instrumental: ON.**
- **Variety: Off** (otherwise Suno rewrites the style text).
- **Max Mode: On** (every cue is over two minutes).
- Weirdness **30**. Style Influence **85**.
- Duration: **Custom**, set to the cue length below.
- Paste the cue's Style text. Paste the shared Exclude list.
- If your form still shows a lyrics box with Instrumental on, paste the cue's section tags there. If it doesn't, the arc is already written into the Style text.
- Generate 4 to 6 times per cue and keep the best two. Fix one weak section with Replace Section instead of re-rolling a good take.
- Suno will not land on exact seconds. Get each cue's shape right, then place it in your editor so the four anchors land (table at the end).

**Exclude (same for all cues):**
`vocals, singing, choir, humming, edm, four-on-the-floor, radio pop, auto-tune`

## The four cues

Every cue starts and ends at a hard edge in the film, so they join cleanly.

| Cue | Film time | Length | Film sections |
|---|---|---|---|
| 1. The Question | 0:00.0 to 3:58.4 | 3:58 | 1 to 3 |
| 2. The Mirror | 3:58.4 to 8:38.4 | 4:40 | 4 to 6 |
| 3. The Descent | 8:38.4 to 12:54.4 | 4:16 | 7 to 10 |
| 4. The Map | 12:54.4 to 18:40.0 | 5:46 | 11 and outro |

### Cue 1. The Question (3:58)

**Style:**
```
Cinematic tribal score at 150 BPM half-time in D minor, instrumental, built to sit under a spoken voice. Deep clean mono sub bass, organic hand drums and frame drums, wide warm analog pads, a low bowed drone. Sparse and spacious, mids carved out so speech stays clear, film score dynamics. Begins in near silence with one sub drone and one dark pad, no drums. A slow heartbeat kick enters quietly. Pulls back to almost nothing for a stretch, then hand percussion enters and one new layer is added at a time, eight clear steps. Grows into a full tribal groove at medium energy, steadily climbing, future bass chords swelling underneath. Ends on a hard cut to total silence, no tail, no reverb.
```

**Section tags (lyrics box, if shown):**
```
[Intro: pianissimo, sub drone and one dark pad, no drums]
[Verse: heartbeat kick enters, very soft]
[Break: almost nothing, pad only]
[Verse: hand drums enter, one new layer every eight bars]
[Build: full tribal groove, climbing]
[End: hard cut to silence]
```

Where things fall in the film (cue time = film time):
- 1:11 "It must be me." and 1:26 "What if it isn't me?": strip to almost nothing around these two lines (about 1:08 to 1:32).
- 1:36: hand percussion enters (section 2, the eight stages). One layer per stage.
- 2:52.8: full groove (section 3, thirty sectors), climbing to the end.
- 3:58.4: **hard cut**. This is the STOP anchor.

### Cue 2. The Mirror (4:40)

**Style:**
```
Cinematic tribal future bass score at 150 BPM half-time in D minor, instrumental, built to sit under a spoken voice. Same sound world: deep clean mono sub, hand drums and frame drums, wide analog pads, low bowed drone, mids carved out for speech. Opens with two bars of total silence. Then intimate close warm pads only, no drums, very still, for about a minute. A four-bar riser with reverse cymbal leads into the biggest drop in the whole score: huge wide chords, full sub, tribal drums at full power, a sense of enormous scale opening up. Settles into a steady medium groove, then a short pause. Then stripped back to pad and sparse percussion, and into a dark, hypnotic, plain repeating pulse with ominous low strings, ritual feeling, kick and shaker on every beat. Near the end, six heavy low drum hits spaced apart, each darker than the last. Ends on a suspended, unresolved chord that pulls inward.
```

**Section tags:**
```
[Intro: silence, two bars]
[Verse: pianissimo, warm pads only, no drums]
[Build: four-bar riser, reverse cymbal]
[Drop: fortissimo, full sub, tribal drums, huge chords]
[Verse: steady medium groove]
[Break: pad and sparse percussion]
[Verse: dark hypnotic pulse, plain kick and shaker, low strings]
[Bridge: six heavy low hits, spaced apart]
[Outro: suspended unresolved chord, pulling in]
[End]
```

Where things fall (cue time / film time):
- 0:00 to 0:03.2 / 3:58.4 to 4:01.6: silence. Your voice alone: "Then the map turned around and looked at me."
- 0:03 to 1:08 / 4:02 to 5:07: pads only (section 4, the mirror).
- 1:08.8 to 1:15.2 / 5:07.2 to 5:13.6: the four-bar riser, under "That is when I understood the size of it."
- **1:15.2 / 5:13.6: the drop.** PEAK1. It lands on "people" in "It was never only people."
- 1:59.8 / 5:58.2: short gap before "That is the fractal."
- 2:06.4 / 6:04.8: stripped back (section 6, "I offer it as one man's sight").
- 2:10 to 3:30 / 6:08 to 7:28: the plain pulse. Table items land on the beat, so keep it simple.
- 3:36 to 3:46 / 7:34 to 7:44: the six low hits, one per name (false god, devil, adversary, matrix, machine, system).
- 4:11 / 8:09.7: "Which means something real was here first." Suspended from here.
- 4:34.5 to 4:40 / 8:32.9 to 8:38.4: two-bar pull-in under "So I stopped trying to climb out, and I went down."

### Cue 3. The Descent (4:16)

**Style:**
```
Cinematic tribal future bass score at 150 BPM half-time, D minor lifting to F major, instrumental, built to sit under a spoken voice. Same sound world: deep clean mono sub, hand drums and frame drums, wide analog pads, low bowed drone, mids carved out for speech. Opens on a heavy drop on the first beat, then descends: pitch falling, one layer removed every two bars until nothing is left. Eight bars of total silence. One pure sustained tone enters, then warm reverent pads, no drums, a slow sacred swell, human and tender, with a soft pulse returning late. Then the kick returns and one new layer is added with each phrase, and the music stops dead. A sixteen-bar build of tribal drum hits every two beats, rising light. Then a release into F major: wide warm chords, the most open and tender moment of the score, not the loudest. Strips quickly to breath and one pad.
```

**Section tags:**
```
[Drop: fortissimo on the first beat]
[Verse: descending, one layer removed every two bars]
[Break: total silence, eight bars]
[Verse: one pure sustained tone, then warm pads, no drums]
[Verse: slow sacred swell, soft pulse returns]
[Build: kick returns, one layer per phrase, then stop dead]
[Build: tribal hits every two beats, sixteen bars, rising]
[Drop: F major, wide and warm, tender not loud]
[Outro: breath and one pad]
[End]
```

Where things fall (cue time / film time):
- **0:00 / 8:38.4: the drop.** PEAK2. It lands on "down" in "I went down."
- 0:01 to 0:15 / 8:39.5 to 8:53.4: the four "Down through..." lines, over the descent.
- 0:33.6 to 0:46.4 / 9:12.0 to 9:24.8: **silence**, voice alone: "And at the bottom, beneath every lie that had been installed as truth, I found it."
- 0:46.4 / 9:24.8: the sustained tone enters, then "In me. Where it had always been." (9:27.6).
- 0:57.6 / 9:36.0: warm pads, slow swell (section 8, the traditions).
- 2:40 / 11:18.4: kick returns, one layer per "you're right" (four lines).
- 3:14 / 11:52.2: **stop dead** after "The destination is the same."
- 3:18.4 to 3:58.4 / 11:56.8 to 12:36.8: the build (section 10, the window).
- **3:58.4 / 12:36.8: the drop into F major.** PEAK3. It lands on "through" in "let the light through."
- 3:59.5 to 4:16 / 12:37.9 to 12:54.4: breath and one pad, under "My original frequency." and "Pulsing quietly, and waiting."

### Cue 4. The Map (5:46)

**Style:**
```
Cinematic tribal future bass score at 150 BPM half-time in F major, instrumental, built to sit under a spoken voice. Same sound world: deep clean mono sub, hand drums and frame drums, wide analog pads, low bowed drone, mids carved out for speech. A confident, full, steady groove, sure-footed and warm, that carries a long spoken passage without getting busy. Small changes every sixteen bars so it never loops. About four minutes in, it strips to one pad and a low pulse for a quiet, forgiving passage, then builds slowly and steadily, with no drop. A final lift with one last big hit, then a long warm ring-out to silence.
```

**Section tags:**
```
[Intro: groove enters, full and sure]
[Verse: steady, warm, leave space for speech]
[Verse: small change, same groove]
[Verse: small change, same groove]
[Break: pianissimo, one pad and low pulse]
[Build: slow and steady, no drop]
[Outro: final lift, one last big hit, long ring-out]
[End]
```

Where things fall (cue time / film time):
- 0:00 to 4:15 / 12:54.4 to 17:10: the full groove (section 11, the map and its tables).
- 4:15.7 / 17:10.1: strip to one pad and a low pulse for "My healing journey meant forgiving..."
- 4:25.9 / 17:20.3: slow build begins under "Justice, to me, comes from breaking every tool they have," and runs through the justice passage. No drop.
- 5:06 / 18:00.6: "It will take me a lifetime to finish." Final lift begins.
- 5:22.8 / 18:17.2: "Now the map is yours." The last big hit lands here.
- 5:32.8 to 5:45.6 / 18:27.2 to 18:40.0: ring out under the end button.

### Hub loop (separate, short)

Set Duration Custom to 0:26 (16 bars). Same settings, same Exclude.

**Style:**
```
Seamless ambient loop at 150 BPM half-time in F major, instrumental. Warm wide pad, soft clean sub pulse, a faint hand drum, the low bowed drone from the film. Calm, endless, no beginning or end, no build, no drop.
```

## The four anchors (must land on the grid in your mix)

| Anchor | Film time | Bar | What lands |
|---|---|---|---|
| STOP | 3:58.4 | 150 | Music cuts as "Then the map turned around and looked at me." begins |
| PEAK1 | 5:13.6 | 197 | Drop on "people" in "It was never only people." |
| PEAK2 | 8:38.4 | 325 | Drop on "down" in "I went down." |
| PEAK3 | 12:36.8 | 474 | Drop into F major on "through" in "let the light through." |

## Your voice

You're sending the vocals separately, which is what the film needs. Recording notes are in `SUNO-VOCAL-SPEC.md` section 4 (dry, mono, 48 kHz, 24-bit WAV, ten seconds of room tone, read the approved script word for word). Send the final mix, voice only and music only, all the same length and start point. Exact seconds will move when your real read comes in; the film re-times itself to your voice, and only the four anchors need to stay on the grid.

## If a cue comes out wrong

- Too busy under speech: add `minimal, sparse, leave space for spoken word` to the start of the Style text.
- Turns into dance music: the Exclude list already fences this. If it still happens, add `dance beat` and remove `radio pop`.
- Hums or sings: check Instrumental is on, then re-roll. Don't add more excludes than eight.
- A silence gets filled: Suno often ignores silences. Leave it and cut the silence in your editor; the film needs real digital silence at 3:58.4 to 4:01.6 and 9:12.0 to 9:24.8 anyway.
