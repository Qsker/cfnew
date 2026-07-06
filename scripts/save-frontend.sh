#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
echo "Saving current frontend templates..."
my_term_start=$(grep -n "const terminalHtml = \`" index.js | head -1 | cut -d: -f1)
my_page_start=$(grep -n "const pageHtml = \`" index.js | head -1 | cut -d: -f1)
awk "NR>=$my_term_start && /^\`;\$/{print NR; exit}" index.js > /tmp/term_end.tmp
awk "NR>=$my_page_start && /^\`;\$/{print NR; exit}" index.js > /tmp/page_end.tmp
my_term_end=$(cat /tmp/term_end.tmp)
my_page_end=$(cat /tmp/page_end.tmp)
sed -n "${my_term_start},${my_term_end}p" index.js > scripts/my-terminal.html
sed -n "${my_page_start},${my_page_end}p" index.js > scripts/my-page.html
echo "  terminalHtml lines $my_term_start-$my_term_end → scripts/my-terminal.html"
echo "  pageHtml     lines $my_page_start-$my_page_end → scripts/my-page.html"
echo "Done."
