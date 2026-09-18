# ASRP Security Sharing — Speaker Script (đọc sẵn)

<style>
/* ── Report layout ── */
.report-meta { color: #57606a; font-size: 0.95rem; line-height: 1.6; margin: 0 0 1.25rem; }
.report-meta strong { color: #24292f; }
.deadline { color: #cf222e; font-weight: 700; }

/* ── Callouts ── */
.callout { border-left: 4px solid #0969da; background: #f6f8fa; padding: 12px 16px; margin: 1rem 0; border-radius: 0 6px 6px 0; font-size: 0.97rem; line-height: 1.55; }
.callout-success { border-left-color: #1a7f37; background: #f0fff4; }
.callout-warning { border-left-color: #bf8700; background: #fffbeb; }
.callout-danger  { border-left-color: #cf222e; background: #fff5f5; }
.callout-title   { font-weight: 700; margin-bottom: 6px; color: #24292f; }

/* ── Overall conclusion panel ── */
.conclusion-panel {
  border: 1px solid #c6e6c6;
  border-radius: 8px;
  overflow: hidden;
  margin: 1.5rem 0 2rem;
  box-shadow: 0 2px 10px rgba(26, 127, 55, 0.08);
}
.conclusion-header {
  display: flex;
  align-items: center;
  gap: 10px;
  background: linear-gradient(180deg, #1a472a 0%, #216e3a 100%);
  color: #fff;
  padding: 12px 20px;
  font-weight: 700;
  font-size: 0.92rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.conclusion-header::before {
  content: "✓";
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  background: rgba(255, 255, 255, 0.18);
  border-radius: 50%;
  font-size: 0.78rem;
  flex-shrink: 0;
}
.conclusion-body {
  background: linear-gradient(180deg, #fafffe 0%, #f6fbf7 100%);
  padding: 18px 22px;
}
.conclusion-lead {
  font-size: 1.02rem;
  line-height: 1.55;
  color: #1f2328;
  margin: 0;
}

/* ── Stats tables ── */
.stats-wrap { display: flex; flex-wrap: wrap; gap: 1.5rem; margin: 1rem 0; }
.stats-table { width: auto; font-size: 0.95rem; border-collapse: collapse; }
.stats-table th { background: #f6f8fa; font-weight: 600; text-align: left; padding: 6px 14px; border: 1px solid #d0d7de; }
.stats-table td { padding: 6px 14px; border: 1px solid #d0d7de; text-align: center; }

/* ── Global markdown tables ── */
table { border-collapse: collapse; width: 100%; font-size: 0.92rem; margin: 0.75rem 0; }
th { background: #f6f8fa; font-weight: 600; text-align: left; }
th, td { border: 1px solid #d0d7de; padding: 6px 10px; vertical-align: top; }
code { font-size: 0.88em; background: #eff1f3; padding: 1px 5px; border-radius: 4px; }

/* ── Summary / impact table ── */
.impact-table { width: 100%; table-layout: fixed; font-size: 0.78rem; line-height: 1.45; border-collapse: collapse; margin: 0.5rem 0 1.5rem; }
.impact-table th { background: #24292f; color: #fff; font-weight: 600; font-size: 0.74rem; text-transform: uppercase; letter-spacing: 0.02em; padding: 8px 6px; border: 1px solid #57606a; vertical-align: bottom; }
.impact-table td { border: 1px solid #d0d7de; padding: 7px 6px; vertical-align: top; word-wrap: break-word; overflow-wrap: anywhere; }
.impact-table tr:nth-child(even) td { background: #f6f8fa; }
.impact-table tr:hover td { background: #eef6ff; }
.impact-table .col-num     { text-align: center; font-weight: 600; color: #57606a; }
.impact-table .col-endpoint code { font-size: 0.76rem; word-break: break-all; }
.impact-table .col-cryptlex { font-size: 0.74rem; color: #424a53; }
.impact-table .col-change  { text-align: center; white-space: nowrap; }
.impact-table .col-tc      { font-size: 0.74rem; }
.impact-table .col-verdict { text-align: center; }
.impact-table .col-code    { text-align: center; }
.impact-table .col-action  { font-size: 0.74rem; }

/* ── Badges & highlights ── */
.verdict { display: inline-block; font-weight: 700; font-size: 0.80rem; padding: 2px 7px; border-radius: 10px; letter-spacing: 0.03em; }
.verdict.pass     { color: #1a7f37; background: #dafbe1; }
.verdict.fail     { color: #cf222e; background: #ffebe9; }
.verdict.skipped  { color: #9a6700; background: #fff8c5; }

.code-update { font-weight: 700; font-size: 0.86rem; }
.code-update.no       { color: #1a7f37; }
.code-update.unlikely { color: #9a6700; }
.code-update.yes      { color: #cf222e; }

.action { font-size: 0.82rem; font-weight: 600; }
.action.none    { color: #57606a; }
.action.manual  { color: #0969da; }
.action.required { color: #9a6700; }
.action.optional { color: #57606a; }

.tag-skip   { color: #9a6700; font-weight: 700; }
.tag-review { color: #0969da; font-weight: 700; }
.tag-ok     { color: #1a7f37; font-weight: 700; }
.note-detail { display: block; margin-top: 4px; font-size: 0.80rem; color: #57606a; line-height: 1.4; }
.em-dash { color: #8c959f; }

h2 { border-bottom: 1px solid #d0d7de; padding-bottom: 0.35em; margin-top: 2em; }
h3 { margin-top: 1.25em; color: #24292f; }
.section-desc { font-size: 0.95rem; color: #57606a; margin: 0 0 10px; line-height: 1.5; }
.change-box { background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 6px; padding: 12px 16px; margin: 10px 0; font-size: 0.95rem; line-height: 1.55; }
.change-box h3 { margin: 0 0 8px; font-size: 1.02rem; }
.change-box .unchanged { margin-top: 10px; padding-top: 8px; border-top: 1px dashed #d0d7de; font-size: 0.90rem; }
.impact-unknown { color: #9a6700; font-weight: 700; }
.impact-ok      { color: #1a7f37; font-weight: 700; }
.impact-break   { color: #cf222e; font-weight: 700; }

.section-header { background: linear-gradient(135deg, #24292f 0%, #424a53 100%); color: #fff; padding: 12px 18px; border-radius: 6px; margin: 2.5rem 0 1.25rem; }
.section-header h2 { color: #fff; border: none; margin: 0; padding: 0; font-size: 1.12rem; letter-spacing: 0.01em; }

/* ── Item cards (generic + test-case alias) ── */
.report-item, .test-case {
  border: 1px solid #b8c5d0;
  border-radius: 8px;
  margin: 2.25rem 0;
  padding: 0 20px 1.5rem;
  background: #fff;
  box-shadow: 0 2px 8px rgba(27, 31, 36, 0.07);
}
.report-item + .report-item, .test-case + .test-case { margin-top: 2.5rem; }
.report-item-title, .test-case-title {
  margin: 0 -20px 1.25rem !important;
  padding: 14px 20px !important;
  background: linear-gradient(180deg, #eef3f7 0%, #e2eaf0 100%);
  color: #1f2328 !important;
  border: none !important;
  border-bottom: 1px solid #c5d0da !important;
  border-left: 5px solid #3d6b8a !important;
  border-radius: 8px 8px 0 0;
  font-size: 1.06rem !important;
  line-height: 1.4;
  letter-spacing: 0.01em;
}
.item-badge, .tc-badge {
  display: inline-block;
  background: #3d6b8a;
  border: 1px solid #2f5570;
  color: #fff;
  padding: 3px 11px;
  border-radius: 4px;
  font-weight: 700;
  margin-right: 12px;
  font-size: 0.85em;
  letter-spacing: 0.05em;
  vertical-align: middle;
  box-shadow: 0 1px 2px rgba(47, 85, 112, 0.25);
}
.report-item h3, .test-case h3 {
  color: #2f3d4a;
  border-bottom: 1px solid #d8e0e8;
  padding-bottom: 0.35em;
  margin-top: 1.5rem;
  font-size: 0.97rem;
}
.report-item h4, .test-case h4 { color: #4a5866; margin-top: 1rem; font-size: 0.92rem; }

.appendix-table { font-size: 0.88rem; table-layout: fixed; width: 100%; }
.appendix-table .col-tc { width: 6%; text-align: center; font-weight: 600; }
.appendix-table .col-verdict { width: 8%; text-align: center; }

/* ── Diagram panels ── */
.diagram-panel {
  border: 1px solid #c5d0da;
  border-radius: 8px;
  background: #fafbfc;
  padding: 16px 12px 8px;
  margin: 0 0 1.25rem;
  overflow-x: auto;
}
.diagram-caption {
  font-size: 0.88rem;
  color: #57606a;
  text-align: center;
  margin: 0.75rem 0 0.5rem;
  font-style: italic;
}
.legend-table { width: 100%; font-size: 0.85rem; margin: 0; }
.legend-table td { padding: 4px 8px; border: none; vertical-align: top; }
.legend-table td:first-child { font-weight: 600; white-space: nowrap; width: 1%; color: #24292f; }

/* ── Diagram domain color accents ── */
.diagram-panel--catalog     { background: linear-gradient(180deg, #f8fbff 0%, #fafbfc 100%); border-color: #b6d4fe; border-left: 4px solid #0969da; }
.diagram-panel--blueprint   { background: linear-gradient(180deg, #faf8ff 0%, #fafbfc 100%); border-color: #d4c4f0; border-left: 4px solid #6e40c9; }
.diagram-panel--fulfillment { background: linear-gradient(180deg, #f6fffa 0%, #fafbfc 100%); border-color: #b8e6c8; border-left: 4px solid #1a7f37; }
.diagram-panel--customer    { background: linear-gradient(180deg, #fffcf5 0%, #fafbfc 100%); border-color: #f0d89a; border-left: 4px solid #bf8700; }
.diagram-panel--context     { background: linear-gradient(180deg, #f8fbff 0%, #fffcf5 100%); border-color: #c5d0da; border-left: 4px solid #3d6b8a; }
.diagram-panel--flow        { background: linear-gradient(180deg, #fafbfc 0%, #f6f8fa 100%); border-color: #c5d0da; border-left: 4px solid #424a53; }

.color-key {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 14px;
  margin: 10px 0 0;
  padding: 0;
  list-style: none;
}
.color-key li {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.82rem;
  color: #424a53;
}
.color-swatch {
  display: inline-block;
  width: 14px;
  height: 14px;
  border-radius: 3px;
  border: 1px solid rgba(27, 31, 36, 0.15);
  flex-shrink: 0;
}
.color-swatch--catalog     { background: #ddf4ff; border-color: #0969da; }
.color-swatch--blueprint   { background: #e8dfff; border-color: #6e40c9; }
.color-swatch--fulfillment { background: #dafbe1; border-color: #1a7f37; }
.color-swatch--customer    { background: #fff8c5; border-color: #bf8700; }
.color-swatch--cross       { background: repeating-linear-gradient(135deg, #f6f8fa, #f6f8fa 3px, #d0d7de 3px, #d0d7de 4px); border-color: #8c959f; }
</style>

<p class="report-meta">
  <strong>Version:</strong> 1.0 &nbsp;|&nbsp;
  <strong>Status:</strong> Ready for sharing &nbsp;|&nbsp;
  <strong>Audience:</strong> Presenter &nbsp;|&nbsp;
  <strong>Last updated:</strong> 2026-09-17 &nbsp;|&nbsp;
  <strong>Companion:</strong> <a href="architecture-overview.md">architecture-overview.md</a> · <a href="q&a.md">q&amp;a.md</a> &nbsp;|&nbsp;
  <strong>Demo:</strong> <code>cleverdent/runs/run-20260910_142645/security_review_report.html</code>
</p>

## Table of Contents

- [Executive summary](#executive-summary)
- [Section 1 — Slide scripts (S1–S14)](#section-1--slide-scripts-s1s14)
  - [S1 — Mở đầu (~2 phút)](#s1)
  - [S2 — Vấn đề (~3 phút)](#s2)
  - [S3 — Giải pháp (~2 phút)](#s3)
  - [S4 — Mental Model (~3 phút)](#s4)
  - [S5 — Nguyên tắc (~2 phút)](#s5)
  - [S6 — 6 Layer (~3 phút) — SLIDE ANCHOR](#s6)
  - [S7 — Roadmap (~1 phút)](#s7)
  - [S8 — 7 bước (~2 phút)](#s8)
  - [S9 — Layer 1 (~2 phút)](#s9)
  - [S10 — Layer 2 (~2 phút)](#s10)
  - [S11 — L3 + L5 (~2 phút)](#s11)
  - [S12 — DEMO (~7 phút) — QUAN TRỌNG NHẤT](#s12)
  - [S13 — Vai trò (~2 phút)](#s13)
  - [S14 — Kết + Q&amp;A (~3 phút + 10 phút Q&amp;A)](#s14)
- [Section 2 — Phụ lục &amp; checklist](#section-2--phụ-lục--checklist)
  - [S15 — Phụ lục Q&amp;A](#s15)
  - [S16 — Checklist trước buổi share](#s16)
- [Adversarial Self-Revision](#adversarial-self-revision)

## Executive summary

<div class="stats-wrap">
<table class="stats-table">
<thead>
<tr><th>Chỉ số</th><th>Giá trị</th></tr>
</thead>
<tbody>
<tr><td>Slides</td><td>14</td></tr>
<tr><td>Thời lượng ước tính</td><td>~35 phút + 10 phút Q&amp;A</td></tr>
<tr><td>Demo slide</td><td>S12 (~7 phút)</td></tr>
<tr><td>Case study findings</td><td>51 (19 Critical, 24 High)</td></tr>
<tr><td>Security grade</td><td>F</td></tr>
</tbody>
</table>
</div>

<div class="conclusion-panel">
<div class="conclusion-header">Script tóm tắt</div>
<div class="conclusion-body">
<p class="conclusion-lead">Bản <strong>plain text</strong> để in hoặc đọc trên điện thoại khi trình bày. Mỗi slide có script tương ứng trong HTML comment của file Marp <a href="architecture-overview.md">architecture-overview.md</a>. Demo path: <code>cleverdent/runs/run-20260910_142645/security_review_report.html</code>.</p>
</div>
</div>

<div class="change-box">
<h3>How to read this document / Cách đọc tài liệu</h3>
<p>Companion cho <a href="architecture-overview.md">architecture-overview.md</a>. Mỗi slide có script tương ứng trong HTML comment của file Marp. File này là bản <strong>plain text</strong> để in hoặc đọc trên điện thoại khi trình bày.</p>
<ul>
<li>Mỗi card <strong>S1–S14</strong> tương ứng một slide — timing gợi ý trong tiêu đề.</li>
<li><strong>S12</strong> là slide demo quan trọng nhất — mở report HTML trước khi trình bày.</li>
<li>Phụ lục Q&amp;A (S15) và checklist (S16) dùng trước/sau buổi share.</li>
</ul>
</div>

<div class="section-header" id="section-1--slide-scripts-s1s14"><h2>Section 1 — Slide scripts (S1–S14)</h2></div>

<div class="report-item" id="s1">
<h2 class="report-item-title"><span class="item-badge">S1</span> Mở đầu (~2 phút)</h2>

<p>Chào mọi người. Hôm nay t chia sẻ về <strong>ASRP — Application Security Review Platform</strong>, nền tảng đánh giá bảo mật ứng dụng theo mô hình <strong>Security Review as Code</strong>.</p>

<p>Buổi này tập trung <strong>big picture</strong>: vấn đề gì, ASRP giải quyết thế nào, kiến trúc tổng quan, và <strong>demo report thực tế</strong> trên dự án <code>cleverdent</code>. Không đi sâu YAML hay schema — phần đó để buổi workshop sau.</p>

<p>Mục tiêu: sau buổi này, mọi người biết <strong>khi nào dùng ASRP</strong>, <strong>ai làm gì</strong>, và <strong>đọc báo cáo security để ưu tiên fix</strong>.</p>
</div>

<div class="report-item" id="s2">
<h2 class="report-item-title"><span class="item-badge">S2</span> Vấn đề (~3 phút)</h2>

<p>Trước khi nói giải pháp, nhìn lại pain point team thường gặp.</p>

<p><strong>Thứ nhất:</strong> review <strong>thủ công</strong> — mỗi dự án một kiểu, chậm, khó audit lại sau vài tháng.</p>

<p><strong>Thứ hai:</strong> tool scan <strong>rời rạc</strong> — Semgrep một chỗ, dependency scanner một chỗ, secret scan một chỗ. Output khó gom, khó map chuẩn OWASP hay CWE.</p>

<p><strong>Thứ ba:</strong> hay <strong>quét mà chưa hiểu dự án</strong> — không biết tech stack, scope, component nào quan trọng → scan sai phạm vi, nhiều noise.</p>

<p><strong>Thứ tư:</strong> báo cáo gửi PM hay Tech Lead thường <strong>thiếu evidence</strong> — không chỉ rõ file, dòng code, snippet — và <strong>thiếu roadmap</strong> ưu tiên fix.</p>

<p>ASRP sinh ra để giải bốn vấn đề này.</p>
</div>

<div class="report-item" id="s3">
<h2 class="report-item-title"><span class="item-badge">S3</span> Giải pháp (~2 phút)</h2>

<p>Câu tagline của ASRP: <strong>"Biết dự án trước → quét có lens → báo cáo có căn cứ"</strong>.</p>

<p>Không scan mù. Luôn có <strong>hồ sơ dự án</strong> trước khi chạy engine.</p>

<p>Pipeline thống nhất: <strong>clone source → profile dự án → scan theo assessment lens → sinh báo cáo</strong>.</p>

<p>Platform tự hiểu tech stack, kiến trúc, scope và compliance context. Đánh giá theo chuẩn quốc tế — OWASP Top 10, API Security, ASVS, CWE — cộng rule nội bộ.</p>

<p>Output không chỉ là list lỗi. Là <strong>báo cáo audit-ready</strong>: findings có evidence, executive dashboard cho stakeholder, và remediation roadmap có SLA gợi ý.</p>
</div>

<div class="report-item" id="s4">
<h2 class="report-item-title"><span class="item-badge">S4</span> Mental Model (~3 phút)</h2>

<p>Đây là mental model cần nhớ — <strong>5 bước</strong>, mỗi bước trả lời: <strong>làm gì</strong> và <strong>để làm gì</strong>.</p>

<ul>
<li><strong>Acquire</strong> — clone repo, pin commit SHA.<br>
<em>Mục đích:</em> có <strong>source cố định</strong> — review đúng version, tái lập kết quả sau vài tháng.</li>
<li><strong>Profile</strong> — sinh hồ sơ dự án, 8 file YAML (stack, scope, <code>assessment.yaml</code>…).<br>
<em>Mục đích:</em> engine <strong>hiểu dự án</strong> trước khi scan — không quét mù, không full Application Security Verification Standard mặc định.</li>
<li><strong>Validate</strong> — AppSec review &amp; sign-off hồ sơ.<br>
<em>Mục đích:</em> <strong>human gate</strong> — chặn scan khi profile sai/thiếu; chỉ chạy khi <code>lifecycle_status = validated</code>.</li>
<li><strong>Scan</strong> — AI reviewer trọng tâm; tools (Semgrep, Trivy, Gitleaks…) hỗ trợ theo assessment lens.<br>
<em>Mục đích:</em> phát hiện lỗ hổng <strong>theo ngữ cảnh</strong> (logic flaws, BOLA/IDOR) + pattern/CVE/secrets.</li>
<li><strong>Report</strong> — chuẩn hóa findings → executive HTML dashboard.<br>
<em>Mục đích:</em> stakeholder <strong>đọc, ưu tiên fix</strong>, có evidence &amp; audit trail — không chỉ list lỗi thô.</li>
</ul>

<p><strong>Nguyên tắc:</strong> hồ sơ dự án trước, scan sau. Nhớ 5 từ: <strong>acquire, profile, validate, scan, report</strong>.</p>
</div>

<div class="report-item" id="s5">
<h2 class="report-item-title"><span class="item-badge">S5</span> Nguyên tắc (~2 phút)</h2>

<p>ASRP có <strong>5 nguyên tắc thiết kế</strong>.</p>

<p><strong>Hybrid review:</strong> AI scan là trọng tâm (~50–60%) — phân tích code theo ngữ cảnh dự án. Tools chỉ hỗ trợ (~20–30%) — secrets, CVE, pattern đã biết. Human gate và triage (~10–20%). Không thay thế hoàn toàn con người.</p>

<p><strong>Assessment lens:</strong> không quét full ASVS mặc định. Scope qua <code>assessment.yaml</code> — quét phần cần thiết, giảm noise.</p>

<p><strong>Evidence-first:</strong> mọi finding phải có evidence — file, dòng code, snippet — để audit và re-verify.</p>

<p><strong>One project = one folder:</strong> mỗi dự án là một folder, copy từ template chuẩn.</p>

<p><strong>Knowledge ≠ Rules:</strong> lý thuyết bảo mật tách khỏi rule executable. Đọc OWASP là một nơi; chạy scan là nơi khác.</p>
</div>

<div class="report-item" id="s6">
<h2 class="report-item-title"><span class="item-badge">S6</span> 6 Layer (~3 phút) — SLIDE ANCHOR</h2>

<div class="callout callout-warning">
<div class="callout-title">SLIDE ANCHOR</div>
Đây là <strong>slide anchor</strong> — bức tranh lớn cần nhớ. Mỗi layer trả lời: <strong>vai trò gì</strong> và <strong>để làm gì</strong>.
</div>

<ul>
<li><strong>L1 — Projects Registry</strong> — hồ sơ dự án, 8 file YAML.<br>
<em>Mục đích:</em> engine <strong>biết dự án</strong> trước khi scan — stack, scope, assessment lens; chỉ chạy khi <code>validated</code>.</li>
<li><strong>L2 — Security Knowledge Base</strong> — standards, domains, và <strong>Rule Library</strong> executable.<br>
<em>Mục đích:</em> biết <strong>chuẩn gì</strong> (OWASP, ASVS…) và <strong>rule nào</strong> áp dụng — tách knowledge khỏi rule chạy.</li>
<li><strong>L3 — Assessment Engine</strong> — motor trung tâm.<br>
<em>Mục đích:</em> profile + rules → <strong>findings + evidence</strong>; AI reviewer trọng tâm, tools hỗ trợ theo lens.</li>
<li><strong>L4 — Integrations</strong> — orchestrate Semgrep, Trivy, Gitleaks, CI/CD. <strong>Đang planned.</strong><br>
<em>Mục đích:</em> tools <strong>feed vào L3</strong>, normalize output — không scan rời rạc từng tool.</li>
<li><strong>L5 — Reporting</strong> — executive HTML, technical report, remediation roadmap.<br>
<em>Mục đích:</em> stakeholder <strong>đọc, ưu tiên fix</strong>, có evidence &amp; audit trail.</li>
<li><strong>L6 — Dashboard</strong> — portfolio &amp; analytics. <strong>Cũng planned.</strong><br>
<em>Mục đích:</em> nhìn <strong>cross-project</strong> — risk trends, compliance coverage.</li>
</ul>

<p>Luồng hôm nay: <strong>L1 và L2 là input, L3 là motor, L5 là output chính</strong>.</p>
</div>

<div class="report-item" id="s7">
<h2 class="report-item-title"><span class="item-badge">S7</span> Roadmap (~1 phút)</h2>

<p>Roadmap thẳng thắn — phần nào đã chạy, phần nào chưa.</p>

<p><strong>L1, L2, L3, L5 đã done</strong> — core pipeline chạy được với case study <code>cleverdent</code>.</p>

<p>Rule Library hiện có khoảng <strong>27 rules</strong>, hỗ trợ <strong>6 scanner engines</strong>: Semgrep, Gitleaks, Trivy, Checkov, CI/CD checks, và custom AI rules.</p>

<p><strong>L4 Integrations</strong> và <strong>L6 Dashboard</strong> đang planned — chưa có đầy đủ.</p>

<p>Hôm nay team <strong>có thể dùng ngay</strong>: profile dự án → validate → scan → đọc executive HTML report.</p>
</div>

<div class="report-item" id="s8">
<h2 class="report-item-title"><span class="item-badge">S8</span> 7 bước (~2 phút)</h2>

<p>Chi tiết kỹ thuật — <strong>7 bước</strong>, mỗi bước sinh artifact.</p>

<ol>
<li><strong>Acquire</strong> — clone hoặc copy source.</li>
<li><strong>Profile</strong> — sinh 8 file YAML.</li>
<li><strong>Human validate</strong> — AppSec hoặc Security Lead xác nhận profile. Chỉ khi <code>lifecycle_status = validated</code> engine mới scan.</li>
<li><strong>Resolve rules</strong> — ghép profile với Rule Library → <code>resolved-rules.json</code>.</li>
<li><strong>Scan</strong> — AI reviewer trọng tâm; tools hỗ trợ.</li>
<li><strong>Normalize</strong> — chuẩn hóa, deduplicate → <code>findings.json</code>.</li>
<li><strong>Report</strong> — sinh <code>security_review_report.html</code>.</li>
</ol>

<p>Cổng validate là <strong>bắt buộc</strong>. Engine <strong>không scan</strong> nếu profile chưa validated — tránh quét sai scope.</p>
</div>

<div class="report-item" id="s9">
<h2 class="report-item-title"><span class="item-badge">S9</span> Layer 1 (~2 phút)</h2>

<p><strong>Layer 1 — Projects Registry</strong> — trái tim của "biết dự án trước".</p>

<p>Mỗi dự án có <strong>8 file YAML</strong>: project metadata, components, technologies, architecture, scope, context, assessment, và registry manifest.</p>

<p>File quan trọng: <strong><code>technologies.yaml</code></strong> — engine biết ngôn ngữ, framework để chọn rule. <strong><code>assessment.yaml</code></strong> — định nghĩa assessment lens: quét gì, không quét gì, bật SAST/SCA/secrets/IaC hay không.</p>

<p>Lifecycle: <code>draft</code> → <code>profiled</code> → <code>validated</code> → <code>scanning</code> → <code>completed</code>.</p>

<p>Rule cứng: engine <strong>không scan</strong> khi chưa <code>validated</code>.</p>

<p>Ví dụ: <strong><code>cleverdent</code></strong> — Cleverdent Enterprise Dental Management Platform, NestJS backend + frontend monorepo, đã validated.</p>
</div>

<div class="report-item" id="s10">
<h2 class="report-item-title"><span class="item-badge">S10</span> Layer 2 (~2 phút)</h2>

<p>Slide hay gây nhầm — cần <strong>tách rõ</strong>.</p>

<p><strong>Knowledge</strong> — concept, lý thuyết — nằm ở <code>Security Knowledge Base/knowledge/</code>. Dùng tham chiếu, training, AI/RAG. Ví dụ: "SQL Injection là gì?"</p>

<p><strong>Rules</strong> — executable — nằm ở <code>ASRP/2.3 Rule Library/</code>. Pattern Semgrep, Trivy, Gitleaks. Ví dụ: <code>ASRP-INJ-001</code> — rule SQL Injection chạy trên Python, JS/TS, Go, Java.</p>

<p>Dev thêm rule mới → <strong>Rule Library</strong>. Đọc lý thuyết → <strong>Knowledge Base</strong>. Hai thứ khác nhau, không trộn.</p>
</div>

<div class="report-item" id="s11">
<h2 class="report-item-title"><span class="item-badge">S11</span> L3 + L5 (~2 phút)</h2>

<p><strong>Layer 3 — Assessment Engine</strong> — biến profile + rules thành findings + evidence.</p>

<ul>
<li><strong>Source Acquisition</strong> clone repo và pin SHA.</li>
<li><strong>Rule Evaluation</strong> resolve và chạy rules theo lens.</li>
<li><strong>AI Reviewer</strong> là engine chính — logic flaws, BOLA/IDOR, business logic. Tools hỗ trợ phần pattern/CVE/secrets.</li>
<li><strong>Findings Normalizer</strong> chuẩn hóa output.</li>
<li><strong>Risk Assessment</strong> tính score và ưu tiên.</li>
<li><strong>Report Generator</strong> sinh báo cáo HTML.</li>
</ul>

<p>Mỗi run lưu artifact: <code>scan_context.json</code>, <code>resolved-rules.json</code>, <code>stage_outputs/</code>, <code>findings.json</code>.</p>

<p><strong>Layer 5 — Reporting</strong> — deliverable cho stakeholder. Executive HTML dashboard: security health score, severity breakdown, findings có evidence, mapping OWASP/CWE, remediation roadmap và SLA gợi ý.</p>

<p>PM và Tech Lead <strong>không cần đọc JSON</strong> — mở HTML trong browser.</p>
</div>

<div class="report-item" id="s12">
<h2 class="report-item-title"><span class="item-badge">S12</span> DEMO (~7 phút) — QUAN TRỌNG NHẤT</h2>

<div class="callout callout-danger">
<div class="callout-title">Hành động</div>
Mở <code>security_review_report.html</code> trong browser.<br>
Path: <code>cleverdent/runs/run-20260910_142645/security_review_report.html</code>
</div>

<p>Giờ demo thực tế — case study <strong><code>cleverdent</code></strong>.</p>

<h3>Phần A — Overview (~2 phút)</h3>

<p>Đây là <strong>Cleverdent Enterprise Dental Management Platform</strong> — hệ thống quản lý nha khoa. Hai component: <strong><code>dent-api-nestjs</code></strong> backend NestJS và <strong><code>dent-monorepo</code></strong> frontend.</p>

<p>Run <code>run-20260910_142645</code> phát hiện <strong>51 findings</strong>: <strong>19 Critical</strong>, <strong>24 High</strong>, <strong>8 Medium</strong>. Security Health Score <strong>Grade F — ACTION REQUIRED</strong>.</p>

<p>Đây là executive dashboard — PM và Tech Lead mở browser xem, không cần đọc raw JSON.</p>

<h3>Phần B — Filter (~1 phút)</h3>

<p><em>(Scroll xuống All Findings)</em></p>

<p>Có thể filter theo <strong>Layer 2 Security Module</strong> — Standards, Domains, Rules, Checklists — và theo <strong>component</strong>. Mỗi finding traceable về rule, domain, standard.</p>

<h3>Phần C — Finding 1: Critical Secret (~2 phút)</h3>

<p><em>(Click mở F-FND-001)</em></p>

<p>Finding Critical: <strong>Hardcoded OIDC RSA private signing key</strong> trong <code>dent-api-nestjs</code>.</p>

<ul>
<li>File: <code>apps/dent-login/src/config/privatekey.ts</code></li>
<li>Domain: <strong>Secrets Management</strong></li>
<li>CWE-321, OWASP A02 Cryptographic Failures</li>
<li>Remediation: chuyển signing key sang HSM/secrets manager, <strong>rotate ngay</strong></li>
</ul>

<p>Đây là <strong>evidence-first</strong> — chỉ rõ file, dòng, snippet, và cách fix.</p>

<h3>Phần D — Finding 2: Auth (~1.5 phút)</h3>

<p><em>(Scroll tới finding High)</em></p>

<p>Finding High: <strong>GraphQL subscriptions bypass authentication</strong> — <code>auth.guard.ts</code>. Hoặc <strong>Weak static OIDC client credentials</strong> — client secret hardcoded <code>clever/clever</code>.</p>

<p>Domain <strong>Authentication / Authorization</strong>. AI reviewer bắt logic flaw mà static scan khó phát hiện hết.</p>

<h3>Phần E — Roadmap (~1.5 phút)</h3>

<p><em>(Scroll xuống Remediation Roadmap)</em></p>

<p>Roadmap theo phase: <strong>Phase 1</strong> — Critical fix 24–48h; <strong>Phase 2</strong> — High trong 7 ngày. Mỗi item có effort estimate và team gợi ý.</p>

<h3>Tuỳ chọn — CLI (~1 phút)</h3>

<pre><code>./asrp scan --project cleverdent
asrp status --project cleverdent
</code></pre>

<p>Nếu môi trường không ổn, bỏ qua — report đã có vẫn đủ minh họa.</p>
</div>

<div class="report-item" id="s13">
<h2 class="report-item-title"><span class="item-badge">S13</span> Vai trò (~2 phút)</h2>

<p>Không phải ai cũng cần đọc hết blueprint. <strong>Vai trò quyết định độ sâu.</strong></p>

<table>
<thead>
<tr><th>Vai trò</th><th>Trách nhiệm</th></tr>
</thead>
<tbody>
<tr><td>AppSec / Reviewer</td><td>Profile, human gate, triage findings</td></tr>
<tr><td>Developer</td><td>Cung cấp source, fix theo remediation</td></tr>
<tr><td>Platform / Tooling</td><td>Rule mới, engine, scanner integration</td></tr>
<tr><td>PM / Tech Lead</td><td>Đọc executive report, ưu tiên remediation</td></tr>
</tbody>
</table>

<p>Onboarding nhanh: chạy <code>cleverdent</code> → đọc HTML report → xem 8 YAML profile.</p>
</div>

<div class="report-item" id="s14">
<h2 class="report-item-title"><span class="item-badge">S14</span> Kết + Q&amp;A (~3 phút + 10 phút Q&amp;A)</h2>

<p><strong>Tóm lại ba điểm chính:</strong></p>

<ol>
<li>ASRP chuẩn hóa security review: <strong>profile trước, scan có lens, báo cáo có evidence</strong>.</li>
<li>Core pipeline L1–L3–L5 đã chạy, demo trên <code>cleverdent</code> với 51 findings và remediation roadmap.</li>
<li>Human gate vẫn cần; ASRP <strong>bổ trợ</strong>, không thay pentest hay security review chuyên sâu.</li>
</ol>

<p><strong>Next steps:</strong></p>
<ol>
<li>Setup PATH theo <code>USAGE-GUIDE.md</code>, chạy <code>./asrp scan --project cleverdent</code></li>
<li>Đọc executive HTML report</li>
<li>Buổi sau — workshop <strong>Layer 1</strong>: profile dự án thật của team</li>
</ol>

<p>Cảm ơn mọi người. Giờ mở Q&amp;A.</p>
</div>

<div class="section-header" id="section-2--phụ-lục--checklist"><h2>Section 2 — Phụ lục & checklist</h2></div>

<div class="report-item" id="s15">
<h2 class="report-item-title"><span class="item-badge">S15</span> Phụ lục — Trả lời Q&amp;A</h2>

<table class="impact-table">
<thead>
<tr><th>Câu hỏi</th><th>Trả lời</th></tr>
</thead>
<tbody>
<tr><td>ASRP thay pentest?</td><td>Không. Bổ sung automated review có cấu trúc; pentest vẫn cần.</td></tr>
<tr><td>Khác SonarQube?</td><td>SonarQube là SAST đơn lẻ. ASRP orchestrate profile + lens + multi-tool + AI + report audit-ready.</td></tr>
<tr><td>AI có tin được?</td><td>Hybrid: AI bổ sung logic flaws; mọi finding có evidence; human triage.</td></tr>
<tr><td>Thêm dự án mới?</td><td>Copy <code>1.1 Template</code> → profile → validate → scan.</td></tr>
<tr><td>Khi nào scan được?</td><td>Chỉ khi <code>lifecycle_status = validated</code>.</td></tr>
<tr><td>Cleverdent Grade F là lỗi ASRP?</td><td>Không — kết quả assessment thật. Report surface risk để team fix.</td></tr>
</tbody>
</table>

<p>Chi tiết hơn: xem <a href="q&a.md">q&amp;a.md</a>.</p>
</div>

<div class="report-item" id="s16">
<h2 class="report-item-title"><span class="item-badge">S16</span> Checklist trước buổi share</h2>

<ul>
<li>[ ] Mở Marp preview hoặc export PDF/PPTX từ <code>architecture-overview.md</code></li>
<li>[ ] Mở sẵn <code>security_review_report.html</code> trong browser</li>
<li>[ ] Bookmark findings: <strong>F-FND-001</strong> (OIDC key) và <strong>GraphQL auth bypass</strong></li>
<li>[ ] In <code>speaker-script.md</code> hoặc mở trên điện thoại</li>
<li>[ ] Test <code>./asrp status --project cleverdent</code> (fallback nếu không demo live)</li>
</ul>
</div>

## Adversarial Self-Revision
<!-- Complete after adversarial-critic challenge. -->

| Question ID | Response type | Response | Doc change |
|-------------|---------------|----------|------------|
| | Revise / Answer / ACCEPTED_RISK | | |
