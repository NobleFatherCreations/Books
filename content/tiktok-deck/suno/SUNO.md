# Suno song for the TikTok book video (7:30)

## Settings
- **Model:** the newest Suno model you have (v4.5+ or v5), Custom mode.
- **Weirdness:** 30%
- **Style Influence:** 80%
- **Vocal gender:** Male (if offered)
- **Title:** Words For The Things (Noble Father)

## Style (564 chars)
```
West Coast ratchet trap anthem, 96 BPM, 4/4, minor key, club bounce. Bouncy sliding 808 bass, hard claps and finger snaps on 2 and 4, sparse plucky synth riff, rattling hi-hats, "hey!" gang shouts on downbeats, short drum drop at the top of each new verse. Confident, witty male rap vocal, clear diction, playful punchlines with a serious edge, ad-libs in parentheses. One line per bar. Continuous verses, no chorus, no sung hook, no bridge; every [section] is a new verse. Clean, radio-friendly. Cold open on an airy pad, ends with the beat riding out and fading.
```

## Exclude styles
```
chorus, sung hook, melodic singing, female vocals, autotune ballad, EDM drop, dubstep, rock, guitar, piano ballad, lo-fi, boom bap, slow tempo, explicit
```

## Step 1: main generation, lyrics (4898 chars)
Paste `main.txt`. It covers the intro through **The Silence** (video 0:00 to 4:50).

## Step 2: extend (2397 chars)
On the take you like, choose **Extend**, set "extend from" to the end of [Verse 12] (The Silence) (target 4:50), keep the same Style and Exclude, and paste `extend.txt`. Then use **Get Whole Song**.

## Sync map (video is cut to a 96 BPM grid: 1 bar = 2.5 s)
| Video time | Section (lyric tag) | Bars |
|---|---|---|
| 0:00 | [Intro] angel video | 2 |
| 0:05 | [Verse 1] The Library | 8 |
| 0:25 | [Verse 2] The Author | 3 |
| 0:32 | [Verse 3] The Pattern Decoder | 12 |
| 1:02 | [Verse 4] The Sovereign Divine Feminine | 10 |
| 1:27 | [Verse 5] The Long After | 9 |
| 1:50 | [Verse 6] Playground Protectors | 10 |
| 2:15 | [Verse 7] The Festie Codex | 9 |
| 2:37 | [Verse 8] The Festie Bible | 9 |
| 3:00 | [Verse 9] The Fractal | 12 |
| 3:30 | [Verse 10] The Fracture | 10 |
| 3:55 | [Verse 11] The Sacred Divide | 12 |
| 4:25 | [Verse 12] The Silence | 10 |
| 4:50 | [Verse 13] The Repair | 9 |
| 5:12 | [Verse 14] At Will | 9 |
| 5:35 | [Verse 15] The Slow Take | 9 |
| 5:57 | [Verse 16] The Loop | 9 |
| 6:20 | [Verse 17] The Weighing | 9 |
| 6:42 | [Verse 18] The Root | 9 |
| 7:05 | [Verse 19] Find Yours | 2 |
| 7:10 | [Outro] closing film + signature | 8 |
| 7:30 | end | |

If the song drifts against the video, line up the start of each [section] with the matching video time in your editor; each book changes on a bar line.

## Ending song (separate generation, 25 s, video 7:05-7:30)
Lyrics: `ending.txt` (10 lines = 10 bars at 96 BPM = 25 s).
- Line 1-2 sit on the outro card (7:05), lines 3-7 on the closing film (7:10), lines 8-10 on the signature (7:22.5).
- Style: the main Style plus "short 25-second outro song, starts on the first beat with no intro, ends on a hard stop".
- Exclude: the main Exclude plus "intro, long instrumental".
- In the edit: cut the long song at 7:05 and drop this in from 7:05 to 7:30. Trim any tail past 25 s.
