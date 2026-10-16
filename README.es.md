# 2048 Juego Casual

> Un juego de fusión de números 2048 con tema oscuro «deep-space neon», impulsado por Python + Pygame, hecho para el escritorio de Windows.

**Versión actual: [v0.0.1](https://github.com/MagicSquarekey/2048/releases/tag/v0.0.1)** · [简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Italiano](README.it.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Tiếng Việt](README.vi.md) · [ภาษาไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

---

## 📖 Idiomas

| Idioma | Documento |
|---|---|
| 简体中文 | [README.md](README.md) |
| English | [README.en.md](README.en.md) |
| 日本語 | [README.ja.md](README.ja.md) |
| 繁體中文 | [README.zh-TW.md](README.zh-TW.md) |
| 한국어 | [README.ko.md](README.ko.md) |
| Français | [README.fr.md](README.fr.md) |
| Deutsch | [README.de.md](README.de.md) |
| Español (actual) | [README.es.md](README.es.md) |
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

## ✨ Aspectos destacados

- 🎨 **Tema deep-space neon**: fondo degradado índigo con brillos a la deriva, tarjetas de cristal esmerilado y fichas con degradados, luz de borde y resplandor de neón
- ⚡ **Controles muy suaves**: cola de entrada + deslizamiento continuo al mantener pulsado (~7 movimientos/seg) + animaciones independientes del framerate — los combos rápidos no pierden entradas
- 💥 **Animaciones y efectos**: explosiones de partículas al fusionar, sacudida de pantalla en fusiones grandes, confeti de victoria, transición de fin animada, fundidos de página
- 🌍 **Interfaz bilingüe**: cambia entre chino e inglés con un toque dentro del juego

## 🎮 Modos de juego

| Modo | Descripción |
|------|-------------|
| **Clásico** | Sin límite de tiempo — consigue tu mejor puntuación |
| **Contrarreloj** | Alcanza la puntuación objetivo en 60 segundos |
| **Desafío** | Alcanza la ficha 128 en 50 movimientos |

**Controles**: flechas / WASD / deslizar ratón · `ESC` para pausar

## 🧰 Power-ups

- **Deshacer**: revertir el último movimiento (3 por partida)
- **Limpiar**: eliminar la ficha más pequeña (1 por partida)
- **Reanimar**: tras el game over, elimina dos fichas más pequeñas y sigue jugando

## 🏆 Otras funciones

- Sistema de logros (6 logros por desbloquear)
- Seguimiento de mejor puntuación / total de partidas
- Insignia de nuevo récord + animación de recuento de puntos en la página de resultados
- Interruptores de efectos de sonido y música de fondo

---

## 🖥️ Requisitos del sistema

- Windows 10 / 11
- Python 3.10+
- Pygame 2.6.1

## 🚀 Inicio rápido

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar el juego

```bash
python src/main.py
```

### 3. Empaquetar como EXE

```bash
# Compilación de un clic (recomendado)
python scripts/build_auto.py

# Compilación interactiva
python scripts/build.py
```

El ejecutable queda en `dist/2048/2048.exe` — doble clic para jugar, sin Python ni dependencias. Ver [scripts/README.md](scripts/README.md) para más detalles.

---

## 📁 Estructura del proyecto

```
2048/
├── src/                    # Código fuente
│   ├── main.py             # Punto de entrada
│   ├── config.py           # Config global (tema / animación / entrada)
│   ├── i18n.py             # Localización (chino e inglés)
│   ├── utils.py            # Ayudas de dibujo, cachés, curvas de animación
│   ├── models/             # Modelos de datos (tablero / estado / guardado / logros)
│   └── views/              # Capa de vista
│       ├── ui_components.py  # Componentes UI (botones / tarjetas de puntos / interruptores / alertas)
│       ├── board_view.py     # Renderizado y animación del tablero
│       ├── effects.py        # Sistema de partículas y sacudida de pantalla
│       ├── sound_manager.py  # Gestión de sonido
│       └── pages/            # Páginas (menú / juego / resultado / ajustes / logros / pausa / login)
├── tests/                  # Pruebas (359 pruebas unitarias + simulación de usuario E2E)
├── scripts/                # Scripts de compilación y empaquetado
├── docs/                   # Documentación
├── private/                # Archivos privados
├── dist/                   # Salida de compilación (.gitignore)
├── build/                  # Archivos temporales de compilación (.gitignore)
└── requirements.txt        # Lista de dependencias
```

## 🔧 Guía de desarrollo

### Ejecutar pruebas

```bash
# Todas las pruebas unitarias
python -m pytest tests/

# Simulación de usuario de extremo a extremo (E2E)
python tests/e2e_user_simulation.py

# Capturar capturas de pantalla de la UI
python tests/capture_ui_review.py
```

Cobertura: algoritmo del tablero, estado del juego, ciclos de vida completos de los tres modos, power-ups, pausa/reinicio, combos con cola de entrada, pruebas de estrés y presupuesto de rendimiento de 60FPS.

### Estándares de código

- **Nombres de archivo / función**: `lower_snake_case` · **Nombres de clase**: `PascalCase` · **Indentación**: 4 espacios · **Ancho de línea**: máx. 120 caracteres
- **Commits de Git**: `<type>(<scope>): <subject>` con `feat / fix / docs / style / refactor / test / chore`

---

## 📜 Licencia

[MIT License](LICENSE) © 2026 MagicSquarekey

## 🤝 Contribuir

¡Las Issues y Pull Request son bienvenidas!

## 📞 Contacto

¿Preguntas? A través de [GitHub Issues](https://github.com/MagicSquarekey/2048/issues).
