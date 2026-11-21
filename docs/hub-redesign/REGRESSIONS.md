# Homepage regressions (design-director law 2: every owner-reported fault becomes a check before its fix)

| Date | Owner's words | Cause | Guard (scripts/verify-hub.mjs) |
|---|---|---|---|
| 2026-11-20 | "any book cover that is cut off at the left and right edge" | Fixed 2:3 frames + object-fit:cover trimmed wider covers (Feminine, Festie Codex, Festie Bible); the source art for Fractal/Fracture/Sacred Divide was clipped | "every cover shows whole": each cover's box ratio must equal its image ratio (±2%); remade covers in content/covers/ |
| 2026-11-20 | "remove version update info for home page" | The old build inserted #updates | "no version/update notes" |
| 2026-11-21 | "someone who looks for an individual book isn't put off by seeing the religion one, or fractal one" | All 14 books were on one shelf | "bigger-picture books stay behind the door" (inert + zero height until opened) |
| 2026-11-21 | "NFC guide card should be ahead of castings and seals" | Blueprint order | "NFC guide card comes first in the Workshop row" |
| 2026-11-21 | "there shouldn't be a portal pendant as an icon for the wax seal and casting" | Blueprint reused pendant photos | "Press and Casting use their own icons" (no img in .card.soon) |
| 2026-11-21 | (found in audit) keyboard Tab walked into the hidden phone menu | .sheet{display:grid} overrode [hidden] | "closed phone menu is out of the tab order" |
| 2026-11-21 | "Please pull portal pendants from different sets at least so they aren't all the same" | All three photos (Clockwork, Ember square, Gear moon) were gear pieces from the same look | "Portals come from N different sets" (each figure carries data-set; all distinct, at least 3) |
