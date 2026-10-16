# 2048 Casuäl spel

> Een 2048-cijferfusiespel met een «deep-space neon» donker thema, aangedreven door Python + Pygame, gebouwd voor het Windows-bureaublad.

**Huidige versie: [v0.0.1](https://github.com/MagicSquarekey/2048/releases/tag/v0.0.1)** · [简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Italiano](README.it.md) · [Türkçe](README.tr.md) · [Tiếng Việt](README.vi.md) · [ภาษาไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

---

## 📖 Talen

| Taal | Document |
|---|---|
| 简体中文 | [README.md](README.md) |
| English | [README.en.md](README.en.md) |
| 日本語 | [README.ja.md](README.ja.md) |
| 繁體中文 | [README.zh-TW.md](README.zh-TW.md) |
| 한국어 | [README.ko.md](README.ko.md) |
| Français | [README.fr.md](README.fr.md) |
| Deutsch | [README.de.md](README.de.md) |
| Español | [README.es.md](README.es.md) |
| Português | [README.pt.md](README.pt.md) |
| Русский | [README.ru.md](README.ru.md) |
| Italiano | [README.it.md](README.it.md) |
| Nederlands (huidige) | [README.nl.md](README.nl.md) |
| Türkçe | [README.tr.md](README.tr.md) |
| Tiếng Việt | [README.vi.md](README.vi.md) |
| ภาษาไทย | [README.th.md](README.th.md) |
| Bahasa Indonesia | [README.id.md](README.id.md) |
| हिन्दी | [README.hi.md](README.hi.md) |
| العربية | [README.ar.md](README.ar.md) |

---

## ✨ Hoogtepunten

- 🎨 **Deep-space neon-thema**: indigo gradiëntachtergrond met langzaam bewegende gloeden, glasachtige kaarten en tegels met gradiënten, randlicht en neongloed
- ⚡ **Zeer soepele besturing**: invoerwachtrij + continu schuiven door ingedrukt te houden (~7 zetten/sec) + framerate-onafhankelijke animaties — snelle combo's verliezen geen invoer
- 💥 **Beweging & effecten**: deeltje-explosies bij het samenvoegen, schermschud bij grote samenvoegingen, overwinningsconfetti, geanimeerde game-over-overgang, pagina-fades
- 🌍 **Tweetalige interface**: schakel in-game met één tik tussen Chinees en Engels

## 🎮 Spelmodi

| Modus | Beschrijving |
|-------|-------------|
| **Klassiek** | Geen tijdslimiet — jaag op je beste score |
| **Tegen de klok** | Haal de doelscore binnen 60 seconden |
| **Uitdaging** | Bereik de tegel 128 binnen 50 zetten |

**Besturing**: pijltjestoetsen / WASD / muisschuif · `ESC` om te pauzeren

## 🧰 Power-ups

- **Ongedaan maken**: laatste zet terugdraaien (3 per spel)
- **Wissen**: de kleinste tegel verwijderen (1 per spel)
- **Wederopstanding**: na game over twee kleinste tegels verwijderen en doorgaan

## 🏆 Overige functies

- Prestatiesysteem (6 prestaties te ontgrendelen)
- Bijhouden van beste score / totaal aantal spellen
- Nieuwe-record-badge + score-opbouwanimatie op de resultatenpagina
- Schakelaars voor geluidseffecten en achtergrondmuziek

---

## 🖥️ Systeemvereisten

- Windows 10 / 11
- Python 3.10+
- Pygame 2.6.1

## 🚀 Snelstart

### 1. Installeer afhankelijkheden

```bash
pip install -r requirements.txt
```

### 2. Start het spel

```bash
python src/main.py
```

### 3. Verpak als EXE

```bash
# Eén-kliks build (aanbevolen)
python scripts/build_auto.py

# Interactieve build
python scripts/build.py
```

Het uitvoerbare bestand komt in `dist/2048/2048.exe` — dubbelklik om te spelen, zonder Python of afhankelijkheden. Zie [scripts/README.md](scripts/README.md) voor details.

---

## 📁 Projectstructuur

```
2048/
├── src/                    # Broncode
│   ├── main.py             # Ingangspunt
│   ├── config.py           # Globale configuratie (thema / animatie / invoer)
│   ├── i18n.py             # Lokalisatie (Chinees & Engels)
│   ├── utils.py            # Tekenhelpers, caches, animatiecurves
│   ├── models/             # Gegevensmodellen (bord / staat / opslag / prestaties)
│   └── views/              # View-laag
│       ├── ui_components.py  # UI-componenten (knoppen / scorekaarten / schakelaars / waarschuwingen)
│       ├── board_view.py     # Bordweergave & animatie
│       ├── effects.py        # Deeltjessysteem & schermschud
│       ├── sound_manager.py  # Geluidsbeheer
│       └── pages/            # Pagina's (menu / spel / resultaat / instellingen / prestaties / pauze / login)
├── tests/                  # Tests (359 unit-tests + E2E-gebruikerssimulatie)
├── scripts/                # Build- & verpakkingsscripts
├── docs/                   # Documentatie
├── private/                # Privébestanden
├── dist/                   # Build-uitvoer (.gitignore)
├── build/                  # Tijdelijke build-bestanden (.gitignore)
└── requirements.txt        # Afhankelijkheidslijst
```

## 🔧 Ontwikkelgids

### Tests uitvoeren

```bash
# Alle unit-tests
python -m pytest tests/

# End-to-end gebruikerssimulatie
python tests/e2e_user_simulation.py

# UI-schermafbeeldingen vastleggen
python tests/capture_ui_review.py
```

Dekking: bordalgoritme, spelstatus, volledige levenscycli van alle drie de modi, power-ups, pauze/herstart, invoerwachtrij-combo's, stresstests en 60FPS-prestatiebudget.

### Codenormen

- **Bestands-/functienamen**: `lower_snake_case` · **Klassenamen**: `PascalCase` · **Inspringing**: 4 spaties · **Regelbreedte**: max. 120 tekens
- **Git-commits**: `<type>(<scope>): <subject>` met `feat / fix / docs / style / refactor / test / chore`

---

## 📜 Licentie

[MIT License](LICENSE) © 2026 MagicSquarekey

## 🤝 Bijdragen

Issues en Pull Requests zijn welkom!

## 📞 Contact

Vragen? Via [GitHub Issues](https://github.com/MagicSquarekey/2048/issues).
