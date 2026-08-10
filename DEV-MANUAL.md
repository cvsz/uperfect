# U.Perfect Developer Manual / คู่มือนักพัฒนา

**Repository workspace:** `/mnt/uperfect`
**Runtime:** Python 3.11+ compatible FastAPI service, SQLite local store, vanilla JS PWA
**Local bind:** `192.168.74.130:18765`
**AI boundary:** Ollama at `192.168.74.130:11434`, model `zCoder:latest`

## ภาษาไทย

### 1. โครงสร้างโค้ด

```text
app/
  main.py                         FastAPI app factory and static mounts
  api.py                          JSON routes and request models
  config.py                       environment-only runtime settings
  database.py                     SQLite schema/transaction boundary
  repositories.py                 persistence, idempotency, audit, outbox
  schemas.py                      domain types and stable errors
  seed.py                         merchant catalog and workspace defaults
  services/catalog.py             product memory lookup
  services/conversations.py       intent, context, safe closing, takeover
  services/sales_assets.py        validated bilingual response/media pack
  services/orders.py              pricing, inventory, payment state machine
  services/integrations.py        provider status and normalized webhook gate
  services/notifications.py       retryable LINE outbox
  services/settings.py            safe workspace preferences
web/
  index.html                      PWA shell and navigation
  app.js                          API-driven render and TH/EN i18n
  styles.css                      responsive operational UI
  service-worker.js               static shell cache; never caches API mutations
assets/chatbot/
  sales_response_assets.json      TH/EN intents, objection replies, CTAs
  asset-manifest.json             local media policy and paths
docs/integrations/                provider onboarding guides
tests/                            unit, API, integration, PWA, and asset tests
```

### 2. ติดตั้งและรัน

```bash
cd /mnt/uperfect
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
cp .env.example .env.local  # เก็บนอก Git และไม่ใส่ secret ลงไฟล์ที่แชร์
.venv/bin/uvicorn app.main:app --host 192.168.74.130 --port 18765
```

เปิด `http://192.168.74.130:18765/` หรือใช้ PWA จากอุปกรณ์ใน LAN เดียวกัน

### 3. Environment contract

ค่าที่ runtime อ่านจาก `.env.example` แบ่งเป็น:

- local: `UPERFECT_DATABASE_PATH`, `UPERFECT_LOCAL_ONLY`,
  `UPERFECT_LOCAL_AI_BASE_URL`, `UPERFECT_LOCAL_AI_MODEL`
- Facebook: `FACEBOOK_PAGE_ACCESS_TOKEN`, `FACEBOOK_VERIFY_TOKEN`
- TikTok: `TIKTOK_APP_KEY`, `TIKTOK_APP_SECRET`, `TIKTOK_REFRESH_TOKEN`
- Shopee: `SHOPEE_PARTNER_ID`, `SHOPEE_PARTNER_KEY`, `SHOPEE_SHOP_ID`
- LINE outbox: `LINE_CHANNEL_ACCESS_TOKEN`, `LINE_ADMIN_DESTINATION`
- gated automation/model: `N8N_WEBHOOK_URL`, `GEMINI_API_KEY`

`app.config.Settings` ให้ค่า secret เป็น `repr` ที่ปกปิด และ API ไม่ส่ง secret
กลับไป browser หากต้องเพิ่มค่าใหม่ ให้เพิ่ม test ที่พิสูจน์ว่าไม่รั่วด้วย

### 4. API routes

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/api/health` | brand and process health |
| GET | `/api/dashboard` | summary counts and integration state |
| GET/POST | `/api/products` | list/search and save catalog facts |
| GET | `/api/conversations` | inbox with message history |
| POST | `/api/messages` | normalized local conversation input |
| POST | `/api/conversations/{id}/takeover` | enable/disable human takeover |
| GET/POST | `/api/orders` | list/create priced draft orders |
| POST | `/api/orders/{id}/payment-evidence` | submit evidence to review |
| POST | `/api/orders/{id}/transition` | guarded order status transition |
| GET | `/api/integrations` | secret-free provider truth |
| GET | `/api/integration-guides` | bilingual provider guide links |
| GET | `/api/sales-assets` | validated, secret-free asset pack |
| GET/PATCH | `/api/settings` | safe workspace preferences |
| GET | `/api/notifications` | pending/failed LINE outbox events |
| POST | `/api/webhooks/{provider}` | normalized local webhook test gate |

The local webhook route requires `X-UPerfect-Webhook-Verified: true`, a supported
provider, `event_id`, `customer_id`, and message text. It is not a raw provider
adapter. A production adapter must validate provider signatures before calling
the normalized service.

### 5. Add or edit a response asset

Edit `assets/chatbot/sales_response_assets.json` and keep these invariants:

- both `th` and `en` exist for every intent, objection, selling point, and CTA
- no response promises an unverified price, stock, shipping, medical outcome, or payment approval
- product `close_mode` says `catalog_review` or `admin_review`
- every `asset_id` exists in `asset-manifest.json`
- every manifest path is local, relative, inside project root, and not an HTTP URL
- unpriced products keep `price_verified: false` and cannot create orders

The loader validates the pack on process load. Add or update tests in
`tests/test_sales_assets.py` and `tests/test_conversations.py` for new intent
paths.

### 6. Add a dashboard translation

1. Add the key to both language objects in `web/app.js`.
2. Use `t("key")` for shared labels or `tx(th, en)` for local view copy.
3. Do not add one-language visible text in `web/index.html` unless it is a stable
   brand/product name.
4. Render API content through `localized(item, ...)` when the API returns TH/EN.
5. Test both `document.documentElement.lang` and visible text with a browser check.
6. Bump the PWA cache query/version when shell assets change.

### 7. Test and verify

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m compileall -q app scripts
node --check web/app.js
```

For route smoke tests:

```bash
curl http://192.168.74.130:18765/api/health
curl http://192.168.74.130:18765/api/sales-assets
curl http://192.168.74.130:18765/api/integration-guides
```

For a normalized webhook test, use a non-secret test header only in a trusted
local request and verify the same event twice to prove idempotency.

### 8. Provider adapters

Provider code must be server-side and follow this pipeline:

```text
provider raw event
  -> signature/state/nonce validation
  -> provider-specific permission and timestamp checks
  -> normalized WebhookEvent
  -> idempotent repository claim
  -> ConversationService
  -> provider-specific outbound adapter
```

Do not shortcut raw provider payloads into `/api/webhooks/{provider}`. Keep
provider credentials out of `schemas.py`, the PWA, asset files, SQL seed, tests,
and generated release files.

### 9. Deployment and release

- systemd unit: `deploy/systemd/uperfect.service`
- database: `/mnt/uperfect/uperfect.db` in local mode
- bind: `192.168.74.130:18765`
- static assets: `/assets` and `/guides`
- no ZIP is generated or published in this release

Before a release, run tests, inspect `git diff --check`, inspect files for
credential patterns, and record local/public health evidence separately from
provider verification.

For signed commits, use the configured GPG agent and signing key. Search for a
PIN only for presence; never print, copy, persist, or ask for the PIN. If the
agent is locked, stop the signing attempt and report the condition rather than
placing a passphrase in a command or file.

## English

### 1. Source layout

The `app/` package contains the FastAPI transport, domain schemas, persistence,
services, asset validation, orders, integration truth, notifications, and safe
workspace settings. `web/` is a vanilla JS PWA. `assets/chatbot/` contains the
validated bilingual sales pack and local media manifest. `docs/integrations/`
contains provider onboarding. `tests/` covers the domain and API contracts.

### 2. Install and run

```bash
cd /mnt/uperfect
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
cp .env.example .env.local  # keep it outside Git; do not add shared secrets
.venv/bin/uvicorn app.main:app --host 192.168.74.130 --port 18765
```

Open `http://192.168.74.130:18765/` from a device on the same LAN.

### 3. Environment contract

Local runtime values are `UPERFECT_DATABASE_PATH`, `UPERFECT_LOCAL_ONLY`,
`UPERFECT_LOCAL_AI_BASE_URL`, and `UPERFECT_LOCAL_AI_MODEL`. Provider values
cover Facebook, TikTok Shop, Shopee, LINE outbox, n8n, and gated Gemini as
listed in `.env.example`.

`app.config.Settings` masks secret values in representation and API responses
never expose them. Add a non-disclosure test when introducing a new setting.

### 4. API routes

The Dashboard uses `/api/health`, `/api/dashboard`, `/api/products`,
`/api/conversations`, `/api/messages`, takeover, orders, payment evidence,
guarded transitions, `/api/integrations`, `/api/integration-guides`,
`/api/sales-assets`, `/api/settings`, `/api/notifications`, and the normalized
webhook test route.

The normalized webhook route requires the trusted local test header and event
fields. It is not a raw provider adapter. Production adapters must validate
provider signatures before normalization.

### 5. Response assets

Keep both languages for all intents, objections, selling points, and CTAs. Keep
all prices and promotions tied to catalog facts. Unpriced products must remain
`admin_review` and cannot create orders. Local media must be validated by the
loader and the manifest.

### 6. Dashboard i18n

Add every new visible key to both dictionaries in `web/app.js`, use `t()` or
`tx()`, localize API records, test TH and EN in a browser, and bump the PWA shell
version when static files change.

### 7. Verification commands

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m compileall -q app scripts
node --check web/app.js
git diff --check
```

Run health, sales-assets, integration-guides, and trusted normalized webhook
smoke tests from a controlled local environment. Verify duplicate events are
processed once.

### 8. Provider adapter boundary

Use the sequence `raw event -> provider signature/state validation -> provider
checks -> normalized WebhookEvent -> idempotent claim -> ConversationService ->
provider outbound adapter`. Never bypass the boundary, and never put provider
credentials in frontend code, catalog data, SQL seeds, tests, or release files.

### 9. Deployment and signing

The systemd unit binds to `192.168.74.130:18765`; local assets and guides are
mounted at `/assets` and `/guides`. ZIP export is canceled for this release.

Before release, run the test suite, `git diff --check`, secret-pattern review,
and separate local/public health evidence from provider verification. Use the
configured GPG agent for signed commits. Presence checks must never print or
persist a GPG PIN or passphrase.
