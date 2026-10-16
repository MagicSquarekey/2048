# 2048 Gioco Casual

> Un gioco di fusione di numeri 2048 con tema scuro «deep-space neon», basato su Python + Pygame, realizzato per il desktop Windows.

**Versione attuale: [v0.0.1](https://github.com/MagicSquarekey/2048/releases/tag/v0.0.1)** · [简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Tiếng Việt](README.vi.md) · [ภาษาไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

---

## 📖 Lingue

| Lingua | Documento |
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
| Italiano (attuale) | [README.it.md](README.it.md) |
| Nederlands | [README.nl.md](README.nl.md) |
| Türkçe | [README.tr.md](README.tr.md) |
| Tiếng Việt | [README.vi.md](README.vi.md) |
| ภาษาไทย | [README.th.md](README.th.md) |
| Bahasa Indonesia | [README.id.md](README.id.md) |
| हिन्दी | [README.hi.md](README.hi.md) |
| العربية | [README.ar.md](README.ar.md) |

---

## ✨ Punti di forza

- 🎨 **Tema deep-space neon**: sfondo a gradiente indaco con bagliori alla deriva, carte in vetro smerigliato e tessere con gradienti, luce sul bordo e alone al neon
- ⚡ **Controlli fluidissimi**: coda di input + scorrimento continuo tenendo premuto (~7 mosse/sec) + animazioni indipendenti dal framerate — le combo rapide non perdono input
- 💥 **Animazioni ed effetti**: esplosioni di particelle alla fusione, scuotimento dello schermo sulle fusioni grandi, coriandoli della vittoria, transizione di fine animata, dissolvenze di pagina
- 🌍 **Interfaccia bilingue**: passa tra cinese e inglese con un tocco nel gioco

## 🎮 Modalità di gioco

| Modalità | Descrizione |
|----------|-------------|
| **Classica** | Nessun limite di tempo — insegui il tuo punteggio migliore |
| **A tempo** | Raggiungi il punteggio obiettivo in 60 secondi |
| **Sfida** | Raggiungi la tessera 128 in 50 mosse |

**Comandi**: frecce / WASD / scorrimento col mouse · `ESC` per mettere in pausa

## 🧰 Potenziamenti

- **Annulla**: annulla l'ultima mossa (3 per partita)
- **Pulisci**: rimuovi la tessera più piccola (1 per partita)
- **Rianima**: dopo il game over, rimuovi due tessere più piccole e continua

## 🏆 Altre funzioni

- Sistema di obiettivi (6 obiettivi da sbloccare)
- Tracciamento del punteggio migliore / totale partite
- Distintivo di nuovo record + animazione di conteggio del punteggio nella pagina dei risultati
- Interruttori per effetti sonori e musica di sottofondo

---

## 🖥️ Requisiti di sistema

- Windows 10 / 11
- Python 3.10+
- Pygame 2.6.1

## 🚀 Avvio rapido

### 1. Installa le dipendenze

```bash
pip install -r requirements.txt
```

### 2. Esegui il gioco

```bash
python src/main.py
```

### 3. Impacchetta come EXE

```bash
# Build con un clic (consigliata)
python scripts/build_auto.py

# Build interattiva
python scripts/build.py
```

L'eseguibile si trova in `dist/2048/2048.exe` — fai doppio clic per giocare, senza Python né dipendenze. Vedi [scripts/README.md](scripts/README.md) per i dettagli.

---

## 📁 Struttura del progetto

```
2048/
├── src/                    # Codice sorgente
│   ├── main.py             # Punto di ingresso
│   ├── config.py           # Config globale (tema / animazione / input)
│   ├── i18n.py             # Localizzazione (cinese e inglese)
│   ├── utils.py            # Helper di disegno, cache, curve di animazione
│   ├── models/             # Modelli di dati (scacchiera / stato / salvataggio / obiettivi)
│   └── views/              # Livello di visualizzazione
│       ├── ui_components.py  # Componenti UI (pulsanti / schede punteggio / interruttori / avvisi)
│       ├── board_view.py     # Rendering e animazione della scacchiera
│       ├── effects.py        # Sistema di particelle e scuotimento schermo
│       ├── sound_manager.py  # Gestione del suono
│       └── pages/            # Pagine (menu / gioco / risultati / impostazioni / obiettivi / pausa / login)
├── tests/                  # Test (359 test unitari + simulazione utente E2E)
├── scripts/                # Script di build e impacchettamento
├── docs/                   # Documentazione
├── private/                # File privati
├── dist/                   # Output di build (.gitignore)
├── build/                  # File temporanei di build (.gitignore)
└── requirements.txt        # Elenco dipendenze
```

## 🔧 Guida allo sviluppo

### Esegui i test

```bash
# Tutti i test unitari
python -m pytest tests/

# Simulazione utente end-to-end (E2E)
python tests/e2e_user_simulation.py

# Cattura screenshot della UI
python tests/capture_ui_review.py
```

Copertura: algoritmo della scacchiera, stato del gioco, cicli di vita completi delle tre modalità, potenziamenti, pausa/riavvio, combo con coda di input, test di stress e budget di prestazioni 60FPS.

### Standard di codice

- **Nomi file / funzioni**: `lower_snake_case` · **Nomi classi**: `PascalCase` · **Indentazione**: 4 spazi · **Larghezza riga**: max 120 caratteri
- **Commit Git**: `<type>(<scope>): <subject>` con `feat / fix / docs / style / refactor / test / chore`

---

## 📜 Licenza

[MIT License](LICENSE) © 2026 MagicSquarekey

## 🤝 Contribuire

Issue e Pull Request sono benvenute!

## 📞 Contatti

Domande? Tramite [GitHub Issues](https://github.com/MagicSquarekey/2048/issues).
