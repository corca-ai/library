#!/usr/bin/env python3
# 날짜 폴더(YYMMDD)를 스캔해 메인 index.html(지식나눔터)을 생성한다.
import os, re, html
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
DATE_RE  = re.compile(r'^\d{6}$')
TITLE_RE = re.compile(r'<title[^>]*>(.*?)</title>', re.S | re.I)

def title_of(path):
    try:
        with open(path, encoding='utf-8') as f:
            m = TITLE_RE.search(f.read())
        return html.unescape(m.group(1).strip()) if m else os.path.basename(path)
    except Exception:
        return os.path.basename(path)

def fmt_date(d):  # 260627 -> 2026.06.27
    return f"20{d[0:2]}.{d[2:4]}.{d[4:6]}"

folders = sorted((d for d in os.listdir(ROOT)
                  if DATE_RE.match(d) and os.path.isdir(os.path.join(ROOT, d))),
                 reverse=True)
cards, total = [], 0
for d in folders:
    day_root = os.path.join(ROOT, d)
    clean_dirs = sorted(
        f for f in os.listdir(day_root)
        if os.path.isfile(os.path.join(day_root, f, "index.html"))
    )
    clean_basenames = set(clean_dirs)
    files = sorted(
        f for f in os.listdir(day_root)
        if f.lower().endswith('.html') and os.path.splitext(f)[0] not in clean_basenames
    )
    if not files and not clean_dirs: continue
    lis = []
    for f in files:
        total += 1
        href = quote(f"{d}/{f}")
        lis.append(f'<li><a href="{href}">{html.escape(title_of(os.path.join(ROOT, d, f)))}</a></li>')
    for f in clean_dirs:
        total += 1
        href = quote(f"{d}/{f}/")
        lis.append(f'<li><a href="{href}">{html.escape(title_of(os.path.join(ROOT, d, f, "index.html")))}</a></li>')
    cards.append(f'<section class="day"><div class="date">{fmt_date(d)}</div><ul>{"".join(lis)}</ul></section>')

body = "\n".join(cards) if cards else '<p class="empty">아직 올라온 번역이 없습니다.</p>'
page = f"""<!DOCTYPE html>
<html lang="ko"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>지식나눔터 — 해외 정보 한국어 번역 아카이브</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css">
<style>
:root{{--paper:#F4F5F3;--surface:#FFF;--ink:#16181C;--ink2:#5B6066;--line:#E4E6E1;--accent:#0F5A4E;}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);
font-family:'Pretendard Variable',Pretendard,system-ui,sans-serif;line-height:1.7;-webkit-font-smoothing:antialiased}}
.wrap{{width:min(92vw,720px);margin:0 auto;padding:64px 0 96px}}
header h1{{font-size:30px;margin:0 0 8px}}header p{{color:var(--ink2);margin:0 0 8px;font-size:16px}}
.count{{color:var(--accent);font-size:14px;font-weight:600}}
.day{{margin-top:40px;border-top:1px solid var(--line);padding-top:20px}}
.date{{font-size:14px;font-weight:600;color:var(--accent);letter-spacing:.04em;margin-bottom:12px}}
ul{{list-style:none;margin:0;padding:0}}
li{{margin:0 0 4px}}
li a{{display:block;padding:14px 16px;background:var(--surface);border:1px solid var(--line);
border-radius:10px;color:var(--ink);text-decoration:none;font-size:17px;font-weight:500;transition:.15s}}
li a:hover{{border-color:var(--accent);transform:translateX(3px)}}
.empty{{color:var(--ink2)}}
footer{{margin-top:64px;color:var(--ink2);font-size:13px;border-top:1px solid var(--line);padding-top:20px}}
</style></head><body><div class="wrap">
<header>
<h1>📚 지식나눔터</h1>
<p>해외의 좋은 정보를 한국어로 번역해 함께 보는 아카이브입니다.</p>
<span class="count">총 {total}편 · 최신순</span>
</header>
{body}
<footer>corca-ai/library · 올린 날짜(KST) 기준으로 정리됩니다.</footer>
</div></body></html>"""
with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(page)
print(f"index.html 생성: 폴더 {len(folders)}개 · 기사 {total}편")
