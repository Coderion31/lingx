# -*- coding: utf-8 -*-
import os, re

BASE = r"C:\Users\bunse\OneDrive\Документы\MultiTool\HomeChats\Chat-7"
LANGS = ['cpp', 'c', 'csharp', 'html', 'css', 'js']

for lang in LANGS:
    fp = os.path.join(BASE, lang, 'index.html')
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # 1. updateUserUI: make null-safe
    text = re.sub(
        r'function updateUserUI\(\).*?(?=\nfunction)',
        '''function updateUserUI(){const av=document.getElementById('hAvatar'),em=document.getElementById('hEmail');if(!av&&!em)return;if(userEmail){if(av){av.textContent=userEmail[0].toUpperCase();av.title='Выйти'}if(em)em.textContent=userEmail}else{if(av){av.textContent='?';av.title='Войти'}if(em)em.textContent=''}}''',
        text,
        count=1,
        flags=re.DOTALL
    )

    # 2. updateThemeBtn: null-safe
    text = re.sub(
        r'function updateThemeBtn\(\).*?(?=\nfunction)',
        "function updateThemeBtn(){const tb=document.getElementById('themeBtn');if(tb)tb.textContent=dark?'🌙':'☀️'}",
        text,
        count=1,
        flags=re.DOTALL
    )

    # 3. updateStats: null-safe
    text = re.sub(
        r"function updateStats\(\).*?(?=\nfunction)",
        "function updateStats(){const{t,d}=stats();const st=document.getElementById('statsText');if(st)st.textContent='Решено: '+d+' / '+t;const pb=document.getElementById('prBar');if(pb)pb.style.width=t?(d/t*100)+'%':'0%';renderSidebar()}",
        text,
        count=1,
        flags=re.DOTALL
    )

    # 4. syncAccount: null-safe
    if 'function syncAccount' in text:
        text = re.sub(
            r'function syncAccount\(\).*?(?=\nfunction|\n\n)',
            "function syncAccount(){const ue=localStorage.getItem('lingx_email')||'',tok=localStorage.getItem('lingx_token')||'',hav=document.getElementById('hAvatar'),hem=document.getElementById('hEmail');if(!hav&&!hem)return;if(hav)hav.textContent=ue?ue[0].toUpperCase():'?';if(hem)hem.textContent=ue||''}",
            text,
            count=1,
            flags=re.DOTALL
        )

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"OK {lang}")