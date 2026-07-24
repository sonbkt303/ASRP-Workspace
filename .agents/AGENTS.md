# Project Rules & Customizations

## ASRP Rule Library Design Guardrails

- **One Rule ID = One Security Concept:** Mỗi Rule ID (ví dụ `ASRP-INJ-001`) đại diện cho một loại lỗ hổng bảo mật chuẩn hóa, áp dụng cho tất cả các ngôn ngữ lập trình được hỗ trợ.
- **No Language-Prefixed Rule Files:** Tuyệt đối không đặt tên file rule xé lẻ theo ngôn ngữ (tránh `python-sqli.yaml`, `nodejs-sqli.yaml`). Đặt tên file theo loại lỗ hổng (ví dụ `sql-injection.yaml`, `cors-wildcard.yaml`).
- **Multi-Language Patterns Support:** Trong file Rule YAML, liệt kê danh sách các ngôn ngữ được hỗ trợ tại `applicable_technologies.languages` và định nghĩa danh sách pattern tương ứng của từng ngôn ngữ trong `engine_config.semgrep_patterns`.
