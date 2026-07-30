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

## ASRP Modular Step Execution & AI-Primary Scanning Guardrail

- **Modular Independent Step Execution:** Khi nhận câu lệnh trigger `/asrp-security-review`, AI Agent BẮT BUỘC hỗ trợ thực thi độc lập từng bước tùy theo tham số/yêu cầu của người dùng:
  - `profile` (hoặc `step 1`): Chỉ thực hiện Step 1 (AI Auto-Profiling & Layer 1 Profile Generation).
  - `scan` (hoặc `step 2`): Chỉ thực hiện Step 2 (AI-Primary Security Scanning & Verification từ nguồn clone).
  - `report` (hoặc `step 3`): Chỉ thực hiện Step 3 (Risk Assessment & Executive HTML/MD Report Generation).
  - `full` / `review`: Thực hiện lần lượt toàn bộ 3 bước.
## ASRP Strict Rule Library Traceability Guardrail

## ASRP Layer 2 Multi-Module Knowledge Base Scanning Guardrail

## ASRP Layer 2 Knowledge Base Pre-Building Guardrail

- **Pre-Scan Knowledge Base Completeness:** Trước khi tiến hành quét mã nguồn (Step 2), AI Agent BẮT BUỘC phải chủ động rà soát và xây dựng đầy đủ các bộ Tiêu chuẩn (Layer 2.1), Miền An ninh (Layer 2.2), Checklist kiểm thử (Layer 2.4), Playbooks (Layer 2.5) và Threat Models (Layer 2.6). AI Agent không thực hiện quét rỗng khi chưa có tri thức checklist và quy chuẩn đối soát cụ thể.

## ASRP Layer 2 Complete Single Responsibility & Zero-Overlap Guardrail

- **Strict Separation of Concerns across Layer 2 Assets:** Tất cả 12 module trong Layer 2 BẮT BUỘC tuân thủ phạm vi chức năng duy nhất, tuyệt đối không xâm phạm ranh giới của nhau:
  1. `2.1 Security Standards`: Tri thức định danh & Ma trận quy chiếu tiêu chuẩn quốc tế tĩnh (Khóa chính CWE ID).
  2. `2.2 Security Domains`: Danh mục phân loại miền an ninh kỹ thuật nghiệp vụ (13 Domains).
  3. `2.3 Rule Library`: Pattern thực thi tĩnh dành cho Tooling & AI Prompts (Semgrep AST, Gitleaks Regex, AI System Prompts).
  4. `2.4 Review Checklists`: Câu hỏi thẩm định đối soát dành cho Auditor / AI Reviewer (`verification_requirement`).
  5. `2.5 Playbooks`: Quy trình Vận hành Chuẩn (SOP) từng bước thực hiện đợt Security Review từ Step 1 đến Step 3.
  6. `2.6 Threat Models`: Khung Phân tích Mối đe dọa Kiến trúc (STRIDE Framework) trước khi phát triển.
  7. `2.7 Secure Coding Guidelines`: Hướng dẫn lập trình an toàn dành cho Developer theo từng Framework (NestJS, Django, React).
  8. `2.8 Best Practices`: Nguyên tắc khuyên dùng cấp Kiến trúc & DevSecOps.
  9. `2.9 Attack Patterns`: Kịch bản tấn công giả lập của Hacker (CAPEC Scenarios) dành cho Red Team.
  10. `2.10 Remediation Guides`: Hướng dẫn sửa lỗi chi tiết & Code Diff Patches cho Developer sau khi phát hiện lỗ hổng.
  11. `2.11 Case Studies`: Bài học kinh nghiệm sự cố thực tế (Post-Mortem Incident Reports).
  12. `2.12 Decision Logs`: Nhật ký quyết định kiến trúc an toàn thông tin (Architecture Decision Records - ADR).

## ASRP Layer 2 Modular Stage JSON Output Guardrail

- **Modular Stage Output Files:** Trong Step 2, kết quả đánh giá của từng module Layer 2 (2.1 Standards, 2.2 Domains, 2.3 Rules, 2.4 Checklists, 2.6 Threat Models, 2.10 Remediation) BẮT BUỘC được ghi nhận riêng thành các tệp JSON tương ứng tại `runs/{run_id}/stage_outputs/`:
  - `stage_2_1_standards.json`
  - `stage_2_2_domains.json`
  - `stage_2_3_rules.json`
  - `stage_2_4_checklists.json`
  - `stage_2_6_threats.json`
  - `stage_2_10_remediations.json`
- **Common Template Compliance:** Tất cả các file stage output PHẢI tuân thủ 100% Common Stage JSON Schema với các trường cố định: `stage_id`, `layer_module_ref`, `summary`, `results` (`item_id`, `status`, `evidence`, `standard_mappings`, `remediation`).
- **Report Aggregation Requirement:** Layer 3.7 (Risk Assessor) và Layer 5 (Report Generator) sẽ đọc và hợp nhất dữ liệu từ tất cả các tệp `stage_outputs/*.json` để tính điểm Health Score và tổng hợp báo cáo Executive HTML/MD Report.

## ASRP Real Codebase Deep Discovery Guardrail

- **Recursive Real Codebase Discovery:** AI Agent & Scanner Orchestrator BẮT BUỘC thực hiện rà soát đệ quy toàn bộ cây thư mục mã nguồn thực tế của dự án (đặc biệt là các thư mục `apps/`, `libs/`, `src/`, `packages/`, `services/`, `controllers/`, `dockerfiles/`, `k8s/`). Tuyệt đối không chỉ quét tệp mẫu hoặc tệp thử nghiệm ở thư mục gốc (`main.py`, `test.py`).
- **Framework & Technology Stack Alignment:** Khi quét dự án (ví dụ NestJS Monorepo), AI Agent BẮT BUỘC phải đọc các tệp mã nguồn thuộc đúng techstack chính (`.ts`, `.js`, `.json`, `.yaml`, NestJS `@Controller`, `@Injectable`, `package.json`, `docker-compose.yaml`) của tất cả các microservices trong dự án.

## ASRP Multi-Component Independent Reporting Guardrail

- **Multi-Repo / Multi-Component Separation:** Khi một dự án chứa nhiều repositories/components trong `components.yaml` có techstack khác nhau (như `dent-api-nestjs` cho Backend và `dent-monorepo` cho Frontend), AI Agent & Report Generator BẮT BUỘC:
  1. Đánh giá và xuất báo cáo độc lập cho từng component: `security_review_report_{component_id}.html` & `.md` (Ví dụ: `security_review_report_dent-api-nestjs.html` và `security_review_report_dent-monorepo.html`).
  2. Tạo báo cáo tổng hợp **Executive Project Dashboard** (`security_review_report.html`) hiển thị thẻ điểm Health Score, xếp hạng Grade và bảng so sánh rủi ro song song của tất cả các repository component thuộc dự án.


