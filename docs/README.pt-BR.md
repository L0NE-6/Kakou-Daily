<div align="center">

<sub><strong>L0NE-6 · DAILY SIGNAL</strong></sub>

# 🎯 Kakou Daily

**Check-in diário do Kakou AI · múltiplas contas · leitura do saldo no servidor · JSONL**

[简体中文](../README.md) · [English](README.en.md) · [繁體中文](README.zh-Hant.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · **Português (BR)**
> Versão: **v1.0.0** (2026-11-24)

</div>

## O que faz

Executa o check-in diário do Kakou AI com um JWT de login web. O perfil da conta é lido antes e depois da solicitação, e `CLAIMED` só é informado quando o saldo no servidor aumenta.

## Configuração

Use `KAKOU_TOKENS` (várias contas, uma por linha no formato `rótulo|JWT`) ou `KAKOU_TOKEN` (uma conta). Também estão disponíveis `KAKOU_ACCOUNT_FILE`, `KAKOU_API_BASE`, `KAKOU_PROXY` e `KAKOU_WAIT_SECONDS`.

## Protocolo

```http
GET  /api/v1/user/profile
POST /api/v1/client/checkin
GET  /api/v1/user/profile
Authorization: Bearer <JWT>
```

`claimed_success` sozinho não é sucesso: o saldo relido precisa aumentar. Códigos de já recebido são tratados como `ALREADY`; limite, autenticação inválida, resposta malformada ou saldo sem mudança não são sucesso.

## Execução

```bash
python -m pip install -r requirements.txt
export KAKOU_TOKEN='eyJ...'
python kakou_daily.py
python kakou_daily.py --query
python kakou_daily.py --only 1,3-4
```

## Privacidade

Não faça commit de JWT, arquivos de conta, relatórios, logs ou capturas com credenciais. O script oculta telefone, Token e segredos de notificação.
