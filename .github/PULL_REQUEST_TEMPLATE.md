# U.Perfect Pull Request / คำขอรวมโค้ด

## ภาษาไทย

### สรุปการเปลี่ยนแปลง

<!-- บอกว่าทำอะไรและทำไม -->

### Scope

- [ ] runtime/backend
- [ ] Dashboard/PWA
- [ ] Product Memory/Sales Assets
- [ ] API/provider adapter
- [ ] docs/GitHub template
- [ ] deployment/configuration

### TH/EN i18n

- [ ] ทุก visible label ใหม่มี TH และ EN
- [ ] ตรวจ desktop/mobile แล้ว
- [ ] bump PWA shell version หากแก้ static shell

### Safety and truthfulness

- [ ] ไม่มี token, secret, PIN, passphrase หรือ credential ใน diff/artifact
- [ ] ไม่อ้าง provider live โดยไม่มี verification evidence
- [ ] ราคา/สต็อก/ค่าส่ง/ผลลัพธ์ผูกกับ facts ที่ตรวจสอบได้
- [ ] payment review และ human takeover ยังทำงานตาม gate

### Verification

```text
<!-- ใส่คำสั่งและผลลัพธ์จริง -->
```

### Deployment gates / งานที่ยังไม่พร้อม

<!-- ระบุ account owner, provider approval, migration, env หรือ rollback ที่ยังต้องทำ -->

### Provider approval evidence

- [ ] ถ้าแตะ provider ให้แนบแบบฟอร์ม [TH](../docs/integrations/PROVIDER-APPROVAL-FORM_TH.md) หรือ [EN](../docs/integrations/PROVIDER-APPROVAL-FORM_EN.md) แบบไม่มี secret

## English

### Summary

<!-- What changed and why? -->

### Scope

- [ ] runtime/backend
- [ ] Dashboard/PWA
- [ ] Product Memory/Sales Assets
- [ ] API/provider adapter
- [ ] docs/GitHub template
- [ ] deployment/configuration

### TH/EN i18n

- [ ] Every new visible label has TH and EN.
- [ ] Desktop and mobile were checked.
- [ ] The PWA shell version was bumped when static shell files changed.

### Safety and truthfulness

- [ ] No token, secret, PIN, passphrase, or credential is in the diff/artifacts.
- [ ] No provider is described as live without verification evidence.
- [ ] Price, stock, shipping, and outcomes remain fact-bound.
- [ ] Payment review and human takeover gates remain intact.

### Verification

```text
<!-- Include real commands and results. -->
```

### Deployment gates / remaining work

<!-- Account owner, provider approval, migration, environment, and rollback requirements. -->

### Provider approval evidence

- [ ] If a provider is touched, include the [Thai](../docs/integrations/PROVIDER-APPROVAL-FORM_TH.md) or [English](../docs/integrations/PROVIDER-APPROVAL-FORM_EN.md) workbook with all secrets removed.
