<div align="center">

<sub><strong>L0NE-6 · DAILY SIGNAL</strong></sub>

# 🎯 Kakou Daily

**Kakou AI 일일 체크인 · 다중 계정 · 서버 잔액 재조회 · JSONL**

[简体中文](../README.md) · [English](README.en.md) · [繁體中文](README.zh-Hant.md) · [日本語](README.ja.md) · **한국어** · [Português (BR)](README.pt-BR.md)
> 버전: **v1.0.0** (2026-11-24)

</div>

## 기능

웹 로그인 JWT로 Kakou AI 일일 체크인을 실행합니다. 체크인 전후에 계정 정보를 읽고, 서버 잔액이 증가한 경우에만 `CLAIMED`로 보고합니다.

## 설정

`KAKOU_TOKENS`(다중 계정, 각 줄 `라벨|JWT`) 또는 `KAKOU_TOKEN`(단일 계정)을 설정합니다. `KAKOU_ACCOUNT_FILE`, `KAKOU_API_BASE`, `KAKOU_PROXY`, `KAKOU_WAIT_SECONDS`도 지원합니다.

## 프로토콜

```http
GET  /api/v1/user/profile
POST /api/v1/client/checkin
GET  /api/v1/user/profile
Authorization: Bearer <JWT>
```

`claimed_success`만으로는 성공이 아닙니다. 다시 읽은 잔액이 증가해야 합니다. 이미 받은 코드는 `ALREADY`, 제한·인증 실패·잔액 미변경은 성공으로 처리하지 않습니다.

## 실행

```bash
python -m pip install -r requirements.txt
export KAKOU_TOKEN='eyJ...'
python kakou_daily.py
python kakou_daily.py --query
python kakou_daily.py --only 1,3-4
```

## 개인정보

JWT, 계정 파일, 보고서, 로그, 자격 증명이 포함된 스크린샷을 커밋하지 마세요. 출력에서는 전화번호, Token, 알림 비밀값을 가립니다.
