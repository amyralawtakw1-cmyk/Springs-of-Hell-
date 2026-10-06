"""Static checks that do not call external services."""
import ast
from pathlib import Path

source = Path("main.py").read_text(encoding="utf-8")
ast.parse(source)
assert "supercell.com/en/games/clashofclans/blog" in source
for forbidden in ("AQ.", "c848e673", "710722756852"):
    assert forbidden not in source, f"Found possible secret: {forbidden}"
print("OK: Python syntax, official-source, and secret-scan checks passed")
