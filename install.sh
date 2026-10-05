#!/bin/sh
# Install or update Form Filler. Safe to re-run: the skill is refreshed,
# your store (~/application-agent) is only created if missing — never overwritten.
set -e
cd "$(dirname "$0")"

SKILL_DIR="$HOME/.claude/skills/apply"
DATA_DIR="${APPLY_BASE:-$HOME/application-agent}"

mkdir -p "$SKILL_DIR"
cp skills/apply/SKILL.md skills/apply/setup_form.py "$SKILL_DIR/"

# Copy template files that don't exist yet; leave every existing file alone.
(cd template && find . -type f) | while read -r f; do
  if [ ! -e "$DATA_DIR/$f" ]; then
    mkdir -p "$DATA_DIR/$(dirname "$f")"
    cp "template/$f" "$DATA_DIR/$f"
  fi
done
mkdir -p "$DATA_DIR/research" "$DATA_DIR/applications"

echo "🐆 Form Filler installed."
echo "   skill: $SKILL_DIR"
echo "   data:  $DATA_DIR (your files are never overwritten)"
echo "   Next: open Claude Code and run  /apply setup"
