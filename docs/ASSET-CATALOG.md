# Product and Chatbot Asset Catalog / คลังสินค้าและ asset แชท

## ภาษาไทย

`assets/chatbot/asset-manifest.json` เป็นบัญชี media local และ
`assets/chatbot/sales_response_assets.json` เป็นข้อความ TH/EN ของ Autobot

### สินค้าหลัก

| Product ID | สถานะ | ราคา | การปิดการขาย |
| --- | --- | --- | --- |
| `LOE_VITC_SERUM` | active, catalog review | 98 THB ใน brief; verify ก่อน live | เสนอโปร/สร้าง draft หลังยืนยันจำนวน |
| `MALA_CHILI_OIL` | active, admin review | ไม่ได้ระบุ | ตรวจราคา/สต็อกโดยแอดมินก่อนเสนอ total |
| `LOE_CHARCOAL_SOAP` | reference only | ไม่ได้ยืนยัน | ตรวจราคา/สต็อกโดยแอดมินก่อนเสนอ |
| `CHOE_FOUNDATION` | reference only | ไม่ได้ยืนยัน | ส่งต่อให้แอดมินตรวจ |
| `THE_COPPER_CREAM` | reference only | ไม่ได้ยืนยัน | ส่งต่อให้แอดมินตรวจ |

### Policy

- media ต้องเป็น local relative path ใต้ project root
- ห้ามใช้ CAPTCHA หรืออ้างว่า export สำเร็จเมื่อ public retrieval ถูกบล็อก
- ทุก intent และ CTA ต้องมี TH/EN
- sensitive skin ต้องมี patch-test และหยุดใช้เมื่อระคายเคือง
- unpriced product ห้ามสร้าง order

## English

`asset-manifest.json` indexes local media. `sales_response_assets.json` contains
the bilingual Autobot intents, objections, selling points, and closing CTAs.

| Product ID | State | Price | Closing behavior |
| --- | --- | --- | --- |
| `LOE_VITC_SERUM` | active, catalog review | 98 THB in brief; verify before live | offer/draft after quantity confirmation |
| `MALA_CHILI_OIL` | active, admin review | not supplied | admin verifies price/stock before total |
| `LOE_CHARCOAL_SOAP` | reference only | unverified | admin verifies price/stock before offer |
| `CHOE_FOUNDATION` | reference only | unverified | admin review |
| `THE_COPPER_CREAM` | reference only | unverified | admin review |

Media must be local and validated. A CAPTCHA-blocked public retrieval is never
reported as a successful export. Every response asset has TH/EN content. Unpriced
products cannot create orders, and sensitive-skin replies include patch-test and
stop-use guidance.
