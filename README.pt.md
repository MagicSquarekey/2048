# 2048 Jogo Casual

> Um jogo de fusão de números 2048 com tema escuro «deep-space neon», desenvolvido com Python + Pygame, para o desktop Windows.

**Versão atual: [v0.0.1](https://github.com/MagicSquarekey/2048/releases/tag/v0.0.1)** · [简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Русский](README.ru.md) · [Italiano](README.it.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Tiếng Việt](README.vi.md) · [ภาษาไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

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
| Español | [README.es.md](README.es.md) |
| Português (atual) | [README.pt.md](README.pt.md) |
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

## ✨ Destaques

- 🎨 **Tema deep-space neon**: fundo degradado índigo com brilhos à deriva, cartões de vidro fosco e peças com degradês, luz de borda e brilho de néon
- ⚡ **Controles suaves**: fila de entrada + deslizamento contínuo ao manter pressionado (~7 jogadas/seg) + animações independentes de framerate — combos rápidos não perdem entrada
- 💥 **Animações e efeitos**: explosões de partículas na fusão, tremor de tela em fusões grandes, confete de vitória, transição de fim animada, fusões de página
- 🌍 **Interface bilíngue**: alterne entre chinês e inglês com um toque no jogo

## 🎮 Modos de jogo

| Modo | Descrição |
|------|-----------|
| **Clássico** | Sem limite de tempo — busque sua melhor pontuação |
| **Contrarrelógio** | Alcance a pontuação-alvo em 60 segundos |
| **Desafio** | Alcance a peça 128 em 50 jogadas |

**Controles**: setas / WASD / deslizar o mouse · `ESC` para pausar

## 🧰 Power-ups

- **Desfazer**: reverter a última jogada (3 por partida)
- **Limpar**: remover a menor peça (1 por partida)
- **Reanimar**: após o game over, remova duas menores peças e continue

## 🏆 Outros recursos

- Sistema de conquistas (6 conquistas para desbloquear)
- Rastreamento de melhor pontuação / total de partidas
- Distintivo de novo recorde + animação de contagem de pontos na página de resultados
- Interruptores de efeitos sonoros e música de fundo

---

## 🖥️ Requisitos do sistema

- Windows 10 / 11
- Python 3.10+
- Pygame 2.6.1

## 🚀 Início rápido

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Executar o jogo

```bash
python src/main.py
```

### 3. Empacotar como EXE

```bash
# Compilação de um clique (recomendado)
python scripts/build_auto.py

# Compilação interativa
python scripts/build.py
```

O executável fica em `dist/2048/2048.exe` — clique duplo para jogar, sem Python nem dependências. Veja [scripts/README.md](scripts/README.md) para detalhes.

---

## 📁 Estrutura do projeto

```
2048/
├── src/                    # Código-fonte
│   ├── main.py             # Ponto de entrada
│   ├── config.py           # Config global (tema / animação / entrada)
│   ├── i18n.py             # Localização (chinês e inglês)
│   ├── utils.py            # Auxiliares de desenho, caches, curvas de animação
│   ├── models/             # Modelos de dados (tabuleiro / estado / save / conquistas)
│   └── views/              # Camada de visualização
│       ├── ui_components.py  # Componentes de UI (botões / cartões de pontos / interruptores / alertas)
│       ├── board_view.py     # Renderização e animação do tabuleiro
│       ├── effects.py        # Sistema de partículas e tremor de tela
│       ├── sound_manager.py  # Gerenciamento de som
│       └── pages/            # Páginas (menu / jogo / resultado / ajustes / conquistas / pausa / login)
├── tests/                  # Testes (359 testes unitários + simulação de usuário E2E)
├── scripts/                # Scripts de build e empacotamento
├── docs/                   # Documentação
├── private/                # Arquivos privados
├── dist/                   # Saída de build (.gitignore)
├── build/                  # Arquivos temporários de build (.gitignore)
└── requirements.txt        # Lista de dependências
```

## 🔧 Guia de desenvolvimento

### Executar testes

```bash
# Todos os testes unitários
python -m pytest tests/

# Simulação de usuário de ponta a ponta (E2E)
python tests/e2e_user_simulation.py

# Capturar capturas de tela da UI
python tests/capture_ui_review.py
```

Cobertura: algoritmo do tabuleiro, estado do jogo, ciclos de vida completos dos três modos, power-ups, pausa/reinício, combos com fila de entrada, testes de estresse e orçamento de desempenho de 60FPS.

### Padrões de código

- **Nomes de arquivo / função**: `lower_snake_case` · **Nomes de classe**: `PascalCase` · **Indentação**: 4 espaços · **Largura de linha**: máx. 120 caracteres
- **Commits Git**: `<type>(<scope>): <subject>` com `feat / fix / docs / style / refactor / test / chore`

---

## 📜 Licença

[MIT License](LICENSE) © 2026 MagicSquarekey

## 🤝 Contribuindo

Issues e Pull Requests são bem-vindos!

## 📞 Contato

Dúvidas? Via [GitHub Issues](https://github.com/MagicSquarekey/2048/issues).
