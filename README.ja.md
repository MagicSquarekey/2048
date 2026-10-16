# 2048 カジュアルゲーム

> 「ディープスペース・ネオン」ダークテーマを採用した 2048 数字合成ゲーム。Python + Pygame 製、Windows デスクトップ向け。

**現在のバージョン: [v0.0.1](https://github.com/MagicSquarekey/2048/releases/tag/v0.0.1)** · [简体中文](README.md) · [English](README.en.md)

---

## 📖 言語 / Languages

| 言語 (Language) | ドキュメント (Document) |
|---|---|
| 简体中文 | [README.md](README.md) |
| English | [README.en.md](README.en.md) |
| 日本語 (現在) | [README.ja.md](README.ja.md) |

---

## ✨ 特徴

- 🎨 **ディープスペース・ネオンテーマ**：インディゴ系グラデーション背景 + ゆっくり漂う光斑 + グラスモーフィズムカード。タイルはグラデーション・リムライト・ネオン輝光付き
- ⚡ **なめらかな操作**：入力キュー + 長押し連続スライド（毎秒約 7 手）+ フレームレート非依存アニメーション。連続入力でも取りこぼしなし
- 💥 **モーション & エフェクト**：合体時のパーティクル噴射、大きなタイル合体時の画面振動、勝利時の紙吹雪、終了トランジション演出、ページフェード
- 🌍 **二言語 UI**：ゲーム内で中文 / English をワンタップ切替

## 🎮 ゲームモード

| モード | 説明 |
|------|------|
| **クラシック** | 時間無制限、ハイスコアを目指す |
| **タイムアタック** | 60 秒以内に目標スコアを達成 |
| **チャレンジ** | 50 手以内に 128 タイルを合成 |

**操作方法**：方向キー / WASD / マウススワイプ · `ESC` で一時停止

## 🧰 アイテム

- **アンドゥ**：直前の手を戻す（1 ゲーム 3 回）
- **クリア**：最小のタイルを 1 つ消す（1 ゲーム 1 回）
- **復活**：ゲームオーバー後、最小タイルを 2 つ消して続行

## 🏆 その他の機能

- 実績システム（解除可能 6 件）
- ハイスコア / 総ゲーム数の記録
- リザルト画面の新記録バッジ + スコアロールアップアニメーション
- 効果音・BGM の ON / OFF

---

## 🖥️ 動作環境

- Windows 10 / 11
- Python 3.10+
- Pygame 2.6.1

## 🚀 クイックスタート

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. ゲームを実行

```bash
python src/main.py
```

### 3. EXE にパッケージ化

```bash
# ワンクリックビルド（推奨）
python scripts/build_auto.py

# 対話式ビルド
python scripts/build.py
```

ビルド完了後、実行ファイルは `dist/2048/2048.exe` に出力されます。Python や依存関係のインストール不要でダブルクリック即プレイできます。詳細は [scripts/README.md](scripts/README.md) を参照してください。

---

## 📁 プロジェクト構成

```
2048/
├── src/                    # ソースコード
│   ├── main.py             # エントリポイント
│   ├── config.py           # グローバル設定（テーマ / アニメーション / 入力）
│   ├── i18n.py             # 多言語対応（中文・English）
│   ├── utils.py            # 描画ヘルパー、キャッシュ、アニメーション曲線
│   ├── models/             # データモデル（盤面 / 状態 / セーブ / 実績）
│   └── views/              # ビュー層
│       ├── ui_components.py  # UI コンポーネント（ボタン / スコアカード / スイッチ / ダイアログ）
│       ├── board_view.py     # 盤面レンダリング & アニメーション
│       ├── effects.py        # パーティクルシステム & 画面振動
│       ├── sound_manager.py  # サウンド管理
│       └── pages/            # 各ページ（メニュー / ゲーム / リザルト / 設定 / 実績 / 一時停止 / ログイン）
├── tests/                  # テスト（359 件の単体テスト + E2E ユーザーシミュレーション）
├── scripts/                # ビルド & パッケージングスクリプト
├── docs/                   # ドキュメント
├── private/                # プライベートファイル
├── dist/                   # ビルド出力（.gitignore）
├── build/                  # ビルド一時ファイル（.gitignore）
└── requirements.txt        # 依存関係リスト
```

## 🔧 開発ガイド

### テストの実行

```bash
# 全単体テスト
python -m pytest tests/

# E2E ユーザーシミュレーション
python tests/e2e_user_simulation.py

# UI スクリーンショットの撮影
python tests/capture_ui_review.py
```

カバレッジ：盤面アルゴリズム、ゲーム状態、3 モードの全ライフサイクル、アイテム、一時停止 / リスタート、入力キューの連続操作、ストレステスト、60FPS 性能予算。

### コーディング規約

- **ファイル / 関数名**：`lower_snake_case` · **クラス名**：`PascalCase` · **インデント**：スペース 4 · **行幅**：最大 120 文字
- **Git コミット**：`<type>(<scope>): <subject>`（type は `feat / fix / docs / style / refactor / test / chore`）

---

## 📜 ライセンス

[MIT License](LICENSE) © 2026 MagicSquarekey

## 🤝 コントリビューション

Issue や Pull Request は大歓迎です！

## 📞 お問い合わせ

ご質問は [GitHub Issues](https://github.com/MagicSquarekey/2048/issues) までお願いします。
