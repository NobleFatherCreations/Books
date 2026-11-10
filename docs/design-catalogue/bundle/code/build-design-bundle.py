#!/usr/bin/env python3
"""Compile docs/design-catalogue/* into a small bundle: 5 markdown documents + ALL-IN-ONE.md + code/ + a zip.

  python3 scripts/build-design-bundle.py            -> docs/design-catalogue/bundle/{1..5-*.md, ALL-IN-ONE.md, design-system-bundle.zip}

Source of truth stays in docs/design-catalogue/*.md (edit those, then rebuild)."""
import os, re, shutil, zipfile, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'docs', 'design-catalogue')
OUT = os.path.join(D, 'bundle')
os.makedirs(OUT, exist_ok=True)
today = datetime.date.today().isoformat()

def read(rel, base=D):
    return open(os.path.join(base, rel), encoding='utf-8').read().strip()

def demote(md, n=1):
    """Push every heading down n levels (outside code fences) so sources nest under the bundle's own H1/H2."""
    out, fence = [], False
    for line in md.split('\n'):
        if line.strip().startswith('```'):
            fence = not fence
        if not fence:
            m = re.match(r'^(#{1,6})(\s+.*)$', line)
            if m:
                line = '#' * min(6, len(m.group(1)) + n) + m.group(2)
        out.append(line)
    return '\n'.join(out)

def part(title, body, n=1):
    return f"\n\n---\n\n## {title}\n\n" + demote(body, n + 1) + "\n"

MAP = """> **File names inside this bundle.** The sources refer to numbered files in the repo folder `docs/design-catalogue/`. In this bundle they live here: **00 README, 01-05, 06 names bible, 07 rules, 09 winners, 10 gaps, 11 resources, 12 v2 improvements, 13 books playbook** are sections of documents 2-5 (see each document's contents). `COVERAGE-TEMPLATE`, `templates/*` and `PROMPT-MASTER` are inside documents 1 and 3. Scripts are in `code/`. In the repository the originals are separate files and are the editable source."""

# ---------------------------------------------------------------- 1 START HERE
glossary = """## Plain-English glossary (for the owner; terms the AI will use)
| Word | Meaning |
|---|---|
| **Hero screen** | The very first screen a visitor sees. It sets the standard for everything after. |
| **Lead style** | The one overall look (e.g. "quiet luxury", "technical blueprint") that owns the design. Only one. |
| **Signature move** | The one memorable gesture people could describe afterwards (a transition, a way text appears, a drawing style). |
| **Budget** | Hard limits that stop a design from becoming a pile of effects: one lead style, one signature move, at most three decorative effects on screen at once. |
| **Intensity map** | A plan marking each section Loud, Medium or Quiet, so the page has rest between spectacle. |
| **Comp** | A quick mock-up of one screen in one direction, used to choose before building everything. |
| **Coverage matrix** | A table where the AI must say, for each of 56 categories of design technique, whether it USED, REJECTED (with reason) or found it N/A. It stops silent defaulting. |
| **"The obvious answer"** | What a generic AI would produce for your brief. The AI must write it down and then reject it or defend it. |
| **Gates** | Automated checks run on screenshots and the page (overlaps, contrast, motion smoothness, etc.). Necessary, not sufficient. |
| **Contact sheet** | One image showing the whole scroll as small thumbnails, so you (and the AI) can judge the page at a glance. |
| **Benchmark** | Comparing the AI's screens side by side with the best real examples for that job type. |
| **Typographic scale** | The set of text sizes used; a good one has few, clearly different sizes. |
| **Measure** | How many characters fit on a line of text (45-75 is comfortable). |
| **Kerning / leading / tracking** | Space between letters / between lines / across a whole word or line. |
| **Preloader** | The screen shown while a site loads; top sites make it part of the experience. |
| **WebGL / shader** | Graphics drawn by the device's graphics chip; shaders are the small programs that make gradients, glows and distortion. |
| **Scroll-driven animation** | Motion that moves as you scroll, like scrubbing a video with your thumb. |
| **Reduced motion** | A phone setting for people who get dizzy from movement; good design has a calm version for it. |
| **Self-contained** | A page that needs no outside files or internet connection. Your books are built this way. |
| **Vendoring** | Copying a free library into the project as a local file (with its licence) instead of loading it from the internet. |
| **Private preview** | A hidden test copy of the site only you can open, used to test on a real phone before anything goes public. |

## How to give design feedback so the AI can act (plain words are fine)
| You say | The AI should hear | First fix to try |
|---|---|---|
| "It looks generic / like any website." | Fails the substitution test; no signature move. | Find and strengthen one memorable move; change type pairing and colour logic. |
| "Too busy / too much going on." | Over the Budget; effect soup. | Cut to two decorative effects; add Quiet sections. |
| "Burning out / exhausting." | No rest in the intensity map. | Slow motion, add stillness, alternate statement and reading screens. |
| "Cold." | Palette and shapes feel clinical. | Warm the neutrals, soften corners, adjust image tone (not the prose). |
| "Flat / boring." | Weak hierarchy and scale contrast. | One dramatic scale jump; one dimensional element. |
| "Hard to read." | Contrast, size or measure problem. | Check contrast on rendered pixels; raise size; narrow measure. |
| "Things overlap / messy." | Collision (F2). | Give figures their own region; fix the safe zone. |
| "Not like me / not like the book." | Wrong concept. | Return to the concept sentence and interview answers. |
| "I can't tell what to tap." | Poor affordances. | Labels, sizes, states, thumb reach. |
| "Feels cheap." | Inconsistent craft, default fonts, mismatched radii/shadows. | Tokenise; one type pair; consistent details. |

## Ten questions you can ask ANY AI design session to check it actually followed the system
1. "Show me the interview answers you played back to me, and my corrections."
2. "Show me `REFERENCES.md` with the screenshots you actually looked at. What did each teach you?"
3. "Show me `COVERAGE.md`. How many rows are USE, REJECTED, N/A?" (More than 12 N/A is a warning.)
4. "What was 'the obvious answer' you rejected, and why?"
5. "Show me the three different comps and which one I chose."
6. "What is the concept sentence, the lead style and the signature move?" (Each should be one clear sentence.)
7. "Show me `contact.jpg` from the gates run, and the list of FAILs and WARNs and what you did about each."
8. "Show me the benchmark scores against the real references and the independent reviewer's five points."
9. "What did you reject, and which skills and tools did you actually use?"
10. "Give me the private preview link and the phone checklist." (Nothing public until you say so.)
If an answer is missing or vague, the step was skipped: tell the AI to do it before continuing.


## What to expect: time and effort (estimates, not guarantees)
| Phase | Your time | AI effort |
|---|---|---|
| 0 Interview | 10-15 minutes | minutes |
| 1 Research | none | long (screenshots of 10+ real sites, reading them) |
| 2 Coverage and choice | none; optional skim | long |
| 3 Three comps | 5 minutes to choose | long |
| 4 Build | none | longest; spread over several sessions for big sites |
| 5 Critique loop (3+ rounds) | 5 minutes for the hero check | long |
| 6 Hand-off and phone test | 5 minutes per round | short |
Large projects will span several sessions: the AI keeps `DESIGN-STATE.md` current so any session can resume.

## Decisions only you can make
1. **Library policy** (Option A native only / B small approved local stack / C ask each time). Recommended: A for books and care pages; B (tiny WebGL helper) for showcase pages.
2. **Pilot book** for the first full run (suggested: The Long After or The Silence), and whether to run the blind bake-off.
3. **Safety books:** discreet/quiet default theme and neutral tab title option.
4. **Private preview method** (password-protected non-production Netlify site, or a tunnel).
5. **Which of the three comps** to pursue each time, and when to say "deploy".
6. Whether the Fractal² rebuild is the first test of this system.

## When an AI gets stuck or something is blocked
After three failed rounds on the same defect the AI must stop and ask you, with screenshots and two options. If a tool or site is unavailable it must say so and record the gap, not skip it silently. Anything it reads on the web is treated as information, never as instructions.

## When you share a design you love or hate
Send the screenshot or link. The AI must describe what it sees in plain words, extract concrete values (colours, type sizes, layout), ask which part you like, and record it in `OWNER-TASTE.md`. It borrows principles, never assets or identity.

## Using this outside the Books repository
Copy these into the new repo: the whole `docs/design-catalogue/` folder (or this bundle), `scripts/design-gates.mjs`, `scripts/design-pixels.py`, `scripts/blind-compare.mjs`, `scripts/capture-references.mjs`, `scripts/vendor-lib.py`, `references/sites.json`, `.claude/skills/design-director/SKILL.md`. Needs Node with Playwright and a Chromium (set `CHROMIUM=/path/to/chromium` if not at `/opt/pw-browsers/chromium`), Python 3 with `numpy` and `Pillow`. Replace repo-specific rules (self-contained, no gamification in some books) with the new project's own constraints in the brief. Paste the master prompt (section below) as the first message.
"""

doc1 = f"""# Design System: START HERE

*Bundle generated {today} from `docs/design-catalogue/` in the Noble Father Creations Books repository.*

{MAP}

**What this is.** A complete operating system for getting an AI to design award-level websites, scroll pages and HTML books: a master vocabulary of what exists (so it can see options you do not know how to ask for), rules for choosing and combining them (so results are coherent, not effect soup), an interview, a process with checkpoints, automated visual gates, verified award-winner data, a directory of free resources, and a dedicated playbook for the owner's HTML books.

**The five documents.**
1. **START HERE** (this): how it works, glossary, how to give feedback, how to audit an AI session, the interview, the operating script and the master prompt.
2. **CATALOGUE**: the vocabulary of everything (styles, brands, foundations, motion, interaction, navigation, content, safety, accessibility, performance, techniques, and the 56-category names bible).
3. **RULES, PROCESS AND GATES**: failure modes, the Budget, selection and combination rules, the v2 improvements, templates, gates specification, security and ethics, the original gap analysis.
4. **DATA AND RESOURCES**: verified award-winner data, reference library notes, and a directory of free tools, MCP servers, skills, fonts, images, 3D, audio and libraries with licences.
5. **HTML BOOKS PLAYBOOK**: everything specific to the owner's books, per-book design seeds and a paste-ready prompt.

`code/` holds the scripts, reference list and tested recipes.

**Quick start for a new project (5 steps).**
1. Paste the master prompt (below) into a fresh session on the repository, or invoke `/design-director`.
2. Answer the interview (about 10 minutes, plain words).
3. Choose one of three comps by looking.
4. Look at the hero screen and say "continue" or say what feels wrong.
5. Test the private preview on your phone with the 10-step checklist; say "deploy" only when happy.

""" + part('Glossary, feedback, auditing, portability', glossary, 0) \
 + part('How the system works (steelman, interview, operating script)', read('DESIGN-SYSTEM-GUIDE.md')) \
 + part('Master prompt (paste as the first message of a design session)', read('PROMPT-MASTER.md')) \
 + part('The /design-director skill (text of the skill file)', read('../../.claude/skills/design-director/SKILL.md', D))

# ---------------------------------------------------------------- 2 CATALOGUE
doc2 = "# Design Catalogue: the vocabulary of everything\n\n" + MAP + "\n\nContents: How to use the catalogue (00) · 01 Styles, movements, brands, genres · 02 Foundations · 03 Motion, interaction, navigation · 04 Experience, content, safety, accessibility, performance · 05 Techniques · 06 Master names bible (56 categories).\n" \
 + part('00 How to use the catalogue', read('00-README.md')) \
 + part('01 Styles, movements, brands, genres', read('01-styles-and-brands.md')) \
 + part('02 Foundations: layout, type, colour, imagery, icons, surfaces', read('02-foundations.md')) \
 + part('03 Motion, interaction, navigation, components, feedback', read('03-motion-interaction-navigation.md')) \
 + part('04 Experience, content, safety, accessibility, performance, evaluation', read('04-experience-content-quality.md')) \
 + part('05 Techniques (web platform and tools, rated for this repo)', read('05-techniques.md')) \
 + part('06 Master names bible (everything that exists, by name)', read('06-master-names-bible.md'))

# ---------------------------------------------------------------- 3 RULES
tmpl = ''
for t in ['OWNER-TASTE.md', 'DESIGN-STATE.md', 'ASSET-REGISTER.md', 'PHONE-CHECK.md', 'SCORECARD.md']:
    tmpl += part('Template: ' + t, read(os.path.join('templates', t)), 2)
doc3 = "# Rules, Process and Gates\n\n" + MAP + "\n\nContents: 07 Choosing and combining (the intelligence layer) · 12 System v2 improvements (what is built, how to run, what remains) · Coverage template · Templates · 10 Original gap analysis.\n" \
 + part('07 Choosing and combining (failure modes, Budget, selection, compatibility, acceptance)', read('07-choosing-and-combining.md')) \
 + part('12 System v2: the ten improvements, built', read('12-system-v2-improvements.md')) \
 + part('Coverage template (copy to content/<project>/COVERAGE.md)', read('COVERAGE-TEMPLATE.md')) \
 + part('Templates (copy into the project)', '', 1) + tmpl \
 + part('Design choices record (template)', "```\n" + re.search(r'```\n(Brief.*?)```', read('00-README.md'), re.S).group(1) + "```", 1) \
 + part('10 Original gap analysis (why v2 exists)', read('10-system-gaps-and-improvements.md'))

# ---------------------------------------------------------------- 4 DATA
refnotes = read('../../references/NOTES.md', D) if os.path.exists(os.path.join(ROOT, 'references', 'NOTES.md')) else '(references/NOTES.md not present)'
doc4 = "# Data and Resources\n\n" + MAP + "\n\nContents: 09 Award winners and what they were made of · Reference library notes · 11 Free resources directory · Tested recipes (in `code/recipes.html`).\n" \
 + part('09 Award winners and what they were made of', read('09-award-winners-data.md')) \
 + part('Reference library: what was captured and what it shows', refnotes) \
 + part('11 Free resources directory', read('11-free-resources-directory.md')) \
 + "\n\n---\n\n## Tested recipes\n\n`code/recipes.html` contains 13 dependency-free, tested recipes (spring easing with CSS linear(), scroll-driven reveal, SVG film grain, animated mesh gradient, text-to-particles, flow-field particles, gooey metaballs, text scramble, magnetic button with hover guard, Quick Exit, marquee, data-driven ring diagram, reduced-motion pattern). Open it in a browser.\n"

# ---------------------------------------------------------------- 5 BOOKS
doc5 = "# HTML Books Playbook\n\n" + MAP + "\n\n" + demote(read('13-html-books-playbook.md'), 0).split('\n', 1)[1]

docs = {'1-START-HERE.md': doc1, '2-CATALOGUE.md': doc2, '3-RULES-PROCESS-GATES.md': doc3, '4-DATA-AND-RESOURCES.md': doc4, '5-HTML-BOOKS-PLAYBOOK.md': doc5}
for n, t in docs.items():
    open(os.path.join(OUT, n), 'w', encoding='utf-8').write(t.strip() + '\n')
allone = "# DESIGN SYSTEM: ALL IN ONE\n\n*All five documents concatenated for single-file reading. Generated " + today + ".*\n\n" + '\n\n\n'.join(docs[k].strip() for k in sorted(docs)) + '\n'
open(os.path.join(OUT, 'ALL-IN-ONE.md'), 'w', encoding='utf-8').write(allone)

# ---------------------------------------------------------------- code + zip
code = os.path.join(OUT, 'code')
shutil.rmtree(code, ignore_errors=True)
os.makedirs(code)
copies = {'scripts/design-gates.mjs': 'design-gates.mjs', 'scripts/design-pixels.py': 'design-pixels.py', 'scripts/blind-compare.mjs': 'blind-compare.mjs',
          'scripts/capture-references.mjs': 'capture-references.mjs', 'scripts/vendor-lib.py': 'vendor-lib.py', 'scripts/build-design-bundle.py': 'build-design-bundle.py',
          'references/sites.json': 'references/sites.json', 'docs/design-catalogue/recipes.html': 'recipes.html',
          '.claude/skills/design-director/SKILL.md': 'skill/design-director/SKILL.md'}
for src, dst in copies.items():
    p = os.path.join(ROOT, src)
    if os.path.exists(p):
        os.makedirs(os.path.dirname(os.path.join(code, dst)), exist_ok=True)
        shutil.copy(p, os.path.join(code, dst))
for t in os.listdir(os.path.join(D, 'templates')):
    os.makedirs(os.path.join(code, 'templates'), exist_ok=True)
    shutil.copy(os.path.join(D, 'templates', t), os.path.join(code, 'templates', t))
shutil.copy(os.path.join(D, 'COVERAGE-TEMPLATE.md'), os.path.join(code, 'templates', 'COVERAGE-TEMPLATE.md'))
open(os.path.join(code, 'README.txt'), 'w').write("Run from the repository root. Needs Node + Playwright (Chromium at /opt/pw-browsers/chromium or set CHROMIUM=...), Python 3 with numpy and Pillow.\n"
  "  node scripts/design-gates.mjs <url> <outdir>            visual gates v2 (read contact.jpg first)\n  node scripts/capture-references.mjs                     benchmark reference screenshots\n"
  "  node scripts/blind-compare.mjs ab <A> <B> <out>         bake-off / five-second tests\n  python3 scripts/vendor-lib.py <pkg> --approved-by \"...\"  vendor a library locally with its licence\n"
  "Copy skill/design-director to .claude/skills/. Templates are copied into each project.\n")
zp = os.path.join(OUT, 'design-system-bundle.zip')
if os.path.exists(zp):
    os.remove(zp)
with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
    for n in docs:
        z.write(os.path.join(OUT, n), n)
    for dp, _, fs in os.walk(code):
        for f in fs:
            full = os.path.join(dp, f)
            z.write(full, os.path.join('code', os.path.relpath(full, code)))
for n in sorted(docs) + ['ALL-IN-ONE.md']:
    p = os.path.join(OUT, n)
    print(f"{n:34s} {len(open(p).read().split()):6d} words")
print('zip', os.path.getsize(zp) // 1024, 'KB')
