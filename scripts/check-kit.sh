#!/usr/bin/env bash
# Self-check for the kit: every README command runs, every relative link resolves,
# every named cross-reference exists. Run before each commit that touches docs or templates.
set -uo pipefail
cd "$(dirname "$0")/.."
fail=0; note() { echo "FAIL: $*"; fail=1; }

# 1. README commands (the script ones; uv sync assumed done)
uv run python notebooks/ea_dose_curve.py >/dev/null 2>&1 || note "bundled run"
uv run python notebooks/ea_dose_curve.py --cells data/example-own.csv >/dev/null 2>&1 || note "own-data run"
uv run python notebooks/ea_dose_curve.py --cells data/example-baseline.csv 2>&1 | grep -q "A/A check" || note "A/A run"
[ -f out/example-baseline.png ] || note "A/A run wrote no figure"
printf 'a: "\\u5b89"\n' > /tmp/sia-dify.yml
uv run --with pyyaml python scripts/decode_dify.py /tmp/sia-dify.yml | grep -q "安" || note "decode_dify"
printf '{"nodes":[{"name":"T","type":"n8n-nodes-base.webhook"},{"name":"A","type":"x.noOp"}],"connections":{"T":{"main":[[{"node":"B"}]]}}}' > /tmp/sia-n8n.json
uv run python scripts/check_n8n_export.py /tmp/sia-n8n.json | grep -q "would run as stored: no" || note "check_n8n_export misses broken wiring"
uv run --extra notebook jupytext --to ipynb -o /tmp/sia-check.ipynb notebooks/ea_dose_curve.py >/dev/null 2>&1 || note "jupytext command"

# 2. Relative links in every markdown file resolve (paths in templates are relative to templates/)
while IFS= read -r f; do
  dir=$(dirname "$f")
  grep -oE '\]\([^)#]+' "$f" | sed 's/^](//' | grep -vE '^(https?:|mailto:)' | while read -r l; do
    [ -e "$dir/$l" ] || echo "FAIL: $f links to missing $l"
  done
done < <(find . -name '*.md' -not -path './.venv/*' -not -path './out/*') | tee /tmp/sia-check-links.txt
[ -s /tmp/sia-check-links.txt ] && fail=1

# 3. Named cross-references
grep -rl 'README section "Agent versions"' templates >/dev/null && ! grep -q '^## Agent versions' README.md && note 'templates cite README "Agent versions" but README has no such section'
grep -rq "install section" templates README.md docs && note '"install section" referenced'
grep -q 'example-baseline.csv' README.md && [ ! -f data/example-baseline.csv ] && note "README cites data/example-baseline.csv, missing"
for t in signal-card gold-set; do grep -q '_Example' templates/$t.md || note "README promises an example in $t.md"; done

# 3b. One citation format
grep -n "path#node-id" templates/*.md docs/*.md | grep -v "path:line \[node-id\]" && note "old citation format"

# 4. No absolute links to this kit's own GitHub inside templates (they get copied and the repo may be private)
grep -n 'github.com/Peleke/sia-starter' templates/*.md && note "absolute self-links in templates"
exit $fail
