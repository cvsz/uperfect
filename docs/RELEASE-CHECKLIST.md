# U.Perfect Release Checklist / เช็กลิสต์ก่อน release

## ภาษาไทย

### Code and tests

- [ ] `.venv/bin/python -m pytest -q`
- [ ] `.venv/bin/python -m compileall -q app scripts`
- [ ] `node --check web/app.js`
- [ ] `git diff --check`
- [ ] ตรวจ no secret/token/PIN/passphrase ใน diff และ artifact

### Dashboard

- [ ] เปิดทุก view ได้บน desktop และ mobile
- [ ] TH/EN เปลี่ยน navigation, title, status, forms, Sales Assets และ API guides
- [ ] รูป local โหลดได้และไม่มี external media ที่ไม่ได้อนุมัติ
- [ ] service worker version ถูก bump หลัง shell change

### Business safety

- [ ] ราคาและ promotion ผูกกับ catalog
- [ ] สินค้าไม่มีราคาสร้าง order ไม่ได้
- [ ] sensitive skin มี patch-test
- [ ] human takeover หยุด automated reply
- [ ] payment evidence ต้องผ่าน `pending_review`
- [ ] confirmed order เท่านั้นที่สร้าง LINE outbox event

### Provider and deployment

- [ ] account owner อนุมัติ scope
- [ ] webhook signature/state validation อยู่ server-side
- [ ] provider duplicate/rate-limit/retry test ผ่าน
- [ ] local AI ตรวจ `192.168.74.130:11434` และ model ที่ระบุ
- [ ] public route และ LAN route ตรวจแยกกัน
- [ ] ZIP export ยังคง canceled หากไม่มีคำขอใหม่

## English

### Code and tests

- [ ] Run pytest, compileall, `node --check`, and `git diff --check`.
- [ ] Search the diff and artifacts for secrets, tokens, PINs, and passphrases.

### Dashboard

- [ ] Every view works on desktop and mobile.
- [ ] TH/EN changes navigation, title, status, forms, Sales Assets, and guide links.
- [ ] Local images load without unapproved external media.
- [ ] Service-worker shell version is bumped after shell changes.

### Business safety

- [ ] Prices and promotions are catalog-bound.
- [ ] Unpriced products cannot create orders.
- [ ] Sensitive-skin copy includes patch-test guidance.
- [ ] Human takeover pauses automated replies.
- [ ] Payment evidence stays in `pending_review`.
- [ ] Only confirmed orders create LINE outbox events.

### Provider and deployment

- [ ] The account owner approved scopes.
- [ ] Signature/state validation runs server-side.
- [ ] Duplicate, rate-limit, and retry tests have evidence.
- [ ] Local AI is checked at `192.168.74.130:11434`.
- [ ] LAN and public routes are verified separately.
- [ ] ZIP export remains canceled unless explicitly requested again.
