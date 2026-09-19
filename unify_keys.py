# -*- coding: utf-8 -*-
import os, re

BASE = r"C:\Users\bunse\OneDrive\Документы\MultiTool\HomeChats\Chat-7"

LANGS = {
    'python': 'py',
    'cpp': 'cpp',
    'c': 'c',
    'csharp': 'csharp',
    'html': 'html',
    'css': 'css',
    'js': 'js',
}

# pfx map: lang folder -> actual localStorage prefix used
PFX = {'python':'py', 'cpp':'cpp', 'c':'c', 'csharp':'csharp', 'html':'html', 'css':'css', 'js':'js'}

# Files that use P+ prefix (template-based): c, csharp, html, css, js use `P`
# python and cpp use literal prefix strings.

for lang in LANGS:
    fp = os.path.join(BASE, lang, 'index.html')
    if not os.path.exists(fp):
        print(f"SKIP {lang}")
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Unify localStorage keys -> lingx_
    # For template files: P+'_theme' -> 'lingx_theme', P+'_email', P+'_progress' etc
    text = re.sub(r"P\+'_theme'", "'lingx_theme'", text)
    text = re.sub(r"P\+'_email'", "'lingx_email'", text)
    text = re.sub(r"P\+'_progress'", "'lingx_progress'", text)
    text = re.sub(r"P\+'_progress_'\s*\+\s*email", "'lingx_progress_'+email", text)

    # For python/cpp literal prefix (e.g. 'py_theme', 'cpp_email')
    pfx = PFX[lang]  # 'py' for python, 'cpp' for cpp, etc.
    for k in ['theme', 'email', 'progress']:
        text = re.sub(rf"'{pfx}_{k}'", f"'lingx_{k}'", text)
    text = re.sub(rf"'{pfx}_progress_'\s*\+\s*email", "'lingx_progress_'+email", text)

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"OK {lang}")