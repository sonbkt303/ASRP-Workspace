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

## ASRP 4-Step AI Master Workflow Invariant

1. **Layer 3.1 Source Acquisition:** Clone/copy mã nguồn cố định tại `3.1 Source Acquisition/clones/{project_id}/{component_id}/`.
2. **Layer 1 AI Auto-Profiling:** AI tự đọc mã nguồn clone để tự động sinh 100% tệp Hồ sơ Dự án Layer 1 theo template `1.1 Template` (Không nhập thủ công YAML).
3. **Layer 3.4/3.6 AI Orchestrated Scan:** AI tự chọn Tooling/Rules, lọc False Positives và xuất dữ liệu chuẩn `findings.json`.
4. **Layer 3.7/5 Risk & Reporting:** Tự động tính điểm Health Score, lập lộ trình SLA và xuất Executive HTML Dashboard.
## ASRP Strict Skill Execution & AI Workflow Guardrail

- **Strict Skill Step-by-Step Compliance:** Khi nhận câu lệnh trigger `/asrp-security-review`, AI Agent BẮT BUỘC phải tuân thủ nghiêm ngặt từng bước chi tiết được mô tả trong `SKILL.md` (bắt đầu bằng Step 1: AI Auto-Profiling & Layer 1 Registry Generation từ mã nguồn clone). Không tự ý bỏ qua bước hoặc thực hiện lệnh CLI tắt nếu chưa hoàn tất đúng quy trình chỉ định.

## ASRP Resource Optimization & Non-Essential Exclusion Guardrail

- **Strict Non-Essential Path Exclusion:** Khi thực hiện AI Auto-Profiling, Rule Resolution hoặc Scanner Orchestration, AI Agent & Scanner Orchestrator BẮT BUỘC phải loại trừ hoàn toàn các thư mục/tệp phụ trợ không trực tiếp chứa mã nguồn nghiệp vụ để tối ưu tài nguyên tính toán (avoid unnecessary token & CPU resource consumption).
- **Mandatory Excluded Paths:**
  - Dependencies & Build Artifacts: `node_modules`, `vendor`, `dist`, `build`, `out`, `coverage`, `.pnpm-store`
  - Tooling & IDE Configurations: `.vscode`, `.idea`, `.devcontainer`, `.husky`, `.github`, `.agents`
  ## ASRP Stack-Aware Security Standards Auto-Selection Guardrail

- **Mandatory Intelligent Rule & Standard Selection:** Khi thực hiện Step 1 (AI Auto-Profiling), AI Agent BẮT BUỘC phải đọc toàn bộ mã nguồn, cấu hình (`package.json`, `Dockerfile`, framework, database) và domain nghiệp vụ để tự động lựa chọn & mapping chính xác danh sách Security Standards & Rule Sets từ `2.1 Security Standards` vào `technologies.yaml` (`rule_set_ids`) và `assessment.yaml` (`rule_sets`). Tuyệt đối không để trống hoặc bỏ qua bước tự động chọn quy tắc theo tech stack.



