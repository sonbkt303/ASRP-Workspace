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

## ASRP AI Agentic Architecture Vision

- **AI-Driven Orchestration:** Mô hình ASRP hướng tới sử dụng AI làm Trí tuệ điều phối trung tâm (Agentic Orchestrator). AI tự động hiểu ngữ cảnh dự án, chọn Tooling và Rules phù hợp thay vì phụ thuộc hoàn toàn vào Script cố định.
- **Hybrid Contextual Verification:** AI chịu trách nhiệm kiểm tra lại kết quả quét từ các công cụ tĩnh, lọc bỏ False Positives, phát hiện lỗi Logic Nghiệp vụ phức tạp và đưa ra khuyến nghị sửa lỗi (Code Remediation).

## ASRP Master Workflow Invariant

0. **Layer 3.1 Source Acquisition:** Clone/copy mã nguồn tại `3.1 Source Acquisition/clones/{project_id}/{component_id}/`.
1. **Layer 1 AI Auto-Profiling:** AI sinh hồ sơ Layer 1 từ clone theo `1.1 Template`.
2. **Validate Gate:** `registry.manifest.yaml` → `lifecycle_status == validated` trước khi scan.
3. **Layer 3.4/3.6 AI Orchestrated Scan:** AI audit + 12 stage JSON + `findings.json`.
4. **Layer 3.7/5 Risk & Reporting:** Health Score, SLA roadmap, Executive HTML Dashboard.

## ASRP Security Review Execution

Khi chạy `/asrp-security-review`, tuân thủ runbook tại [`.agents/skills/asrp-security-review/SKILL.md`](skills/asrp-security-review/SKILL.md).

**Invariants (tóm tắt):**

- AI-Primary audit — không shortcut qua `python asrp.py scan` làm sole audit
- Multi-component safe merge — không ghi đè component không liên quan
- 12-stage traceability — mọi finding có `rule_id`, `security_domain`, `standard_mapping`, `review_checklist_ref`
- Template-based reports — `1.1 Template/reports/`; không inline HTML
- Exclude non-source paths — xem `references/exclusion-paths.md` trong skill
- 100% non-PASS stage coverage trong `findings.json` — zero omission

Chi tiết từng step, schema JSON, phased scan protocol: skill `references/` folder.
