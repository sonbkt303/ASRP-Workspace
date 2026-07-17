# Knowledge Base Taxonomy (fallback)

Default domain taxonomy and category resolution when the target repo has no `knowledge/README.md`.

**Priority rule**: If the target repo has `knowledge/README.md`, use that repo's taxonomy and dedup rules instead of this file.

## Domain folders

| Folder | Purpose | Example `category` frontmatter |
|--------|---------|-------------------------------|
| `foundations/` | CS, programming, crypto, math | `foundations`, `foundations/cryptography` |
| `networking/` | Network protocols, DNS, TCP/UDP, TLS/SSL | `networking`, `networking/http` |
| `web/` | HTTP, HTTPS, CDN, web platform | `web` |
| `application-security/` | AuthN/AuthZ, API security, OWASP Top 10 | `application-security` |
| `platform-security/` | DevSecOps, infrastructure security | `platform-security` |
| `cloud-security/` | Cloud-specific security topics | `cloud-security` |
| `offensive-security/` | Offensive techniques (defensive framing in KB) | `offensive-security` |
| `secure-engineering/` | Secure coding, SDLC practices | `secure-engineering` |
| `ai-security/` | AI/ML security topics | `ai-security` |
| `research/` | Research notes, appendix, deep dives | `research` |
| `glossary/` | Terms and short definitions | `glossary` |
| `learning-path/` | Learning paths, index | `learning-path` |

## Category decision tree (path resolution)

| Topic type | `category` | `proposed_path` folder |
|------------|------------|------------------------|
| HTTP, caching, headers, CDN, web platform | `web` | `knowledge/web/` |
| TCP, UDP, DNS, TLS transport | `networking` | `knowledge/networking/` |
| HTTP as transport layer only (not app semantics) | `networking/http` | `knowledge/networking/` |
| AuthN/AuthZ, API security, OWASP | `application-security` | `knowledge/application-security/` |
| DevSecOps, infra hardening | `platform-security` | `knowledge/platform-security/` |
| Secure coding, SDLC | `secure-engineering` | `knowledge/secure-engineering/` |

**Rule**: `category` may use slash; **folder** is always the first segment before `/`.
Example: `category: networking/http` → file at `knowledge/networking/http-overview.md`.

## Dedup and One Concept = One Home

Before creating a new topic, search `knowledge/` in the target repo if it exists. If overlap is significant: cross-link in `#11 Related Topics`, state in-scope/out-of-scope, do not duplicate core content.

## Filename convention

- Kebab-case / lowercase: `http-caching-auth.md`, `dns-records.md`
- Abbreviations in content keep standard form (HTTP, TLS, JWT); filename stays lowercase/kebab-case
