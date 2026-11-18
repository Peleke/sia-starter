"""Print a Dify DSL export with escaped text decoded, so prompts are readable.

Usage: uv run --with pyyaml python scripts/decode_dify.py app.yml
Line numbers change after decoding; cite the original file as `path:line [node-id]`.
"""
import sys
import yaml

print(yaml.safe_dump(yaml.safe_load(open(sys.argv[1], encoding="utf-8")), allow_unicode=True, sort_keys=False))
