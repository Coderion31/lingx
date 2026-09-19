# -*- coding: utf-8 -*-
import os

BASE = r"C:\Users\bunse\OneDrive\Документы\MultiTool\HomeChats\Chat-7"
LANGS = ['python', 'cpp', 'c', 'csharp', 'html', 'css', 'js']

NAMES = {
    'python': 'Python',
    'cpp': 'C++',
    'c': 'C',
    'csharp': 'C#',
    'html': 'HTML',
    'css': 'CSS',
    'js': 'JavaScript'
}

for lang in LANGS:
    fp = os.path.join(BASE, lang, 'index.html')
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    name = NAMES[lang]

    # 1. Update <title>
    old_title = f'<title>{name} Academy</title>'
    new_title = f'<title>{name} — LingX</title>'
    text = text.replace(old_title, new_title)

    # 2. In the nav-bar header area there's no logo element anymore,
    # but in python there's a leftover SVG (h-logo). Remove it since header is gone.
    # Actually just update the text: we don't need to add logos, titles say enough.

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"OK {lang}")