# Knowledge Base Topic Template

Template for consistent structure in `knowledge/`. Domains may add sections but **must not omit** core sections.

## Filename Convention
- File names in `knowledge/` should use `kebab-case / lowercase` (e.g. `dns-records.md`).
- Abbreviations in content may keep standard form (HTTP/TLS/DNS/JWT...); file names stay `lowercase/kebab-case`.

## Frontmatter (required)
```yaml
---
title:
category:
difficulty:
prerequisites:
related:
tags:
references:
last_updated:
status:
---
```

## Content Template

# 1. Overview
Concept and purpose.

# 2. Motivation
Why it exists; what problem it solves.

# 3. Core Concepts
Definitions of key terms.

# 4. How It Works
Step-by-step flow.

# 5. Internal Architecture
Components and how they interact.

# 6. Implementation
Real-world examples (Node.js, NGINX, Kubernetes, AWS... when applicable).

# 7. Security Considerations
Security notes and assumptions (trust boundaries, attack surface...).

# 8. Common Vulnerabilities / Mistakes
Common design or deployment mistakes and how to avoid them.

# 9. Debugging & Observability
How to verify, debug, log, and tools commonly used.

# 10. Best Practices
Deployment and operations recommendations.

# 11. Related Topics
Links to related topics in the Knowledge Base.

# 12. References
RFC, standards, official docs, books, articles.

## Notes for domain adaptation
- Not every topic needs all 12 sections.
- Even when sections are shortened, keep core spirit: Overview, How It Works, Security Considerations, Best Practices, Related Topics.
- Implementation/Internal Architecture may be adapted when the domain does not fit.
