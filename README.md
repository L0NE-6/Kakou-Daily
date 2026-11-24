<div align="center">

<sub><strong>L0NE-6 · KAKOU SIGNAL</strong></sub>

# Kakou Daily

**卡扣 AI 每日签到 · 多账号 · 服务端余额回读 · JSONL 结果**

> 当前版本：**v1.0.0**（2026-11-24） · 签到成功必须由领取后余额正增长确认

[简体中文](README.md) · [English](docs/README.en.md) · [繁體中文](docs/README.zh-Hant.md) · [日本語](docs/README.ja.md) · [한국어](docs/README.ko.md) · [Português (BR)](docs/README.pt-BR.md)

<img src="https://img.shields.io/badge/Features-Balance%20Readback-6F42C1?style=for-the-badge" alt="Features" />
<a href="https://github.com/L0NE-6/Kakou-Daily/releases"><img src="https://img.shields.io/github/v/release/L0NE-6/Kakou-Daily?style=for-the-badge&label=Release&color=2ea44f&logo=github" alt="Release" /></a>
<a href="https://github.com/L0NE-6/Kakou-Daily/stargazers"><img src="https://img.shields.io/github/stars/L0NE-6/Kakou-Daily?style=for-the-badge&label=Stars&color=FFC75F&logo=github" alt="Stars" /></a>
<img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Qinglong-4EAA25?style=for-the-badge&logo=linux&logoColor=white" alt="Platform" />
<img src="https://img.shields.io/badge/License-MIT-F472B6?style=for-the-badge" alt="License" />

🔐 Bearer JWT · 🎁 每日签到 · 👥 多账号隔离 · 🧾 JSONL · 📢 可选推送 · 🐧 青龙 · ☁️ Actions

[⚡ 30 秒速览](#quick-look) · [🔁 协议与回读](#protocol) · [🔐 凭据](#credentials) · [🐧 青龙](#qinglong) · [☁️ Actions](#actions) · [⌨️ CLI](#cli-json) · [✅ 成功判据](#success) · [✦ 星轨](#star-trail)

</div>

---

<a id="usage-policy"></a>
## 🚫 使用边界与禁止倒卖

> [!IMPORTANT]
> **官方版本永久免费。** 未经作者书面许可，禁止倒卖、付费包装、搬运引流、冒充作者，或使用作者身份与二维码制造官方授权假象。

本仓库、脚本、部署说明和 Release 下载保持免费公开。禁止将本项目或其轻度改名版本包装为付费资源、内部版、独家版、会员权益、收费课程、代部署服务或包更新服务；禁止搬运到其他账号、群组、频道、网盘、电商平台或付费社群进行涨粉、截流、倒卖和引流；禁止删除作者与版权信息后冒充原创。

完整规则见 [NOTICE.md](NOTICE.md)。第三方以“下载费 / 激活费 / 内部版 / 代部署 / 会员门槛”等名义收费，均与作者无关，请停止付款并保留证据。

---

<a id="quick-look"></a>
## ⚡ 30 秒速览

| 维度 | 说明 |
| :--- | :--- |
| **做什么** | 使用卡扣 AI 网页登录 JWT 领取每日签到奖励。 |
| **输入** | `KAKOU_TOKENS` 多账号，或 `KAKOU_TOKEN` 单账号；也支持账号文件。 |
| **协议** | `GET /api/v1/user/profile` → `POST /api/v1/client/checkin` → `GET /api/v1/user/profile`。 |
| **回读** | 领取前后读取账户资料，要求余额正增长。 |
| **输出** | 每账号一条 JSON，最后一行 `SUMMARY` JSON。 |
| **成功判据** | `claimed_success` 且领取后余额增长；HTTP 200 不算成功。 |

---

## 🧭 这是什么 / 覆盖范围

Kakou 脚本使用网页登录 JWT 访问 `api.kakouai.com/api/v1`，先读取 `/user/profile`，再提交 `/client/checkin`，最后重新读取资料确认余额。

### 覆盖范围

- `KAKOU_TOKENS`、`KAKOU_TOKEN`、JSON 账号和账号文件。
- `--query` 只读资料，不发送签到请求。
- `CHECKIN_USER_ALREADY_CLAIMED` / `CHECKIN_CLIENT_ALREADY_CLAIMED` 中性处理。
- `CHECKIN_RATE_LIMITED`、鉴权失效、结构异常和未确认余额明确分类。
- JSONL、汇总 JSON、可选 PushPlus / Bark / 企业微信 / 钉钉 / 通用 webhook。

---

<a id="protocol"></a>
## 🔁 协议与回读流程

### 请求链

```http
GET  /api/v1/user/profile
POST /api/v1/client/checkin
GET  /api/v1/user/profile
Authorization: Bearer <KAKOU_WEB_JWT>
```

### 关键判定

| 字段 / 代码 | 说明 |
| :--- | :--- |
| `claimed_success` | 签到请求被接受，但还需余额回读。 |
| `CHECKIN_USER_ALREADY_CLAIMED` | 用户级已领取，结果 `ALREADY`。 |
| `CHECKIN_CLIENT_ALREADY_CLAIMED` | 客户端级已领取，结果 `ALREADY`。 |
| `CHECKIN_RATE_LIMITED` | 服务端限流，结果失败并保留建议重试时间。 |
| `balance` | 领取前后账户余额。 |
| `balance_delta` | 领取后余额减领取前余额。 |

资料读取失败、余额未增长或响应结构异常时返回 `UNCONFIRMED`，不会把签到请求本身写成成功。

---

<a id="credentials"></a>
## 🔐 凭据与环境变量

### 账号格式

```text
主号|eyJ...
小号|eyJ...
```

也支持 JSON：

```json
[{"name":"主号","token":"eyJ..."},{"name":"小号","token":"eyJ..."}]
```

| 变量 | 必填 | 说明 |
| :--- | :---: | :--- |
| `KAKOU_TOKENS` | 二选一 | 多账号，每行 `备注\|JWT`。 |
| `KAKOU_TOKEN` | 二选一 | 单账号 JWT。 |
| `KAKOU_ACCOUNT_FILE` | 否 | 账号文件路径。 |
| `KAKOU_API_BASE` | 否 | API 根地址覆盖。 |
| `KAKOU_PROXY` | 否 | HTTP(S) 代理。 |
| `KAKOU_WAIT_SECONDS` | 否 | 余额回读等待秒数，默认 `1.5`。 |
| `PUSHPLUS_TOKEN` | 否 | PushPlus。 |
| `BARK_URL` | 否 | Bark。 |
| `WECOM_WEBHOOK` | 否 | 企业微信机器人。 |
| `DINGTALK_WEBHOOK` | 否 | 钉钉机器人。 |
| `GENERIC_WEBHOOK_URL` | 否 | 通用 JSON webhook。 |

---

## 💻 本地快速开始

### PowerShell

```powershell
python -m pip install -r requirements.txt
$env:KAKOU_TOKEN = "eyJ..."
python .\kakou_daily.py
```

### Bash

```bash
python -m pip install -r requirements.txt
export KAKOU_TOKEN='eyJ...'
python kakou_daily.py
```

常用参数：`--query`、`--only 1,3-4`、`--accounts-file kakou_accounts.txt`、`--wait-seconds 1.5`、`--no-notify`。

---

<a id="qinglong"></a>
## 🐧 青龙

1. 在青龙依赖管理中安装 `requests`，或执行 `pip3 install -r requirements.txt`。
2. 上传 `kakou_daily.py` 到脚本目录。
3. 在环境变量中配置 `KAKOU_TOKENS` 或 `KAKOU_TOKEN`。
4. 新建定时任务，命令使用 `task kakou_daily.py`，不要直接写裸 `python`。
5. 建议北京时间：`17 7 * * *`。青龙按面板本地时间执行。

```bash
pip3 install -r requirements.txt
task kakou_daily.py
```

---

<a id="actions"></a>
## ☁️ GitHub Actions、Secrets 与定时

工作流：`.github/workflows/kakou.yml`。

| 事件 | 行为 |
| :--- | :--- |
| `push` 到 `main` | 离线测试、编译检查、Ruff。 |
| `schedule` | 先测试，再执行签到并上传 JSONL artifact。 |
| `workflow_dispatch` | 手动执行。 |
| 未配置 Secret | 输出 notice 并跳过在线执行。 |

### Secrets

| Secret | 说明 |
| :--- | :--- |
| `KAKOU_TOKENS` | 多账号 JWT。 |
| `KAKOU_TOKEN` | 单账号 JWT。 |
| `PUSHPLUS_TOKEN` / `BARK_URL` | 推送凭据。 |
| `WECOM_WEBHOOK` | 企业微信群机器人。 |
| `DINGTALK_WEBHOOK` | 钉钉机器人。 |
| `GENERIC_WEBHOOK_URL` | 通用 JSON webhook。 |

内置定时为 UTC `17 23 * * *`，对应北京时间约 07:17。原始 JSONL 作为 `kakou-report` artifact 保留。

---

<a id="cli-json"></a>
## ⌨️ CLI 与 JSON 输出

```powershell
python .\kakou_daily.py
python .\kakou_daily.py --query
python .\kakou_daily.py --only 1,3-4
python .\kakou_daily.py --no-notify
```

账号 JSON 示例：

```json
{"type":"account","provider":"kakou","index":1,"label":"主号","status":"CLAIMED","ok":true,"message":"服务端确认签到","http_status":200,"balance_before":"10","balance_after":"15","balance_delta":"5","amount":"5","next_checkin_at":"2026-11-25T00:00:00+08:00","username":"masked","details":[]}
```

| 字段 | 说明 |
| :--- | :--- |
| `status` / `ok` | 结果状态与是否成功。 |
| `balance_before` / `balance_after` / `balance_delta` | 余额回读。 |
| `amount` / `next_checkin_at` | 奖励与下次可签时间。 |
| `username` | 脱敏后的用户标识。 |
| `details` | 非敏感补充信息。 |

---

<a id="result-codes"></a>
## 🧾 结果码

| 结果码 | 成功 | 含义 |
| :--- | :---: | :--- |
| `CLAIMED` | 是 | 领取回执成功且余额正增长。 |
| `ALREADY` | 是 | 服务端确认今天已经领取。 |
| `QUERY` | 是 | 查询模式，未发送签到请求。 |
| `INACTIVE` | 是 | 服务端明确表示活动未启用。 |
| `AUTH_EXPIRED` | 否 | JWT 失效或需要重新登录。 |
| `RATE_LIMITED` | 否 | 服务端限流。 |
| `UNCONFIRMED` | 否 | 请求已发，但余额或状态无法确认。 |
| `API_ERROR` | 否 | HTTP、JSON 或业务错误。 |
| `CONFIG_ERROR` | 否 | 账号、文件或参数配置错误。 |

`SUMMARY.ok=true` 要求至少一个账号且所有结果均为成功或中性状态。

---

<a id="success"></a>
## ✅ 成功判据

| 场景 | 必须满足 |
| :--- | :--- |
| 本次签到 | `claimed_success` 且领取后余额相对领取前为正增长。 |
| 今日已签到 | 服务端明确返回已领取代码，或资料已体现今日已签。 |
| 查询模式 | 只读 `/user/profile`，不得发送 POST。 |
| 未确认 | 余额未变化、资料读取失败或结构异常时返回 `UNCONFIRMED`。 |

---

## 🧪 测试与静态检查

```bash
python -m pytest -q
python -m compileall -q .
python -m ruff check .
```

离线测试覆盖账号解析、JSON 账号、Bearer 前缀、序号范围、查询模式、余额增长、余额未增长、已领取、限流、鉴权和汇总失败。测试使用 fake session，不访问真实接口。

---

## 🧱 设计原则

- **资料前后读**：签到前建立余额基线，签到后复核。
- **余额增长优先**：不只看 `claimed_success`。
- **已领取中性**：重复运行不产生失败噪音。
- **限流可见**：保留服务端建议重试时间。
- **凭据脱敏**：手机号、JWT 和推送凭据不进入输出。

---

## 🔒 隐私

仓库不包含账号、手机号、JWT 或推送凭据。`kakou_accounts.txt`、`kakou-report.json`、`kakou-report.jsonl`、`auth.json`、Cookie、日志和缓存已由 `.gitignore` 排除。

---

## 📁 目录结构

```text
Kakou-Daily/
├── .github/workflows/kakou.yml
├── assets/
│   ├── donate-alipay.jpg
│   └── donate-wechat.png
├── docs/
│   ├── README.en.md
│   ├── README.zh-Hant.md
│   ├── README.ja.md
│   ├── README.ko.md
│   └── README.pt-BR.md
├── tests/test_kakou_daily.py
├── CHANGELOG.md
├── LICENSE
├── NOTICE.md
├── THIRD_PARTY_NOTICES.md
├── kakou_daily.py
├── pyproject.toml
├── README.md
└── requirements.txt
```

---

## 📦 版本与发布

- 当前清单版本：`v1.0.0`，日期 `2026-11-24`。
- 脚本版本与 `kakou_daily.py` 内的 `VERSION` 保持一致。
- 更新记录见 [CHANGELOG.md](CHANGELOG.md)，下载入口见 [Releases](https://github.com/L0NE-6/Kakou-Daily/releases)。
- Release 徽标由 GitHub 实时生成；如果页面尚未创建对应 Release，以 `CHANGELOG.md` 和仓库提交为准。

---

## ⚠️ 免责声明

本项目用于个人学习与个人自动化。卡扣 AI 的活动规则、接口、奖励、风控策略和账号资格由服务方决定。使用前请确认对应服务条款，并自行承担接口变化、账号限制和网络环境带来的风险。

---

## ☕ 支持与投喂

脚本完全免费，赞赏纯自愿，不影响任何功能，也不影响 Issue 响应。

<p align="center">
  <img src="assets/donate-wechat.png" width="260" alt="微信赞赏码" />
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/donate-alipay.jpg" width="260" alt="支付宝收款码" />
</p>
<p align="center"><sub>💚 微信支付（左） &nbsp;|&nbsp; 💙 支付宝（右，支持信用卡 / 花呗）</sub></p>

> 收款码仅用于向作者自愿赞赏。任何第三方以代下载、代部署、内部资源或会员群为由收费，均与作者无关。

---

## 💬 反馈与贡献

- 提交 [Issue](https://github.com/L0NE-6/Kakou-Daily/issues) 时附运行日志、脱敏后的错误字段和复现步骤。
- 发起 [Pull Request](https://github.com/L0NE-6/Kakou-Daily/pulls) 时保持单文件运行、离线测试和凭据脱敏约束。
- 不要在任何 Issue、PR、截图或日志中粘贴真实 Token、Cookie、密码、UID、手机号或邮箱。

---

<a id="star-trail"></a>
## ✦ Star History / 星轨

<a href="https://star-history.com/#L0NE-6/Kakou-Daily&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=L0NE-6/Kakou-Daily&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=L0NE-6/Kakou-Daily&type=Date" />
    <img alt="Kakou-Daily Star History" src="https://api.star-history.com/svg?repos=L0NE-6/Kakou-Daily&type=Date" />
  </picture>
</a>

<div align="center">
  <sub>L0NE-6 · DAILY SIGNAL &nbsp;|&nbsp; 点个 <b>Star</b>，让下一轮自动化有迹可循</sub>
</div>
