# Still to do (as of 2026-11-23)

## A. The owner's decisions (ask in one message, early)
1. **Facebook and Instagram handles or links.** Only TikTok is known (`@noblefathercreatorsource`). They're needed for:
   - the bio's "tell me how it helped you" link
   - `sameAs` in the schema
   - the About page
2. **Feedback box: build it?** It's the owner's fallback request: *"build me an anonymous feedback thing on my home page where people can write to me with a way for me to reply. Easy no fluff."* See section B1.
3. **The bio's last words:** "screw it" or the owner's own word? "Nothing else quite like it" or "better than anything out there"?
4. **AI-use disclosure:** whether to have one, and its wording. The Long After, the Decoder About page and `/about` all wait on it.
5. **Composite stories:** a "A composite story" tag on each example, or keep the current "made up" line?
6. **Voice sample:** 1 or 2 pieces of the owner's unedited writing, for the voice-fingerprint pass.
7. **Root and Listening Room links** in heavy chapters (links only, never autoplay): yes or no?
8. **Long After design:** keep Dusk to first light and add the shell mechanics (recommended), or a wider redesign?
9. **The 16 sites with the menu count 310 to 335** in the repo but not live (list in 02, incident 1): deploy which, if any?
10. **The six broken meta descriptions** (02, incident 6): fix and redeploy loop, scale, silence, atwill, repair and slowtake?
11. **New share cards for the other 13 books?**
12. **Next book:** The Silence is recommended (05). Confirm.

## B. Build work, ready to start
1. **Anonymous feedback box with replies** (homepage first, then linked from `/about` and every book's "Who made this" line). No fluff.
   - **Reader side:**
     - The reader writes a message.
     - The page shows a random reply code, for example `ROSE-4821-KITE`, and tells them to screenshot or write it down. Nothing is saved in their browser.
     - They come back, type the code and see the owner's reply.
   - **Server side:**
     - One same-site Netlify Function, `hub/netlify/functions/feedback.mjs`, stores messages in Netlify Blobs.
     - No email or name is collected, there is no third-party service, and nothing is logged beyond the message.
     - A simple rate limit and size cap stop spam.
   - **Owner side:**
     - A private page, `/f/inbox`, lists the messages, with a reply box under each one.
     - It is protected by a secret the owner sets himself as a Netlify environment variable (for example `FEEDBACK_ADMIN_KEY`). Never pasted in chat.
   - **Build steps:**
     - Build it through `scripts/seo/build_home.py` (the homepage is never hand-edited).
     - Test it locally with `netlify dev` or a function harness.
     - Screenshot it at 375 and 1440.
     - Deploy only on "deploy the homepage".
   - **Safety copy beside the box:** "Don't include your name or anything that identifies you or anyone else. If you're in danger, use the help page." This is a link to the existing help page, not a helpline list.
2. **The `/about` page** from `content/about.md`. See 06 for placement and design.
3. **"Who made this" everywhere:** 06.
4. **Facebook re-scrape of the homepage** (the owner does it in the Sharing Debugger: "Scrape Again").
5. **IndexNow** after every deploy.

## C. The Long After: finish to v6
The full order is in 04. Short version:
1. tooling
2. reports
3. writing fixes in 15 steps
4. content freeze
5. design
6. release

## D. Outreach and submissions (owner actions; packets ready)
`docs/SUBMISSIONS.md` and `docs/SUBMISSION-PACKETS.md`:
- **Gmail drafts:** review and send the 4.
- **Forms:** VAWnet, Curlie (3 sites).
- **Records and accounts:**
  - Open Library (14 records)
  - Zenodo (the Decoder dataset, a DOI)
  - ORCID
  - Goodreads
  - Internet Archive
  - llms.txt directories
  - 8 university library guides
- **Later:** Wikipedia and Wikidata, only after independent coverage.

## E. Older open items (from MEMORY.md)
- **Fractal²:** v6 is in the repo and v5 is live. The owner decides deploy or rollback, and a real-phone test is owed.
- **`/fractal/entertainment`:** the redirect leads to a 404 (02, incident 10).
- **SOVEREIGN defined terms on Feminine pages:** waiting on the owner's yes.
- **The Weighing:** check its live status before claiming anything.
