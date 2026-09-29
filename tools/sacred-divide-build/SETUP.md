# Sacred Divide v5: build tooling

Build-time only; nothing here is loaded by a live page (rule: no external requests).

    npm install            # in this folder
    pip install -r requirements.txt
    apt-get install -y poppler-utils qpdf ghostscript imagemagick sqlite3
    # Chromium: pre-installed at /opt/pw-browsers (never run `playwright install`)

Page size for print: **US Letter (8.5 x 11 in)**, decided 2026-09-29. v4 PDFs were A4.

## Claude plugins to enable (claude.ai, done by the account owner)
Axe Accessibility, ADA PDF Compliance (privileged access: read its permissions),
ux-ui-audit, jp-web-design-guardrails, Design (Anthropic), design-skills.
Enable via claude.ai > Settings > Plugins (or the install card in the session), then confirm with ListPlugins.

## Upstream links (unverified from the build container; github.com returned 403 there)
- https://github.com/dequelabs/axe-accessibility
- https://github.com/anthropics/knowledge-work-plugins
- https://github.com/microsoft/playwright-mcp
- https://github.com/veraPDF/veraPDF-library (PDF/UA validator; not installable via pip)

## Installed 2026-09-29 (project scope, recorded in .claude/settings.json)
Marketplaces: anthropics/skills, anthropics/knowledge-work-plugins, dequelabs/axe-accessibility.
Plugins: example-skills, document-skills, design@knowledge-work-plugins, axe-accessibility@deque.
New sessions are prompted to install them from settings.json.

### Axe: owner action needed (account credential, cannot be done by the agent)
1. Run `/axe-accessibility:mcp-setup`, choose API key or OAuth.
   - API key: create one in the Axe Account Portal (API Keys > "Axe MCP Server"), then `export AXE_API_KEY=...`
   - OAuth: `npx -y @deque/axe-auth login` (browser PKCE; token kept in OS keychain)
2. Verify with `/mcp`, then `/axe-accessibility:mcp-generate-instructions all`.
Note: the bundled MCP runs `npx -y axe-mcp-server` and talks to Deque's service.

### Still claude.ai-side (owner enables): ADA PDF Compliance, ux-ui-audit, jp-web-design-guardrails, design-skills.

### veraPDF 1.30.2
Installed from https://software.verapdf.org/releases/verapdf-installer.zip (headless izpack). Not in the repo (binary).
Baseline: v4 Catholicism PDF fails PDF/UA-1 on 7 rules (14,838 untagged content marks, no XMP metadata stream,
327 links lacking /Contents, 3 figures without alt, 83 malformed LI). Target for v5: zero failures.
