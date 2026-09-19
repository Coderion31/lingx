# -*- coding: utf-8 -*-
import os, re

BASE = r"C:\Users\bunse\OneDrive\Документы\MultiTool\HomeChats\Chat-7"
LANGS = ['python', 'cpp', 'c', 'csharp', 'html', 'css', 'js']

for lang in LANGS:
    fp = os.path.join(BASE, lang, 'index.html')
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # Remove entire <header>...</header> block (multiline)
    text = re.sub(r'<header>[^<]*(?:<(?!/header>)[^<]*)*</header>', '', text, count=1, flags=re.DOTALL)

    # Also remove header CSS rule (the line that starts with "header{")
    text = re.sub(r'\nheader\{[^}]*\}', '', text, count=1)

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"OK {lang}")