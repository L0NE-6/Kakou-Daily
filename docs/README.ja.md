<div align="center">

<sub><strong>L0NE-6 · DAILY SIGNAL</strong></sub>

# 🎯 Kakou Daily

**Kakou AI 毎日チェックイン · 複数アカウント · サーバー残高の再読取 · JSONL**

[简体中文](../README.md) · [English](README.en.md) · [繁體中文](README.zh-Hant.md) · **日本語** · [한국어](README.ko.md) · [Português (BR)](README.pt-BR.md)
> バージョン：**v1.0.0**（2026-11-24）

</div>

## 機能

Web ログイン JWT を使って Kakou AI の毎日チェックインを実行します。チェックイン前後でアカウント情報を読み取り、残高が増えた場合だけ `CLAIMED` と報告します。

## 設定

`KAKOU_TOKENS`（複数アカウント、`ラベル|JWT`）または `KAKOU_TOKEN`（単一アカウント）を設定します。`KAKOU_ACCOUNT_FILE`、`KAKOU_API_BASE`、`KAKOU_PROXY`、`KAKOU_WAIT_SECONDS` も利用できます。

## プロトコル

```http
GET  /api/v1/user/profile
POST /api/v1/client/checkin
GET  /api/v1/user/profile
Authorization: Bearer <JWT>
```

`claimed_success` だけでは成功ではありません。再読取した残高が増えている必要があります。既に受取済みのコードは `ALREADY`、制限・認証失敗・残高未変化は成功扱いしません。

## 実行

```bash
python -m pip install -r requirements.txt
export KAKOU_TOKEN='eyJ...'
python kakou_daily.py
python kakou_daily.py --query
python kakou_daily.py --only 1,3-4
```

## プライバシー

JWT、アカウントファイル、レポート、ログ、認証情報を含む画像をコミットしないでください。出力では電話番号、Token、通知用の秘密情報を伏せます。
