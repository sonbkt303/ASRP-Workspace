# Knowledge Base Topic Template

Template gốc để mọi bài trong `knowledge/` có cấu trúc nhất quán. Domain có thể mở rộng thêm section riêng nhưng **không bỏ** các mục cốt lõi.

## Filename Convention
- Tên file trong `knowledge/` nên dùng `kebab-case / lowercase` (ví dụ: `dns-records.md`).
- Các chữ viết tắt trong nội dung có thể giữ dạng đúng chuẩn (HTTP/TLS/DNS/JWT...), nhưng file name vẫn theo `lowercase/kebab-case`.

## Frontmatter (bắt buộc)
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

## Content Template (bản gốc)

# 1. Overview
Khái niệm và mục đích.

# 2. Motivation
Vì sao nó ra đời? Giải quyết vấn đề gì?

# 3. Core Concepts
Định nghĩa các thuật ngữ quan trọng.

# 4. How It Works
Luồng hoạt động từng bước.

# 5. Internal Architecture
Các thành phần và cách chúng tương tác.

# 6. Implementation
Ví dụ triển khai trong thực tế (Node.js, NGINX, Kubernetes, AWS... nếu phù hợp).

# 7. Security Considerations
Các lưu ý bảo mật và các giả định (trust boundaries, attack surface...).

# 8. Common Vulnerabilities / Mistakes
Các lỗi thiết kế hoặc triển khai thường gặp và cách phòng tránh.

# 9. Debugging & Observability
Cách kiểm tra, debug, log, công cụ thường dùng.

# 10. Best Practices
Khuyến nghị triển khai và vận hành.

# 11. Related Topics
Liên kết đến các chủ đề liên quan trong Knowledge Base.

# 12. References
RFC, tiêu chuẩn, tài liệu chính thức, sách, bài viết.

## Notes for domain adaptation
- Không phải mọi topic đều cần đủ 12 mục.
- Dù domain có lược bỏ section nào, vẫn nên đảm bảo có các mục cốt lõi: `Overview`, `How It Works`, `Security Considerations`, `Best Practices`, `Related Topics`.
- Có thể rút gọn hoặc đổi tên section `Implementation`/`Internal Architecture` nếu domain không phù hợp, miễn là vẫn giữ được tinh thần “cách hoạt động” và “cấu trúc/thành phần”.
