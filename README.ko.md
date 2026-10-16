# 2048 캐주얼 게임

> 「딥스페이스 네온」 다크 테마로 제작된 2048 숫자 합성 게임. Python + Pygame 기반, Windows 데스크톱용.

**현재 버전: [v0.0.1](https://github.com/MagicSquarekey/2048/releases/tag/v0.0.1)** · [简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [繁體中文](README.zh-TW.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Italiano](README.it.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Tiếng Việt](README.vi.md) · [ภาษาไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

---

## 📖 언어

| 언어 | 문서 |
|---|---|
| 简体中文 | [README.md](README.md) |
| English | [README.en.md](README.en.md) |
| 日本語 | [README.ja.md](README.ja.md) |
| 繁體中文 | [README.zh-TW.md](README.zh-TW.md) |
| 한국어 (현재) | [README.ko.md](README.ko.md) |
| Français | [README.fr.md](README.fr.md) |
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

## ✨ 주요 특징

- 🎨 **딥스페이스 네온 테마**: 인디고 그라데이션 배경 + 천천히 떠다니는 발광 + 글래스모피즘 카드. 타일은 그라데이션·림 라이트·네온 발광 포함
- ⚡ **부드러운 조작**: 입력 큐 + 길게 눌러 연속 슬라이드(초당 약 7수) + 프레임률 무관 애니메이션. 연속 입력도 누락 없음
- 💥 **모션 & 효과**: 합체 시 파티클 분출, 큰 타일 합체 시 화면 흔들림, 승리 시 색종환, 종료 트랜지션, 페이지 페이드
- 🌍 **이중 언어 UI**: 게임 내에서 중국어 / English 원탭 전환

## 🎮 게임 모드

| 모드 | 설명 |
|------|------|
| **클래식** | 시간 제한 없이 최고 점수 도전 |
| **타임어택** | 60초 안에 목표 점수 달성 |
| **챌린지** | 50수 안에 128 타일 합성 |

**조작 방법**: 방향키 / WASD / 마우스 스와이프 · `ESC` 일시정지

## 🧰 아이템

- **언두**: 직전 수 되돌리기 (게임당 3회)
- **클리어**: 가장 작은 타일 1개 제거 (게임당 1회)
- **부활**: 게임 오버 후 가장 작은 타일 2개를 제거하고 계속

## 🏆 기타 기능

- 업적 시스템 (잠금 해제 가능 6종)
- 최고 점수 / 총 게임 수 기록
- 결과 화면의 신기록 배지 + 점수 롤업 애니메이션
- 효과음·BGM ON / OFF

---

## 🖥️ 실행 환경

- Windows 10 / 11
- Python 3.10+
- Pygame 2.6.1

## 🚀 빠른 시작

### 1. 종속성 설치

```bash
pip install -r requirements.txt
```

### 2. 게임 실행

```bash
python src/main.py
```

### 3. EXE로 패키징

```bash
# 원클릭 빌드 (권장)
python scripts/build_auto.py

# 대화형 빌드
python scripts/build.py
```

빌드 완료 후 실행 파일은 `dist/2048/2048.exe`에 출력됩니다. Python 이나 종속성 설치 없이 더블클릭으로 바로 플레이할 수 있습니다. 자세한 내용은 [scripts/README.md](scripts/README.md)를 참조하세요.

---

## 📁 프로젝트 구조

```
2048/
├── src/                    # 소스 코드
│   ├── main.py             # 진입점
│   ├── config.py           # 전역 설정 (테마 / 애니메이션 / 입력)
│   ├── i18n.py             # 다국어 (중국어·English)
│   ├── utils.py            # 그리기 헬퍼, 캐시, 애니메이션 곡선
│   ├── models/             # 데이터 모델 (보드 / 상태 / 세이브 / 업적)
│   └── views/              # 뷰 계층
│       ├── ui_components.py  # UI 컴포넌트 (버튼 / 점수 카드 / 스위치 / 대화상자)
│       ├── board_view.py     # 보드 렌더링 & 애니메이션
│       ├── effects.py        # 파티클 시스템 & 화면 흔들림
│       ├── sound_manager.py  # 사운드 관리
│       └── pages/            # 각 페이지 (메뉴 / 게임 / 결과 / 설정 / 업적 / 일시정지 / 로그인)
├── tests/                  # 테스트 (359개 단위 테스트 + E2E 사용자 시뮬레이션)
├── scripts/                # 빌드 & 패키징 스크립트
├── docs/                   # 문서
├── private/                # 비공개 파일
├── dist/                   # 빌드 출력 (.gitignore)
├── build/                  # 빌드 임시 파일 (.gitignore)
└── requirements.txt        # 종속성 목록
```

## 🔧 개발 가이드

### 테스트 실행

```bash
# 전체 단위 테스트
python -m pytest tests/

# E2E 사용자 시뮬레이션
python tests/e2e_user_simulation.py

# UI 스크린샷 촬영
python tests/capture_ui_review.py
```

커버리지: 보드 알고리즘, 게임 상태, 3모드 전체 라이프사이클, 아이템, 일시정지 / 재시작, 입력 큐 연속 조작, 스트레스 테스트, 60FPS 성능 예산.

### 코딩 규칙

- **파일 / 함수명**: `lower_snake_case` · **클래스명**: `PascalCase` · **들여쓰기**: 스페이스 4 · **행 너비**: 최대 120자
- **Git 커밋**: `<type>(<scope>): <subject>` (type은 `feat / fix / docs / style / refactor / test / chore`)

---

## 📜 라이선스

[MIT License](LICENSE) © 2026 MagicSquarekey

## 🤝 기여

Issue 나 Pull Request 환영합니다!

## 📞 문의

질문은 [GitHub Issues](https://github.com/MagicSquarekey/2048/issues)로 부탁드립니다.
