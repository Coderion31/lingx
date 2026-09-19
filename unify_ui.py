# -*- coding: utf-8 -*-
import os, re

BASE = r"C:\Users\bunse\OneDrive\Документы\MultiTool\HomeChats\Chat-7"

# Hub nav+menu HTML snippet to inject
NAV_HTML = '''<div class="nav-bar">
<button onclick="history.back()" title="Назад">←</button>
<button onclick="location.href='/'" title="Домой">⌂</button>
<button onclick="history.forward()" title="Вперёд">→</button>
</div>

<button class="menu-btn" id="menuBtn" onclick="toggleMenu()">
<span></span><span></span><span></span>
</button>

<div class="menu-overlay" id="menuOverlay">
<div class="menu-items" onclick="closeMenu()">
<a href="/">Главная</a>
<a href="/python/">Python</a>
<a href="/cpp/">C++</a>
<a href="/c/">C</a>
<a href="/csharp/">C#</a>
<a href="/html/">HTML</a>
<a href="/css/">CSS</a>
<a href="/js/">JavaScript</a>
</div>
<div class="menu-bottom">
<div class="menu-account" id="menuAccount" style="display:none">
<div class="acc-avatar" id="accAvatar"></div>
<div class="acc-info"><span id="accName"></span><span id="accEmail"></span></div>
</div>
<button class="menu-settings" onclick="openSettings()">Настройки</button>
</div>
</div>'''

# CSS for nav and menu (to inject into <style>)
NAV_CSS = '''
.nav-bar{position:fixed;top:16px;right:68px;display:flex;gap:2px;z-index:100;background:rgba(255,255,255,0.06);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-radius:22px;border:1px solid rgba(255,255,255,0.1);padding:4px;height:44px}
.nav-bar button{background:transparent;border:none;color:rgba(255,255,255,0.7);padding:8px 14px;cursor:pointer;border-radius:18px;font-size:16px;transition:.3s;display:flex;align-items:center;justify-content:center;height:36px;width:36px}
.nav-bar button:hover{background:rgba(255,255,255,0.12);color:#fff}
.menu-btn{position:fixed;top:16px;right:16px;width:44px;height:44px;border-radius:50%;border:none;background:rgba(255,255,255,0.08);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.15);cursor:pointer;z-index:100;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;transition:.3s}
.menu-btn:hover{background:rgba(255,255,255,0.15);transform:scale(1.05)}
.menu-btn span{display:block;width:18px;height:2px;background:rgba(255,255,255,0.8);border-radius:2px;transition:.3s}
.menu-overlay{position:fixed;top:12px;left:12px;bottom:12px;width:280px;background:rgba(15,23,42,0.92);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-radius:20px;z-index:99;transform:translateX(-110%);transition:transform .35s ease;display:flex;flex-direction:column;padding:80px 16px 16px;border:1px solid rgba(255,255,255,0.08)}
.menu-overlay.open{transform:translateX(0)}
.menu-items{display:flex;flex-direction:column;gap:8px;width:100%;flex:1}
.menu-items a{color:#e2e8f0;text-decoration:none;font-size:16px;font-weight:500;padding:10px 16px;border-radius:100px;background:rgba(255,255,255,0.04);transition:.3s;display:block}
.menu-items a:hover{background:rgba(255,255,255,0.1)}
.menu-bottom{margin-top:auto;width:100%;display:flex;flex-direction:column;gap:8px}
.menu-account{display:flex;align-items:center;gap:10px;width:100%;padding:10px 14px;border-radius:100px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.08)}
.acc-avatar{width:32px;height:32px;border-radius:50%;background:rgba(255,255,255,0.12);display:flex;align-items:center;justify-content:center;color:#e2e8f0;font-size:13px;font-weight:600;flex-shrink:0}
.acc-info{display:flex;flex-direction:column;overflow:hidden}
.acc-info span:first-child{font-size:13px;font-weight:500;color:#e2e8f0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.acc-info span:last-child{font-size:11px;color:#94a3b8;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.menu-settings{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;padding:12px 16px;border-radius:100px;border:1px solid rgba(255,255,255,0.1);background:rgba(255,255,255,0.06);color:#cbd5e1;cursor:pointer;font-size:14px;font-weight:500;transition:.3s}
.menu-settings:hover{background:rgba(255,255,255,0.12);color:#fff}
'''

LANGS = ['python', 'cpp', 'c', 'csharp', 'html', 'css', 'js']

for lang in LANGS:
    fp = os.path.join(BASE, lang, 'index.html')
    with open(fp, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Inject NAV_CSS before @media
    text = text.replace('@media', NAV_CSS + '\n@media', 1)

    # 2. Inject NAV_HTML after <body>
    text = text.replace('<body>', '<body>\n' + NAV_HTML, 1)

    # 3. Add JS functions. Find the end of </script> and add before it
    # Add toggleMenu, closeMenu, updateAccountUI
    JS_ADD = '''
function toggleMenu(){document.getElementById('menuOverlay').classList.toggle('open')}
function closeMenu(){document.getElementById('menuOverlay').classList.remove('open')}
function syncAccount(){
const ue=localStorage.getItem('lingx_email')||'';
const tok=localStorage.getItem('lingx_token')||'';
const av=document.getElementById('accAvatar'),em=document.getElementById('accEmail'),nm=document.getElementById('accName'),bx=document.getElementById('menuAccount'),hbx=document.getElementById('hEmail'),hav=document.getElementById('hAvatar');
if(bx){bx.style.display=ue?'flex':'none'}
if(ue&&av)av.textContent=ue[0].toUpperCase();
if(ue&&nm)nm.textContent=ue.split('@')[0];
if(ue&&em)em.textContent=ue;
if(hav){hav.textContent=ue?ue[0].toUpperCase():'?';hav.onclick=function(){if(ue&&tok){localStorage.removeItem('lingx_token');localStorage.removeItem('lingx_email');localStorage.removeItem('lingx_verified');location.reload()}else{location.href='/'}}}
if(hbx)hbx.textContent=ue||'';
}
syncAccount();
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeMenu()});
'''
    text = text.replace('</script>', JS_ADD + '\n</script>', 1)

    # 4. Settings button in menu should go to hub (login/settings live there)
    text = text.replace(
        '<button class="menu-settings" onclick="openSettings()">Настройки</button>',
        '<button class="menu-settings" onclick="location.href=\'/\'">Настройки</button>'
    )

    # 5. Disable old local login modal in courses: clicking header avatar goes to hub
    # Remove old openLogin binding by overriding: replace function openLogin body if present
    text = text.replace(
        "function openLogin(){if(userEmail){logout();return;}",
        "function openLogin(){"
    )
    # For template files: openLogin sometimes triggers login modal. We add a fallback:
    if 'function openLogin' in text:
        text = text.replace(
            "function openLogin(){",
            "function openLogin(){location.href='/';return;"
        )

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"OK {lang}")