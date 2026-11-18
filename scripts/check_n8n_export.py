"""Would this n8n export run as stored? Checks the wiring an export needs.

Usage: uv run python scripts/check_n8n_export.py workflow.json
n8n keys `connections` by source node *name*, and each target names a node too (n8n docs, workflow JSON).
"""
import json, sys

d = json.load(open(sys.argv[1]))
d = d.get("data", d)
nodes = {n["name"]: n for n in d.get("nodes", [])}
problems = []
for src, outs in d.get("connections", {}).items():
    if src not in nodes:
        problems.append(f"connection from unknown node {src!r}")
    for branch in outs.get("main", []):
        for t in branch or []:
            if t.get("node") not in nodes:
                problems.append(f"connection to unknown node {t.get('node')!r}")
wired = set(d.get("connections", {})) | {t["node"] for o in d.get("connections", {}).values() for b in o.get("main", []) for t in (b or [])}
loose = [n for n, v in nodes.items() if n not in wired and not v["type"].endswith("stickyNote")]
triggers = [n for n, v in nodes.items() if "trigger" in v["type"].lower() or v["type"].endswith((".cron", ".webhook", ".start"))]
print(f"nodes: {len(nodes)}  triggers: {triggers or 'none found'}  active: {d.get('active')}")
for n, v in nodes.items():
    if v["type"].endswith("noOp"):
        problems.append(f"{n!r} is a no-op placeholder")
    if v.get("credentials"):
        print(f"needs credentials: {n!r} -> {list(v['credentials'])}")
for p in problems:
    print("PROBLEM:", p)
if loose:
    print("not connected to anything:", loose)
print("would run as stored: " + ("no" if problems or loose else "yes, as far as wiring goes (credentials and data not checked)"))
