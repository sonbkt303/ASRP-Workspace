# Hướng dẫn sử dụng: appsec-research-orchestrator

Tài liệu này dành cho **người dùng** muốn nghiên cứu chủ đề Application Security và nhận output dạng **Knowledge Base topic(s)** trong `knowledge/`.

- **Runtime (agent)**: [`../../SKILL.md`](../../SKILL.md) (cursor-agents: `skills/appsec-research-orchestrator/SKILL.md`)
- **Tên persona (SSoT)**: [`role-glossary.md`](role-glossary.md)
- **Prompt copy-paste (SSoT)**: [`prompt-template.md`](prompt-template.md)

---

## 1. Skill là gì?

Skill `appsec-research-orchestrator` do **Mr P (Professional)** điều phối. Mr P không viết KB trực tiếp mà phối hợp một “đội security” (Mr A → Mr W), mỗi người phụ trách một góc, rồi gộp thành KB topic đúng template 12 section.

**Khi nào dùng orchestrator:**

- Bạn muốn nghiên cứu topic AppSec (ví dụ: `HTTP caching`, `JWT validation`, `SSRF prevention`) và cần output có cấu trúc, evidence, threat model, failure modes, mitigations.
- Bạn muốn kiểm tra trùng lặp với `knowledge/` trước khi viết mới (One Concept = One Home).

**Khi nào dùng `kb-write-topic` thay thế:**

- Bạn đã có nội dung sẵn, chỉ cần format nhanh **một** KB topic — không cần chạy multi-role pipeline.

| Skill / mode | Khi dùng |
|--------------|----------|
| `appsec-research-orchestrator` + `batch` | KB đầy đủ trong một lần |
| `appsec-research-orchestrator` + `interactive` | Review từng Mr, hỏi/sửa giữa chừng |
| `appsec-research-orchestrator` + `qa-only` | Hỏi nhanh qua Mr QA |
| `appsec-research-orchestrator` + `single-role` | Chỉ cần output một góc (threat, failure mode, evidence…) |
| `kb-write-topic` | Viết một KB topic nhanh, không qua team |

---

## 2. Cách gọi skill

Skill có `disable-model-invocation: true` — bạn phải **invoke tường minh**, không tự kích hoạt ngầm.

**Cách 1:** Gõ `@appsec-research-orchestrator` trong Cursor chat.

**Cách 2:** Dòng đầu prompt:

```text
Use appsec-research-orchestrator (Mr P — Professional).
```

Thêm `Execution mode:` nếu không dùng batch (mặc định là `batch`).

### Trường bắt buộc (batch / interactive)

| Trường | Ví dụ |
|--------|-------|
| Research Topic | `SSRF prevention in microservices` |
| Category | `application-security` |
| Difficulty | `beginner` / `intermediate` / `advanced` |
| Tags | `ssrf, microservices, egress` |
| Status | `draft` |
| Last updated | `2026-07-17` |
| References requirement | `RFC/standards first, then OWASP` |

Nếu pre-flight tìm thấy topic trùng trong `knowledge/`, cung cấp thêm `Related` hoặc để Mr P ghi trong job plan.

---

## 3. Bốn execution mode

| Mode | Khi nào dùng | Output chính |
|------|--------------|--------------|
| `batch` (mặc định) | Muốn KB đầy đủ một lần | `SecurityResearchJob` → role stubs → KB topic(s) |
| `interactive` | Muốn review từng Mr, hỏi/sửa trước bước tiếp | Một Mr mỗi turn + `## Checkpoint` |
| `qa-only` | Hỏi khái niệm nhanh, không cần KB | `## Mr QA (Query Assistant)` |
| `single-role` | Cần một góc cụ thể | Một `### Mr X (...)` stub, không KB final |

Chi tiết protocol interactive: [`interactive-mode.md`](interactive-mode.md).

```text
Batch:       Job → [split?] → all stubs → KB
Interactive: Job → [split?] → Mr A → Checkpoint → … → Mr W → KB
Qa-only:     Mr QA answer
Single-role: One Mr stub
```

---

## 4. Đội ngũ — thành viên, chức năng, nhiệm vụ

**Mnemonic chain** (dễ nhớ): Professional → Analyst → Strategist → Hazard → Realist → Builder → Qualifier → Writer (P → A → S → H → R → B → Q → W).

| Thành viên | Chức năng | Nhiệm vụ chính | KB sections |
|------------|-----------|----------------|-------------|
| **Mr P (Professional)** | Điều phối | Pre-flight, dedup `knowledge/`, job plan, phối hợp team | — |
| **Mr A (Analyst)** | Phân tích lý thuyết | Cơ chế hoạt động, terminology; không viết controls trong phần theory | `#3`, `#4`, tối thiểu `#1–#2` |
| **Mr S (Strategist)** | Kiến trúc bảo mật | Threat model, trust boundaries, attack surface, in/out scope | `#7`, `#1` |
| **Mr H (Hazard)** | Rủi ro / lỗi | Failure modes, common mistakes — **defensive framing**, không exploit walkthrough | `#8` |
| **Mr R (Realist)** | Phản biện | Assumptions, edge cases — nơi defense có thể fail | `#7`, `#8` |
| **Mr B (Builder)** | Phòng thủ | Mitigations, best practices, verification signals | `#7`, `#9`, `#10` |
| **Mr Q (Qualifier)** | Thư viện tri thức | Evidence pack, related links, qualify claims | `#11`, `#12` |
| **Mr W (Writer)** | Biên tập | Merge stubs → KB final, dedupe, reconciliation, quality gates | `#1–#12` |
| **Mr QA (Query Assistant)** | Hỏi đáp | Giải thích stub, terminology, gợi ý `Proceed` / `Amend` | — (interactive-only) |

### Thứ tự pipeline (bắt buộc)

```text
Mr A (Analyst) → Mr S (Strategist) → Mr H (Hazard) → Mr R (Realist) → Mr B (Builder) → Mr Q (Qualifier) → Mr W (Writer)
```

**Mr QA** không nằm trong chuỗi trên — gọi on-demand tại checkpoint hoặc qua mode `qa-only`.

**Lưu ý:** Mr H chạy **trước** Mr B để mỗi item `#10` (mitigation) có thể map về `#8` (failure mode) hoặc edge case từ Mr R.

Bảng đầy đủ và quy tắc đặt tên: [`role-glossary.md`](role-glossary.md).

---

## 5. Kịch bản sử dụng

Mỗi kịch bản: **Mục tiêu** → **Prompt** (copy-paste) → **Kỳ vọng** → **Bước tiếp theo**.

Prompt đầy đủ: [`prompt-template.md`](prompt-template.md).

---

### Kịch bản 1 — Nghiên cứu topic mới, nhận KB một lần

**Mục tiêu:** Topic mới, tin tưởng pipeline, muốn full KB trong một response.

**Prompt:**

```text
Use appsec-research-orchestrator (Mr P — Professional).
Execution mode: batch.

Research Topic: HTTP cache key and Vary header correctness.
Category: web. Difficulty: intermediate. Tags: http, caching, vary.
Status: draft. Last updated: 2026-07-17.
References requirement: RFC/standards first, then OWASP.
Theory-first (70/30), but defensive must include hardening + monitoring + verification (proof signals in #9).
Check knowledge/ for duplicates before writing.
Output: SecurityResearchJob YAML first, then role stubs, then KB topic(s) (#1–#12). Output mode: propose file path.
```

**Kỳ vọng:** `## SecurityResearchJob` → `## Role outputs (internal)` (tất cả Mr) → `## KB topic(s)` với `**Proposed path**:`.

**Bước tiếp theo:** Review KB, chỉnh tay hoặc `write to knowledge/` nếu muốn ghi file.

---

### Kịch bản 2 — Topic rộng, cần confirm split trước

**Mục tiêu:** Topic span nhiều “mechanism axis”; muốn Mr P đề xuất split và bạn duyệt trước khi chạy roles.

**Prompt:** Giống batch, thêm dòng:

```text
If too broad, split into subtopics (atomic documents) and confirm split plan first.
```

**Kỳ vọng:** Job YAML có `split_confirmation.required: true` — agent **dừng** sau job plan, chưa emit stubs/KB.

**Bước tiếp theo:** Reply một trong:

```text
Approve split plan: all 3 subtopics. Proceed.
```

```text
Merge to 1 doc: <title>. Proceed.
```

---

### Kịch bản 3 — Review từng Mr, sửa giữa chừng

**Mục tiêu:** Kiểm soát từng bước; không nhận full dump một lần.

**Prompt:**

```text
Use appsec-research-orchestrator (Mr P — Professional).
Execution mode: interactive.

Research Topic: SSRF prevention in microservices.
Category: application-security. Difficulty: intermediate.
Tags: ssrf, microservices, egress.
Status: draft. Last updated: 2026-07-17.
References requirement: RFC/standards first, then OWASP.
Output mode: propose file path.
```

**Kỳ vọng:** Turn 1 = Job YAML + Mr A stub + `## Checkpoint`. Mỗi turn sau = tối đa một Mr + Checkpoint.

**Bước tiếp theo:** Reply `Proceed` để sang Mr tiếp theo.

---

### Kịch bản 4 — Hỏi Mr QA tại checkpoint

**Mục tiêu:** Làm rõ stub vừa emit hoặc terminology trước khi tiếp tục.

**Prompt:** (Trong interactive, sau khi nhận Checkpoint)

```text
Ask Mr QA: What is the difference between egress filtering and SSRF allowlists?
```

**Kỳ vọng:** `## Mr QA (Query Assistant)` + Checkpoint (**Next** role không đổi).

**Bước tiếp theo:** `Proceed` hoặc `Amend Mr X: ...` nếu cần sửa stub.

---

### Kịch bản 5 — Amend stub đã emit

**Mục tiêu:** Sửa output của một Mr; invalidate các Mr downstream cùng subtopic.

**Prompt:**

```text
Amend Mr H: Add failure mode for DNS rebinding in internal metadata access.
```

**Kỳ vọng:** Mr H stub được re-emit; stubs sau H (R, B, Q, W) bị invalidate cho subtopic đó.

**Bước tiếp theo:** `Proceed` để chạy lại từ Mr R (hoặc role tiếp theo trong job state).

---

### Kịch bản 6 — Dừng và resume sau

**Mục tiêu:** Tạm dừng giữa session; tiếp tục sau.

**Dừng:**

```text
Abort
```

**Resume (session mới):**

```text
Resume interactive
[paste hoặc reference SecurityResearchJob YAML từ turn trước]
Proceed
```

**Kỳ vọng:** Agent re-emit job YAML với `interactive` state cập nhật, tiếp từ `next_role`.

**Lưu ý:** Stubs không còn trong context = không hợp lệ — cần paste lại hoặc re-run từ role bị mất. Chi tiết: [`interactive-mode.md`](interactive-mode.md).

---

### Kịch bản 7 — Hỏi khái niệm nhanh, không KB

**Mục tiêu:** Câu hỏi AppSec đơn lẻ, không cần pipeline hay KB.

**Prompt:**

```text
Use appsec-research-orchestrator (Mr P — Professional).
Execution mode: qa-only.

Topic: HTTP cache poisoning.
Ask Mr QA: When should I use Vary: Cookie vs marking responses private?
```

**Kỳ vọng:** Chỉ `## Mr QA (Query Assistant)` — không job YAML, không stubs, không KB.

---

### Kịch bản 8 — Chỉ cần failure modes

**Mục tiêu:** Lấy góc Hazard mà không chạy full pipeline.

**Prompt:**

```text
Use appsec-research-orchestrator (Mr P — Professional).
Execution mode: single-role.

Role: Mr H (Hazard).
Topic: JWT alg confusion.
Question: List common failure modes (defensive framing only).
```

**Kỳ vọng:** `## Role outputs (internal)` với một heading `### Mr H (Hazard)`.

**Các role khác:** `Mr A (Analyst)`, `Mr S (Strategist)`, `Mr R (Realist)`, `Mr B (Builder)`, `Mr Q (Qualifier)`.

---

### Kịch bản 9 — Chỉ cần evidence pack

**Mục tiêu:** Thu thập references và qualify claims cho một topic.

**Prompt:**

```text
Use appsec-research-orchestrator (Mr P — Professional).
Execution mode: single-role.

Role: Mr Q (Qualifier).
Topic: OAuth 2.0 PKCE for public clients.
Question: List RFC/standards and OWASP references for PKCE claims; flag anything that needs evidence.
```

**Kỳ vọng:** Stub Mr Q với evidence-oriented bullets, không KB final.

---

### Kịch bản 10 — Chọn orchestrator hay kb-write-topic

| Tình huống | Chọn |
|------------|------|
| Topic mới, cần threat + failure modes + mitigations + evidence | `appsec-research-orchestrator` batch |
| Muốn review/sửa từng bước | `interactive` |
| Một câu hỏi ngắn | `qa-only` |
| Chỉ cần threat model hoặc failure modes | `single-role` |
| Đã có outline, chỉ cần format KB | `kb-write-topic` |

---

## 6. Lệnh reply trong interactive mode

Sau mỗi Checkpoint, reply **một** trong các lệnh sau:

| Lệnh | Hành vi |
|------|---------|
| `Proceed` | Chạy Mr tiếp theo |
| `Ask Mr QA: <câu hỏi>` | Mr QA trả lời; pipeline không advance |
| `Amend Mr X: <thay đổi>` | Sửa stub Mr X; invalidate downstream |
| `Skip to Mr W` | Merge stubs đã có (cảnh báo: pipeline chưa đủ) |
| `Abort` | Dừng; giữ job state để resume |

Split confirmation: `Approve split plan: ...` / `Merge to 1 doc: ...` — xem [`interactive-mode.md`](interactive-mode.md).

Ví dụ turn interactive: [`../example-interactive-turn.md`](../example-interactive-turn.md).

---

## 7. Output và chất lượng

### Output modes (giao file)

| Mode | Đề xuất path | Ghi file |
|------|--------------|----------|
| `propose file path` (mặc định) | Có (`**Proposed path**:`) | Không |
| `chat-only` | Không | Không |
| `write to knowledge/` | Có | Có (không overwrite không confirm) |

Path: `knowledge/<folder>/<kebab-case>.md` — folder = segment đầu của `category`.

Category taxonomy: ưu tiên `knowledge/README.md` của repo đích; fallback [`../knowledge-taxonomy.md`](../knowledge-taxonomy.md).

### Quality gates (tóm tắt)

- **One Concept = One Home** — dedup `knowledge/` trước khi viết; cross-link `#11`, không copy core content.
- **Evidence strictness** — `#12`: ≥2 RFC/standards + ≥1 OWASP (hoặc exception có ghi chú).
- **Defensive depth** — khi `defensive_scope` non-empty: `#9` có ≥2 verification signals.
- **Reconciliation** — mỗi item `#10` map về `#8` hoặc edge case Mr R.
- **Theory-first 70/30** — theory ở `#3`/`#4`; defensive ở `#7`–`#10`.

---

## 8. Tài liệu tham chiếu

| Tài liệu | Nội dung |
|----------|----------|
| [SKILL.md](../../SKILL.md) | Agent contract (runtime) |
| [role-glossary.md](role-glossary.md) | Tên persona (SSoT) |
| [role-output-contract.md](role-output-contract.md) | Ràng buộc từng Mr |
| [job-schema.md](job-schema.md) | Schema `SecurityResearchJob` |
| [interactive-mode.md](interactive-mode.md) | Checkpoint, resume, amend (SSoT) |
| [prompt-template.md](prompt-template.md) | Prompt copy-paste (SSoT) |
| [README.md](README.md) | Pipeline overview |
| [knowledge-taxonomy.md](../knowledge-taxonomy.md) | Domain taxonomy fallback |
| [knowledge-base-topic-template.md](../knowledge-base-topic-template.md) | Template 12 section |
