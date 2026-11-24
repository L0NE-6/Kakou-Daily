<div align="center">

<sub><strong>L0NE-6 · DAILY SIGNAL</strong></sub>

# 🎯 Kakou Daily
[简体中文](../README.md) · **English** · [繁體中文](README.zh-Hant.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Português (BR)](README.pt-BR.md)
> Version: **v1.0.0** (2026-11-24)

**Kakou AI daily check-in · multi-account · server-side balance readback · JSONL**


</div>

## What it does

This repository runs the Kakou AI daily check-in with a web-login JWT. It reads
the account profile before and after the claim, and only reports `CLAIMED`
when the server-side balance increases.

## Configuration

| Variable | Required | Description |
| :--- | :---: | :--- |
| `KAKOU_TOKENS` | one of two | Multi-account lines in `label\|JWT` form |
| `KAKOU_TOKEN` | one of two | Single-account JWT |
| `KAKOU_ACCOUNT_FILE` | optional | Local account file |
| `KAKOU_API_BASE` | optional | API base override |
| `KAKOU_PROXY` | optional | HTTP(S) proxy |
| `KAKOU_WAIT_SECONDS` | optional | Wait before balance readback |
| `PUSHPLUS_TOKEN` | optional | PushPlus |
| `BARK_URL` | optional | Bark |
| `WECOM_WEBHOOK` | optional | WeCom bot |
| `DINGTALK_WEBHOOK` | optional | DingTalk bot |
| `GENERIC_WEBHOOK_URL` | optional | Generic JSON webhook |

## Protocol and success

```http
GET  /api/v1/user/profile
POST /api/v1/client/checkin
GET  /api/v1/user/profile
Authorization: Bearer <KAKOU_WEB_JWT>
```

`claimed_success` is not enough by itself. The after-claim profile must show a
positive balance delta. Already-claimed codes are reported as neutral `ALREADY`.
Rate limiting, authentication failures, malformed responses, and an unchanged
balance are not reported as success.

## Run locally

```bash
python -m pip install -r requirements.txt
export KAKOU_TOKEN='eyJ...'
python kakou_daily.py
python kakou_daily.py --query
python kakou_daily.py --only 1,3-4
```

## Deploy

For Qinglong, upload `kakou_daily.py`, set `KAKOU_TOKENS` or `KAKOU_TOKEN`, and
run `task kakou_daily.py`. For GitHub Actions, add the same value as a
repository Secret and run the included workflow.

## Privacy

Do not commit JWTs, account files, reports, logs, or screenshots containing
credentials. The script redacts phone numbers, tokens, and notification
secrets from errors and output.

## Test

```bash
python -m unittest discover -s tests -v
python -m compileall -q .
python -m ruff check .
```

All tests use fake HTTP sessions and do not call the live service.

## License and support

MIT. See `LICENSE`, `NOTICE.md`, and `THIRD_PARTY_NOTICES.md`. Donation QR codes
are only for voluntary support of the author.
