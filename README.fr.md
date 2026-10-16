# 2048 Jeu Décontracté

> Un jeu de fusion de nombres 2048 au thème sombre « deep-space neon », propulsé par Python + Pygame, conçu pour le bureau Windows.

**Version actuelle : [v0.0.1](https://github.com/MagicSquarekey/2048/releases/tag/v0.0.1)** · [简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Italiano](README.it.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Tiếng Việt](README.vi.md) · [ภาษาไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

---

## 📖 Langues

| Langue | Document |
|---|---|
| 简体中文 | [README.md](README.md) |
| English | [README.en.md](README.en.md) |
| 日本語 | [README.ja.md](README.ja.md) |
| 繁體中文 | [README.zh-TW.md](README.zh-TW.md) |
| 한국어 | [README.ko.md](README.ko.md) |
| Français (actuel) | [README.fr.md](README.fr.md) |
| Deutsch | [README.de.md](README.de.md) |
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

## ✨ Points forts

- 🎨 **Thème deep-space neon** : fond dégradé indigo avec lueurs dérivantes, cartes en verre dépoli, et tuiles avec dégradés, liseré lumineux et halo néon
- ⚡ **Contrôles ultra fluides** : file d'entrée + glissement continu par appui long (~7 coups/sec) + animations indépendantes du framerate — les combos rapides ne perdent aucune entrée
- 💥 **Animations & effets** : explosions de particules à la fusion, secousse d'écran sur les grandes fusions, confettis de victoire, transition de fin animée, fondus de page
- 🌍 **Interface bilingue** : basculez entre chinois et anglais en un clic dans le jeu

## 🎮 Modes de jeu

| Mode | Description |
|------|-------------|
| **Classique** | Sans limite de temps — battez votre meilleur score |
| **Contre-la-montre** | Atteignez le score cible en 60 secondes |
| **Défi** | Atteignez la tuile 128 en 50 coups |

**Commandes** : touches fléchées / WASD / glissement souris · `ESC` pour mettre en pause

## 🧰 Power-ups

- **Annuler** : revenir au coup précédent (3 par partie)
- **Nettoyer** : supprimer la plus petite tuile (1 par partie)
- **Réanimer** : après un game over, supprimez deux plus petites tuiles et continuez

## 🏆 Autres fonctionnalités

- Système de succès (6 succès à débloquer)
- Suivi du meilleur score / du total de parties
- Badge de nouveau record + animation de décompte du score sur la page de résultats
- Interrupteurs d'effets sonores et de musique de fond

---

## 🖥️ Configuration requise

- Windows 10 / 11
- Python 3.10+
- Pygame 2.6.1

## 🚀 Démarrage rapide

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Lancer le jeu

```bash
python src/main.py
```

### 3. Empaqueter en EXE

```bash
# Construction en un clic (recommandé)
python scripts/build_auto.py

# Construction interactive
python scripts/build.py
```

L'exécutable se trouve dans `dist/2048/2048.exe` — double-cliquez pour jouer, sans Python ni dépendances. Voir [scripts/README.md](scripts/README.md) pour plus de détails.

---

## 📁 Structure du projet

```
2048/
├── src/                    # Code source
│   ├── main.py             # Point d'entrée
│   ├── config.py           # Config globale (thème / animation / entrée)
│   ├── i18n.py             # Localisation (chinois & anglais)
│   ├── utils.py            # Assistants de dessin, caches, courbes d'animation
│   ├── models/             # Modèles de données (plateau / état / sauvegarde / succès)
│   └── views/              # Couche vue
│       ├── ui_components.py  # Composants UI (boutons / cartes de score / interrupteurs / alertes)
│       ├── board_view.py     # Rendu & animation du plateau
│       ├── effects.py        # Système de particules & secousse d'écran
│       ├── sound_manager.py  # Gestion du son
│       └── pages/            # Pages (menu / jeu / résultats / réglages / succès / pause / connexion)
├── tests/                  # Tests (359 tests unitaires + simulation utilisateur E2E)
├── scripts/                # Scripts de build & d'empaquetage
├── docs/                   # Documentation
├── private/                # Fichiers privés
├── dist/                   # Sortie de build (.gitignore)
├── build/                  # Fichiers temporaires de build (.gitignore)
└── requirements.txt        # Liste des dépendances
```

## 🔧 Guide de développement

### Lancer les tests

```bash
# Tous les tests unitaires
python -m pytest tests/

# Simulation utilisateur de bout en bout (E2E)
python tests/e2e_user_simulation.py

# Capturer les captures d'écran UI
python tests/capture_ui_review.py
```

Couverture : algorithme du plateau, état du jeu, cycles de vie complets des trois modes, power-ups, pause/redémarrage, combos à file d'entrée, tests de charge et budget de performance 60FPS.

### Normes de code

- **Nommage fichier / fonction** : `lower_snake_case` · **Nommage classe** : `PascalCase` · **Indentation** : 4 espaces · **Largeur de ligne** : 120 caractères max
- **Commits Git** : `<type>(<scope>): <subject>` avec `feat / fix / docs / style / refactor / test / chore`

---

## 📜 Licence

[MIT License](LICENSE) © 2026 MagicSquarekey

## 🤝 Contribution

Les Issues et Pull Request sont les bienvenues !

## 📞 Contact

Des questions ? Passez par [GitHub Issues](https://github.com/MagicSquarekey/2048/issues).
