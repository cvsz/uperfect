# U.Perfect Deployment / การ deploy U.Perfect

## ภาษาไทย

### ขอบเขต release ปัจจุบัน

Runtime หลักเป็น FastAPI + PWA แบบ local-only ที่ bind อยู่กับ
`192.168.74.130:18765` และใช้ Ollama ที่ `192.168.74.130:11434` สำหรับ
`zCoder:latest` เท่านั้นเมื่อ model พร้อมใช้งาน

```bash
systemctl --user enable --now uperfect.service
systemctl --user status uperfect.service
curl -fsS http://192.168.74.130:18765/api/health
```

ไฟล์ unit อยู่ที่ `deploy/systemd/uperfect.service` และต้องตรวจ owner/process
ก่อน restart ทุกครั้ง

### Public route

`uperfect.zeaz.dev` เป็น public route ที่จัดการนอก repository นี้ โดย
Cloudflare/Terraform ใช้ origin ภายใน `http://192.168.74.130:18765` ตาม
deployment environment ของ owner โปรเจกต์ Terraform ที่เป็น owner ของ route อยู่
ที่ `/home/cvsz/zeaz/infrastructure/terraform/cloudflare/` บนเครื่อง deployment
ไม่ใช่ source directory ของแอปนี้

ตรวจ local และ public แยกกัน:

```bash
curl -fsS http://192.168.74.130:18765/api/health
curl -fsS https://uperfect.zeaz.dev/api/health
```

Local `200` ไม่ใช่หลักฐานว่า Cloudflare tunnel, DNS, TLS หรือ public route ใช้งาน
ได้ ต้องตรวจ response จาก public URL หลัง apply ทุกครั้ง

### Secret และ rollback

ห้ามใส่ Cloudflare API token, Terraform state, tunnel credential หรือ provider
secret ใน repository, PWA, log หรือ screenshot ใช้ secret backend/environment ของ
deployment เท่านั้น ก่อน apply ให้รัน `terraform plan` และเก็บ plan/evidence ที่
ไม่มี secret หาก route ผิดให้หยุด public exposure, ตรวจ origin/ingress และ rollback
ผ่าน owner ของ Terraform โดยไม่แก้ application database เป็นทางลัด

ZIP export ถูกยกเลิกและไม่สร้าง archive ใน release นี้

## English

### Current release boundary

The application is a local-only FastAPI + PWA runtime bound to
`192.168.74.130:18765`. The no-cost AI boundary is Ollama at
`192.168.74.130:11434`, using `zCoder:latest` only when that model is available.

```bash
systemctl --user enable --now uperfect.service
systemctl --user status uperfect.service
curl -fsS http://192.168.74.130:18765/api/health
```

The unit file is `deploy/systemd/uperfect.service`. Identify the owning unit and
process before restarting anything.

### Public route

`uperfect.zeaz.dev` is managed outside this repository. The Cloudflare/Terraform
deployment uses the internal origin `http://192.168.74.130:18765` in the owner’s
deployment environment. The Terraform owner directory is
`/home/cvsz/zeaz/infrastructure/terraform/cloudflare/` on the deployment host;
it is not this application source directory.

Verify local and public routes separately:

```bash
curl -fsS http://192.168.74.130:18765/api/health
curl -fsS https://uperfect.zeaz.dev/api/health
```

A local `200` does not prove that the Cloudflare tunnel, DNS, TLS, or public route
works. Check the public response after every infrastructure apply.

### Secrets and rollback

Never commit Cloudflare API tokens, Terraform state, tunnel credentials, or
provider secrets to this repository, the PWA, logs, or screenshots. Use the
deployment environment/secret backend. Run `terraform plan` before applying and
retain only redacted evidence. If routing is wrong, stop public exposure, trace
origin/ingress ownership, and roll back through the Terraform owner instead of
editing application data as a shortcut.

ZIP export is canceled and no archive is generated in this release.
