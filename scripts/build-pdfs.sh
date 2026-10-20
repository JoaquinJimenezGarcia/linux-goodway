#!/usr/bin/env bash
# Build sorted lesson PDFs from Markdown sources.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LESSONS_DIR="$ROOT/lessons"
PDFS_DIR="$ROOT/pdfs"
TEMPLATE="$ROOT/templates/lesson.yaml"

mkdir -p "$PDFS_DIR"

ENGINE=""
if command -v typst >/dev/null 2>&1; then
  ENGINE="typst"
elif command -v xelatex >/dev/null 2>&1; then
  ENGINE="xelatex"
elif command -v pdflatex >/dev/null 2>&1; then
  ENGINE="pdflatex"
else
  echo "No PDF engine found. Install typst: brew install typst" >&2
  exit 1
fi

if ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc not found. Install with: brew install pandoc" >&2
  exit 1
fi

count=0
for lesson in "$LESSONS_DIR"/*/lesson.md; do
  [[ -f "$lesson" ]] || continue
  dir="$(dirname "$lesson")"
  slug="$(basename "$dir")"
  out="$PDFS_DIR/${slug}.pdf"
  echo "Building $slug -> $out (engine=$ENGINE)"
  pandoc "$lesson" \
    --metadata-file="$TEMPLATE" \
    --pdf-engine="$ENGINE" \
    -V geometry:margin=1in \
    -o "$out"
  count=$((count + 1))
done

echo "Built $count PDFs into $PDFS_DIR"
ls -1 "$PDFS_DIR" | sort
