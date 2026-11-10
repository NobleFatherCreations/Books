Run from the repository root. Needs Node + Playwright (Chromium at /opt/pw-browsers/chromium or set CHROMIUM=...), Python 3 with numpy and Pillow.
  node scripts/design-gates.mjs <url> <outdir>            visual gates v2 (read contact.jpg first)
  node scripts/capture-references.mjs                     benchmark reference screenshots
  node scripts/blind-compare.mjs ab <A> <B> <out>         bake-off / five-second tests
  python3 scripts/vendor-lib.py <pkg> --approved-by "..."  vendor a library locally with its licence
Copy skill/design-director to .claude/skills/. Templates are copied into each project.
