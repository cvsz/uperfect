# GitHub Workflow / แนวทางใช้ GitHub

## ภาษาไทย

ใช้ issue สำหรับงานที่ตรวจสอบย้อนกลับได้ และ PR สำหรับการเปลี่ยนแปลงที่มี scope
ชัดเจน ทุก PR ต้องระบุ test evidence, ผลกระทบ TH/EN, provider/deployment gate
และ secret review

- bug: ใช้ `ISSUE_TEMPLATE/bug_report.md`
- feature: ใช้ `ISSUE_TEMPLATE/feature_request.md`
- provider: ใช้ `ISSUE_TEMPLATE/integration_request.md`
- docs/i18n: ใช้ `ISSUE_TEMPLATE/documentation_request.md`
- PR: ใช้ `PULL_REQUEST_TEMPLATE.md`

คำขอเชื่อมต่อ provider ต้องแนบ [แบบฟอร์มอนุมัติ TH](../docs/integrations/PROVIDER-APPROVAL-FORM_TH.md)
หรือ [EN](../docs/integrations/PROVIDER-APPROVAL-FORM_EN.md) โดยลบ secret ออกทั้งหมด

ห้ามแนบ token, key, PIN, passphrase, `.env` หรือ database ที่มีข้อมูลจริง

## English

Use issues for traceable work and pull requests for scoped changes. Every PR
must include test evidence, TH/EN impact, provider/deployment gates, and a
secret review.

- bugs: `ISSUE_TEMPLATE/bug_report.md`
- features: `ISSUE_TEMPLATE/feature_request.md`
- provider access: `ISSUE_TEMPLATE/integration_request.md`
- docs/i18n: `ISSUE_TEMPLATE/documentation_request.md`
- pull requests: `PULL_REQUEST_TEMPLATE.md`

Provider requests must include the [Thai approval workbook](../docs/integrations/PROVIDER-APPROVAL-FORM_TH.md)
or [English workbook](../docs/integrations/PROVIDER-APPROVAL-FORM_EN.md), with all secrets removed.

Never attach tokens, keys, PINs, passphrases, `.env` files, or real databases.
