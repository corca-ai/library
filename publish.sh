#!/usr/bin/env bash
# 루트에 떨어진 *.html을 KST 날짜 폴더로 옮기고 인덱스 갱신 후 push.
set -euo pipefail
cd "$(dirname "$0")"
DATE="${1:-$(TZ='Asia/Seoul' date +%y%m%d)}"
mkdir -p "$DATE"
shopt -s nullglob
moved=0
for f in *.html; do
  [ "$f" = "index.html" ] && continue
  mv "$f" "$DATE/" && echo "이동: $f -> $DATE/" && moved=$((moved+1))
done
python3 build_index.py
git add -A
git diff --cached --quiet && { echo "변경 없음"; exit 0; }
git commit -m "Add ${DATE} 번역 (${moved}편)"
git push
echo "✅ 완료 → https://corca-ai.github.io/library/"
