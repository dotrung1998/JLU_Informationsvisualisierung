#!/bin/bash
# Baut den Stand der Freebuff-Vorschau aus lernserver.html.
#
# Warum ein eigenes Skript: die Vorschau wird nicht von GitHub Actions versorgt,
# sondern von einer eigenen Sites-Deployment mit Anmeldung und D1. Patcher,
# Worker-Quelle und Manifest lagen bis 25.11.2026 nur unter dem ignorierten
# _build/ und mussten von Hand nachgezogen werden; dabei blieb die Vorschau auf
# dem alten Stand, obwohl lernserver.html längst geändert war. Jetzt liegen die
# Quellen versioniert neben diesem Skript und ein Aufruf erzeugt immer denselben
# Build:
#
#   bash Wissen_Informationsvisualisierung/_tools/freebuff-preview/build.sh
#
# Das Skript schreibt ausschließlich nach _build/freebuff-preview/ (ignoriert):
# page.html (gepatchte Seite), dist/worker.js (Bundle), deploy.json (Manifest),
# package*.json (Kopie für npm) und bei Bedarf node_modules. Es committet,
# pusht und deployt nichts — die Auslieferung ist ein Sites-Aufruf, kein
# Shell-Befehl, und wird am Ende ausgegeben.
#
# Exit-Codes:
#   0  gebaut (mit oder ohne Änderung am Quellstand)
#   1  liegt in keinem Git-Repository
#   2  Voraussetzung fehlt (python3, node, npm, Quelldatei)
#   3  build_page.py fehlgeschlagen
#   4  npm ci fehlgeschlagen
#   5  Bündeln mit esbuild fehlgeschlagen
#   6  Prüfung des Ergebnisses fehlgeschlagen
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Wurzel über Git bestimmen, nicht über ../..: liegt das Skript woanders, würde
# der relative Pfad aus dem Repository herauszeigen.
if ! ROOT="$(git -C "$DIR" rev-parse --show-toplevel 2>/dev/null)"; then
  echo "build: $DIR liegt in keinem Git-Repository." >&2
  exit 1
fi
cd "$ROOT" || exit 1

OUTDIR="$ROOT/_build/freebuff-preview"
PAGE_SRC="$ROOT/Wissen_Informationsvisualisierung/00 Start/lernserver.html"
PREVIEW_URL="https://lernserver-108-tin-3-trang-4wz4jg-preview.freebuff.site"
SITE_ID="5d78289e-4c8e-4be5-85de-4f40e75b7821"

for tool in python3 node npm; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "build: $tool fehlt im PATH." >&2
    exit 2
  fi
done
if [ ! -f "$PAGE_SRC" ]; then
  echo "build: $PAGE_SRC fehlt." >&2
  exit 2
fi

mkdir -p "$OUTDIR" || exit 2

# worker.js bindet die gepatchte Seite als Text ein und muss deshalb neben
# page.html liegen; deploy.json beschreibt Pfade relativ zu sich selbst.
cp "$DIR/worker.js" "$DIR/deploy.json" "$DIR/package.json" "$DIR/package-lock.json" "$OUTDIR/" || exit 2

# Abhängigkeiten nur beim ersten Lauf oder wenn sie fehlen. npm ci hält sich an
# package-lock.json, damit der Build nicht unbemerkt andere Versionen zieht.
if [ ! -x "$OUTDIR/node_modules/.bin/esbuild" ] || [ ! -d "$OUTDIR/node_modules/@freebuff/auth" ]; then
  echo "build: node_modules fehlen — npm ci"
  ( cd "$OUTDIR" && npm ci --no-audit --no-fund ) || exit 4
fi

hash_all() {
  if command -v shasum >/dev/null 2>&1; then shasum -a 256; else sha256sum; fi
}
STAMP_FILE="$OUTDIR/.source-hash"
NEW_HASH="$(cat "$PAGE_SRC" "$DIR/worker.js" "$DIR/build_page.py" | hash_all | cut -d' ' -f1)"

python3 "$DIR/build_page.py" --out "$OUTDIR/page.html" || exit 3

"$OUTDIR/node_modules/.bin/esbuild" "$OUTDIR/worker.js" \
  --bundle --format=esm --platform=browser --loader:.html=text \
  --outfile="$OUTDIR/dist/worker.js" || exit 5

# Prüfungen am Ergebnis, nicht am Protokoll: ohne Konto-Sync oder ohne Bundle
# würde die Vorschau zwar starten, aber Fortschritt und Name verlieren.
RC=0
check() {
  if ! grep -q -- "$2" "$1"; then
    echo "build: $3 — Muster fehlt in $1" >&2
    RC=1
  fi
}
[ -s "$OUTDIR/dist/worker.js" ] || { echo "build: dist/worker.js ist leer." >&2; RC=1; }
check "$OUTDIR/page.html" 'fetch("/api/progress"' "Seite lädt den Cloud-Stand nicht"
check "$OUTDIR/page.html" 'id="cloudState"' "Seite zeigt den Sync-Zustand nicht"
check "$OUTDIR/page.html" 'action="/auth/freebuff/signout"' "Seite hat keine Abmeldung"
check "$OUTDIR/dist/worker.js" 'cloudState' "Bundle enthält die gepatchte Seite nicht"
[ "$RC" -eq 0 ] || exit 6

PAGE_BYTES="$(wc -c < "$OUTDIR/page.html" | tr -d ' ')"
BUNDLE_BYTES="$(wc -c < "$OUTDIR/dist/worker.js" | tr -d ' ')"

echo "build: page.html $PAGE_BYTES B, dist/worker.js $BUNDLE_BYTES B"
if [ -f "$STAMP_FILE" ] && [ "$(cat "$STAMP_FILE")" = "$NEW_HASH" ]; then
  echo "build: Quellstand unverändert seit dem letzten Build — kein neues Ausliefern nötig,"
  echo "       solange das letzte Deploy geklappt hat."
else
  echo "build: Quellstand neu — die Vorschau zeigt den Stand erst nach dem Deploy."
fi
printf '%s\n' "$NEW_HASH" > "$STAMP_FILE"

cat <<EOF

Nächster Schritt (kein Shell-Befehl, daher hier nur der Aufruf):
  sites_deploy siteId=$SITE_ID environment=preview requestId=<neu>
               manifestPath=_build/freebuff-preview/deploy.json

Danach prüfen — das beweist nur, dass die Vorschau läuft:
  curl -s -o /dev/null -w '%{http_code}\\n' $PREVIEW_URL/healthz   # 200
  curl -s -o /dev/null -w '%{http_code}\\n' $PREVIEW_URL           # 302 Anmeldung
Den neuen Stand selbst sieht nur das angemeldete Konto.
EOF

exit 0
