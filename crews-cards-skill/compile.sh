#!/usr/bin/env bash
# Compile a CREWS cards Markdown file to PDF via pandoc + typst.
#
# Usage:
#   bash compile.sh <input.md> <format>
#
# Arguments:
#   input.md — path to a crews-cards Markdown file (ending in -cards.md)
#   format   — either "3x5" or "letter"
#
# Outputs three files alongside the input:
#   <stem>-body.typ       (pandoc output)
#   <stem>-final.typ      (preamble + body concatenated)
#   <stem>-<format>.pdf   (typst output)
#
# Requires: pandoc, typst on PATH. Verdana font if available; typst will
# fall back to its default sans-serif and warn if not.

set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: bash compile.sh <input.md> <format>" >&2
  echo "  <format> is '3x5' or 'letter'" >&2
  exit 1
fi

INPUT="$1"
FORMAT="$2"

if [ ! -f "$INPUT" ]; then
  echo "Error: input file not found: $INPUT" >&2
  exit 1
fi

case "$FORMAT" in
  3x5|letter) ;;
  *)
    echo "Error: format must be '3x5' or 'letter' (got '$FORMAT')" >&2
    exit 1
    ;;
esac

# Check for required tools.
for tool in pandoc typst; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "Error: $tool not found on PATH. Install with 'brew install $tool' on macOS." >&2
    exit 1
  fi
done

# Resolve the skill directory (where this script and the preambles live).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PREAMBLE="$SCRIPT_DIR/preamble-$FORMAT.typ"

if [ ! -f "$PREAMBLE" ]; then
  echo "Error: preamble not found: $PREAMBLE" >&2
  exit 1
fi

# Derive stem and output paths.
INPUT_DIR="$(cd "$(dirname "$INPUT")" && pwd)"
INPUT_BASE="$(basename "$INPUT" .md)"
STEM="$INPUT_DIR/$INPUT_BASE"

BODY="$STEM-body.typ"
FINAL="$STEM-final.typ"
PDF="$STEM-$FORMAT.pdf"

# Compile.
pandoc "$INPUT" -o "$BODY" --to typst --from markdown+hard_line_breaks
cat "$PREAMBLE" "$BODY" > "$FINAL"
typst compile "$FINAL" "$PDF"

echo "Compiled: $PDF"
