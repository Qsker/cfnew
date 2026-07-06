#!/usr/bin/env python3
import re

with open('index.js', 'r') as f:
    content = f.read()

# === Common theme button CSS ===
theme_btn_css = '''
            .theme-btn {
                background: none;
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 4px 8px;
                cursor: pointer;
                font-size: 16px;
                line-height: 1;
                transition: all 0.2s;
            }
            .theme-btn:hover {
                background: var(--surface-strong);
                border-color: var(--accent);
            }'''

# Insert theme button CSS after first <style>
first_style = content.find('<style>')
first_style_end = content.find('>', first_style)
content = content[:first_style_end+1] + '\n' + theme_btn_css + content[first_style_end+1:]

# === Add toggle button to lang-bar (terminal template, then page template) ===
# Terminal template lang-bar
old_term_bar = '''        <div class="lang-bar">
            <select id="languageSelector" onchange="changeLanguage(this.value)">
                <option value="zh" ${!isFarsi ? 'selected' : ''}>🇨🇳 中文</option>
                <option value="fa" ${isFarsi ? 'selected' : ''}>🇮🇷 فارسی</option>
            </select>
        </div>'''

new_bar = '''        <div class="lang-bar">
            <select id="languageSelector" onchange="changeLanguage(this.value)">
                <option value="zh" ${!isFarsi ? 'selected' : ''}>🇨🇳 中文</option>
                <option value="fa" ${isFarsi ? 'selected' : ''}>🇮🇷 فارسی</option>
            </select>
            <button id="themeToggle" class="theme-btn" onclick="toggleTheme()" title="切换主题">🎨</button>
        </div>'''

content = content.replace(old_term_bar, new_bar, 1)

# Page template lang-bar (second occurrence)
content = content.replace(old_term_bar, new_bar, 1)

# === Theme JS for terminal template ===
theme_js = '''
        <script>
            (function() {
                var saved = localStorage.getItem('cfnew-theme');
                if (saved === 'antfu') {
                    document.documentElement.classList.add('theme-antfu');
                    var btns = document.querySelectorAll('#themeToggle');
                    btns.forEach(function(b) { b.textContent = '🌙'; });
                    var s1 = document.getElementById('theme-antfu');
                    var s2 = document.getElementById('theme-antfu-page');
                    if (s1) s1.disabled = false;
                    if (s2) s2.disabled = false;
                }
                document.addEventListener('click', function(e) {
                    if (e.target && e.target.id === 'themeToggle') {
                        var root = document.documentElement;
                        var isAntfu = root.classList.toggle('theme-antfu');
                        localStorage.setItem('cfnew-theme', isAntfu ? 'antfu' : 'default');
                        var btns = document.querySelectorAll('#themeToggle');
                        btns.forEach(function(b) { b.textContent = isAntfu ? '🌙' : '🎨'; });
                        var s1 = document.getElementById('theme-antfu');
                        var s2 = document.getElementById('theme-antfu-page');
                        if (s1) s1.disabled = !isAntfu;
                        if (s2) s2.disabled = !isAntfu;
                    }
                });
            })();
        </script>'''

# Insert theme JS before the terminal template's closing backtick
term_backtick = content.find('`;', content.find('handleUUIDInput'))
if term_backtick > 0:
    term_close_html = content.rfind('</html>', 0, term_backtick)
    if term_close_html > 0:
        content = content[:term_close_html+7] + theme_js + content[term_close_html+7:]

# Insert theme JS before the page template's closing backtick
page_backtick = content.find('`;', content.find('const pageHtml'))
if page_backtick > 0:
    page_close_html = content.rfind('</html>', 0, page_backtick)
    if page_close_html > 0:
        content = content[:page_close_html+7] + theme_js + content[page_close_html+7:]

with open('index.js', 'w') as f:
    f.write(content)

print('Done! Added theme toggle system')
