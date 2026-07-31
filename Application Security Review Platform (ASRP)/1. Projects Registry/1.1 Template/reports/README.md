# ASRP Report Templates

Thư mục này chứa các HTML template chuẩn cho ASRP Security Review reports.

## Templates

| File | Mục đích | Render khi |
|------|----------|-----------|
| `executive_dashboard.html` | Executive Project Dashboard – so sánh song song tất cả components | Sau khi hoàn tất Step 2 (scan) cho tất cả components |
| `component_report.html` | Chi tiết bảo mật của một component đơn lẻ | Một component mỗi lần render |

## Placeholder Convention

Tất cả template sử dụng cú pháp `{{PLACEHOLDER}}` để AI Agent điền dữ liệu từ `stage_outputs/*.json` và `risk_assessment.json`.

### Placeholders chuẩn

| Placeholder | Nguồn dữ liệu | Ví dụ |
|-------------|--------------|-------|
| `{{PROJECT_ID}}` | `run_metadata.project_id` | `cleverdent` |
| `{{PROJECT_NAME}}` | `project.yaml → project.name` | `Cleverdent` |
| `{{RUN_ID}}` | `run_metadata.run_id` | `run-20260731_145000` |
| `{{RUN_DATE}}` | `run_metadata.created_at` | `2026-07-31` |
| `{{ENGINE}}` | `run_metadata.engine` | `Claude Sonnet 4.6 Thinking` |
| `{{COMPONENT_ID}}` | `component.id` | `dent-api-nestjs` |
| `{{COMPONENT_NAME}}` | `component.name` | `dent-api-nestjs` |
| `{{COMPONENT_STACK}}` | `technologies.yaml` | `NestJS · MongoDB · Redis · GraphQL` |
| `{{HEALTH_SCORE}}` | `risk_assessment.components[id].health_score` | `68` |
| `{{HEALTH_GRADE}}` | `risk_assessment.components[id].grade` | `D` |
| `{{GATE_STATUS}}` | `risk_assessment.components[id].gate_status` | `ACTION REQUIRED` |
| `{{TOTAL_FINDINGS}}` | `findings.json → count` | `7` |
| `{{COUNT_CRITICAL}}` | findings by severity | `1` |
| `{{COUNT_HIGH}}` | findings by severity | `3` |
| `{{COUNT_MEDIUM}}` | findings by severity | `2` |
| `{{COUNT_LOW}}` | findings by severity | `1` |
| `{{FINDINGS_JSON}}` | `findings.json` embedded as JS | JSON array |
| `{{REMEDIATIONS_JSON}}` | `stage_outputs/stage_2_10_remediations.json` | JSON array |

### Dynamic Sections

Các block lặp lại sử dụng cú pháp:
```
{{#EACH findings}}
  {{finding.id}} · {{finding.title}} · {{finding.severity}}
{{/EACH}}
```

## Usage Workflow

1. **AI Agent** đọc template này từ `1.1 Template/reports/`
2. **AI Agent** load dữ liệu từ `runs/{run_id}/stage_outputs/*.json` và `risk_assessment.json`
3. **AI Agent** render template → output vào `runs/{run_id}/security_review_report*.html`
4. Report tự động có interactive stage filtering theo Layer 2 modules (2.1→2.10)

## Design System

Templates sử dụng:
- **Font**: Inter (body) + JetBrains Mono (code/IDs)
- **Color Palette**: Dark mode `#060912` base với accent blue `#4f8ef7`
- **Severity Colors**: Critical `#f43f5e` · High `#fb923c` · Medium `#fbbf24` · Low `#60a5fa`
- **Interactive**: Click-to-expand findings, Stage pill filters, Component filters
- **No external dependencies**: Chỉ Google Fonts CDN

## Report Types

### 1. `executive_dashboard.html`
- Side-by-side health score comparison (tất cả components)
- Unified findings table với **dual-axis filter** (Stage + Component)
- SLA Roadmap table (Phase 1/2/3)
- Quick links đến component reports

### 2. `component_report.html`
- Single component deep-dive
- Health score ring chart (SVG)
- Stage navigation pills (filter by 2.1→2.10 Layer 2 modules)
- Accordion findings với code diff patches
- SLA accordion sections
- Positive findings (security strengths)

## Notes

> Không edit trực tiếp file template với data thật – chỉ edit placeholders/structure.
> Data thật luôn đến từ `stage_outputs/*.json` và được điền bởi AI Agent lúc report generation.
