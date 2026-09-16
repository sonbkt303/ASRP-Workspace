# ASRP Security Sharing — Speaker Script (đọc sẵn)

> Companion cho [`architecture-overview.md`](architecture-overview.md).  
> Mỗi slide có script tương ứng trong HTML comment của file Marp. File này là bản **plain text** để in hoặc đọc trên điện thoại khi trình bày.

**Demo:** mở `cleverdent/runs/run-20260910_142645/security_review_report.html`

---

## SLIDE 1 — Mở đầu (~2 phút)

Chào mọi người. Hôm nay t chia sẻ về **ASRP — Application Security Review Platform**, nền tảng đánh giá bảo mật ứng dụng theo mô hình **Security Review as Code**.

Buổi này tập trung **big picture**: vấn đề gì, ASRP giải quyết thế nào, kiến trúc tổng quan, và **demo report thực tế** trên dự án `cleverdent`. Không đi sâu YAML hay schema — phần đó để buổi workshop sau.

Mục tiêu: sau buổi này, mọi người biết **khi nào dùng ASRP**, **ai làm gì**, và **đọc báo cáo security để ưu tiên fix**.

---

## SLIDE 2 — Vấn đề (~3 phút)

Trước khi nói giải pháp, nhìn lại pain point team thường gặp.

**Thứ nhất:** review **thủ công** — mỗi dự án một kiểu, chậm, khó audit lại sau vài tháng.

**Thứ hai:** tool scan **rời rạc** — Semgrep một chỗ, dependency scanner một chỗ, secret scan một chỗ. Output khó gom, khó map chuẩn OWASP hay CWE.

**Thứ ba:** hay **quét mà chưa hiểu dự án** — không biết tech stack, scope, component nào quan trọng → scan sai phạm vi, nhiều noise.

**Thứ tư:** báo cáo gửi PM hay Tech Lead thường **thiếu evidence** — không chỉ rõ file, dòng code, snippet — và **thiếu roadmap** ưu tiên fix.

ASRP sinh ra để giải bốn vấn đề này.

---

## SLIDE 3 — Giải pháp (~2 phút)

Câu tagline của ASRP: **"Biết dự án trước → quét có lens → báo cáo có căn cứ"**.

Không scan mù. Luôn có **hồ sơ dự án** trước khi chạy engine.

Pipeline thống nhất: **clone source → profile dự án → scan theo assessment lens → sinh báo cáo**.

Platform tự hiểu tech stack, kiến trúc, scope và compliance context. Đánh giá theo chuẩn quốc tế — OWASP Top 10, API Security, ASVS, CWE — cộng rule nội bộ.

Output không chỉ là list lỗi. Là **báo cáo audit-ready**: findings có evidence, executive dashboard cho stakeholder, và remediation roadmap có SLA gợi ý.

---

## SLIDE 4 — Mental Model (~3 phút)

Đây là mental model cần nhớ — **5 bước**, mỗi bước trả lời: **làm gì** và **để làm gì**.

- **Acquire** — clone repo, pin commit SHA.  
  *Mục đích:* có **source cố định** — review đúng version, tái lập kết quả sau vài tháng.

- **Profile** — sinh hồ sơ dự án, 8 file YAML (stack, scope, `assessment.yaml`…).  
  *Mục đích:* engine **hiểu dự án** trước khi scan — không quét mù, không full ASVS mặc định.

- **Validate** — AppSec review & sign-off hồ sơ.  
  *Mục đích:* **human gate** — chặn scan khi profile sai/thiếu; chỉ chạy khi `lifecycle_status = validated`.

- **Scan** — AI reviewer trọng tâm; tools (Semgrep, Trivy, Gitleaks…) hỗ trợ theo assessment lens.  
  *Mục đích:* phát hiện lỗ hổng **theo ngữ cảnh** (logic flaws, BOLA/IDOR) + pattern/CVE/secrets.

- **Report** — chuẩn hóa findings → executive HTML dashboard.  
  *Mục đích:* stakeholder **đọc, ưu tiên fix**, có evidence & audit trail — không chỉ list lỗi thô.

**Nguyên tắc:** hồ sơ dự án trước, scan sau. Nhớ 5 từ: **acquire, profile, validate, scan, report**.

---

## SLIDE 5 — Nguyên tắc (~2 phút)

ASRP có **5 nguyên tắc thiết kế**.

**Hybrid review:** AI scan là trọng tâm (~50–60%) — phân tích code theo ngữ cảnh dự án. Tools chỉ hỗ trợ (~20–30%) — secrets, CVE, pattern đã biết. Human gate và triage (~10–20%). Không thay thế hoàn toàn con người.

**Assessment lens:** không quét full ASVS mặc định. Scope qua `assessment.yaml` — quét phần cần thiết, giảm noise.

**Evidence-first:** mọi finding phải có evidence — file, dòng code, snippet — để audit và re-verify.

**One project = one folder:** mỗi dự án là một folder, copy từ template chuẩn.

**Knowledge ≠ Rules:** lý thuyết bảo mật tách khỏi rule executable. Đọc OWASP là một nơi; chạy scan là nơi khác.

---

## SLIDE 6 — 6 Layer (~3 phút) — SLIDE ANCHOR

Đây là **slide anchor** — bức tranh lớn cần nhớ. Mỗi layer trả lời: **vai trò gì** và **để làm gì**.

- **L1 — Projects Registry** — hồ sơ dự án, 8 file YAML.  
  *Mục đích:* engine **biết dự án** trước khi scan — stack, scope, assessment lens; chỉ chạy khi `validated`.

- **L2 — Security Knowledge Base** — standards, domains, và **Rule Library** executable.  
  *Mục đích:* biết **chuẩn gì** (OWASP, ASVS…) và **rule nào** áp dụng — tách knowledge khỏi rule chạy.

- **L3 — Assessment Engine** — motor trung tâm.  
  *Mục đích:* profile + rules → **findings + evidence**; AI reviewer trọng tâm, tools hỗ trợ theo lens.

- **L4 — Integrations** — orchestrate Semgrep, Trivy, Gitleaks, CI/CD. **Đang planned.**  
  *Mục đích:* tools **feed vào L3**, normalize output — không scan rời rạc từng tool.

- **L5 — Reporting** — executive HTML, technical report, remediation roadmap.  
  *Mục đích:* stakeholder **đọc, ưu tiên fix**, có evidence & audit trail.

- **L6 — Dashboard** — portfolio & analytics. **Cũng planned.**  
  *Mục đích:* nhìn **cross-project** — risk trends, compliance coverage.

Luồng hôm nay: **L1 và L2 là input, L3 là motor, L5 là output chính**.

---

## SLIDE 7 — Roadmap (~1 phút)

Roadmap thẳng thắn — phần nào đã chạy, phần nào chưa.

**L1, L2, L3, L5 đã done** — core pipeline chạy được với case study `cleverdent`.

Rule Library hiện có khoảng **27 rules**, hỗ trợ **6 scanner engines**: Semgrep, Gitleaks, Trivy, Checkov, CI/CD checks, và custom AI rules.

**L4 Integrations** và **L6 Dashboard** đang planned — chưa có đầy đủ.

Hôm nay team **có thể dùng ngay**: profile dự án → validate → scan → đọc executive HTML report.

---

## SLIDE 8 — 7 bước (~2 phút)

Chi tiết kỹ thuật — **7 bước**, mỗi bước sinh artifact.

1. **Acquire** — clone hoặc copy source.
2. **Profile** — sinh 8 file YAML.
3. **Human validate** — AppSec hoặc Security Lead xác nhận profile. Chỉ khi `lifecycle_status = validated` engine mới scan.
4. **Resolve rules** — ghép profile với Rule Library → `resolved-rules.json`.
5. **Scan** — AI reviewer trọng tâm; tools hỗ trợ.
6. **Normalize** — chuẩn hóa, deduplicate → `findings.json`.
7. **Report** — sinh `security_review_report.html`.

Cổng validate là **bắt buộc**. Engine **không scan** nếu profile chưa validated — tránh quét sai scope.

---

## SLIDE 9 — Layer 1 (~2 phút)

**Layer 1 — Projects Registry** — trái tim của "biết dự án trước".

Mỗi dự án có **8 file YAML**: project metadata, components, technologies, architecture, scope, context, assessment, và registry manifest.

File quan trọng: **`technologies.yaml`** — engine biết ngôn ngữ, framework để chọn rule. **`assessment.yaml`** — định nghĩa assessment lens: quét gì, không quét gì, bật SAST/SCA/secrets/IaC hay không.

Lifecycle: `draft` → `profiled` → `validated` → `scanning` → `completed`.

Rule cứng: engine **không scan** khi chưa `validated`.

Ví dụ: **`cleverdent`** — Cleverdent Enterprise Dental Management Platform, NestJS backend + frontend monorepo, đã validated.

---

## SLIDE 10 — Layer 2 (~2 phút)

Slide hay gây nhầm — cần **tách rõ**.

**Knowledge** — concept, lý thuyết — nằm ở `Security Knowledge Base/knowledge/`. Dùng tham chiếu, training, AI/RAG. Ví dụ: "SQL Injection là gì?"

**Rules** — executable — nằm ở `ASRP/2.3 Rule Library/`. Pattern Semgrep, Trivy, Gitleaks. Ví dụ: `ASRP-INJ-001` — rule SQL Injection chạy trên Python, JS/TS, Go, Java.

Dev thêm rule mới → **Rule Library**. Đọc lý thuyết → **Knowledge Base**. Hai thứ khác nhau, không trộn.

---

## SLIDE 11 — L3 + L5 (~2 phút)

**Layer 3 — Assessment Engine** — biến profile + rules thành findings + evidence.

- **Source Acquisition** clone repo và pin SHA.
- **Rule Evaluation** resolve và chạy rules theo lens.
- **AI Reviewer** là engine chính — logic flaws, BOLA/IDOR, business logic. Tools hỗ trợ phần pattern/CVE/secrets.
- **Findings Normalizer** chuẩn hóa output.
- **Risk Assessment** tính score và ưu tiên.
- **Report Generator** sinh báo cáo HTML.

Mỗi run lưu artifact: `scan_context.json`, `resolved-rules.json`, `stage_outputs/`, `findings.json`.

**Layer 5 — Reporting** — deliverable cho stakeholder. Executive HTML dashboard: security health score, severity breakdown, findings có evidence, mapping OWASP/CWE, remediation roadmap và SLA gợi ý.

PM và Tech Lead **không cần đọc JSON** — mở HTML trong browser.

---

## SLIDE 12 — DEMO (~7 phút) — QUAN TRỌNG NHẤT

> **Hành động:** Mở `security_review_report.html` trong browser.

Giờ demo thực tế — case study **`cleverdent`**.

### Phần A — Overview (~2 phút)

Đây là **Cleverdent Enterprise Dental Management Platform** — hệ thống quản lý nha khoa. Hai component: **`dent-api-nestjs`** backend NestJS và **`dent-monorepo`** frontend.

Run `run-20260910_142645` phát hiện **51 findings**: **19 Critical**, **24 High**, **8 Medium**. Security Health Score **Grade F — ACTION REQUIRED**.

Đây là executive dashboard — PM và Tech Lead mở browser xem, không cần đọc raw JSON.

### Phần B — Filter (~1 phút)

*(Scroll xuống All Findings)*

Có thể filter theo **Layer 2 Security Module** — Standards, Domains, Rules, Checklists — và theo **component**. Mỗi finding traceable về rule, domain, standard.

### Phần C — Finding 1: Critical Secret (~2 phút)

*(Click mở F-FND-001)*

Finding Critical: **Hardcoded OIDC RSA private signing key** trong `dent-api-nestjs`.

- File: `apps/dent-login/src/config/privatekey.ts`
- Domain: **Secrets Management**
- CWE-321, OWASP A02 Cryptographic Failures
- Remediation: chuyển signing key sang HSM/secrets manager, **rotate ngay**

Đây là **evidence-first** — chỉ rõ file, dòng, snippet, và cách fix.

### Phần D — Finding 2: Auth (~1.5 phút)

*(Scroll tới finding High)*

Finding High: **GraphQL subscriptions bypass authentication** — `auth.guard.ts`. Hoặc **Weak static OIDC client credentials** — client secret hardcoded `clever/clever`.

Domain **Authentication / Authorization**. AI reviewer bắt logic flaw mà static scan khó phát hiện hết.

### Phần E — Roadmap (~1.5 phút)

*(Scroll xuống Remediation Roadmap)*

Roadmap theo phase: **Phase 1** — Critical fix 24–48h; **Phase 2** — High trong 7 ngày. Mỗi item có effort estimate và team gợi ý.

### Tuỳ chọn — CLI (~1 phút)

```bash
./asrp scan --project cleverdent
asrp status --project cleverdent
```

Nếu môi trường không ổn, bỏ qua — report đã có vẫn đủ minh họa.

---

## SLIDE 13 — Vai trò (~2 phút)

Không phải ai cũng cần đọc hết blueprint. **Vai trò quyết định độ sâu.**

| Vai trò | Trách nhiệm |
|---------|-------------|
| AppSec / Reviewer | Profile, human gate, triage findings |
| Developer | Cung cấp source, fix theo remediation |
| Platform / Tooling | Rule mới, engine, scanner integration |
| PM / Tech Lead | Đọc executive report, ưu tiên remediation |

Onboarding nhanh: chạy `cleverdent` → đọc HTML report → xem 8 YAML profile.

---

## SLIDE 14 — Kết + Q&A (~3 phút + 10 phút Q&A)

**Tóm lại ba điểm chính:**

1. ASRP chuẩn hóa security review: **profile trước, scan có lens, báo cáo có evidence**.
2. Core pipeline L1–L3–L5 đã chạy, demo trên `cleverdent` với 51 findings và remediation roadmap.
3. Human gate vẫn cần; ASRP **bổ trợ**, không thay pentest hay security review chuyên sâu.

**Next steps:**
1. Setup PATH theo `USAGE-GUIDE.md`, chạy `./asrp scan --project cleverdent`
2. Đọc executive HTML report
3. Buổi sau — workshop **Layer 1**: profile dự án thật của team

Cảm ơn mọi người. Giờ mở Q&A.

---

## Phụ lục — Trả lời Q&A

| Câu hỏi | Trả lời |
|---------|---------|
| ASRP thay pentest? | Không. Bổ sung automated review có cấu trúc; pentest vẫn cần. |
| Khác SonarQube? | SonarQube là SAST đơn lẻ. ASRP orchestrate profile + lens + multi-tool + AI + report audit-ready. |
| AI có tin được? | Hybrid: AI bổ sung logic flaws; mọi finding có evidence; human triage. |
| Thêm dự án mới? | Copy `1.1 Template` → profile → validate → scan. |
| Khi nào scan được? | Chỉ khi `lifecycle_status = validated`. |
| Cleverdent Grade F là lỗi ASRP? | Không — kết quả assessment thật. Report surface risk để team fix. |

---

## Checklist trước buổi share

- [ ] Mở Marp preview hoặc export PDF/PPTX từ `architecture-overview.md`
- [ ] Mở sẵn `security_review_report.html` trong browser
- [ ] Bookmark findings: **F-FND-001** (OIDC key) và **GraphQL auth bypass**
- [ ] In `speaker-script.md` hoặc mở trên điện thoại
- [ ] Test `./asrp status --project cleverdent` (fallback nếu không demo live)
