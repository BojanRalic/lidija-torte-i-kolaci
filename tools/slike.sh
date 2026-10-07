#!/bin/sh
# Makes 400 px and 800 px WebP copies of every original photo, used by srcset in index.html.
# Run after adding or replacing a photo in assets/img/ (keep originals 1080 px or wider).
cd "$(dirname "$0")/../assets/img" || exit 1
for f in *.webp; do
  case "$f" in *-400.webp|*-800.webp|og-*) continue ;; esac
  for w in 400 800; do cwebp -quiet -q 80 -resize "$w" 0 "$f" -o "${f%.webp}-$w.webp"; done
done
echo "gotovo"
