"""Patches the Lernserver page for the Freebuff preview (account sync, D1).

Called by build.sh; the patched page is written to _build/freebuff-preview/page.html
and bundled into dist/worker.js there. Nothing in the repository is changed.

Usage: python3 build_page.py [--out PATH]
"""

from pathlib import Path
import argparse
import subprocess

HERE = Path(__file__).resolve().parent

# Root via git, not via ../..: the script may move inside _tools/ without the
# relative depth silently pointing outside the repository.
try:
    ROOT = Path(
        subprocess.check_output(
            ["git", "-C", str(HERE), "rev-parse", "--show-toplevel"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    )
except (OSError, subprocess.CalledProcessError):
    raise SystemExit(f"build_page: {HERE} liegt in keinem Git-Repository.")

SRC = ROOT / "Wissen_Informationsvisualisierung" / "00 Start" / "lernserver.html"

parser = argparse.ArgumentParser(description="Freebuff-Vorschau der Lernserver-Seite bauen.")
parser.add_argument(
    "--out",
    default=str(ROOT / "_build" / "freebuff-preview" / "page.html"),
    help="Zielpfad der gepatchten Seite (Standard: _build/freebuff-preview/page.html)",
)
OUT = Path(parser.parse_args().out).resolve()
OUT.parent.mkdir(parents=True, exist_ok=True)

s = SRC.read_text(encoding="utf-8")


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Expected {count} occurrence(s), found {n}: {old[:120]!r}")
    s = s.replace(old, new, count)


# 1. Die IIFE darf vor dem initialen Store-Load auf die Cloud warten.
rep('<script>\n(function(){\n  "use strict";\n\n  /* ---------------- Storage', '<script>\n(async function(){\n  "use strict";\n\n  /* ---------------- Storage')

# 2. Remote-Progress vor dem lokalen Fallback laden.
old_store = '''  let store;
  try { store = Object.assign({}, defaults, JSON.parse(localStorage.getItem(KEY) || "{}")); }
  catch(e){ store = Object.assign({}, defaults); }'''
new_store = '''  let remoteData = null;
  try {
    const controller = new AbortController();
    const timer = setTimeout(function(){ controller.abort(); }, 5000);
    const response = await fetch("/api/progress", {
      headers: { accept: "application/json" },
      cache: "no-store",
      signal: controller.signal
    });
    clearTimeout(timer);
    if(response.ok){
      const payload = await response.json();
      if(payload && payload.data && typeof payload.data === "object" && !Array.isArray(payload.data)){
        remoteData = payload.data;
      }
    }
  } catch(e){}

  let store;
  if(remoteData){
    store = Object.assign({}, defaults, remoteData);
  } else {
    try { store = Object.assign({}, defaults, JSON.parse(localStorage.getItem(KEY) || "{}")); }
    catch(e){ store = Object.assign({}, defaults); }
  }'''
rep(old_store, new_store)

# 3. Speichern: lokal + debounced Cloud-PUT.
old_save = '''  function save(){ try{ localStorage.setItem(KEY, JSON.stringify(store)); }catch(e){} }'''
new_save = '''  let pushTimer = null, dirty = false, saveVersion = 0;
  function setSyncState(state){
    const el = document.getElementById("cloudState");
    if(!el) return;
    const labels = {
      saving: "Speichert …",
      synced: "Synchronisiert",
      offline: "Offline — lokal gespeichert",
      error: "Sync-Fehler — lokal gespeichert"
    };
    el.textContent = labels[state] || "Cloud-Sync";
    el.dataset.state = state;
  }
  async function pushProgress(){
    const version = saveVersion;
    try {
      setSyncState("saving");
      const response = await fetch("/api/progress", {
        method: "PUT",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ data: store })
      });
      if(!response.ok) throw new Error("HTTP " + response.status);
      if(version === saveVersion) dirty = false;
      setSyncState("synced");
    } catch(e){
      setSyncState(navigator.onLine === false ? "offline" : "error");
    }
  }
  function save(){
    dirty = true; saveVersion++;
    try{ localStorage.setItem(KEY, JSON.stringify(store)); }catch(e){}
    clearTimeout(pushTimer);
    pushTimer = setTimeout(pushProgress, 250);
  }'''
rep(old_save, new_save)

# 4. Fortschrittsseite: ehrliche Cloud-Texte und Konto-/Sync-Anzeige.
rep(
    '<p>Welche Kapitel du geöffnet und als gelernt markiert hast, deine Merkliste und die nächsten Fristen. Alles bleibt lokal im Browser.</p>\n          <div class="hero-meta"><span class="pill">localStorage</span><span class="pill">Kein Konto, keine Übertragung</span></div>',
    '<p>Welche Kapitel du geöffnet und als gelernt markiert hast, deine Merkliste und die nächsten Fristen. Der Stand liegt in deinem Freebuff-Konto und wird zwischen Geräten synchronisiert.</p>\n          <div class="hero-meta" id="cloudBox"><span class="pill" id="cloudUser">Freebuff-Konto</span><span class="pill" id="cloudState" data-state="synced">Synchronisiert</span><form method="post" action="/auth/freebuff/signout" style="display:inline;margin:0"><button class="btn ghost small" type="submit">Abmelden</button></form></div>',
)
rep(
    '<div class="head"><span class="author" style="--ac:#c9cdfb">Lernbot</span><span class="tag bot">BOT</span><span class="time">Lokal gespeichert</span></div>\n            <div class="text"><p><strong>Dein Stand.</strong> „Gelesen“ setzt sich beim Öffnen eines Kapitels, „gelernt“ markierst du selbst. Nichts wird übertragen; alles liegt im localStorage dieses Browsers.</p></div>',
    '<div class="head"><span class="author" style="--ac:#c9cdfb">Lernbot</span><span class="tag bot">BOT</span><span class="time">Cloud-Sync</span></div>\n            <div class="text"><p><strong>Dein Stand.</strong> „Gelesen“ setzt sich beim Öffnen eines Kapitels, „gelernt“ markierst du selbst. Der Stand wird in deinem Freebuff-Konto gespeichert und zwischen Geräten synchronisiert; lokal bleibt eine Kopie.</p></div>',
)
rep(
    'const note = $("#pfNote"); if(note) note.textContent = done + " von " + pfItems.length + " Punkten erledigt — lokal gespeichert.";',
    'const note = $("#pfNote"); if(note) note.textContent = done + " von " + pfItems.length + " Punkten erledigt — synchronisiert.";',
)

# 5. Vietnamesische Fortschrittsnotiz und Graph-Caption an den Cloud-Stand anpassen.
rep('"fortschritt":[["Tiến độ học — lưu cục bộ"', '"fortschritt":[["Tiến độ học — đồng bộ tài khoản"')
rep(
    'Không có dữ liệu nào được gửi đi; mọi thứ nằm trong localStorage của trình duyệt này.',
    'Tiến độ được lưu trong tài khoản Freebuff và đồng bộ giữa các thiết bị; localStorage chỉ là bản sao cục bộ.',
)
rep('"Lưu trong localStorage"]', '"Đồng bộ qua tài khoản"]')
rep(
    'Chỉ localStorage — không tài khoản, không gửi dữ liệu.',
    'Đồng bộ qua tài khoản Freebuff; localStorage chỉ là bản sao.',
)

# 6. Kleine Statusfarben für die Cloud-Anzeige.
rep(
    "</style>",
    """#cloudBox{gap:8px;flex-wrap:wrap}
#cloudBox form{margin:0}
#cloudState[data-state="saving"]{color:#ffe0a3;border-color:#8a6a2f}
#cloudState[data-state="offline"],#cloudState[data-state="error"]{color:#ffb4a8;border-color:#7a2e2e}
</style>""",
)

# 7. Boot: Nutzername laden, Sync-Status setzen, letzte Änderung per Beacon sichern.
rep(
    """  renderProgress();
  renderChecklist();
  renderQuiz();
  renderBookmarks();
  renderChangelog();
})();""",
    """  renderProgress();
  renderChecklist();
  renderQuiz();
  renderBookmarks();
  renderChangelog();
  setSyncState("synced");
  fetch("/api/me", { headers: { accept: "application/json" }, cache: "no-store" })
    .then(function(response){ return response.ok ? response.json() : null; })
    .then(function(payload){
      if(!payload || !payload.user) return;
      const el = document.getElementById("cloudUser");
      if(el) el.textContent = payload.user.name || payload.user.email || "Freebuff-Konto";
    })
    .catch(function(){});
  window.addEventListener("pagehide", function(){
    if(!dirty) return;
    try {
      navigator.sendBeacon("/api/progress", new Blob([JSON.stringify({ data: store })], { type: "application/json" }));
    } catch(e){}
  });
})();""",
)

# 8. Sicherheitsnetz: die erwarteten Marker müssen vorhanden sein.
required = [
    'await fetch("/api/progress"',
    'async function pushProgress()',
    'id="cloudState"',
    'id="cloudUser"',
    'action="/auth/freebuff/signout"',
    'setSyncState("synced")',
    'navigator.sendBeacon("/api/progress"',
]
for marker in required:
    if marker not in s:
        raise SystemExit(f"Missing marker after patch: {marker}")

OUT.write_text(s, encoding="utf-8")
print(f"wrote {OUT} ({len(s.encode('utf-8'))} bytes)")
print("original bytes:", len(SRC.read_bytes()))
print("script marker:", "async function(){" in s)
