# 2048 Casual Game

> Ein 2048-Zahlen-Zusammensetzungs-Spiel im Dark-Theme „Deep-Space Neon", angetrieben von Python + Pygame, für den Windows-Desktop entwickelt.

**Aktuelle Version: [v0.0.1](https://github.com/MagicSquarekey/2048/releases/tag/v0.0.1)** · [简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Français](README.fr.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Italiano](README.it.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Tiếng Việt](README.vi.md) · [ภาษาไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

---

## 📖 Sprachen

| Sprache | Dokument |
|---|---|
| 简体中文 | [README.md](README.md) |
| English | [README.en.md](README.en.md) |
| 日本語 | [README.ja.md](README.ja.md) |
| 繁體中文 | [README.zh-TW.md](README.zh-TW.md) |
| 한국어 | [README.ko.md](README.ko.md) |
| Français | [README.fr.md](README.fr.md) |
| Deutsch (aktuell) | [README.de.md](README.de.md) |
| Español | [README.es.md](README.es.md) |
| Português | [README.pt.md](README.pt.md) |
| Русский | [README.ru.md](README.ru.md) |
| Italiano | [README.it.md](README.it.md) |
| Nederlands | [README.nl.md](README.nl.md) |
| Türkçe | [README.tr.md](README.tr.md) |
| Tiếng Việt | [README.vi.md](README.vi.md) |
| ภาษาไทย | [README.th.md](README.th.md) |
| Bahasa Indonesia | [README.id.md](README.id.md) |
| हिन्दी | [README.hi.md](README.hi.md) |
| العربية | [README.ar.md](README.ar.md) |

---

## ✨ Highlights

- 🎨 **Deep-Space-Neon-Theme**: indigofarbener Farbverlauf-Hintergrund mit driftenden Leuchteffekten, Glas-Karten und Steinen mit Farbverläufen, Randlicht und Neon-Glow
- ⚡ **Butterweiche Steuerung**: Eingabe-Warteschlange + Gleiten durch Gedrückthalten (~7 Züge/Sek.) + framerate-unabhängige Animationen — schnelle Combos verlieren keine Eingabe
- 💥 **Motion & Effekte**: Partikel-Explosionen beim Verschmelzen, Bildschirmwackeln bei großen Verschmelzungen, Sieges-Konfetti, animierter Game-Over-Übergang, Seiten-Fades
- 🌍 **Zweisprachige UI**: im Spiel per Tastendruck zwischen Chinesisch und Englisch wechseln

## 🎮 Spielmodi

| Modus | Beschreibung |
|------|-------------|
| **Klassisch** | Kein Zeitlimit — jagen Sie Ihren Bestwert |
| **Zeitrennen** | Erreichen Sie den Ziel-Score in 60 Sekunden |
| **Herausforderung** | Erreichen Sie den Stein 128 in 50 Zügen |

**Steuerung**: Pfeiltasten / WASD / Maus-Wischen · `ESC` zum Pausieren

## 🧰 Power-ups

- **Rückgängig**: letzten Zug zurücknehmen (3 pro Spiel)
- **Löschen**: den kleinsten Stein entfernen (1 pro Spiel)
- **Wiederbeleben**: nach Game Over zwei kleinste Steine entfernen und weiterspielen

## 🏆 Weitere Funktionen

- Erfolgssystem (6 Erfolge freizuschalten)
- Bestwert / Gesamtspiele-Verfolgung
- Rekord-Abzeichen + Score-Aufroll-Animation auf der Ergebnisseite
- Schalter für Soundeffekte und Hintergrundmusik

---

## 🖥️ Systemanforderungen

- Windows 10 / 11
- Python 3.10+
- Pygame 2.6.1

## 🚀 Schnellstart

### 1. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 2. Spiel starten

```bash
python src/main.py
```

### 3. Als EXE paketieren

```bash
# Ein-Klick-Build (empfohlen)
python scripts/build_auto.py

# Interaktiver Build
python scripts/build.py
```

Die ausführbare Datei liegt unter `dist/2048/2048.exe` — doppelklicken zum Spielen, ohne Python oder Abhängigkeiten. Details unter [scripts/README.md](scripts/README.md).

---

## 📁 Projektstruktur

```
2048/
├── src/                    # Quellcode
│   ├── main.py             # Einstiegspunkt
│   ├── config.py           # Globale Konfiguration (Theme / Animation / Eingabe)
│   ├── i18n.py             # Lokalisierung (Chinesisch & Englisch)
│   ├── utils.py            # Zeichenhelfer, Caches, Animationskurven
│   ├── models/             # Datenmodelle (Board / Zustand / Speichern / Erfolge)
│   └── views/              # View-Schicht
│       ├── ui_components.py  # UI-Komponenten (Buttons / Score-Karten / Schalter / Alarme)
│       ├── board_view.py     # Board-Rendering & Animation
│       ├── effects.py        # Partikelsystem & Bildschirmwackeln
│       ├── sound_manager.py  # Sound-Verwaltung
│       └── pages/            # Seiten (Menü / Spiel / Ergebnis / Einstellungen / Erfolge / Pause / Login)
├── tests/                  # Tests (359 Unit-Tests + E2E-Nutzersimulation)
├── scripts/                # Build- & Paketierungsskripte
├── docs/                   # Dokumentation
├── private/                # Private Dateien
├── dist/                   # Build-Ausgabe (.gitignore)
├── build/                  # Build-Temp-Dateien (.gitignore)
└── requirements.txt        # Abhängigkeitsliste
```

## 🔧 Entwicklungshandbuch

### Tests ausführen

```bash
# Alle Unit-Tests
python -m pytest tests/

# End-to-End-Nutzersimulation
python tests/e2e_user_simulation.py

# UI-Screenshots aufnehmen
python tests/capture_ui_review.py
```

Abdeckung: Board-Algorithmus, Spielzustand, vollständige Lebenszyklen aller drei Modi, Power-ups, Pause/Neustart, Eingabe-Warteschlange-Combos, Lasttests und 60FPS-Performance-Budget.

### Code-Standards

- **Datei- / Funktionsbenennung**: `lower_snake_case` · **Klassenbenennung**: `PascalCase` · **Einrückung**: 4 Leerzeichen · **Zeilenbreite**: max. 120 Zeichen
- **Git-Commits**: `<type>(<scope>): <subject>` mit `feat / fix / docs / style / refactor / test / chore`

---

## 📜 Lizenz

[MIT License](LICENSE) © 2026 MagicSquarekey

## 🤝 Mitwirken

Issues und Pull Requests sind willkommen!

## 📞 Kontakt

Fragen? Über [GitHub Issues](https://github.com/MagicSquarekey/2048/issues).
