#!/usr/bin/env python3
"""Record a findability round in sites.json: version, changelog entry, folder as repoPath.
Usage: python3 scripts/seo/ledger.py <slug> <version> "<summary>" [repoPath]"""
import json, sys, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
slug, ver, summary = sys.argv[1:4]
repo = sys.argv[4] if len(sys.argv) > 4 else None
p = ROOT / "sites.json"
d = json.loads(p.read_text())
for proj in d["projects"]:
    if proj["url"].rstrip("/").rsplit("/", 1)[-1] == slug:
        proj["version"] = ver
        cl = [c for c in proj.get("changelog", []) if c.get("version") != ver]
        proj["changelog"] = [{"date": datetime.date.today().isoformat(), "version": ver, "summary": summary}] + cl
        if repo:
            proj["repoPath"] = repo
        proj["pendingDeploy"] = {"note": f"Repo is AHEAD of live: {ver} findability round built {datetime.date.today()}, awaiting owner go-ahead to deploy."}
        break
else:
    sys.exit(f"no project {slug}")
p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
print(slug, ver, repo or "")
