#!/usr/bin/env python3
"""Schickt einen ausführlichen Arbeitsbericht des letzten Laufs an Discord.

Ziel: Der Bericht soll allein genügen, um die nächsten Aufgaben zu erledigen.
Er enthält deshalb

  1. einen Kopf mit Zählern und Warnungen,
  2. alle Fristen aus `fristen.json` mit Abstand, Zuständigkeit und Detail,
  3. jede offene Board-Karte (To Do, Doing) mit Kennung, Tag, Frist, Belegstand,
     Kurzbeschreibung und Zielnotiz,
  4. die „Nächste Aktion“ aus `Status.md` und die offenen Punkte aus
     `Offene Entscheidungen.md` samt dem, was sie blockieren,
  5. den Quellenstand (neu/geändert/offen) und Warnungen,
  6. **eine einzige Kopiervorlage** als Code-Block: alle Aufgaben als `- [ ]`-Zeilen,
     damit ein Klick im Discord-Client alles kopiert.

Der Webhook ist ein Geheimnis. Er wird hier gelesen, in dieser Reihenfolge:
  1. Umgebungsvariable DISCORD_WEBHOOK
  2. Datei `~/.config/informationsvisualisierung/discord-webhook` (eigener Kanal)
  3. Datei `~/.config/projektplanung/discord-webhook` (vorhandener Kanal, Rückfall)
Fehlt alles, wird nichts gesendet. Der Webhook steht nie im Vault und nie im Repo.

Aufruf:
    python3 Wissen_Informationsvisualisierung/_tools/discord_notify.py
    python3 Wissen_Informationsvisualisierung/_tools/discord_notify.py --dry-run
    python3 Wissen_Informationsvisualisierung/_tools/discord_notify.py --status fail --detail "ingest.py"
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import date, datetime
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
VAULT = TOOLS.parent
ROOT = VAULT.parent
NEU = VAULT / "00 Start" / "Neu seit letztem Lauf.md"
BOARD = VAULT / "00 Start" / "Board.md"
STATUS_NOTE = VAULT / "00 Start" / "Status.md"
OFFEN = VAULT / "00 Start" / "Offene Entscheidungen.md"
FRISTEN = TOOLS / "fristen.json"
ABDECKUNG = TOOLS / "abdeckung.json"
LOG = TOOLS / "daily.log"
WEBHOOK_FILES = (
    Path.home() / ".config" / "informationsvisualisierung" / "discord-webhook",
    Path.home() / ".config" / "projektplanung" / "discord-webhook",
)

DRY = "--dry-run" in sys.argv
TITEL = "Informationsvisualisierung"
TODAY = date.today()

# Grenzen der Discord-API.
MAX_CONTENT = 2000
MAX_EMBEDS = 10
MAX_DESC = 4096
MAX_FIELD = 1024
MAX_NAME = 256
# Eigene Obergrenze für content + embeds zusammen (Discord: 6000).
BUDGET = 5800

CARD_RE = re.compile(
    r"^- \[(?P<box>[ x])\] \*\*(?P<id>[^*]+?) · (?P<rest_title>[^*]+)\*\*(?P<rest>.*)$"
)
HEAD_RE = re.compile(r"^##\s+(To Do|Doing|Done)\s*$")
FALLIG_RE = re.compile(r"fällig:\s*(\d{4}-\d{2}-\d{2})")
BELEG_RE = re.compile(r'beleg:\s*"([^"]+)"')
GEN_RE = re.compile(
    r"\s·\s(?:überfällig \([^)]*\)|Beleg (?:vorhanden|fehlt)|erledigt \d{4}-\d{2}-\d{2})\s*$"
)
TAG_RE = re.compile(r"\s*#(person|team|auto)\b")


def arg_value(name: str, default: str = "") -> str:
    if name in sys.argv:
        index = sys.argv.index(name)
        if index + 1 < len(sys.argv):
            return sys.argv[index + 1]
    return default


STATUS = arg_value("--status", "ok")
DETAIL = arg_value("--detail", "")
ALLOWED = (
    "https://discord.com/api/webhooks/",
    "https://canary.discord.com/api/webhooks/",
    "https://ptb.discord.com/api/webhooks/",
    "https://discordapp.com/api/webhooks/",
)


def webhook() -> str:
    url = os.environ.get("DISCORD_WEBHOOK", "").strip()
    if url:
        return url
    for path in WEBHOOK_FILES:
        try:
            return path.read_text(encoding="utf-8").strip()
        except OSError:
            continue
    return ""


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def grab(text: str, pattern: str, default: str = "", flags: int = re.S) -> str:
    match = re.search(pattern, text, flags)
    return match.group(1) if match else default


def plain(text: str) -> str:
    """Wikilinks auflösen, Markdown-Reste entfernen, Backticks meiden."""
    text = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    text = text.replace("`", "'").replace("**", "").replace("_", "")
    return re.sub(r"\s+", " ", text).strip(" ·—")


def kuerzen(text: str, limit: int) -> str:
    """An der Wortgrenze kürzen, ohne den Text zu verfälschen."""
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(" ·,;:")
    return cut or text[:limit]


def abstand(datum: str) -> tuple[int | None, str]:
    try:
        delta = (datetime.fromisoformat(datum).date() - TODAY).days
    except ValueError:
        return None, "Datum unklar"
    if delta < 0:
        return delta, f"überfällig seit {-delta} Tag{'en' if -delta != 1 else ''}"
    if delta == 0:
        return delta, "heute"
    if delta == 1:
        return delta, "morgen"
    return delta, f"in {delta} Tagen"


def kurz(datum: str) -> str:
    """2027-03-31 → 31.03.2027"""
    return datum[8:10] + "." + datum[5:7] + "." + datum[0:4] if len(datum) >= 10 else datum


def last_run_stamp() -> str:
    """Zeitpunkt des letzten Laufs aus daily.log (nicht aus der Notiz)."""
    lines = read(LOG).splitlines()
    for line in reversed(lines):
        match = re.match(r"^=== (\d{4}-\d{2}-\d{2} \d{2}:\d{2}):\d{2} ===$", line)
        if match:
            return match.group(1)
    return ""


# ---------------------------------------------------------------- Board


def strip_generated(rest: str) -> str:
    while True:
        new = GEN_RE.sub("", rest)
        if new == rest:
            return rest
        rest = new


def beleg_exists(pattern: str) -> bool:
    try:
        return any(ROOT.glob(pattern))
    except (OSError, ValueError):
        return False


def parse_card(line: str) -> dict | None:
    m = CARD_RE.match(line)
    if not m:
        return None
    rest = strip_generated(m.group("rest"))
    tags = TAG_RE.findall(rest)
    rest = TAG_RE.sub("", rest)
    fallig = FALLIG_RE.search(rest)
    beleg = BELEG_RE.search(rest)
    rest = FALLIG_RE.sub("", rest)
    rest = BELEG_RE.sub("", rest)

    link = ""
    link_match = re.search(r"→\s*\[\[([^\]|]+)(?:\|[^\]]*)?\]\]", rest)
    if link_match:
        link = link_match.group(1)
    rest = re.sub(r"\s*·?\s*→\s*\[\[[^\]]+\]\]", "", rest)

    rest = rest.strip()
    if rest.startswith("—"):
        rest = rest[1:]
    return {
        "id": plain(m.group("id")),
        "title": plain(m.group("rest_title")),
        "box": m.group("box"),
        "tags": tags,
        "fallig": fallig.group(1) if fallig else "",
        "beleg": beleg.group(1) if beleg else "",
        "text": plain(rest),
        "link": link,
    }


def board() -> dict:
    lanes = {"To Do": [], "Doing": [], "Done": []}
    lane = ""
    for line in read(BOARD).splitlines():
        head = HEAD_RE.match(line)
        if head:
            lane = head.group(1)
            continue
        if lane and line.startswith("- ["):
            card = parse_card(line)
            if card:
                lanes[lane].append(card)
    return lanes


def sortiert(cards: list) -> list:
    """Überfällig zuerst, dann nach Frist, dann der Rest in Board-Reihenfolge."""
    def key(indexed):
        index, card = indexed
        if not card["fallig"]:
            return (2, "", index)
        delta, _ = abstand(card["fallig"])
        if delta is None:
            return (2, "", index)
        return (0 if delta < 0 else 1, card["fallig"], index)

    return [card for _, card in sorted(enumerate(cards), key=key)]


def card_meta(card: dict) -> str:
    parts = []
    if card["tags"]:
        parts.append(" ".join(f"#{tag}" for tag in card["tags"]))
    if card["fallig"]:
        _, when = abstand(card["fallig"])
        parts.append(f"fällig {kurz(card['fallig'])} ({when})")
    if card["beleg"]:
        parts.append("Beleg vorhanden" if beleg_exists(card["beleg"]) else "Beleg fehlt")
    if card["box"] == "x":
        parts.append("erledigt")
    return " · ".join(parts)


def card_lines(card: dict) -> str:
    """Feldinhalt einer Board-Karte; Kennung und Titel stehen schon im Feldnamen."""
    lines = []
    meta = card_meta(card)
    if meta:
        lines.append(meta)
    if card["text"]:
        lines.append(kuerzen(card["text"], 90))
    if card["link"]:
        lines.append(f"→ {card['link']}")
    return "\n".join(lines)


# ---------------------------------------------------------------- Fristen


def fristen() -> list:
    try:
        items = json.loads(read(FRISTEN) or "[]")
    except ValueError:
        return []
    rows = []
    for item in sorted(items, key=lambda entry: entry.get("datum", "")):
        delta, when = abstand(item.get("datum", ""))
        rows.append({**item, "delta": delta, "when": when})
    return rows


def fristen_kurz() -> list:
    return [row for row in fristen() if row["delta"] is not None and row["delta"] <= 7]


# ---------------------------------------------------------------- Notizen


def naechste_aktion() -> tuple[list, str]:
    """Nummerierte Schritte aus `## Nächste Aktion` und der „Zu klären“-Absatz."""
    text = read(STATUS_NOTE)
    section = grab(text, r"## Nächste Aktion\s*\n(.*?)(?=\n## |\Z)", "")
    steps = []
    for line in section.splitlines():
        m = re.match(r"^\d+\.\s+(.*)$", line.strip())
        if m and not m.group(1).strip().startswith("**Stand"):
            steps.append(plain(m.group(1)))
        elif steps and line.startswith("   ") and line.strip():
            steps[-1] = f"{steps[-1]} {plain(line)}"
    zu_klaren = plain(
        grab(section, r"\*\*Zu klären[^*]*:\*\*\s*((?:.|\n)*?)(?=\n\s*\n|\Z)", "")
    )
    return steps, zu_klaren


def offene_entscheidungen() -> list:
    """Abschnitte aus `Offene Entscheidungen.md`, deren Stand „offen“ ist."""
    text = read(OFFEN)
    rows = []
    for match in re.finditer(
        r"^##\s+(\d+)\.\s+(.+?)\n(.*?)(?=\n##\s+\d+\.|\Z)", text, re.S | re.M
    ):
        number, title, body = match.group(1), plain(match.group(2)), match.group(3)
        # Offen ist alles, wofür kein Entscheidungsvermerk vorliegt.
        if re.search(r"\*\*Stand:\s*\*{0,2}\s*entschieden", body):
            continue
        blockiert = plain(grab(body, r"\*\*Blockiert:\*\*\s*(.+)", ""))
        beleg = plain(grab(body, r"\*\*Stand:\s*\*{0,2}\s*((?:.|\n)*?)(?=\n\s*\n|\Z)", ""))
        rows.append(
            {
                "nr": number,
                "titel": title,
                "blockiert": blockiert,
                "stand": beleg[:260],
            }
        )
    return rows


def quellen() -> dict:
    text = read(NEU)
    try:
        deckung = json.loads(read(ABDECKUNG) or "{}")
    except ValueError:
        deckung = {}
    new_items = re.findall(r"^- `([^`]+)`", grab(text, r"## Neu \(\d+\)\s*(.*?)(?=\n## |\Z)", ""), re.M)
    changed = re.findall(
        r"^- `([^`]+)`", grab(text, r"## Geändert \(\d+\)\s*(.*?)(?=\n## |\Z)", ""), re.M
    )
    return {
        "gesamt": grab(text, r"Quellen gesamt:\s*\*\*(\d+)\*\*", "?"),
        "notiz": grab(text, r"durch Notiz:\s*(\d+)", "?"),
        "manuell": grab(text, r"manuell beschrieben:\s*(\d+)", "?"),
        "ausgeschlossen": grab(text, r"ausgeschlossen:\s*(\d+)", "?"),
        "unbekannt": grab(text, r"\*\*unbekannt:\s*(\d+)\*\*", "?"),
        "neu": grab(text, r"## Neu \((\d+)\)", "0"),
        "geaendert": grab(text, r"## Geändert \((\d+)\)", "0"),
        "unveraendert": grab(text, r"## Unverändert:\s*(\d+) Quellen", "0"),
        "neue_liste": new_items,
        "geaenderte_liste": changed,
        "ohne_frist": deckung.get("wochen_ohne_frist", []),
        "unbekannte_dateien": [
            entry.get("pfad", "?")
            for entry in deckung.get("dateien", [])
            if entry.get("status") == "unbekannt"
        ],
    }


# ---------------------------------------------------------------- Bericht


def kopf() -> str:
    lanes = board()
    done = len(lanes["Done"])
    total = done + len(lanes["To Do"]) + len(lanes["Doing"])
    term = fristen()
    faellig = fristen_kurz()
    ueberfaellig = [row for row in term if row["delta"] is not None and row["delta"] < 0]
    q = quellen()
    stamp = last_run_stamp() or datetime.now().strftime("%Y-%m-%d %H:%M")

    if STATUS == "fail":
        lines = [f"❌ **{TITEL} · Lauf {stamp} fehlgeschlagen**"]
        lines.append(
            f"⚠️ Kernschritt fehlgeschlagen: **{DETAIL or 'unbekannt'}** — "
            "Zahlen unten können veraltet sein."
        )
    else:
        lines = [f"**{TITEL} · Lauf {stamp}**"]

    kennzahlen = [
        f"Board {done}/{total}",
        f"offen {len(lanes['To Do'])}",
        f"in Arbeit {len(lanes['Doing'])}",
        f"Fristen bis 7 T. {len(faellig)}",
        f"Quellen {q['gesamt']}",
    ]
    lines.append(" · ".join(kennzahlen))

    warnungen = []
    if ueberfaellig:
        warnungen.append(
            "🔴 überfällig: "
            + ", ".join(f"{row.get('id', '?')} ({-row['delta']} T.)" for row in ueberfaellig)
        )
    if q["unbekannt"] not in ("0", "?"):
        warnungen.append(f"⚠️ {q['unbekannt']} Quellen ohne Abdeckung")
    if q["ohne_frist"]:
        warnungen.append("⚠️ ohne Frist: " + ", ".join(q["ohne_frist"]))
    for warning in warnungen:
        lines.append(warning)
    lines.append(
        "Alle Aufgaben stehen in der **zweiten Nachricht** in einer Kopiervorlage "
        "(ein Code-Block, ein Klick kopiert alles)."
    )
    return "\n".join(lines)


def embed_fristen() -> dict | None:
    rows = fristen()
    if not rows:
        return None
    fields = []
    for row in rows:
        name = f"{kurz(row.get('datum', '?'))} · {row['when']}"
        if row.get("wer"):
            name += f" · {row['wer']}"
        fields.append({"name": name[:MAX_NAME], "value": plain(row.get("titel", "?"))})
    return {
        "title": "⏰ Fristen (belegt, aus fristen.json)",
        "color": 0xE74C3C if any((row["delta"] or 0) < 0 for row in rows) else 0x2ECC71,
        "fields": fields,
    }


def embed_lane(lane: str, icon: str) -> dict | None:
    cards = sortiert(board()[lane])
    if not cards:
        return None
    fields = []
    for card in cards:
        fields.append(
            {"name": f"{card['id']} · {card['title']}"[:MAX_NAME], "value": card_lines(card)}
        )
    return {
        "title": f"{icon} {lane} ({len(cards)})",
        "color": 0xF1C40F if lane == "Doing" else 0x3498DB,
        "fields": fields,
    }


def embed_aktionen() -> dict | None:
    steps, zu_klaren = naechste_aktion()
    if not steps and not zu_klaren:
        return None
    lines = []
    for index, step in enumerate(steps, 1):
        lines.append(f"**{index}.** {kuerzen(step, 300)}")
    if zu_klaren:
        lines.append("")
        lines.append(f"**Zu klären:** {zu_klaren}")
    return {
        "title": "🎯 Nächste Aktion (Status.md)",
        "color": 0x9B59B6,
        "description": "\n".join(lines),
    }


def embed_entscheidungen() -> dict | None:
    rows = offene_entscheidungen()
    if not rows:
        return None
    fields = []
    for row in rows:
        value = f"Blockiert: {kuerzen(row['blockiert'], 150) or '—'}"
        fields.append({"name": f"{row['nr']}. {row['titel']}"[:MAX_NAME], "value": value})
    return {
        "title": f"❓ Offene Entscheidungen ({len(rows)})",
        "color": 0xE67E22,
        "fields": fields,
    }


def embed_quellen() -> dict | None:
    q = quellen()
    if q["gesamt"] == "?":
        return None
    lines = [
        f"Gesamt **{q['gesamt']}**: {q['notiz']} Notiz · {q['manuell']} manuell · "
        f"{q['ausgeschlossen']} ausgeschlossen · **{q['unbekannt']} unbekannt**",
        f"Neu {q['neu']} · geändert {q['geaendert']} · unverändert {q['unveraendert']}",
    ]
    if q["neue_liste"]:
        lines.append("Neu: " + ", ".join(q["neue_liste"][:8]))
    if q["geaenderte_liste"]:
        lines.append("Geändert: " + ", ".join(q["geaenderte_liste"][:8]))
    if q["ohne_frist"]:
        lines.append("Ohne Frist in fristen.json: " + ", ".join(q["ohne_frist"]))
    if q["unbekannte_dateien"]:
        lines.append("Ohne Notiz: " + ", ".join(q["unbekannte_dateien"][:8]))
    return {
        "title": "📥 Quellenstand (letzter Lauf)",
        "color": 0x95A5A6,
        "description": "\n".join(lines),
    }


def kopiervorlage() -> str:
    """Eine Vorlage mit allen Aufgaben als `- [ ]`-Zeilen."""
    lanes = board()
    q = quellen()
    lines = [f"{TITEL} · Stand {TODAY.isoformat()}"]

    rows = fristen()
    if rows:
        lines.append("")
        lines.append("== FRISTEN ==")
        for row in rows:
            wer = f" · {row['wer']}" if row.get("wer") else ""
            lines.append(
                f"- [ ] {kurz(row.get('datum', '?'))} ({row['when']}) "
                f"{row.get('id', '?')} · {plain(row.get('titel', '?'))}{wer}"
            )
            if row.get("detail"):
                lines.append(f"      {kuerzen(plain(row['detail']), 100)}")

    for lane, label in (("To Do", "BOARD · TO DO"), ("Doing", "BOARD · IN ARBEIT")):
        cards = sortiert(lanes[lane])
        if not cards:
            continue
        lines.append("")
        lines.append(f"== {label} ({len(cards)}) ==")
        for card in cards:
            tags = " ".join(f"#{tag}" for tag in card["tags"])
            head = f"- [ ] {card['id']} · {card['title']}"
            if tags:
                head += f" · {tags}"
            if card["fallig"]:
                _, when = abstand(card["fallig"])
                head += f" · fällig {kurz(card['fallig'])} ({when})"
            lines.append(head)
            detail = kuerzen(card["text"], 110)
            if card["beleg"]:
                detail += (
                    " · Beleg vorhanden" if beleg_exists(card["beleg"]) else " · Beleg fehlt"
                )
            if card["link"]:
                detail = f"{detail} · siehe {card['link']}" if detail else f"siehe {card['link']}"
            if detail:
                lines.append(f"      {detail.strip(' ·')}")

    steps, zu_klaren = naechste_aktion()
    if steps:
        lines.append("")
        lines.append("== NÄCHSTE AKTIONEN ==")
        for index, step in enumerate(steps, 1):
            lines.append(f"- [ ] ({index}) {kuerzen(step, 140)}")

    offen = offene_entscheidungen()
    if offen:
        lines.append("")
        lines.append("== ZU KLÄREN ==")
        for row in offen:
            lines.append(f"- [ ] Frage {row['nr']}: {row['titel']}")
            if row["blockiert"]:
                lines.append(f"      blockiert: {kuerzen(row['blockiert'], 120)}")

    if q["unbekannt"] not in ("0", "?"):
        lines.append("")
        lines.append(f"- [ ] {q['unbekannt']} Quellen ohne Abdeckung prüfen")

    lines.append("")
    lines.append("== BELEGE / ORDNER ==")
    lines.append("Portfolio: e-Portfolio/Portfolio/ · Code: e-Portfolio/Programmcode/")
    lines.append("Vorleistung: Prüfungsvorleistung/ · Seite 2: Visual 3. Semester/")
    return "\n".join(lines)


def size_of(content: str, embeds: list) -> int:
    total = len(content)
    for embed in embeds:
        total += len(embed.get("title", "")) + len(embed.get("description", ""))
        for field in embed.get("fields", []):
            total += len(field["name"]) + len(field["value"])
    return total


def validate(content: str, embeds: list, label: str) -> list:
    problems = []
    if len(content) > MAX_CONTENT:
        problems.append(f"{label}: content {len(content)} > {MAX_CONTENT}")
    if len(embeds) > MAX_EMBEDS:
        problems.append(f"{label}: {len(embeds)} embeds > {MAX_EMBEDS}")
    total = size_of(content, embeds)
    if total > 6000:
        problems.append(f"{label}: content+embeds {total} > 6000")
    for embed in embeds:
        if len(embed.get("title", "")) > MAX_NAME:
            problems.append(f"{label}: embed-Titel zu lang")
        if len(embed.get("description", "")) > MAX_DESC:
            problems.append(f"{label}: Beschreibung {len(embed['description'])} > {MAX_DESC}")
        for field in embed.get("fields", []):
            if len(field["name"]) > MAX_NAME or len(field["value"]) > MAX_FIELD:
                problems.append(f"{label}: Feldgrenze gerissen ({field['name'][:40]})")
    return problems


def block_embed() -> dict:
    """Eine Nachricht, ein Code-Block: ein Klick kopiert alle Aufgaben."""
    block = kopiervorlage()
    while len(block) > MAX_DESC - 12 and block.count("\n") > 4:
        block = "\n".join(block.splitlines()[:-1])
    return {
        "title": "📄 Kopiervorlage — ein Klick kopiert alles",
        "color": 0x1ABC9C,
        "description": f"```text\n{block}\n```",
    }


def trim_details(embeds: list) -> None:
    """Kürzt bei sehr großem Board den längsten Block, bis der Bericht passt."""
    def trim_once() -> bool:
        best = None
        for embed in embeds:
            description = embed.get("description", "")
            if description and (best is None or len(description) > best[0]):
                best = (len(description), embed, "description")
            for field in embed.get("fields", []):
                if best is None or len(field["value"]) > best[0]:
                    best = (len(field["value"]), field, "value")
        if not best or best[0] < 160:
            return False
        size, holder, key = best
        rows = holder[key].splitlines()
        holder[key] = (
            "\n".join(rows[:-1]) if len(rows) > 1 else holder[key][: size - 120].rstrip() + " …"
        )
        return True

    while size_of(kopf(), embeds) > BUDGET and trim_once():
        continue


def build() -> tuple[tuple[str, list], tuple[str, list]]:
    embeds = [
        embed
        for embed in (
            embed_fristen(),
            embed_lane("To Do", "🟦"),
            embed_lane("Doing", "🟨"),
            embed_aktionen(),
            embed_entscheidungen(),
            embed_quellen(),
        )
        if embed
    ]
    trim_details(embeds)
    details = (kopf()[:MAX_CONTENT], embeds)
    copy = (
        "📄 **Kopiervorlage unten** — Fristen, offene Karten, nächste Schritte und offene "
        "Fragen in einem Block. Ein Klick auf das Kopiersymbol des Blocks kopiert alles.",
        [block_embed()],
    )
    return details, copy


def show(content: str, embeds: list, label: str) -> None:
    print(f"── {label} ──")
    print(content)
    for embed in embeds:
        print()
        print(f"── {embed.get('title', '')} ──")
        if embed.get("description"):
            print(embed["description"])
        for field in embed.get("fields", []):
            print(f"• {field['name']}")
            for line in field["value"].splitlines():
                print(f"    {line}")


def send(url: str, content: str, embeds: list) -> int:
    body = json.dumps(
        {"content": content, "embeds": embeds, "username": TITEL},
        ensure_ascii=False,
    ).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", "User-Agent": "InfoVis-Notifier"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.status


def main() -> int:
    (details_text, details_embeds), (copy_text, copy_embeds) = build()
    problems = validate(details_text, details_embeds, "Bericht") + validate(
        copy_text, copy_embeds, "Kopiervorlage"
    )
    url = webhook()

    if DRY:
        show(details_text, details_embeds, "Nachricht 1 · Bericht")
        print()
        show(copy_text, copy_embeds, "Nachricht 2 · Kopiervorlage")
        print()
        print(
            "Prüfung: Bericht "
            f"{size_of(details_text, details_embeds)}/6000 · Kopiervorlage "
            f"{size_of(copy_text, copy_embeds)}/6000 · content "
            f"{len(details_text)}/{MAX_CONTENT} · embeds "
            f"{len(details_embeds) + len(copy_embeds)}/{MAX_EMBEDS * 2}"
        )
        for problem in problems:
            print(f"FEHLER: {problem}")
        if not url:
            print("\nDiscord: kein Webhook hinterlegt, nicht gesendet.")
        return 1 if problems else 0

    if not url:
        print("Discord: übersprungen (kein Webhook hinterlegt)")
        return 0

    if not url.startswith(ALLOWED):
        print("Discord: Adresse ist keine Discord-Webhook-Adresse, nicht gesendet")
        return 1

    codes = []
    try:
        for content, embeds in ((details_text, details_embeds), (copy_text, copy_embeds)):
            codes.append(send(url, content, embeds))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:300]
        print(f"Discord: Fehler HTTP {exc.code} {detail} (nach {len(codes)} von 2 Nachrichten)")
        return 1
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"Discord: Fehler {exc} (nach {len(codes)} von 2 Nachrichten)")
        return 1

    print(f"Discord: gesendet (HTTP {', '.join(str(code) for code in codes)}, 2 Nachrichten)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
