# ASRP Slide Decks

Slide giới thiệu security ASRP cho team, viết bằng [Marp](https://marp.app/) (Markdown → PDF / HTML / PPTX).

**Theme:** `asrp-security` — dark security style, custom layout cards & diagrams.

## Files

| File | Mô tả | Thời lượng |
|------|-------|------------|
| [`architecture-overview.md`](architecture-overview.md) | 14 slide + **script đọc sẵn** trong Speaker Notes | ~25 phút + Q&A |
| [`speaker-script.md`](speaker-script.md) | Bản plain text để in / đọc trên điện thoại | Companion |
| [`themes/asrp-security.css`](themes/asrp-security.css) | Custom Marp theme (dark, cards, metrics) | — |
| [`assets/`](assets/) | SVG diagrams + demo mockup | — |

## Cách trình bày (đọc script)

1. Mở `architecture-overview.md` trong Cursor/VS Code
2. Cài extension **[Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)**
3. Bật **Marp Preview** (`Ctrl+Shift+P` → **Marp: Open Preview**)
4. Bật **Presenter View** để xem Speaker Notes (script đọc sẵn) bên cạnh slide
5. Hoặc in/mở `speaker-script.md` trên điện thoại khi trình bày

**Trước buổi share:** mở sẵn `cleverdent/runs/run-*/security_review_report.html` cho slide Demo (slide 12).

## Cách export PDF / PPTX

### Option 1 — VS Code / Cursor (khuyến nghị)

1. Mở `architecture-overview.md`
2. Export: `Ctrl+Shift+P` → **Marp: Export Slide Deck** → PDF, HTML, hoặc PPTX

Theme `asrp-security` được load tự động qua `.vscode/settings.json`.

### Option 2 — Marp CLI

```bash
npm install -g @marp-team/marp-cli

marp docs/slides/architecture-overview.md \
  --theme-set docs/slides/themes \
  -o docs/slides/architecture-overview.pdf

marp docs/slides/architecture-overview.md \
  --theme-set docs/slides/themes \
  -o docs/slides/architecture-overview.pptx
```

## Assets (diagrams)

| File | Dùng cho slide |
|------|----------------|
| `assets/asrp-6-layer.svg` | Slide 6 — Kiến trúc 6 Layer |
| `assets/pipeline-mental-model.svg` | Slide 4 — Mental Model |
| `assets/pipeline-7-steps.svg` | Slide 8 — Luồng 7 bước |
| `assets/demo-report-mockup.svg` | Slide 12 — Demo backup visual |

**Tip:** Thay `demo-report-mockup.svg` bằng screenshot thật từ `security_review_report.html` nếu muốn slide demo sống động hơn.

## Cấu trúc 14 slide

| # | Slide | Thời gian |
|---|-------|----------|
| 1 | Mở đầu | 2 phút |
| 2 | Vấn đề hiện tại | 3 phút |
| 3 | ASRP giải quyết gì | 2 phút |
| 4 | Mental Model (5 bước + mục đích) | 3 phút |
| 5 | Nguyên tắc thiết kế | 2 phút |
| 6 | Kiến trúc 6 Layer | 3 phút |
| 7 | Trạng thái triển khai | 1 phút |
| 8 | Luồng 7 bước | 2 phút |
| 9 | Layer 1 — Projects Registry | 2 phút |
| 10 | Layer 2 — Knowledge vs Rules | 2 phút |
| 11 | Layer 3 + Layer 5 | 2 phút |
| 12 | **Demo cleverdent** | 7 phút |
| 13 | Ai làm gì trong team | 2 phút |
| 14 | Q&A + Next Steps | 3 phút + Q&A |

## Phiên bản rút gọn (15 phút)

Nếu thiếu thời gian, trình bày slide: **1, 3, 6, 7, 8, 12, 13, 14**.
