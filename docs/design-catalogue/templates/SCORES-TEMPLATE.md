# SCORES: copy to `content/<project>/design/SCORES.md`. The exit gate reads the json block.
Fixed rubric (do not change between rounds, so rounds are comparable): hierarchy, type, space, craft, distinctiveness, feeling, phone, legibility, continuity. Each 1-5. Threshold 4.
Fixed capture: `node scripts/capture-critic-set.mjs <url> <outdir>` (same frames every round). The critic is a FRESH agent each round, given only the captures, the brief and this rubric.
Record the build hash with `node scripts/design-exit.mjs --sha <build files>`.

```json
{"threshold":4,"rounds":[
 {"round":1,"date":"YYYY-MM-DD","sha":"","scores":{"hierarchy":0,"type":0,"space":0,"craft":0,"distinctiveness":0,"feeling":0,"phone":0,"legibility":0,"continuity":0},
  "weaknesses":[{"id":"W1","text":"","status":"open"}]}
]}
```

## Low-score protocol (mandatory for every score below 4)
For each low score write, below, three candidate solutions that come from DIFFERENT places (a catalogue category in 06, a benchmark in references/, a first-principles idea). Build or mock each (comp or A/B screenshot), read the results, choose one, say why, apply it, then run a NEW scored round. Record candidates and the choice here.
