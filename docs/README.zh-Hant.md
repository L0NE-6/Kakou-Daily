<div align="center">

<sub><strong>L0NE-6 · DAILY SIGNAL</strong></sub>

# 🎯 Kakou Daily

**卡扣 AI 每日簽到 · 多帳號 · 服務端餘額回讀 · JSONL**

[简体中文](../README.md) · [English](README.en.md) · **繁體中文** · [日本語](README.ja.md) · [한국어](README.ko.md) · [Português (BR)](README.pt-BR.md)
> 版本：**v1.0.0**（2026-11-24）

</div>

## 功能

使用卡扣 AI 網頁登入 JWT 執行每日簽到，並在領取前後讀取帳戶資料。只有在服務端餘額正增長時才回報 `CLAIMED`。

## 設定

使用 `KAKOU_TOKENS`（多帳號，每行 `備註|JWT`）或 `KAKOU_TOKEN`（單帳號）。也可使用 `KAKOU_ACCOUNT_FILE`。支援 `KAKOU_PROXY`、`KAKOU_API_BASE`、`KAKOU_WAIT_SECONDS` 及可選推送變數。

## 協議與成功判定

```http
GET  /api/v1/user/profile
POST /api/v1/client/checkin
GET  /api/v1/user/profile
Authorization: Bearer <JWT>
```

`claimed_success` 不能單獨當作成功；領取後必須讀到餘額增加。已領取代碼為中性 `ALREADY`；限流、登入失效、格式異常或餘額未變都不算成功。

## 執行

```bash
python -m pip install -r requirements.txt
export KAKOU_TOKEN='eyJ...'
python kakou_daily.py
python kakou_daily.py --query
python kakou_daily.py --only 1,3-4
```

## 隱私

不要提交 JWT、帳號檔案、報告、日誌或含憑證的截圖。腳本會遮蔽手機號、Token 與推送憑證。

## 測試

```bash
python -m unittest discover -s tests -v
python -m compileall -q .
python -m ruff check .
```

測試使用假 HTTP session，不訪問真實服務。
