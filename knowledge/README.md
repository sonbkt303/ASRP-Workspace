# Knowledge Base

`knowledge/` chứa các bài Knowledge Base theo domain. Mỗi khái niệm chỉ tồn tại một lần (**One Concept = One Home**).

Trước khi tạo topic mới, search `knowledge/` để tránh trùng lặp. Nếu overlap đáng kể: cross-link ở `#11 Related Topics`, ghi rõ in-scope/out-of-scope, không viết lại nội dung cốt lõi.

Template: [`docs/knowledge-base-topic-template.md`](../docs/knowledge-base-topic-template.md)

## Domain folders

| Folder | Mục đích | Ví dụ `category` frontmatter |
|--------|----------|------------------------------|
| `foundations/` | Kiến thức nền (CS, programming, crypto, math) | `foundations`, `foundations/cryptography` |
| `networking/` | Giao thức mạng, DNS, TCP/UDP, TLS/SSL | `networking`, `networking/http` |
| `web/` | HTTP, HTTPS, CDN, web platform | `web` |
| `application-security/` | AuthN/AuthZ, API security, OWASP Top 10, proxy | `application-security` |
| `platform-security/` | DevSecOps, infrastructure security | `platform-security` |
| `cloud-security/` | Cloud-specific security topics | `cloud-security` |
| `offensive-security/` | Offensive techniques (defensive framing in KB) | `offensive-security` |
| `secure-engineering/` | Secure coding, SDLC practices | `secure-engineering` |
| `ai-security/` | AI/ML security topics | `ai-security` |
| `research/` | Research notes, appendix, deep dives | `research` |
| `glossary/` | Thuật ngữ, định nghĩa ngắn | `glossary` |
| `learning-path/` | Lộ trình học, index | `learning-path` |

## Chọn `category` cho frontmatter

- Dùng path tương đối với domain folder: `web`, `networking`, `application-security`, v.v.
- Sub-domain có thể dùng slash: `networking/http`, `foundations/cryptography`.
- Không chắc → đọc README trong domain (ví dụ [`foundations/README.md`](foundations/README.md)) hoặc hỏi user.

### Category decision tree (path resolution)

| Topic type | `category` | `proposed_path` folder |
|------------|------------|------------------------|
| HTTP, caching, headers, CDN, web platform | `web` | `knowledge/web/` |
| TCP, UDP, DNS, TLS transport | `networking` | `knowledge/networking/` |
| HTTP as transport layer only (not app semantics) | `networking/http` | `knowledge/networking/` |
| AuthN/AuthZ, API security, OWASP | `application-security` | `knowledge/application-security/` |
| DevSecOps, infra hardening | `platform-security` | `knowledge/platform-security/` |
| Secure coding, SDLC | `secure-engineering` | `knowledge/secure-engineering/` |

**Rule**: `category` có thể có slash; **folder** luôn là segment đầu tiên trước `/`.
Ví dụ: `category: networking/http` → file tại `knowledge/networking/http-overview.md`.

## Domain boundaries

Một số giới hạn phạm vi (tránh nhảy domain quá sớm) — chi tiết trong [`foundations/README.md`](foundations/README.md):
- `programming/`: không JavaScript/Node/React
- `data/`: không API, không HTTP
- `cryptography/`: không JWT, không TLS (có topic riêng ở domain khác)

## Filename convention

- Kebab-case / lowercase: `http-caching-auth.md`, `dns-records.md`
- Abbreviations trong nội dung giữ chuẩn (HTTP, TLS, JWT); filename vẫn lowercase/kebab-case

## AppSec research pipeline

Khi nghiên cứu topic mới qua orchestrator skill (`appsec-research-orchestrator`, Mr P — Professional) — runtime SSoT: [`cursor-agents/skills/appsec-research-orchestrator/SKILL.md`](../../cursor-agents/skills/appsec-research-orchestrator/SKILL.md):
1. Dedup search trong `knowledge/` (bước pre-flight bắt buộc)
2. Resolve `category` từ bảng domain trên
3. Output theo template 12 section — xem [`docs/appsec-research-pipeline/README.md`](../docs/appsec-research-pipeline/README.md) và [`role-glossary.md`](../docs/appsec-research-pipeline/role-glossary.md)
