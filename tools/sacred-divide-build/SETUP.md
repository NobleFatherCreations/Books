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
