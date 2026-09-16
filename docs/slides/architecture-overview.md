---
marp: true
theme: asrp-security
paginate: true
size: 16:9
title: ASRP — Security Sharing
description: Giới thiệu ASRP — Security Review as Code (slide + script đọc sẵn)
---

<!-- _class: lead -->

# Application Security Review Platform

## Security Review as Code

<!--
SCRIPT — SLIDE 1 (Mở đầu) · ~2 phút

Chào mọi người. Hôm nay t chia sẻ về ASRP — Application Security Review Platform,
nền tảng đánh giá bảo mật ứng dụng theo mô hình Security Review as Code.

Buổi này tập trung big picture: vấn đề gì, ASRP giải quyết thế nào, kiến trúc tổng quan,
và demo report thực tế trên dự án cleverdent. Không đi sâu YAML hay schema — phần đó để buổi workshop sau.

Mục tiêu: sau buổi này, mọi người biết khi nào dùng ASRP, ai làm gì,
và đọc báo cáo security để ưu tiên fix.
-->

---

## Vấn đề hiện tại

<div class="columns">

<div class="card">
<h3>🔍 Review thủ công</h3>
<p>Mỗi dự án một kiểu — chậm, khó audit lại sau vài tháng</p>
</div>

<div class="card">
<h3>🧩 Tool rời rạc</h3>
<p>Semgrep, SCA, secrets… output khó gom, khó map OWASP/CWE</p>
</div>

</div>

<div class="columns">

<div class="card">
<h3>📂 Thiếu hồ sơ dự án</h3>
<p>Quét mà chưa hiểu stack & scope → false positive, noise</p>
</div>

<div class="card">
<h3>📋 Báo cáo yếu</h3>
<p>Thiếu evidence (file, dòng, snippet) và roadmap ưu tiên fix</p>
</div>

</div>

<!--
SCRIPT — SLIDE 2 (Vấn đề) · ~3 phút

Trước khi nói giải pháp, nhìn lại pain point team thường gặp.

Thứ nhất: review thủ công — mỗi dự án một kiểu, chậm, khó audit lại sau vài tháng.

Thứ hai: tool scan rời rạc — Semgrep một chỗ, dependency scanner một chỗ, secret scan một chỗ.
Output khó gom, khó map chuẩn OWASP hay CWE.

Thứ ba: hay quét mà chưa hiểu dự án — không biết tech stack, scope, component nào quan trọng
→ scan sai phạm vi, nhiều noise.

Thứ tư: báo cáo gửi PM hay Tech Lead thường thiếu evidence — không chỉ rõ file, dòng code, snippet —
và thiếu roadmap ưu tiên fix.

ASRP sinh ra để giải bốn vấn đề này.
-->

---

## ASRP giải quyết gì?

> **Biết dự án trước → quét có lens → báo cáo có căn cứ**

<div class="pill-row">
<span class="pill">clone → profile → scan → report</span>
<span class="pill ok">OWASP · ASVS · CWE</span>
<span class="pill">audit-ready output</span>
</div>

- Pipeline thống nhất — không scan mù
- Tự hiểu tech stack, kiến trúc, scope, compliance context
- Findings có **evidence** · executive dashboard · remediation roadmap + SLA

<!--
SCRIPT — SLIDE 3 (Giải pháp) · ~2 phút

Câu tagline của ASRP: "Biết dự án trước → quét có lens → báo cáo có căn cứ".

Không scan mù. Luôn có hồ sơ dự án trước khi chạy engine.

Pipeline thống nhất: clone source → profile dự án → scan theo assessment lens → sinh báo cáo.

Platform tự hiểu tech stack, kiến trúc, scope và compliance context.
Đánh giá theo chuẩn quốc tế — OWASP Top 10, API Security, ASVS, CWE — cộng rule nội bộ.

Output không chỉ là list lỗi. Là báo cáo audit-ready:
findings có evidence, executive dashboard cho stakeholder, và remediation roadmap có SLA gợi ý.
-->

---

<!-- _class: small -->

## Mental Model — 5 bước, mỗi bước có mục đích

![w:920](assets/pipeline-mental-model.svg)

| Bước | Làm gì | Mục đích (để làm gì) |
|------|--------|----------------------|
| **Acquire** | Clone repo, pin commit SHA | Có **source cố định** — review đúng version, tái lập kết quả sau vài tháng |
| **Profile** | Sinh 8 YAML (stack, scope, `assessment.yaml`…) | Engine **hiểu dự án** trước khi scan — không quét mù, không full ASVS mặc định |
| **Validate** | AppSec review & sign-off hồ sơ | **Human gate** — chặn scan khi profile sai/thiếu; chỉ chạy khi `validated` |
| **Scan** | AI reviewer trọng tâm + tools hỗ trợ theo lens | Phát hiện lỗ hổng **theo ngữ cảnh** dự án (logic flaws, BOLA…) + pattern/CVE/secrets |
| **Report** | Chuẩn hóa findings → executive HTML | Stakeholder **đọc, ưu tiên fix**, có evidence & audit trail — không chỉ list lỗi thô |

<!--
SCRIPT — SLIDE 4 (Mental Model) · ~3 phút

Đây là mental model cần nhớ — 5 bước, mỗi bước trả lời câu hỏi: làm gì và để làm gì.

Acquire — clone repo và pin commit SHA.
Mục đích: có source cố định. Review đúng version, sau vài tháng vẫn tái lập được kết quả.

Profile — sinh hồ sơ dự án, 8 file YAML: stack, kiến trúc, scope, assessment lens.
Mục đích: engine hiểu dự án trước khi scan. Không quét mù, không full ASVS mặc định.

Validate — AppSec hoặc Security Lead review và sign-off hồ sơ.
Mục đích: human gate. Chặn scan khi profile sai hoặc chưa đủ. Engine chỉ chạy khi lifecycle_status = validated.

Scan — AI reviewer là trọng tâm; tools (Semgrep, Trivy, Gitleaks…) chỉ hỗ trợ theo assessment lens.
Mục đích: phát hiện lỗ hổng theo ngữ cảnh dự án — logic flaws, BOLA/IDOR — cộng pattern, CVE, secrets.

Report — chuẩn hóa findings, sinh executive HTML dashboard.
Mục đích: stakeholder đọc, ưu tiên fix, có evidence và audit trail. Không chỉ là list lỗi thô.

Nhớ nguyên tắc: hồ sơ dự án trước, scan sau. Không bấm scan bừa.
5 từ: acquire, profile, validate, scan, report.
-->

---

## Nguyên tắc thiết kế

<div class="pill-row">
<span class="pill">Hybrid review</span>
<span class="pill">Assessment lens</span>
<span class="pill ok">Evidence-first</span>
<span class="pill">One project = one folder</span>
<span class="pill warn">Knowledge ≠ Rules</span>
</div>

| Nguyên tắc | Mô tả |
|------------|-------|
| **Hybrid review** | AI (~50–60%) trọng tâm · Tools hỗ trợ (~20–30%) · Human gate (~10–20%) |
| **Assessment lens** | Không full ASVS mặc định — scope qua `assessment.yaml` |
| **Evidence-first** | Mọi finding phải có evidence để audit & re-verify |
| **One project = one folder** | Mỗi dự án = instance từ `1.1 Template` |
| **Knowledge ≠ Rules** | Concept KB (lý thuyết) tách biệt Rule Library (executable) |

<!--
SCRIPT — SLIDE 5 (Nguyên tắc) · ~2 phút

ASRP có 5 nguyên tắc thiết kế.

Hybrid review: AI scan là trọng tâm (~50–60%) — phân tích code theo ngữ cảnh dự án.
Tools chỉ hỗ trợ (~20–30%) — secrets, CVE, pattern đã biết. Human gate và triage (~10–20%).
Không thay thế hoàn toàn con người.

Assessment lens: không quét full ASVS mặc định.
Scope qua assessment.yaml — quét phần cần thiết, giảm noise.

Evidence-first: mọi finding phải có evidence — file, dòng code, snippet — để audit và re-verify.

One project = one folder: mỗi dự án là một folder, copy từ template chuẩn.

Knowledge ≠ Rules: lý thuyết bảo mật tách khỏi rule executable.
Đọc OWASP là một nơi; chạy scan là nơi khác.
-->

---

<!-- _class: anchor small -->

## Kiến trúc 6 Layer — mỗi layer có vai trò

![w:900](assets/asrp-6-layer.svg)

| Layer | Vai trò | Mục đích (để làm gì) |
|-------|---------|----------------------|
| **L1** Projects Registry | Hồ sơ dự án — 8 YAML profile | Engine **biết dự án** trước khi scan: stack, scope, assessment lens; chỉ chạy khi `validated` |
| **L2** Knowledge Base | Standards + **Rule Library** executable | Biết **chuẩn gì** (OWASP, ASVS…) và **rule nào** áp dụng — tách knowledge khỏi rule chạy |
| **L3** Assessment Engine | Motor trung tâm | Profile + rules → **findings + evidence**; AI reviewer trọng tâm, tools hỗ trợ theo lens |
| **L4** Integrations | Orchestrate tools bên ngoài | Semgrep, Trivy, Gitleaks, CI/CD **feed vào L3** — normalize output, không scan rời rạc |
| **L5** Reporting | Output cho stakeholder | Executive HTML, technical report — **đọc, ưu tiên fix**, có evidence & audit trail |
| **L6** Dashboard | Portfolio & analytics | Nhìn **cross-project**: risk trends, compliance coverage, rule coverage — planned |

<div class="pill-row">
<span class="pill ok">L1 · L2 · L3 · L5 — Done</span>
<span class="pill warn">L4 · L6 — Planned</span>
</div>

<!--
SCRIPT — SLIDE 6 (6 Layer) · ~3 phút — SLIDE ANCHOR

Đây là slide anchor — bức tranh lớn cần nhớ. Mỗi layer trả lời: vai trò gì và để làm gì.

L1 Projects Registry — hồ sơ dự án, 8 file YAML.
Mục đích: engine biết dự án trước khi scan — stack, scope, assessment lens. Human gate: chỉ scan khi validated.

L2 Security Knowledge Base — standards, security domains, và Rule Library executable.
Mục đích: biết chuẩn gì và rule nào chạy. Knowledge tách khỏi rule — đọc OWASP là một nơi, chạy scan là nơi khác.

L3 Assessment Engine — motor trung tâm.
Mục đích: nhận profile + rules, sinh findings và evidence. AI reviewer trọng tâm; tools chỉ hỗ trợ theo lens.

L4 Integrations — orchestrate tools bên ngoài: Semgrep, Trivy, Gitleaks, CI/CD. Đang planned.
Mục đích: tools feed vào L3, normalize output — không chạy scan rời rạc từng tool.

L5 Reporting — executive HTML, technical report, remediation roadmap.
Mục đích: stakeholder đọc, ưu tiên fix, có evidence và audit trail.

L6 Dashboard — portfolio view, risk trends, compliance coverage. Cũng planned.
Mục đích: nhìn xuyên suốt nhiều dự án, không chỉ một lần scan.

Luồng hôm nay: L1 và L2 là input, L3 là motor, L5 là output chính.
-->

---

## Trạng thái triển khai

| Layer | Status | Ghi chú |
|-------|--------|---------|
| **L1** — Projects Registry | ✅ **Done** | Template + schema + `cleverdent/` |
| **L2** — Rule Library | ✅ **Done** | ~27 rules · 6 scanner engines |
| **L3** — Assessment Engine | ✅ **Done** | Resolver, orchestrator, normalizer |
| **L5** — Reporting | ✅ **Done** | Executive HTML & MD report |
| **L4** — Integrations | 🔜 Planned | GitHub, CI, DAST… |
| **L6** — Dashboard | 🔜 Planned | Portfolio, trends, coverage |

**Hôm nay team có thể:** profile → validate → scan → đọc HTML report

<!--
SCRIPT — SLIDE 7 (Roadmap) · ~1 phút

Roadmap thẳng thắn — phần nào đã chạy, phần nào chưa.

L1, L2, L3, L5 đã done — core pipeline chạy được với case study cleverdent.

Rule Library hiện có khoảng 27 rules, hỗ trợ 6 scanner engines:
Semgrep, Gitleaks, Trivy, Checkov, CI/CD checks, và custom AI rules.

L4 Integrations và L6 Dashboard đang planned — chưa có đầy đủ.

Hôm nay team có thể dùng ngay: profile dự án → validate → scan → đọc executive HTML report.
-->

---

## Luồng End-to-End (7 bước)

![w:900](assets/pipeline-7-steps.svg)

**CLI:** `asrp validate --project {id}`

<!--
SCRIPT — SLIDE 8 (7 bước) · ~2 phút

Chi tiết kỹ thuật — 7 bước, mỗi bước sinh artifact.

Bước 1: Acquire — clone hoặc copy source.
Bước 2: Profile — sinh 8 file YAML.
Bước 3: Human validate — AppSec hoặc Security Lead xác nhận profile.
         Chỉ khi lifecycle_status = validated engine mới scan.
Bước 4: Resolve rules — ghép profile với Rule Library → resolved-rules.json.
Bước 5: Scan — AI reviewer trọng tâm; tools hỗ trợ.
Bước 6: Normalize — chuẩn hóa, deduplicate → findings.json.
Bước 7: Report — sinh security_review_report.html.

Cổng validate là bắt buộc. Engine không scan nếu profile chưa validated — tránh quét sai scope.
-->

---

## Layer 1 — Projects Registry

<div class="columns">

<div>

**Vai trò:** Hồ sơ dự án — engine đọc **trước khi** scan

<div class="pill-row">
<span class="pill">project.yaml</span>
<span class="pill">technologies.yaml</span>
<span class="pill warn">assessment.yaml</span>
<span class="pill">+ 5 files</span>
</div>

</div>

<div class="card">

**Lifecycle**

`draft` → `profiled` → **`validated`** → `scanning` → `completed`

**Human gate:** Engine **không scan** khi `!= validated`

**Example:** `cleverdent/` — NestJS + monorepo ✅

</div>

</div>

<!--
SCRIPT — SLIDE 9 (Layer 1) · ~2 phút

Layer 1 — Projects Registry — trái tim của "biết dự án trước".

Mỗi dự án có 8 file YAML: project metadata, components, technologies, architecture,
scope, context, assessment, và registry manifest.

File quan trọng: technologies.yaml — engine biết ngôn ngữ, framework để chọn rule.
assessment.yaml — định nghĩa assessment lens: quét gì, không quét gì,
bật SAST, SCA, secrets, IaC hay không.

Lifecycle: draft → profiled → validated → scanning → completed.

Rule cứng: engine không scan khi chưa validated.

Ví dụ: cleverdent — Cleverdent Enterprise Dental Management Platform,
NestJS backend + frontend monorepo, đã validated.
-->

---

## Layer 2 — Knowledge vs Rules

<div class="columns">

<div class="card" style="border-color:#3b82f6">

### 📚 KNOWLEDGE
*concept · lý thuyết*

- `Security Knowledge Base/knowledge/`
- OWASP, best practices, training
- Ví dụ: *"SQL Injection là gì?"*

</div>

<div class="card" style="border-color:#f59e0b">

### ⚡ RULES
*executable · chạy scan*

- `ASRP/2.3 Rule Library/`
- Semgrep, Trivy, Gitleaks patterns
- Ví dụ: `ASRP-INJ-001`

</div>

</div>

**Rule:** Dev thêm rule → **Rule Library** · Đọc lý thuyết → **Knowledge Base**

<!--
SCRIPT — SLIDE 10 (Layer 2) · ~2 phút

Slide hay gây nhầm — cần tách rõ.

Knowledge — concept, lý thuyết — nằm ở Security Knowledge Base/knowledge/.
Dùng tham chiếu, training, AI/RAG. Ví dụ: "SQL Injection là gì?"

Rules — executable — nằm ở ASRP/2.3 Rule Library/.
Pattern Semgrep, Trivy, Gitleaks. Ví dụ: ASRP-INJ-001 — rule SQL Injection
chạy trên Python, JS/TS, Go, Java.

Dev thêm rule mới → Rule Library. Đọc lý thuyết → Knowledge Base. Hai thứ khác nhau, không trộn.
-->

---

## Layer 3 + Layer 5 — Engine & Output

<div class="columns small">

<div>

**L3 — Assessment Engine**

| Module | Chức năng |
|--------|-----------|
| Source Acquisition | Clone repo, pin SHA |
| Rule Evaluation | Resolve & chạy rules |
| AI Reviewer | BOLA/IDOR, logic flaws |
| Findings + Risk | Normalize, scoring |
| Report Generator | Sinh HTML |

</div>

<div>

**L5 — Reporting**

- Security health score
- Findings + **evidence**
- OWASP / CWE mapping
- Remediation roadmap + SLA

`cleverdent/runs/run-*/security_review_report.html`

</div>

</div>

<!--
SCRIPT — SLIDE 11 (L3 + L5) · ~2 phút

Layer 3 — Assessment Engine — biến profile + rules thành findings + evidence.

Source Acquisition clone repo và pin SHA.
Rule Evaluation resolve và chạy rules theo lens.
AI Reviewer là engine chính — logic flaws, BOLA/IDOR, business logic. Tools hỗ trợ phần pattern/CVE/secrets.
Findings Normalizer chuẩn hóa output. Risk Assessment tính score và ưu tiên.
Report Generator sinh báo cáo HTML.

Mỗi run lưu artifact: scan_context.json, resolved-rules.json, stage_outputs/, findings.json.

Layer 5 — Reporting — deliverable cho stakeholder.
Executive HTML dashboard: security health score, severity breakdown,
findings có evidence, mapping OWASP/CWE, remediation roadmap và SLA gợi ý.

PM và Tech Lead không cần đọc JSON — mở HTML trong browser.
-->

---

<!-- _class: demo small -->

## Demo — cleverdent

<div class="columns">

<div>

**Cleverdent Enterprise Dental Management Platform**

<div class="metric-hero">
<div class="metric critical"><span class="num">19</span><span class="lbl">Critical</span></div>
<div class="metric high"><span class="num">24</span><span class="lbl">High</span></div>
<div class="metric medium"><span class="num">8</span><span class="lbl">Medium</span></div>
<div class="metric grade"><span class="num">F</span><span class="lbl">Grade</span></div>
</div>

Run: `run-20260910_142645` · **51 findings**

```bash
./asrp scan --project cleverdent
asrp status --project cleverdent
```

</div>

<div>

![w:480](assets/demo-report-mockup.svg)

<span class="demo-path">cleverdent/runs/run-*/security_review_report.html</span>

</div>

</div>

**Live demo:** Overview → F-FND-001 (OIDC key) → GraphQL auth → Roadmap

<!--
SCRIPT — SLIDE 12 (DEMO) · ~7 phút — QUAN TRỌNG NHẤT

[HÀNH ĐỘNG: Mở file security_review_report.html trong browser]

Giờ demo thực tế — case study cleverdent.

── Phần A: Overview (~2 phút) ──

Đây là Cleverdent Enterprise Dental Management Platform — hệ thống quản lý nha khoa.
Hai component: dent-api-nestjs backend NestJS và dent-monorepo frontend.

Run run-20260910_142645 phát hiện 51 findings: 19 Critical, 24 High, 8 Medium.
Security Health Score Grade F — ACTION REQUIRED.

Đây là executive dashboard — PM và Tech Lead mở browser xem, không cần đọc raw JSON.

── Phần B: Filter & navigation (~1 phút) ──

[Scroll xuống phần All Findings]

Có thể filter theo Layer 2 Security Module — Standards, Domains, Rules, Checklists —
và theo component. Mỗi finding traceable về rule, domain, standard.

── Phần C: Finding 1 — Critical Secret (~2 phút) ──

[Click mở finding F-FND-001]

Finding Critical: Hardcoded OIDC RSA private signing key trong dent-api-nestjs.
File: apps/dent-login/src/config/privatekey.ts.
Domain: Secrets Management. CWE-321, OWASP A02 Cryptographic Failures.

Evidence: snippet private key ngay trong source — có thể forge OIDC token.
Remediation: chuyển signing key sang HSM hoặc secrets manager, rotate ngay.

Đây là evidence-first — không chỉ nói "có lỗi secret",
mà chỉ rõ file, dòng, snippet, và cách fix.

── Phần D: Finding 2 — Auth/Config (~1.5 phút) ──

[Scroll tới finding High về GraphQL hoặc OIDC]

Finding High: GraphQL subscriptions bypass authentication — auth.guard.ts.
Hoặc: Weak static OIDC client credentials — client secret hardcoded clever/clever.

Domain Authentication / Authorization.
AI reviewer bắt logic flaw mà static scan khó phát hiện hết.

── Phần E: Remediation Roadmap (~1.5 phút) ──

[Scroll xuống Remediation Roadmap]

Báo cáo có roadmap theo phase:
Phase 1 — Critical fix trong 24–48h.
Phase 2 — High trong 7 ngày.
Mỗi item có effort estimate và team gợi ý.

Tech Lead dùng slide này để prioritize sprint, không phải tự phân loại từ đầu.

── Tuỳ chọn: Demo CLI (~1 phút) ──

[Mở terminal nếu môi trường ổn định]
./asrp scan --project cleverdent
asrp status --project cleverdent

Nếu môi trường không ổn, bỏ qua — report đã có vẫn đủ minh họa pipeline.
-->

---

## Ai làm gì trong team?

<div class="columns-3">

<div class="card">
<h3>🛡 AppSec / Reviewer</h3>
<p>Profile dự án · human gate · triage findings</p>
</div>

<div class="card">
<h3>💻 Developer</h3>
<p>Cung cấp source · fix theo remediation</p>
</div>

<div class="card">
<h3>⚙ Platform / Tooling</h3>
<p>Rule mới · engine · scanner integration</p>
</div>

</div>

<div class="card" style="margin-top:0.6rem">

<h3>📊 PM / Tech Lead</h3>
<p>Đọc executive report · ưu tiên remediation cho sprint</p>

</div>

**Onboarding nhanh:** `cleverdent` → HTML report → 8 YAML profile

<!--
SCRIPT — SLIDE 13 (Vai trò) · ~2 phút

Không phải ai cũng cần đọc hết blueprint. Vai trò quyết định độ sâu.

AppSec / Reviewer: profile dự án, human gate validate, triage findings.

Developer: cung cấp source, fix theo remediation guidance trong report.

Platform / Tooling: thêm rule mới, mở rộng engine, tích hợp scanner.

PM / Tech Lead: đọc executive report, ưu tiên remediation cho sprint.

Onboarding nhanh: chạy cleverdent → đọc HTML report → xem 8 YAML profile
để hiểu ASRP "biết dự án" trước khi scan.
-->

---

<!-- _class: lead -->

# Q & A

### Tóm lại

1. **Profile trước · scan có lens · báo cáo có evidence**
2. Pipeline **L1–L3–L5** chạy — demo `cleverdent` (51 findings)
3. ASRP **bổ trợ**, không thay pentest

### Next Steps

1. Setup PATH → `./asrp scan --project cleverdent`
2. Đọc executive HTML report
3. Workshop **Layer 1** — profile dự án thật

`USAGE-GUIDE.md` · `ARCHITECTURE-BLUEPRINT.md`

<!--
SCRIPT — SLIDE 14 (Kết + Q&A) · ~3 phút + 10 phút Q&A

Tóm lại ba điểm chính:

Một — ASRP chuẩn hóa security review: profile trước, scan có lens, báo cáo có evidence.

Hai — Core pipeline L1–L3–L5 đã chạy, demo trên cleverdent với 51 findings và remediation roadmap.

Ba — Human gate vẫn cần; ASRP bổ trợ, không thay pentest hay security review chuyên sâu.

Next steps:
1. Setup PATH theo USAGE-GUIDE.md, chạy ./asrp scan --project cleverdent
2. Đọc executive HTML report
3. Buổi sau — nếu team đồng ý — workshop Layer 1: profile dự án thật của team

Cảm ơn mọi người. Giờ mở Q&A.

── PHỤ LỤC: Trả lời Q&A (đọc khi được hỏi) ──

Q: ASRP thay pentest?
A: Không. Bổ sung automated review có cấu trúc; pentest và manual review vẫn cần cho logic phức tạp.

Q: Khác SonarQube?
A: SonarQube là SAST đơn lẻ. ASRP orchestrate profile + lens + multi-tool + AI + report audit-ready.

Q: AI có tin được?
A: Hybrid: AI bổ sung logic flaws; mọi finding có evidence; human triage trước khi escalate.

Q: Thêm dự án mới?
A: Copy 1.1 Template → điền profile → validate → scan.

Q: Khi nào scan được?
A: Chỉ khi lifecycle_status = validated.

Q: Cleverdent Grade F có phải lỗi ASRP?
A: Không — đó là kết quả assessment thật. Report đang làm đúng việc: surface risk để team fix.
-->
