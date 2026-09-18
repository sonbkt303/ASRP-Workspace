# ASRP Security Sharing — Q&A

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
  <strong>Audience:</strong> AppSec, Developer, PM/Tech Lead &nbsp;|&nbsp;
  <strong>Last updated:</strong> 2026-09-17 &nbsp;|&nbsp;
  <strong>Companion:</strong> <a href="architecture-overview.md">architecture-overview.md</a> · <a href="speaker-script.md">speaker-script.md</a> &nbsp;|&nbsp;
  <strong>Case study:</strong> <code>cleverdent</code> — 51 findings (19 Critical, 24 High, Grade F) &nbsp;|&nbsp;
  <strong>Tham chiếu:</strong> <a href="../../Application%20Security%20Review%20Platform%20(ASRP)/ARCHITECTURE-BLUEPRINT.md">ARCHITECTURE-BLUEPRINT.md</a> · <a href="../../USAGE-GUIDE.md">USAGE-GUIDE.md</a>
</p>

## Table of Contents

- [Executive summary](#executive-summary)
- [Section 1 — Tổng quan ASRP](#section-1--tổng-quan-asrp)
  - [Q1 — ASRP là gì?](#q1)
  - [Q2 — ASRP giải quyết vấn đề gì?](#q2)
  - [Q3 — ASRP thay pentest không?](#q3)
  - [Q4 — ASRP khác SonarQube / SAST đơn lẻ thế nào?](#q4)
  - [Q5 — Ai nên dùng ASRP?](#q5)
- [Section 2 — Công cụ scan & chuẩn phân loại](#section-2--công-cụ-scan--chuẩn-phân-loại)
  - [Q6 — Semgrep là gì?](#q6)
  - [Q7 — SCA là gì?](#q7)
  - [Q8 — Secrets scan là gì?](#q8)
  - [Q9 — Semgrep, SCA, Secrets bổ sung nhau thế nào?](#q9)
  - [Q10 — OWASP là gì?](#q10)
  - [Q11 — CWE là gì?](#q11)
  - [Q12 — Quan hệ giữa tool scan và OWASP/CWE?](#q12)
  - [Q13 — Tại sao chạy tool rời rạc là vấn đề?](#q13)
  - [Q14 — ASRP giải quyết vấn đề tool rời rạc như thế nào?](#q14)
- [Section 3 — Kiến trúc & pipeline](#section-3--kiến-trúc--pipeline)
  - [Q15 — Mental Model 5 bước là gì?](#q15)
  - [Q16 — 6 Layer ASRP là gì?](#q16)
  - [Q17 — Knowledge và Rules khác nhau thế nào?](#q17)
  - [Q18 — Hybrid review trong ASRP là gì?](#q18)
  - [Q19 — Assessment lens là gì?](#q19)
  - [Q20 — Layer 4 (Integrations) đã chạy chưa?](#q20)
- [Section 4 — Sử dụng thực tế](#section-4--sử-dụng-thực-tế)
  - [Q21 — Thêm dự án mới vào ASRP?](#q21)
  - [Q22 — Khi nào được scan?](#q22)
  - [Q23 — File YAML quan trọng nhất là gì?](#q23)
  - [Q24 — Làm sao chạy scan trên cleverdent?](#q24)
  - [Q25 — Mỗi run scan lưu artifact gì?](#q25)
  - [Q26 — Cleverdent Grade F có phải lỗi ASRP?](#q26)
- [Section 5 — AI & độ tin cậy](#section-5--ai--độ-tin-cậy)
  - [Q27 — AI reviewer có tin được không?](#q27)
  - [Q28 — AI reviewer bắt được gì mà Semgrep không bắt?](#q28)
- [Section 6 — Báo cáo & output](#section-6--báo-cáo--output)
  - [Q29 — Báo cáo ASRP khác list lỗi thông thường thế nào?](#q29)
  - [Q30 — Evidence-first nghĩa là gì?](#q30)
- [Section 7 — Roadmap & trạng thái hiện tại](#section-7--roadmap--trạng-thái-hiện-tại)
  - [Q31 — ASRP đã chạy được gì?](#q31)
  - [Q32 — Phần nào chưa có?](#q32)
  - [Q33 — Next steps sau buổi share?](#q33)
- [Section 8 — Câu hỏi nhanh](#section-8--câu-hỏi-nhanh)
- [Adversarial Self-Revision](#adversarial-self-revision)

## Executive summary

<div class="stats-wrap">
<table class="stats-table">
<thead>
<tr><th>Chỉ số</th><th>Giá trị</th></tr>
</thead>
<tbody>
<tr><td>Sections Q&amp;A</td><td>8</td></tr>
<tr><td>Câu hỏi chi tiết</td><td>33</td></tr>
<tr><td>Layers ASRP</td><td>6</td></tr>
<tr><td>Rule Library</td><td>27 rules</td></tr>
<tr><td>Scanner engines</td><td>6</td></tr>
<tr><td>Case study findings</td><td>51</td></tr>
<tr><td>Critical / High</td><td>19 / 24</td></tr>
<tr><td>Security grade</td><td>F</td></tr>
</tbody>
</table>
</div>

<div class="conclusion-panel">
<div class="conclusion-header">Tóm tắt Q&amp;A</div>
<div class="conclusion-body">
<p class="conclusion-lead">Tài liệu này tổng hợp <strong>33 câu hỏi thường gặp</strong> khi giới thiệu ASRP — từ tổng quan platform, công cụ scan, kiến trúc 6 layer, đến sử dụng thực tế và roadmap. Dùng khi trình bày hoặc trả lời sau buổi share; tham chiếu case study <code>cleverdent</code> (51 findings, Grade F) và slide deck <a href="architecture-overview.md">architecture-overview.md</a>.</p>
</div>
</div>

<div class="change-box">
<h3>How to read this document / Cách đọc tài liệu</h3>
<p>Tổng hợp câu hỏi thường gặp khi giới thiệu ASRP — dùng khi trình bày hoặc trả lời sau buổi share.</p>
<ul>
<li>Mỗi câu hỏi nằm trong card <strong>Q1–Q33</strong> — tra cứu nhanh theo badge hoặc mục lục.</li>
<li>Mục 8 là <strong>bảng tra cứu nhanh</strong> — dùng khi cần trả lời ngắn trong Q&amp;A session.</li>
<li>Companion: <a href="architecture-overview.md">Slide deck</a> · <a href="speaker-script.md">Speaker script</a>.</li>
</ul>
</div>

<div class="section-header" id="section-1--tổng-quan-asrp"><h2>Section 1 — Tổng quan ASRP</h2></div>

<div class="report-item" id="q1">
<h2 class="report-item-title"><span class="item-badge">Q1</span> ASRP là gì?</h2>

<p><strong>ASRP (Application Security Review Platform)</strong> là nền tảng đánh giá bảo mật ứng dụng theo mô hình <strong>Security Review as Code</strong>. Tagline: <strong>"Biết dự án trước → quét có lens → báo cáo có căn cứ"</strong>.</p>

<p>Pipeline thống nhất: clone source → profile dự án → scan theo assessment lens → sinh báo cáo audit-ready (findings có evidence, mapping OWASP/CWE, remediation roadmap).</p>
</div>

<div class="report-item" id="q2">
<h2 class="report-item-title"><span class="item-badge">Q2</span> ASRP giải quyết vấn đề gì?</h2>

<p>Bốn pain point phổ biến:</p>

<ol>
<li><strong>Review thủ công</strong> — mỗi dự án một kiểu, chậm, khó audit lại sau vài tháng.</li>
<li><strong>Tool scan rời rạc</strong> — Semgrep, SCA, secret scan chạy riêng; output khó gom, khó map OWASP/CWE.</li>
<li><strong>Quét mà chưa hiểu dự án</strong> — không biết stack, scope → scan sai phạm vi, nhiều noise.</li>
<li><strong>Báo cáo yếu</strong> — thiếu evidence (file, dòng, snippet) và roadmap ưu tiên fix.</li>
</ol>
</div>

<div class="report-item" id="q3">
<h2 class="report-item-title"><span class="item-badge">Q3</span> ASRP thay pentest không?</h2>

<div class="callout callout-warning">
<div class="callout-title">Không</div>
ASRP bổ sung automated review có cấu trúc. Pentest và manual review vẫn cần cho logic phức tạp, business flow, và kiểm thử runtime.
</div>
</div>

<div class="report-item" id="q4">
<h2 class="report-item-title"><span class="item-badge">Q4</span> ASRP khác SonarQube / SAST đơn lẻ thế nào?</h2>

<p>SonarQube là <strong>SAST đơn lẻ</strong> — quét code theo rule tĩnh. ASRP <strong>orchestrate</strong> toàn bộ quy trình:</p>

<ul>
<li>Profile dự án trước khi scan (L1)</li>
<li>Assessment lens — không quét full ASVS mặc định</li>
<li>Multi-tool + AI reviewer + normalize output (L3)</li>
<li>Báo cáo audit-ready với OWASP/CWE mapping (L5)</li>
</ul>
</div>

<div class="report-item" id="q5">
<h2 class="report-item-title"><span class="item-badge">Q5</span> Ai nên dùng ASRP?</h2>

<table>
<thead>
<tr><th>Vai trò</th><th>Làm gì với ASRP</th></tr>
</thead>
<tbody>
<tr><td><strong>AppSec / Reviewer</strong></td><td>Profile dự án, human gate validate, triage findings</td></tr>
<tr><td><strong>Developer</strong></td><td>Cung cấp source, fix theo remediation roadmap</td></tr>
<tr><td><strong>Platform / Tooling</strong></td><td>Thêm rule mới, mở rộng engine, tích hợp scanner</td></tr>
<tr><td><strong>PM / Tech Lead</strong></td><td>Đọc executive report, ưu tiên remediation cho sprint</td></tr>
</tbody>
</table>
</div>

<div class="section-header" id="section-2--công-cụ-scan--chuẩn-phân-loại"><h2>Section 2 — Công cụ scan & chuẩn phân loại</h2></div>

<div class="report-item" id="q6">
<h2 class="report-item-title"><span class="item-badge">Q6</span> Semgrep là gì?</h2>

<p><strong>Semgrep</strong> là công cụ <strong>SAST</strong> (Static Application Security Testing) — quét <strong>source code</strong> tìm pattern lỗ hổng đã biết: SQL injection, hardcoded secret, unsafe API call, v.v.</p>

<p>Trong ASRP: Semgrep là một trong các <strong>scanner engines hỗ trợ</strong> (~20–30%), chạy theo rule trong Rule Library (ví dụ <code>ASRP-INJ-001</code>).</p>
</div>

<div class="report-item" id="q7">
<h2 class="report-item-title"><span class="item-badge">Q7</span> SCA là gì?</h2>

<p><strong>SCA (Software Composition Analysis)</strong> quét <strong>thư viện/phụ thuộc</strong> (npm, pip, Maven…) tìm <strong>CVE</strong> đã biết trong package bên thứ ba.</p>

<p>Trong ASRP: dùng <strong>Trivy</strong> — rule <code>ASRP-SCA-001</code> trong domain <code>dependencies/</code>.</p>
</div>

<div class="report-item" id="q8">
<h2 class="report-item-title"><span class="item-badge">Q8</span> Secrets scan là gì?</h2>

<p>Quét repository tìm <strong>credential bị lộ</strong>: API key, password, token commit nhầm vào Git.</p>

<p>Trong ASRP: dùng <strong>Gitleaks</strong> — một trong 6 scanner engines hỗ trợ.</p>
</div>

<div class="report-item" id="q9">
<h2 class="report-item-title"><span class="item-badge">Q9</span> Semgrep, SCA, Secrets bổ sung nhau thế nào?</h2>

<table>
<thead>
<tr><th>Loại</th><th>Bắt lỗi ở đâu</th></tr>
</thead>
<tbody>
<tr><td><strong>Semgrep (SAST)</strong></td><td>Code tự viết — logic, pattern nguy hiểm</td></tr>
<tr><td><strong>SCA (Trivy)</strong></td><td>Package bên thứ ba — CVE đã biết</td></tr>
<tr><td><strong>Secrets (Gitleaks)</strong></td><td>Credential lộ trong repo</td></tr>
</tbody>
</table>

<p>Ba loại bổ sung nhau; ASRP gom output của cả ba vào một <code>findings.json</code> chuẩn hóa.</p>
</div>

<div class="report-item" id="q10">
<h2 class="report-item-title"><span class="item-badge">Q10</span> OWASP là gì?</h2>

<p><strong>OWASP</strong> là bộ <strong>chuẩn/tài liệu</strong> phân loại rủi ro bảo mật ứng dụng — dùng để nói chung ngôn ngữ với team, PM, audit.</p>

<p>Ví dụ trong ASRP:</p>

<ul>
<li>OWASP Top 10 (A01–A10)</li>
<li>OWASP API Security Top 10</li>
<li>OWASP ASVS (Application Security Verification Standard)</li>
</ul>
</div>

<div class="report-item" id="q11">
<h2 class="report-item-title"><span class="item-badge">Q11</span> CWE là gì?</h2>

<p><strong>CWE (Common Weakness Enumeration)</strong> là <strong>danh mục chi tiết</strong> loại lỗ hổng phần mềm — mỗi weakness có ID riêng.</p>

<p>Ví dụ:</p>

<ul>
<li><code>CWE-798</code> — Use of Hard-coded Credentials</li>
<li><code>CWE-321</code> — Use of Hard-coded Cryptographic Key</li>
</ul>
</div>

<div class="report-item" id="q12">
<h2 class="report-item-title"><span class="item-badge">Q12</span> Quan hệ giữa tool scan và OWASP/CWE?</h2>

<ul>
<li><strong>Tool</strong> báo: <em>"tìm thấy lỗi X tại file Y"</em></li>
<li><strong>OWASP/CWE</strong> trả lời: <em>"lỗi này thuộc loại gì, nghiêm trọng theo chuẩn nào"</em></li>
</ul>

<p>Ví dụ từ demo <code>cleverdent</code>:</p>

<ul>
<li>Finding: OIDC signing key hardcoded</li>
<li>Map: <strong>CWE-321</strong> + <strong>OWASP A02</strong> (Cryptographic Failures)</li>
</ul>
</div>

<div class="report-item" id="q13">
<h2 class="report-item-title"><span class="item-badge">Q13</span> Tại sao chạy tool rời rạc là vấn đề?</h2>

<p>Khi chạy từng tool riêng:</p>

<pre><code>Semgrep  →  report A (format riêng)
Trivy    →  report B (CVE list)
Gitleaks →  report C (secret hits)
</code></pre>

<p>Hệ quả: khó gom, khó map OWASP/CWE, quét mù (nhiều false positive), báo cáo thiếu evidence.</p>
</div>

<div class="report-item" id="q14">
<h2 class="report-item-title"><span class="item-badge">Q14</span> ASRP giải quyết vấn đề tool rời rạc như thế nào?</h2>

<p>ASRP <strong>không thay thế</strong> Semgrep/SCA/Secrets — mà <strong>gom, chuẩn hóa và đặt vào ngữ cảnh dự án</strong>:</p>

<ol>
<li><strong>L1</strong> — profile dự án trước (<code>technologies.yaml</code>, <code>assessment.yaml</code>) → chỉ chạy rule phù hợp</li>
<li><strong>L2</strong> — rule executable đã map OWASP/CWE sẵn trong Rule Library</li>
<li><strong>L3</strong> — AI reviewer trọng tâm + tools feed vào engine → <code>findings_normalizer</code> merge &amp; dedupe</li>
<li><strong>L5</strong> — báo cáo thống nhất với evidence + OWASP/CWE mapping + remediation roadmap</li>
</ol>
</div>

<div class="section-header" id="section-3--kiến-trúc--pipeline"><h2>Section 3 — Kiến trúc & pipeline</h2></div>

<div class="report-item" id="q15">
<h2 class="report-item-title"><span class="item-badge">Q15</span> Mental Model 5 bước là gì?</h2>

<table>
<thead>
<tr><th>Bước</th><th>Làm gì</th><th>Mục đích</th></tr>
</thead>
<tbody>
<tr><td><strong>Acquire</strong></td><td>Clone repo, pin commit SHA</td><td>Source cố định — tái lập kết quả</td></tr>
<tr><td><strong>Profile</strong></td><td>Sinh 8 file YAML</td><td>Engine hiểu dự án trước khi scan</td></tr>
<tr><td><strong>Validate</strong></td><td>AppSec review &amp; sign-off</td><td>Human gate — chỉ scan khi <code>validated</code></td></tr>
<tr><td><strong>Scan</strong></td><td>AI reviewer + tools theo lens</td><td>Phát hiện lỗ hổng theo ngữ cảnh</td></tr>
<tr><td><strong>Report</strong></td><td>Chuẩn hóa findings → HTML</td><td>Stakeholder đọc, ưu tiên fix, có audit trail</td></tr>
</tbody>
</table>
</div>

<div class="report-item" id="q16">
<h2 class="report-item-title"><span class="item-badge">Q16</span> 6 Layer ASRP là gì?</h2>

<table>
<thead>
<tr><th>Layer</th><th>Vai trò</th><th>Trạng thái</th></tr>
</thead>
<tbody>
<tr><td><strong>L1</strong> Projects Registry</td><td>Hồ sơ dự án — 8 YAML profile</td><td>Done</td></tr>
<tr><td><strong>L2</strong> Knowledge Base</td><td>Standards + Rule Library executable</td><td>Done</td></tr>
<tr><td><strong>L3</strong> Assessment Engine</td><td>Motor trung tâm — findings + evidence</td><td>Done</td></tr>
<tr><td><strong>L4</strong> Integrations</td><td>Orchestrate Semgrep, Trivy, Gitleaks, CI/CD</td><td>Planned</td></tr>
<tr><td><strong>L5</strong> Reporting</td><td>Executive HTML, technical report, roadmap</td><td>Done</td></tr>
<tr><td><strong>L6</strong> Dashboard</td><td>Portfolio &amp; analytics cross-project</td><td>Planned</td></tr>
</tbody>
</table>

<p>Luồng core hôm nay: <strong>L1 + L2 (input) → L3 (motor) → L5 (output)</strong>.</p>
</div>

<div class="report-item" id="q17">
<h2 class="report-item-title"><span class="item-badge">Q17</span> Knowledge và Rules khác nhau thế nào?</h2>

<table>
<thead>
<tr><th></th><th>Knowledge</th><th>Rules</th></tr>
</thead>
<tbody>
<tr><td><strong>Là gì</strong></td><td>Concept, lý thuyết</td><td>Executable — chạy scan</td></tr>
<tr><td><strong>Vị trí</strong></td><td><code>Security Knowledge Base/knowledge/</code></td><td><code>ASRP/2.3 Rule Library/</code></td></tr>
<tr><td><strong>Dùng để</strong></td><td>Tham chiếu, training, AI/RAG</td><td>Pattern Semgrep, Trivy, Gitleaks</td></tr>
<tr><td><strong>Ví dụ</strong></td><td>"SQL Injection là gì?"</td><td><code>ASRP-INJ-001</code> — rule chạy trên Python, JS/TS</td></tr>
</tbody>
</table>

<p><strong>Nguyên tắc:</strong> Đọc OWASP là một nơi; chạy scan là nơi khác.</p>
</div>

<div class="report-item" id="q18">
<h2 class="report-item-title"><span class="item-badge">Q18</span> Hybrid review trong ASRP là gì?</h2>

<table>
<thead>
<tr><th>Thành phần</th><th>Tỷ trọng</th><th>Vai trò</th></tr>
</thead>
<tbody>
<tr><td><strong>AI reviewer</strong></td><td>~50–60%</td><td>Phân tích code theo ngữ cảnh — logic flaws, BOLA/IDOR, business logic</td></tr>
<tr><td><strong>Tools</strong></td><td>~20–30%</td><td>Hỗ trợ — secrets, CVE, pattern đã biết (Semgrep, Trivy, Gitleaks…)</td></tr>
<tr><td><strong>Human gate</strong></td><td>~10–20%</td><td>Validate profile, triage findings — không thay thế hoàn toàn con người</td></tr>
</tbody>
</table>
</div>

<div class="report-item" id="q19">
<h2 class="report-item-title"><span class="item-badge">Q19</span> Assessment lens là gì?</h2>

<p>Không quét <strong>full ASVS mặc định</strong>. Scope được định nghĩa qua <code>assessment.yaml</code> — quét phần cần thiết, giảm noise.</p>

<p>Ví dụ: bật/tắt SAST, SCA, secrets, IaC theo từng dự án.</p>
</div>

<div class="report-item" id="q20">
<h2 class="report-item-title"><span class="item-badge">Q20</span> Layer 4 (Integrations) đã chạy chưa?</h2>

<p><strong>Chưa — đang planned.</strong> Hiện tại tools có thể chạy qua Rule Library và engine, nhưng orchestration CI/CD đầy đủ (L4) vẫn trong roadmap.</p>
</div>

<div class="section-header" id="section-4--sử-dụng-thực-tế"><h2>Section 4 — Sử dụng thực tế</h2></div>

<div class="report-item" id="q21">
<h2 class="report-item-title"><span class="item-badge">Q21</span> Thêm dự án mới vào ASRP?</h2>

<ol>
<li>Copy <code>1. Projects Registry/1.1 Template/</code> → folder dự án mới</li>
<li>Điền 8 file YAML profile (stack, scope, assessment lens…)</li>
<li>AppSec validate → <code>lifecycle_status = validated</code></li>
<li>Chạy <code>./asrp scan --project {project_id}</code></li>
</ol>
</div>

<div class="report-item" id="q22">
<h2 class="report-item-title"><span class="item-badge">Q22</span> Khi nào được scan?</h2>

<div class="callout callout-warning">
<div class="callout-title">Chỉ khi <code>lifecycle_status = validated</code></div>
Lifecycle: <code>draft</code> → <code>profiled</code> → <strong><code>validated</code></strong> → <code>scanning</code> → <code>completed</code>
</div>

<p>Engine <strong>không scan</strong> nếu profile chưa validated — tránh quét sai scope.</p>
</div>

<div class="report-item" id="q23">
<h2 class="report-item-title"><span class="item-badge">Q23</span> File YAML quan trọng nhất là gì?</h2>

<ul>
<li><strong><code>technologies.yaml</code></strong> — engine biết ngôn ngữ, framework để chọn rule</li>
<li><strong><code>assessment.yaml</code></strong> — định nghĩa assessment lens: quét gì, không quét gì, bật SAST/SCA/secrets/IaC hay không</li>
</ul>
</div>

<div class="report-item" id="q24">
<h2 class="report-item-title"><span class="item-badge">Q24</span> Làm sao chạy scan trên cleverdent?</h2>

<pre><code>./asrp scan --project cleverdent
</code></pre>

<p>Sau scan, đọc report tại:</p>

<pre><code>cleverdent/runs/run-*/security_review_report.html
</code></pre>
</div>

<div class="report-item" id="q25">
<h2 class="report-item-title"><span class="item-badge">Q25</span> Mỗi run scan lưu artifact gì?</h2>

<ul>
<li><code>scan_context.json</code> — AI pre-flight context</li>
<li><code>resolved-rules.json</code> — rule set sau filtering</li>
<li><code>stage_outputs/</code> — 12 catalog-driven stage JSON</li>
<li><code>findings.json</code> — findings đã dedupe, chuẩn hóa</li>
</ul>
</div>

<div class="report-item" id="q26">
<h2 class="report-item-title"><span class="item-badge">Q26</span> Cleverdent Grade F có phải lỗi ASRP?</h2>

<div class="callout callout-success">
<div class="callout-title">Không</div>
Đó là kết quả assessment thật trên codebase <code>cleverdent</code>. Report đang làm đúng việc: surface risk để team fix.
</div>

<p>Demo <code>cleverdent</code> có <strong>51 findings</strong> — ví dụ nổi bật:</p>

<ul>
<li><strong>F-FND-001</strong> — OIDC signing key hardcoded (CWE-321, OWASP A02)</li>
<li>GraphQL auth bypass — logic flaw mà static scan khó phát hiện hết</li>
</ul>
</div>

<div class="section-header" id="section-5--ai--độ-tin-cậy"><h2>Section 5 — AI & độ tin cậy</h2></div>

<div class="report-item" id="q27">
<h2 class="report-item-title"><span class="item-badge">Q27</span> AI reviewer có tin được không?</h2>

<p><strong>Hybrid model</strong> — không tin AI 100%:</p>

<ul>
<li>AI bổ sung phần tools không cover (logic flaws, BOLA/IDOR)</li>
<li>Mọi finding <strong>phải có evidence</strong> (file, dòng, snippet)</li>
<li><strong>Human triage</strong> trước khi escalate — AppSec xác nhận finding quan trọng</li>
</ul>
</div>

<div class="report-item" id="q28">
<h2 class="report-item-title"><span class="item-badge">Q28</span> AI reviewer bắt được gì mà Semgrep không bắt?</h2>

<p>Logic flaws theo ngữ cảnh dự án:</p>

<ul>
<li>BOLA / IDOR (Broken Object Level Authorization)</li>
<li>GraphQL auth bypass</li>
<li>Business logic flaws</li>
<li>Misconfiguration theo kiến trúc cụ thể</li>
</ul>

<p>Semgrep tốt ở <strong>pattern đã biết</strong>; AI tốt ở <strong>ngữ cảnh và luồng logic</strong>.</p>
</div>

<div class="section-header" id="section-6--báo-cáo--output"><h2>Section 6 — Báo cáo & output</h2></div>

<div class="report-item" id="q29">
<h2 class="report-item-title"><span class="item-badge">Q29</span> Báo cáo ASRP khác list lỗi thông thường thế nào?</h2>

<table>
<thead>
<tr><th>Thông thường</th><th>ASRP</th></tr>
</thead>
<tbody>
<tr><td>List lỗi thô</td><td>Findings có <strong>evidence</strong> (file, dòng, snippet)</td></tr>
<tr><td>Không map chuẩn</td><td><strong>OWASP / CWE mapping</strong> trên từng finding</td></tr>
<tr><td>Không biết fix gì trước</td><td><strong>Remediation roadmap</strong> + SLA gợi ý</td></tr>
<tr><td>Khó đọc cho PM</td><td><strong>Executive HTML dashboard</strong> — security health score, severity breakdown</td></tr>
</tbody>
</table>
</div>

<div class="report-item" id="q30">
<h2 class="report-item-title"><span class="item-badge">Q30</span> Evidence-first nghĩa là gì?</h2>

<p>Mọi finding phải có evidence cụ thể — file path, line number, code snippet — để:</p>

<ul>
<li>Audit và re-verify</li>
<li>Developer biết chính xác chỗ cần fix</li>
<li>Không escalate finding không có căn cứ</li>
</ul>
</div>

<div class="section-header" id="section-7--roadmap--trạng-thái-hiện-tại"><h2>Section 7 — Roadmap & trạng thái hiện tại</h2></div>

<div class="report-item" id="q31">
<h2 class="report-item-title"><span class="item-badge">Q31</span> ASRP đã chạy được gì?</h2>

<p><strong>L1, L2, L3, L5 — Done.</strong> Core pipeline chạy được với case study <code>cleverdent</code>.</p>

<p>Rule Library hiện có khoảng <strong>27 rules</strong>, hỗ trợ <strong>6 scanner engines</strong>: Semgrep, Gitleaks, Trivy, Checkov, CI/CD checks, và custom AI rules.</p>
</div>

<div class="report-item" id="q32">
<h2 class="report-item-title"><span class="item-badge">Q32</span> Phần nào chưa có?</h2>

<ul>
<li><strong>L4 Integrations</strong> — orchestrate tools + CI/CD đầy đủ</li>
<li><strong>L6 Dashboard</strong> — portfolio view, risk trends cross-project</li>
</ul>
</div>

<div class="report-item" id="q33">
<h2 class="report-item-title"><span class="item-badge">Q33</span> Next steps sau buổi share?</h2>

<ol>
<li>Setup PATH theo <code>USAGE-GUIDE.md</code>, chạy <code>./asrp scan --project cleverdent</code></li>
<li>Đọc executive HTML report</li>
<li>Workshop <strong>Layer 1</strong> — profile dự án thật của team</li>
</ol>
</div>

<div class="section-header" id="section-8--câu-hỏi-nhanh"><h2>Section 8 — Câu hỏi nhanh</h2></div>

<div class="report-item" id="quick-ref">
<h2 class="report-item-title"><span class="item-badge">REF</span> Bảng tra cứu nhanh</h2>

<table class="impact-table">
<thead>
<tr><th>Câu hỏi</th><th>Trả lời ngắn</th></tr>
</thead>
<tbody>
<tr><td>ASRP thay pentest?</td><td>Không — bổ sung automated review có cấu trúc</td></tr>
<tr><td>Khác SonarQube?</td><td>ASRP orchestrate profile + lens + multi-tool + AI + report</td></tr>
<tr><td>AI tin được?</td><td>Hybrid: evidence-first + human triage</td></tr>
<tr><td>Thêm dự án mới?</td><td>Copy <code>1.1 Template</code> → profile → validate → scan</td></tr>
<tr><td>Khi nào scan được?</td><td>Chỉ khi <code>lifecycle_status = validated</code></td></tr>
<tr><td>Cleverdent Grade F?</td><td>Kết quả assessment thật, không phải lỗi ASRP</td></tr>
<tr><td>Semgrep vs SCA vs Secrets?</td><td>SAST code / CVE package / credential lộ — ASRP gom cả ba</td></tr>
<tr><td>OWASP vs CWE?</td><td>Chuẩn phân loại rủi ro / danh mục weakness chi tiết</td></tr>
<tr><td>AI hay tool quan trọng hơn?</td><td>AI ~50–60% trọng tâm; tools ~20–30% hỗ trợ</td></tr>
</tbody>
</table>
</div>

## Adversarial Self-Revision
<!-- Complete after adversarial-critic challenge. -->

| Question ID | Response type | Response | Doc change |
|-------------|---------------|----------|------------|
| | Revise / Answer / ACCEPTED_RISK | | |
