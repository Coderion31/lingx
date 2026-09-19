# -*- coding: utf-8 -*-
import re, os

BASE = r"C:\Users\bunse\OneDrive\Документы\MultiTool\HomeChats\Chat-7"

# Hub dark palette as :root
HUB_ROOT = ':root{--bg:#0f172a;--card:#1e293b;--text:#e2e8f0;--text2:#94a3b8;--border:#334155;--hover:#1e293b;--active:#1e3a5f;--accent:#60a5fa;--accent2:#3b82f6;--ok:#48bb78;--okbg:#1a2e1a;--err:#fc8181;--errbg:#2e1a1a;--code-bg:#1a2332;--shadow:rgba(0,0,0,0.3);--editor-bg:#1a2332;--header-bg:#1a2332}'

# Old light palette as .light class
LIGHT_CLASS = '.light{--bg:#f0f4f8;--card:#fff;--text:#1e293b;--text2:#475569;--border:#e2e8f0;--hover:#f1f5f9;--active:#eff6ff;--accent:#2563eb;--accent2:#1d4ed8;--ok:#38a169;--okbg:#f0fff4;--err:#e53e3e;--errbg:#fff5f5;--code-bg:#f1f5f9;--shadow:rgba(0,0,0,0.05);--editor-bg:#f8fafc;--header-bg:#fff}'

LANGS = ['python', 'cpp', 'c', 'csharp', 'html', 'css', 'js']

for lang in LANGS:
    fp = os.path.join(BASE, lang, 'index.html')
    if not os.path.exists(fp):
        print(f"SKIP {lang}: no file")
        continue

    with open(fp, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Replace :root{...} with hub dark
    text = re.sub(
        r':root\{[^}]+\}',
        HUB_ROOT,
        text,
        count=1
    )

    # 2. Replace .dark{...} with .light{...} (old light palette)
    text = re.sub(
        r'\.dark\{[^}]+\}',
        LIGHT_CLASS,
        text,
        count=1
    )

    # 3. Fix JS: default dark = true (or localStorage !== 'light')
    # Patterns: let dark=...(P+'_theme')==='dark'... or let dark = ...
    text = re.sub(
        r'(let\s+dark\s*=\s*(localStorage\.getItem\([^)]+\)\s*===\s*[\'"])(dark)([\'"]\s*))',
        r'\1light\4',
        text,
        count=1
    )
    # Fallback for: let dark = ...
    text = re.sub(
        r'(let\s+dark\s*=\s*)(true|false)',
        r'\1true',
        text,
        count=1
    )

    # 4. Replace if(dark)body.classList.add('dark') → if(!light) body.classList.remove('dark'); body.classList.toggle('dark',true);
    # Actually simpler: change class toggle
    # Find: if\s*\(dark\)\s*[^.]*\.classList\.add\(['"]dark['"]\)
    # Replace with: if(dark) { document.body.classList.add('dark'); document.body.classList.remove('light'); } else { document.body.classList.remove('dark'); document.body.classList.add('light'); }
    # But dark is now default, so we need to flip the toggle logic
    # Instead let me find the init block and fix it
    text = re.sub(
        r'if\s*\(dark\)\s*document\.body\.classList\.add\([\'"]dark[\'"]\)',
        r"if(dark){document.body.classList.add('dark')}else{document.body.classList.add('light')}",
        text,
        count=1
    )

    # Find toggleTheme and fix class swapping
    text = re.sub(
        r'(function toggleTheme\(\)\{)([^}]+)(\}\s*function)',
        lambda m: m.group(1) + '''
dark=!dark;
localStorage.setItem(P+'_theme',dark?'dark':'light');
if(dark){document.body.classList.remove('light');document.body.classList.add('dark')}
else{document.body.classList.remove('dark');document.body.classList.add('light')}
''' + m.group(3),
        text,
        count=1
    )

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"OK {lang}")