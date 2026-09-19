# -*- coding: utf-8 -*-
import os

BASE = r"C:\Users\bunse\OneDrive\Документы\MultiTool\HomeChats\Chat-7"
LANGS = ['c', 'csharp', 'html', 'css', 'js']

for lang in LANGS:
    fp = os.path.join(BASE, lang, 'index.html')
    with open(fp, 'r', encoding='utf-8') as f:
        text = f.read()

    # Fix broken dark init: ==='dark'light'  ->  !== 'light'
    text = text.replace(
        "let dark=localStorage.getItem(P+'_theme')==='dark'light';",
        "let dark=localStorage.getItem(P+'_theme')!=='light';"
    )

    # Fix init class: replace the line
    text = text.replace(
        "if(dark){document.body.classList.add('dark')}else{document.body.classList.add('light')};",
        "if(!dark){document.body.classList.add('light')};"
    )

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"OK {lang}")