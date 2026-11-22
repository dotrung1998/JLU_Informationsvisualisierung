#!/usr/bin/env python3
"""Liest Kursmaterial und Abgabeordner in den Vault ein und prueft die Abdeckung.

Quellen:
    00_Materialien/               Kursmaterial (PDF, DOCX, TEX)
    Visual 3. Semester/           Einstiegsseite (Handskizze und Erwartungen)
    Pruefungsvorleistung/         Uebungsaufgabe U01-U14, Praesentation
    e-Portfolio/Portfolio/        Gesamtportfolio
    e-Portfolio/Programmcode/     Programmcode zu den Ergebnissen
    Projektordner (Dateien direkt in der Wurzel)

Jede Quelldatei muss am Ende genau einen Zustand haben:
    notiz            automatisch erzeugte (Quelle)-Notiz
    manuell          in einer handgeschriebenen Notiz beschrieben (abdeckung-regeln.json)
    ausgeschlossen   bewusst ausgelassen, mit Grund (abdeckung-regeln.json)
    unbekannt        nichts davon -> wird gemeldet und der Lauf endet mit Fehler

Geschrieben werden ausschliesslich:
    10 Kurs/*(Quelle).md        40 Portfolio/Abgaben/*(Quelle).md
    10 Kurs/Abgaben (auto).md   90 Anhänge/…
    00 Start/Ingest Log.md      00 Start/Neu seit letztem Lauf.md
    _tools/abdeckung.json       _tools/.ingest-state.json

Handgeschriebene Notizen bleiben unangetastet.

Aufruf:
    python3 Wissen/_tools/ingest.py            # einlesen und Abdeckung pruefen
    python3 Wissen/_tools/ingest.py --check    # nur berichten
    python3 Wissen/_tools/ingest.py --force    # alles neu rendern
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
VAULT = TOOLS.parent
ROOT = VAULT.parent

MATERIAL = ROOT / "00_Materialien"
ATTACH = VAULT / "90 Anhänge"

STATE_FILE = TOOLS / ".ingest-state.json"
RULES_FILE = TOOLS / "abdeckung-regeln.json"
COVER_FILE = TOOLS / "abdeckung.json"
LOG_FILE = VAULT / "00 Start" / "Ingest Log.md"
NEWS_FILE = VAULT / "00 Start" / "Neu seit letztem Lauf.md"
ABGABEN_FILE = VAULT / "10 Kurs" / "Abgaben (auto).md"

CHECK_ONLY = "--check" in sys.argv
FORCE = "--force" in sys.argv
NOW = datetime.now().strftime("%Y-%m-%d %H:%M")
TODAY = datetime.now().strftime("%Y-%m-%d")
RENDER_VERSION = 1

SKIP_NAMES = {".gitkeep", ".DS_Store"}
SKIP_SUFFIX = {".zip", ".csv"}

# Abgabeordner: Pfad -> (Titel, Zielnotiz, Frist laut Handout, Hinweis)
ABGABEN = {
    "Visual 3. Semester": (
        "Einstiegsseite",
        "Einstiegsseite (Quelle).md",
        "2026-10-25",
        "Handskizze und Erwartungen, Seite 2 des Portfolios; Abgabe bis 25.10.2026 (Handout S. 1)",
    ),
    "Prüfungsvorleistung": (
        "Prüfungsvorleistung",
        "Prüfungsvorleistung (Quelle).md",
        "offen",
        "Eine Übungsaufgabe U01–U14 vorstellen; Termin nicht dokumentiert",
    ),
    "e-Portfolio/Portfolio": (
        "e-Portfolio – Portfolio",
        "e-Portfolio Portfolio (Quelle).md",
        "2027-03-31",
        "Gesamtportfolio, 5–10 Seiten; Abgabe bis 31.03.2027 (Handout S. 1)",
    ),
    "e-Portfolio/Programmcode": (
        "e-Portfolio – Programmcode",
        "e-Portfolio Programmcode (Quelle).md",
        "2027-03-31",
        "Programmcode, den Ergebnissen nachvollziehbar zugeordnet (Handout S. 2)",
    ),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def run_tool(cmd: list) -> str:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    except (OSError, subprocess.SubprocessError):
        return ""
    return out.stdout if out.returncode == 0 else ""


def extract(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return run_tool(["pdftotext", "-layout", str(path), "-"])
    if suffix == ".docx":
        return run_tool(["pandoc", str(path), "-t", "plain"])
    if suffix in {".tex", ".md", ".txt"}:
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return ""
    return ""


def load_json(path: Path, fallback):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            print(f"Warnung: {path.name} unlesbar, wird neu aufgebaut.")
    return fallback


def load_state() -> dict:
    return load_json(STATE_FILE, {})


def load_rules() -> dict:
    data = load_json(RULES_FILE, {})
    data.setdefault("ausgeschlossen", [])
    data.setdefault("manuell", [])
    return data


def save_state(state: dict) -> None:
    STATE_FILE.write_text(
        json.dumps(state, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def fence(text: str, limit: int = 6000) -> str:
    text = text.strip()
    if not text:
        return ""
    if len(text) > limit:
        text = text[:limit].rstrip() + "\n… (gekürzt)"
    return "~~~~\n" + text.replace("~~~~", "~~~") + "\n~~~~"


def write_if_changed(path: Path, body: str, volatile: str = r"^$") -> bool:
    if path.exists():
        old = path.read_text(encoding="utf-8")
        strip = lambda t: re.sub(volatile, "", t, flags=re.M)
        if strip(old) == strip(body):
            return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return True


def source_note(title: str, label: str, src: Path, body: str, hash_value: str) -> str:
    stamp = datetime.fromtimestamp(src.stat().st_mtime).strftime("%Y-%m-%d")
    return (
        "---\n"
        f'titel: "{title}"\n'
        f'quelle: "{label}"\n'
        f"stand: {stamp}\n"
        f"hash: {hash_value[:12]}\n"
        "automatisch: true\n"
        "---\n\n"
        f"> Automatisch eingelesen aus `{label}` am {TODAY}. Nicht bearbeiten —\n"
        "> inhaltliche Arbeit gehört in die handgeschriebenen Notizen.\n\n"
        + body.strip()
        + "\n"
    )


# ---------------------------------------------------------------- Material


def material_target(src: Path):
    name = src.name
    if name.startswith("Handout_"):
        return (
            VAULT / "10 Kurs" / "Handout Portfolio und Abschlussseminar (Quelle).md",
            ATTACH / "Handout Informationsvisualisierung.pdf",
            "Handout Portfolio und Abschlussseminar",
        )
    if name.startswith("InfoVis_Uebungen_"):
        return (
            VAULT / "10 Kurs" / "Übungsaufgaben Kapitel 01–05 (Quelle).md",
            ATTACH / "Übungsaufgaben Kapitel 01–05.pdf",
            "Übungsaufgaben Kapitel 01–05",
        )
    if name.startswith("Informationsvisualisierung_Gesamt"):
        return (
            VAULT / "10 Kurs" / "Vorlesungsfolien Gesamt Kapitel 00–08 (Quelle).md",
            ATTACH / "Vorlesungsfolien Gesamt Kapitel 00–08.pdf",
            "Vorlesungsfolien Gesamt Kapitel 00–08",
        )
    if name.startswith("Kapitel_"):
        stem = src.stem.replace("_", " ")
        return (
            VAULT / "10 Kurs" / f"{stem} (Quelle).md",
            ATTACH / f"{stem}.pdf",
            stem,
        )
    if name.startswith("Projektion_"):
        stem = src.stem.replace("_", " ")
        return (
            VAULT / "10 Kurs" / f"{stem} (Quelle).md",
            ATTACH / f"{stem}.pdf",
            stem,
        )

    stem = src.stem.replace("_", " ")
    return VAULT / "90 Anhänge" / f"{stem} (Quelle).md", ATTACH / name, stem


def ingest_material(src: Path, state: dict, log: list) -> str:
    label = rel(src)
    current = digest(src)
    dest, attach, title = material_target(src)
    prev = state.get(label, {})
    if (
        prev.get("hash") == current
        and prev.get("v") == RENDER_VERSION
        and dest.exists()
        and not FORCE
    ):
        return "unverändert"

    text = extract(src)
    body = f"# {title} (Quelle)\n\n"
    if attach is not None:
        body += f"Anhang: `{attach.relative_to(VAULT).as_posix()}`\n\n"
    body += "## Inhalt (automatisch extrahiert)\n\n"
    body += (
        fence(text)
        if text.strip()
        else "_Kein Text extrahiert. Die Datei ist ein Bild oder ein nicht lesbares Format._\n"
    )

    action = "neu" if not prev else "geändert"
    if CHECK_ONLY:
        print(f"[{action}] {label} -> {dest.relative_to(VAULT)}")
        return action

    write_if_changed(dest, source_note(title, label, src, body, current))
    if attach is not None:
        attach.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, attach)

    state[label] = {
        "hash": current,
        "ziel": dest.relative_to(VAULT).as_posix(),
        "anhang": attach.relative_to(VAULT).as_posix() if attach else "",
        "text": bool(text.strip()),
        "v": RENDER_VERSION,
        "eingelesen": NOW,
    }
    log.append((action, label, dest.relative_to(VAULT).as_posix()))
    return action


def root_files():
    return sorted(
        p for p in ROOT.iterdir()
        if p.is_file()
        and p.suffix.lower() in {".pdf", ".docx", ".tex"}
        and p.name not in SKIP_NAMES
    )


def ingest_root(src: Path, state: dict, log: list) -> str:
    label = "root/" + src.name
    current = digest(src)
    dest = VAULT / "90 Anhänge" / f"{src.stem.replace('_', ' ')} (Quelle).md"
    prev = state.get(label, {})
    if (
        prev.get("hash") == current
        and prev.get("v") == RENDER_VERSION
        and dest.exists()
        and not FORCE
    ):
        return "unverändert"

    text = extract(src)
    title = src.stem.replace("_", " ")
    body = f"# {title} (Quelle)\n\nDatei lag direkt im Projektordner.\n\n## Inhalt\n\n"
    body += fence(text) if text.strip() else "_Kein Text extrahiert._\n"

    action = "neu" if not prev else "geändert"
    if CHECK_ONLY:
        print(f"[{action}] {label} -> {dest.relative_to(VAULT)}")
        return action

    write_if_changed(dest, source_note(title, label, src, body, current))
    ATTACH.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, ATTACH / src.name)
    state[label] = {
        "hash": current,
        "ziel": dest.relative_to(VAULT).as_posix(),
        "anhang": (ATTACH / src.name).relative_to(VAULT).as_posix(),
        "text": bool(text.strip()),
        "v": RENDER_VERSION,
        "eingelesen": NOW,
    }
    log.append((action, label, dest.relative_to(VAULT).as_posix()))
    return action


# ----------------------------------------------------------- Abgabeordner


def resolve(name: str):
    """Pfad auflösen, auch wenn macOS den Namen zerlegt (NFD) gespeichert hat."""
    current = ROOT
    for part in Path(name).parts:
        candidate = current / part
        if candidate.exists():
            current = candidate
            continue
        target = unicodedata.normalize("NFC", part)
        match = next(
            (
                child
                for child in current.iterdir()
                if unicodedata.normalize("NFC", child.name) == target
            ),
            None,
        )
        if match is None:
            return None
        current = match
    return current


def abgabe_folders():
    """(Pfad, Schlüssel) für jeden vorhandenen Abgabeordner."""
    found = []
    for key in ABGABEN:
        folder = resolve(key)
        if folder is not None and folder.is_dir():
            found.append((folder, key))
    return found


def folder_files(folder: Path):
    """Alle echten Dateien des Ordners, samt Unterordnern; Systemdateien nicht."""
    return sorted(
        p for p in folder.rglob("*")
        if p.is_file()
        and p.name not in SKIP_NAMES
        and not p.name.startswith(".")
        and p.suffix.lower() != ".zip"
        and p.name != ".DS_Store"
    )


def is_own(name: str) -> bool:
    return "Do_Trung" in name


def manual_note_for(path: Path, rules: dict) -> str:
    key = unicodedata.normalize("NFC", rel(path))
    for entry in rules.get("manuell", []):
        if entry.get("pfad") == key:
            return entry.get("notiz", "")
    return ""


def ingest_abgabe(folder: Path, key: str, state: dict, log: list, rules: dict) -> str:
    title, note_name, frist, hinweis = ABGABEN[key]
    label = "Abgabe/" + key
    files = folder_files(folder)
    signature = hashlib.sha256(
        "".join(f"{p.relative_to(folder).as_posix()}:{digest(p)};" for p in files).encode("utf-8")
    ).hexdigest()
    prev = state.get(label, {})
    dest = VAULT / "40 Portfolio" / "Abgaben" / note_name

    if (
        prev.get("hash") == signature
        and prev.get("v") == RENDER_VERSION
        and dest.exists()
        and not FORCE
    ):
        return "unverändert"
    if not files and not dest.exists():
        return "unverändert"

    rows, blocks, ohne_text = [], [], []
    for p in files:
        kb = max(1, round(p.stat().st_size / 1024))
        herkunft = "eigene Datei" if is_own(p.name) else "Fremddatei oder Vorlage"
        name = p.relative_to(folder).as_posix()
        rows.append(f"| `{name}` | {kb} KB | {p.suffix.lstrip('.').upper()} | {herkunft} |")
        text = extract(p)
        if text.strip():
            blocks.append(f"### {name}\n\n" + fence(text))
        else:
            ohne_text.append(name)
            hand = manual_note_for(p, rules)
            if hand:
                stem = Path(hand).stem
                blocks.append(
                    f"### {name}\n\n"
                    f"_Kein Text extrahiert (Bild). Inhalt beschrieben in [[{stem}]]._\n"
                )
            elif p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                blocks.append(
                    f"### {name}\n\n"
                    "_Kein Text extrahiert (Bild). Inhalt noch nicht beschrieben — "
                    "als offenen Punkt im Vault vermerken._\n"
                )
            else:
                blocks.append(
                    f"### {name}\n\n"
                    "_Kein Text extrahiert. Datei nicht lesbar — Grund im Lauf prüfen._\n"
                )

    if not files:
        body = f"# {title} (Quelle)\n\nDer Ordner `{key}` ist leer.\n\n{hinweis}\n"
    else:
        frist_text = f"Frist: {frist}" if frist != "offen" else "Frist: nicht dokumentiert"
        body = (
            f"# {title} (Quelle)\n\n"
            f"{hinweis}. {frist_text}. Quelle: `{key}`\n\n"
            "## Dateien\n\n| Datei | Größe | Typ | Herkunft |\n|---|---|---|---|\n"
            + "\n".join(rows)
            + "\n\n"
        )
        if any(is_own(p.name) for p in files):
            body += "> Eigene Datei vorhanden.\n\n"
        else:
            body += (
                "> **Keine eigene Datei in diesem Ordner.** Was hier liegt, ist nicht die\n"
                "> eigene Abgabe ([[Portfolio Trung]]).\n\n"
            )
        body += "## Inhalt\n\n" + "\n".join(blocks)

    action = "neu" if not prev else "geändert"
    if CHECK_ONLY:
        print(f"[{action}] {label} -> {dest.relative_to(VAULT)}")
        return action

    write_if_changed(dest, source_note(title, label, folder, body, signature))

    target = ATTACH / "Abgaben" / title.replace(" – ", " ")
    target.mkdir(parents=True, exist_ok=True)
    keep = {p.relative_to(folder).as_posix() for p in files}
    for old in sorted(target.rglob("*"), reverse=True):
        if old.is_file() and old.relative_to(target).as_posix() not in keep:
            old.unlink()
    for p in files:
        sub = target / p.relative_to(folder)
        sub.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(p, sub)
        except OSError:
            pass

    state[label] = {
        "hash": signature,
        "ziel": dest.relative_to(VAULT).as_posix(),
        "anhang_dir": target.relative_to(VAULT).as_posix(),
        "ohne_text": ohne_text,
        "v": RENDER_VERSION,
        "eingelesen": NOW,
    }
    log.append((action, label, dest.relative_to(VAULT).as_posix()))
    return action


# ------------------------------------------------------------ Abgabenliste


def render_abgaben() -> bool:
    rows = []
    for key, (title, _note, frist, _hinweis) in ABGABEN.items():
        folder = resolve(key)
        files = folder_files(folder) if folder is not None and folder.is_dir() else []
        own = [p for p in files if is_own(p.name)]
        own_pdf = [p for p in own if p.suffix.lower() == ".pdf"]
        if not files:
            stand = "leer"
        elif own_pdf:
            stand = "eigene PDF vorhanden"
        elif own:
            stand = "eigene Datei, **keine PDF**"
        else:
            stand = "**nur Fremddateien**"
        rows.append(
            f"| `{key}` | {title} | {frist if frist != 'offen' else '—'} | {len(files)} | {stand} |"
        )

    body = (
        "---\n"
        "titel: Abgaben (auto)\n"
        f"stand: {TODAY}\n"
        "automatisch: true\n"
        "---\n\n"
        "# Abgaben (automatisch)\n\n"
        f"Lauf: {NOW}. Quelle: die Abgabeordner im Projektordner.\n\n"
        "| Ordner | Was | Frist | Dateien | Stand |\n|---|---|---|---|---|\n"
        + "\n".join(rows)
        + "\n\n"
        "Der Stand zählt nur Dateien im jeweiligen Ordner. Eine Abgabe in Stud.IP ist damit\n"
        "nicht nachgewiesen, nur die lokale Sicherung.\n"
    )
    return write_if_changed(ABGABEN_FILE, body, r"^Lauf: .*$")


# ---------------------------------------------------------------- Abdeckung


def discover_sources() -> list:
    found = []
    if MATERIAL.is_dir():
        found += [p for p in MATERIAL.rglob("*") if p.is_file()]
    for folder, _key in abgabe_folders():
        found += folder_files(folder)
    found += root_files()
    return sorted(set(found))


def state_key_for(path: Path) -> str:
    if MATERIAL in path.parents:
        return "00_Materialien/" + path.relative_to(MATERIAL).as_posix()
    for folder, key in abgabe_folders():
        if folder in path.parents:
            return "Abgabe/" + key
    return "root/" + path.name


def coverage(state: dict, rules: dict) -> dict:
    entries = []
    unknown = []
    ohne_text = []

    for p in discover_sources():
        key = unicodedata.normalize("NFC", rel(p))
        if key.startswith("Wissen/"):
            continue
        status, ziel, grund = "", "", ""

        for rule in rules.get("ausgeschlossen", []):
            if fnmatch.fnmatch(key, rule["muster"]) or fnmatch.fnmatch(p.name, rule["muster"]):
                status, grund = "ausgeschlossen", rule.get("grund", "")
                break

        if not status:
            for entry in rules.get("manuell", []):
                if entry.get("pfad") == key:
                    status, ziel, grund = "manuell", entry.get("notiz", ""), entry.get("grund", "")
                    break

        if not status:
            skey = state_key_for(p)
            if skey in state:
                status, ziel = "notiz", state[skey]["ziel"]

        if not status:
            status = "unbekannt"
            unknown.append(key)

        if status in {"notiz", "manuell"} and p.suffix.lower() in {
            ".pdf", ".docx", ".tex", ".md", ".txt"
        }:
            skey = state_key_for(p)
            if status == "notiz" and skey in state:
                readable = state[skey].get("text", True)
                if skey.startswith("Abgabe/"):
                    base = resolve(skey[len("Abgabe/"):])
                    sub = p.relative_to(base).as_posix() if base else p.name
                    readable = sub not in state[skey].get("ohne_text", [])
            else:
                readable = True
            if not readable:
                ohne_text.append(key)

        entries.append({"pfad": key, "status": status, "ziel": ziel, "grund": grund})

    ordner_mit, ordner_ohne_frist = [], []
    for folder, key in abgabe_folders():
        if not folder_files(folder):
            continue
        ordner_mit.append(key)
        if ABGABEN[key][2] == "offen":
            ordner_ohne_frist.append(key)

    summary = {
        "stand": NOW,
        "dateien": entries,
        "unbekannt": unknown,
        "ohne_text": ohne_text,
        "ordner_mit_dateien": ordner_mit,
        "wochen_ohne_frist": ordner_ohne_frist,
        "zaehlung": {
            s: sum(1 for e in entries if e["status"] == s)
            for s in ("notiz", "manuell", "ausgeschlossen", "unbekannt")
        },
    }
    return summary


# ---------------------------------------------------------------- Protokoll


def append_log(entries: list) -> None:
    if not entries:
        return
    rows = "\n".join(f"| {NOW} | {a} | `{b}` | `{c}` |" for a, b, c in entries)
    if LOG_FILE.exists():
        lines = LOG_FILE.read_text(encoding="utf-8").splitlines()
    else:
        lines = [
            "---", "titel: Ingest Log", "---", "", "# Ingest Log", "",
            "| Zeitpunkt | Aktion | Quelle | Ziel |", "|---|---|---|---|",
        ]
    insert_at = None
    for i, line in enumerate(lines):
        if re.match(r"^\|\s*-{3,}", line):
            insert_at = i + 1
            break
    if insert_at is None:
        lines += ["", "| Zeitpunkt | Aktion | Quelle | Ziel |", "|---|---|---|---|"]
        insert_at = len(lines)
    lines.insert(insert_at, rows)
    LOG_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_news(new: list, changed: list, unchanged: int, cov: dict) -> None:
    def block(items):
        return "\n".join(f"- `{i}`" for i in items) + "\n" if items else "_nichts_\n"

    z = cov["zaehlung"]
    unknown = cov["unbekannt"]
    ohne_text = cov["ohne_text"]
    ohne_frist = cov["wochen_ohne_frist"]

    body = (
        "---\n"
        "titel: Neu seit letztem Lauf\n"
        f"stand: {TODAY}\n"
        "---\n\n"
        "# Neu seit letztem Lauf\n\n"
        f"Lauf: {NOW}\n\n"
        f"## Neu ({len(new)})\n\n{block(new)}\n"
        f"## Geändert ({len(changed)})\n\n{block(changed)}\n"
        f"## Unverändert: {unchanged} Quellen\n\n"
        "## Abdeckung\n\n"
        f"- Quellen gesamt: **{sum(z.values())}**\n"
        f"- durch Notiz: {z['notiz']} · manuell beschrieben: {z['manuell']} · "
        f"ausgeschlossen: {z['ausgeschlossen']} · **unbekannt: {z['unbekannt']}**\n"
        + (
            "\n**Unbekannt (weder Notiz noch Ausschluss):**\n\n"
            + "\n".join(f"- `{u}`" for u in unknown)
            + "\n\n> Diese Dateien tragen möglicherweise Kursinformation und sind noch nicht\n"
            "> erfasst. Entweder einlesen oder in `_tools/abdeckung-regeln.json` mit Grund\n"
            "> ausschließen.\n"
            if unknown else "\nAlle Quellen sind erfasst oder begründet ausgeschlossen.\n"
        )
        + (
            "\n**Ohne Text extrahiert:**\n\n"
            + "\n".join(f"- `{u}`" for u in ohne_text)
            + "\n"
            if ohne_text else ""
        )
        + (
            "\n**Abgabeordner mit Dateien, aber ohne bekannte Frist:** `"
            + "`, `".join(ohne_frist)
            + "` — Frist in `_tools/fristen.json` nachtragen.\n"
            if ohne_frist else ""
        )
        + "\n## Was jetzt zu tun ist\n\n"
        "1. Neue Abgaben prüfen: Ist die eigene Datei dabei, richtig benannt, als PDF?\n"
        "2. Neue Unterlagen lesen: Fristen, Seitenumfang, Wortlimits → [[Status]] und\n"
        "   [[Board]] fortschreiben.\n"
        "3. Geänderte Vorgaben (Prüfungsform, Abgabedatum, Seitenzahl) in\n"
        "   [[Entscheidungen]] mit Datum und Grund festhalten.\n"
    )
    write_if_changed(NEWS_FILE, body, r"^Lauf: .*$")


def cleanup(state: dict, live: set) -> list:
    """Quellen weg oder Zielnotiz verschwunden -> Zustand und Notiz aufräumen.

    Rückgabe: Liste (Schlüssel, Zielnotiz) für das Protokoll.
    """
    removed = []
    for key in [k for k in state if k in live]:
        entry = state[key]
        target = VAULT / entry.get("ziel", "")
        if not target.is_file():
            state.pop(key)
            removed.append((key, entry.get("ziel", "")))
    for key in [k for k in state if k not in live]:
        entry = state.pop(key)
        target = VAULT / entry.get("ziel", "")
        if entry.get("ziel") and target.is_file():
            target.unlink()
        if entry.get("anhang"):
            attachment = VAULT / entry["anhang"]
            if attachment.is_file():
                attachment.unlink()
        if entry.get("anhang_dir"):
            directory = VAULT / entry["anhang_dir"]
            if directory.is_dir():
                shutil.rmtree(directory)
        removed.append((key, entry.get("ziel", "")))
    return removed


def main() -> int:
    state = load_state()
    rules = load_rules()
    new, changed, unchanged, log = [], [], 0, []

    sources = []
    if MATERIAL.is_dir():
        for p in sorted(MATERIAL.rglob("*")):
            if p.is_file() and p.name not in SKIP_NAMES and p.suffix.lower() not in SKIP_SUFFIX:
                sources.append(("material", p))
    for folder, key in abgabe_folders():
        sources.append(("abgabe", (folder, key)))
    for p in root_files():
        sources.append(("root", p))

    for kind, src in sources:
        if kind == "material":
            result = ingest_material(src, state, log)
            label = rel(src)
        elif kind == "abgabe":
            folder, key = src
            result = ingest_abgabe(folder, key, state, log, rules)
            label = "Abgabe/" + key
        else:
            result = ingest_root(src, state, log)
            label = "root/" + src.name
        if result == "neu":
            new.append(label)
        elif result == "geändert":
            changed.append(label)
        else:
            unchanged += 1

    live = set()
    if MATERIAL.is_dir():
        for p in MATERIAL.rglob("*"):
            if p.is_file() and p.name not in SKIP_NAMES and p.suffix.lower() not in SKIP_SUFFIX:
                live.add(rel(p))
    live |= {"Abgabe/" + key for _folder, key in abgabe_folders()}
    live |= {"root/" + p.name for p in root_files()}

    cov = coverage(state, rules)

    if CHECK_ONLY:
        print(f"\nNeu: {len(new)}, geändert: {len(changed)}, unverändert: {unchanged}")
        print(
            f"Abdeckung: {cov['zaehlung']['notiz']} Notiz, "
            f"{cov['zaehlung']['manuell']} manuell, "
            f"{cov['zaehlung']['ausgeschlossen']} ausgeschlossen, "
            f"{cov['zaehlung']['unbekannt']} unbekannt"
        )
        for u in cov["unbekannt"]:
            print(f"  unbekannt: {u}")
        return 1 if cov["unbekannt"] else 0

    removed = cleanup(state, live)
    log.extend(("entfernt", key, ziel) for key, ziel in removed)
    save_state(state)
    append_log(log)
    # Ohne Quellenänderung bleibt der letzte Bericht stehen, damit "neu seit letztem
    # Lauf" nicht beim nächsten ereignislosen Lauf wieder leer ist. Ändert sich aber
    # die Abdeckung (unbekannte Datei kommt oder geht), wird neu geschrieben.
    def coverage_stale() -> bool:
        if not NEWS_FILE.exists():
            return True
        text = NEWS_FILE.read_text(encoding="utf-8")
        u = re.search(r"unbekannt: (\d+)", text)
        t = re.search(r"Quellen gesamt: \*\*(\d+)\*\*", text)
        return (
            not u or not t
            or int(u.group(1)) != len(cov["unbekannt"])
            or int(t.group(1)) != sum(cov["zaehlung"].values())
        )

    if new or changed or removed or coverage_stale():
        write_news(new, changed, unchanged, cov)
    abgaben_changed = render_abgaben()
    COVER_FILE.write_text(
        json.dumps(cov, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(f"Lauf {NOW}")
    print(f"  neu:         {len(new)}")
    print(f"  geändert:    {len(changed)}")
    print(f"  unverändert: {unchanged}")
    if removed:
        print(f"  entfernt:    {len(removed)} (verwaiste Zustände/Notizen aufgeräumt)")
    if abgaben_changed:
        print("  Abgaben-Tabelle aktualisiert: 10 Kurs/Abgaben (auto).md")
    print(
        f"  Abdeckung:   {cov['zaehlung']['notiz']} Notiz, "
        f"{cov['zaehlung']['manuell']} manuell, "
        f"{cov['zaehlung']['ausgeschlossen']} ausgeschlossen, "
        f"{cov['zaehlung']['unbekannt']} unbekannt"
    )
    if cov["unbekannt"]:
        print("\n  WARNUNG: Quellen ohne Notiz und ohne Ausschluss:")
        for u in cov["unbekannt"]:
            print(f"    - {u}")
        print("  -> einlesen oder in _tools/abdeckung-regeln.json begründet ausschließen.")
        return 1
    if cov["ohne_text"]:
        print("  ohne Text extrahiert:")
        for u in cov["ohne_text"]:
            print(f"    - {u}")
    if cov["wochen_ohne_frist"]:
        print("  Abgabeordner ohne bekannte Frist: " + ", ".join(cov["wochen_ohne_frist"]))
    if not log and not abgaben_changed and not removed:
        print("  keine Änderungen an den Quellen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
