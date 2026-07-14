# AppSec Research Pipeline (Professor P)

## Goal
Khi bạn chat một AppSec topic (ví dụ: `HTTP caching`, `OAuth token validation`, `SSRF defense`), pipeline sẽ điều phối “team security” theo vai trò, và hệ thống hóa thành **Knowledge Base topic(s)** trong `knowledge/`.

## Workflow (mỗi subtopic = 1 KB topic)
1. Mr A + Mr S: theory-first mechanism (70/30)
2. Mr B + Mr H + Mr R: defensive (hardening + monitoring + verification) và common mistakes
3. Mr Q: evidence pack (RFC/standards/OWASP links)
4. Mr W: assemble thành KB topic đúng output contract

## When to split subtopic
Split nếu bạn thấy topic chứa nhiều “mechanism axis” khác nhau mà không thể gói chung hợp lý trong 1 tài liệu:
- `cơ chế semantics` vs `trust boundaries/threat scenarios` vs `verification/observability signals`

## One Concept = One Home (cross-link guideline)
Trước khi tạo KB topic mới, cố gắng kiểm tra trong `knowledge/` xem có topic gần trùng không (ví dụ `knowledge/web/HTTP.md`).
Nếu overlap đáng kể:
- không viết lại nội dung cốt lõi
- đặt cross-link ở `# 11. Related Topics`
- ghi rõ ranh giới in-scope/out-of-scope trong `# 1` và/hoặc `# 7`

## Template prompt bạn dùng
`Research Topic: <topic>. Theory-first (70/30), defensive phải bao gồm hardening + monitoring + verification. Nếu quá lớn hãy tách subtopic. Ưu tiên RFC/OWASP references.`

