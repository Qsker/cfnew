#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."

echo "=== 1/4: Save current frontend ==="
MY_TERM=$(mktemp)
MY_PAGE=$(mktemp)
my_term_start=$(grep -n "const terminalHtml = \`" index.js | head -1 | cut -d: -f1)
my_page_start=$(grep -n "const pageHtml = \`" index.js | head -1 | cut -d: -f1)
my_term_end=$(awk "NR>=$my_term_start && /^\`;\$/{print NR; exit}" index.js)
my_page_end=$(awk "NR>=$my_page_start && /^\`;\$/{print NR; exit}" index.js)
sed -n "${my_term_start},${my_term_end}p" index.js > "$MY_TERM"
sed -n "${my_page_start},${my_page_end}p" index.js > "$MY_PAGE"
echo "  terminalHtml lines $my_term_start-$my_term_end (backed up)"
echo "  pageHtml     lines $my_page_start-$my_page_end (backed up)"

echo "=== 2/4: Pull upstream (Qsker/cfnew) ==="
git fetch upstream 2>&1 || {
  echo "No upstream remote, adding Qsker/cfnew..."
  git remote add upstream https://github.com/Qsker/cfnew.git
  git fetch upstream
}
git merge upstream/main --no-edit 2>&1 || echo "⚠️  Merge conflicts — resolve them manually, then re-run this script"

echo "=== 3/4: Restore our frontend ==="
export MY_TERM_PATH="$MY_TERM"
export MY_PAGE_PATH="$MY_PAGE"
python3 << 'PYEOF'
import re, os

with open('index.js', 'r') as f:
    content = f.read()

my_term_path = os.environ['MY_TERM_PATH']
my_page_path = os.environ['MY_PAGE_PATH']

with open(my_term_path, 'r') as f:
    new_term = f.read()
with open(my_page_path, 'r') as f:
    new_page = f.read()

content = re.sub(
    r'const terminalHtml = `.*?^`;',
    new_term,
    content,
    flags=re.DOTALL | re.MULTILINE
)

content = re.sub(
    r'const pageHtml = `.*?^`;',
    new_page,
    content,
    flags=re.DOTALL | re.MULTILINE
)

with open('index.js', 'w') as f:
    f.write(content)
print("  Templates restored.")
PYEOF
rm -f "$MY_TERM" "$MY_PAGE"

echo "=== 4/4: Verify ==="
node -c index.js && echo "  ✅ Syntax OK"
echo ""
echo "Done. Run 'wrangler deploy' to deploy."
