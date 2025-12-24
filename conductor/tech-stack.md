# Tech Stack

## プログラミング言語
- Python (Python 3.13以上)

## フレームワーク/ライブラリ
### コア
- `click`: コマンドラインインターフェース構築用
- `opencv-python`: pi0dispがない環境での表示用
- `pi0disp`: Raspberry Pi接続LCDへの表示用 (ローカル依存、ST7789Vドライバを使用)
- `pigpio`: Raspberry Pi GPIO制御用

### 開発
- `mypy`: 静的型チェッカー
- `pytest`: テストフレームワーク
- `ruff`: リンターおよびフォーマッター

## その他
- `uv`: パッケージマネージャーおよびビルドシステム