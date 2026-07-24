# Layer 2.4 — Review Checklists (`2.4 Review Checklists/`)

Thư mục `2.4 Review Checklists/` lưu trữ các **Bảng câu hỏi kiểm tra bảo mật thủ công (Human Review Checklists)** dành cho Security Auditor thực hiện khi tiến hành phỏng vấn team dev, đánh giá sơ đồ kiến trúc hoặc cấp sign-off cho `registry.manifest.yaml`.

Khác với `2.3 Rule Library` (dành cho Máy/Tool tự động quét), `2.4 Review Checklists` dành cho **Con người (Human Gate)** thực hiện.

---

## 🏗️ Cấu trúc Checklists

```
2.4 Review Checklists/
├── README.md                           # Tài liệu hướng dẫn (file này)
├── architecture-security-checklist.yaml # Checklist Đánh giá Bảo mật Kiến trúc & Phân quyền
└── deployment-security-checklist.yaml   # Checklist Đánh giá Quy trình Triển khai & CI/CD
```

---

## 📝 Định dạng một Checklist Item (YAML Spec)

```yaml
checklist:
  id: "CHK-ARCH-001"
  title: "Xác thực 2 yếu tố (2FA/OTP) cho hành động nhạy cảm"
  category: "authentication"
  review_method: "interview_and_code_walkthrough" # phỏng vấn hoặc xem code trực tiếp
  verification_steps:
    - "Kiểm tra xem các hành động rút tiền/đổi mật khẩu có bắt buộc nhập OTP không."
    - "Xác nhận OTP có thời gian hết hạn < 5 phút và chống Brute Force."
  compliance_mapping:
    owasp_asvs: "V2.8.1"
```
