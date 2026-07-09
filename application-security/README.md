# Application Security Roadmap

## Mục tiêu tổng thể
Sau khi hoàn thành đủ 9 module, bạn có khả năng:
- Nhận diện asset/data và trust boundaries trong hệ thống web/backend.
- Thiết kế cơ chế AuthN/AuthZ và API authorization theo nguyên tắc least privilege.
- Áp dụng tư duy OWASP Top 10 (pin OWASP Top 10 2021) để biến “lỗ hổng” thành checklist phòng vệ.
- Viết/sửa code và endpoint theo các nguyên tắc Secure Coding có thể kiểm chứng.
- Tạo threat model, review và viết findings có evidence plan.
- Đưa các kiểm tra security vào vòng đời CI/CD (DevSecOps) để giảm rủi ro lặp lại.

## Cách dùng roadmap
1. Đọc `toc.md` để theo thứ tự chương.
2. Mỗi `module-N-*` là một chương.
3. Trong mỗi module, bạn chọn các category (TCP/UDP/HTTP/HTTPS/...) phù hợp và bổ sung nội dung từ “topic” bạn cung cấp.
4. Architecture PASS chỉ yêu cầu chuẩn hóa cấu trúc + heading + checklist item format. Phần nội dung đầy đủ sẽ được bạn tự fill/agent tổng hợp ở bước tiếp theo.

## Glossary tối thiểu
- **Asset**: thứ có giá trị đối với hệ thống (data, quyền truy cập, tài nguyên…).
- **Trust boundary**: ranh giới giữa hai miền tin cậy khác nhau (client↔server, app↔auth provider…).
- **AuthN/AuthZ**: Xác thực / Ủy quyền.
- **Risk**: mức độ tổn hại dựa trên impact và likelihood.
- **Threat**: tác nhân/đường tấn công có thể gây hại.
- **Vulnerability**: điểm yếu kỹ thuật có thể bị khai thác.
- **Finding**: kết quả review; cần evidence + remediation.
- **Mitigation**: biện pháp giảm rủi ro (control).

---

> Lưu ý: tài liệu này được thiết kế “book-like”: mỗi heading/subsection có tên cố định để TOC thống nhất.

---

## Prerequisites (tối thiểu theo thứ tự Module 1 → 9)
Áp dụng cho general application security (web + backend APIs).

- Trước Module 3 (`module-3-owasp-top10`): hoàn thành Module 1 + nắm AuthN/AuthZ ở mức khái niệm.
- Trước Module 5 (`module-5-api-security`): nắm Secure Coding (Module 4) và AuthN/AuthZ (Module 2).
- Trước Module 7 (`module-7-threat-modeling`): đã học Threat Surface và các control nền tảng từ Module 1–6.
- Trước Module 8 (`module-8-security-review`): có checklist kiểm tra + biết mapping findings → controls (Module 1–7).
- Trước Module 9 (`module-9-devsecops`): biết cách đưa mitigations thành CI checks/policy (từ Module 8) + có nền infra (Module 6).

