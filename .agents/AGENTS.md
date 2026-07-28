# Project Rules & Customizations

## ASRP Rule Library Design Guardrails

- **One Rule ID = One Security Concept:** Mỗi Rule ID (ví dụ `ASRP-INJ-001`) đại diện cho một loại lỗ hổng bảo mật chuẩn hóa, áp dụng cho tất cả các ngôn ngữ lập trình được hỗ trợ.
- **No Language-Prefixed Rule Files:** Tuyệt đối không đặt tên file rule xé lẻ theo ngôn ngữ (tránh `python-sqli.yaml`, `nodejs-sqli.yaml`). Đặt tên file theo loại lỗ hổng (ví dụ `sql-injection.yaml`, `cors-wildcard.yaml`).
- **Multi-Language Patterns Support:** Trong file Rule YAML, liệt kê danh sách các ngôn ngữ được hỗ trợ tại `applicable_technologies.languages` và định nghĩa danh sách pattern tương ứng của từng ngôn ngữ trong `engine_config.semgrep_patterns`.

## ASRP CLI Portability & Persistent Source Acquisition Guardrails

- **Dynamic Workspace Root Resolution:** Tất cả các module CLI Python (như `asrp.py`, `source_acquisition.py`, `rule_resolver.py`, `scanner_orchestrator.py`, `findings_normalizer.py`, `risk_assessor.py`, `report_generator.py`) PHẢI tính toán đường dẫn dựa trên `os.path.dirname(os.path.abspath(__file__))`. Tuyệt đối không hardcode đường dẫn tuyệt đối dạng `C:\Users\...`.
- **Persistent Workspace Location:** Mã nguồn clone/copy luôn nằm cố định tại `3. Assessment Engine/3.1 Source Acquisition/clones/{project_id}/{component_id}/`.
- **Idempotent Re-acquisition:**
  - Nếu thư mục `clones/{project_id}/{component_id}` đã tồn tại -> Giữ nguyên mã nguồn & `git pull` bản mới nhất.
  - Nếu thư mục bị xóa hoặc chưa có -> Tự động clone/copy mới từ đầu.

