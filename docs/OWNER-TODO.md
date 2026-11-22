# Your to-do list (only you can do these)

Your domain's DNS is at **SiteGround** (nameservers ns1/ns2.siteground.net), so that's where the two records go.

## 1. Google Search Console (~10 min) — most important
1. Open https://search.google.com/search-console and sign in with your Google account.
2. Click **Add property** → choose **Domain** (left box) → type `noblefathercreations.com` → **Continue**.
3. Google shows a TXT record starting `google-site-verification=…`. Click **Copy**. Leave this tab open.
4. In a new tab open https://my.siteground.com → **Websites** → noblefathercreations.com → **Site Tools** →
   **Domain** → **DNS Zone Editor** → **TXT** tab.
5. Name: leave blank (or `@`). Value: paste the Google text. TTL: default. Click **Create**.
6. Back in Search Console click **Verify**. If it says not found, wait 10–30 minutes and press Verify again.
7. Once verified: left menu **Sitemaps** → enter `sitemap.xml` → **Submit**. (It lists every book's sitemap.)
8. Optional: **URL inspection** → paste `https://noblefathercreations.com/` → **Request indexing**. Repeat for
   `/fracture`, `/feminine`, `/children`, `/festival`, `/wook`, `/fractal`, `/faith`.

## 2. Bing Webmaster Tools (~3 min) — also feeds ChatGPT search, Copilot and DuckDuckGo
1. Open https://www.bing.com/webmasters and sign in.
2. Choose **Import from Google Search Console** → allow → tick noblefathercreations.com → **Import**.
   (Do step 1 first. This copies verification and the sitemap; nothing else needed.)
3. Check **Sitemaps** shows `https://noblefathercreations.com/sitemap.xml`; if not, **Submit sitemap** and paste it.

## 3. Let me reach the playbook update (pick ONE)
The files are in a private repo on another account (`miakamikee1101-collab/mieee`) and the three Claude pages aren't
shared with this account, so I can't download them.
- **Easiest:** download `0_HANDOFF_AND_STANDARD_LIST.zip` (and the `playbook_update` files) while signed in to that
  GitHub account, then attach them in this chat.
- **Or:** in that repo go to **Settings → Collaborators → Add people** → invite `noblefathercreations`, accept the
  invite, then reconnect at https://claude.ai/connect-github and tell me "added".
- **Or:** open each Claude page (Downloads, Project Guide, Combo Tiers Map) → **Share** → **Anyone with the link**.

## 4. Later, optional
- Off-site steps (resource pages, directories): drafts only, you send them — `docs/OFFSITE-PLAN.md`.
- Check results in Search Console → **Pages** and **Performance** after 1–2 weeks.
