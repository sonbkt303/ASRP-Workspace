# 🛡️ ASRP CLI Quick Start Guide

## 1. Setup PATH (Chạy lệnh `asrp` ở bất kỳ đâu)
Thêm đường dẫn thư mục `ASRP Workspace` trên máy bạn vào Windows Environment Variable **Path**.

---

## 2. Bảng Lệnh CLI Nhanh

### 📦 Tiếp nhận mã nguồn (Source Acquisition):
```bash
# Trong Git Bash:
./acquire
# Trong CMD / PowerShell:
acquire

# Truyền trực tiếp đường dẫn local / git URL:
./acquire --project my-app --source "C:\Path\To\SourceCode"
```

### 🛡️ Quét & Đánh giá tự động Full Pipeline 6 bước:
```bash
# Quét dự án mẫu cleverdent (Git Bash: ./asrp | CMD: asrp):
./asrp scan --project cleverdent

# Quét trực tiếp mã nguồn local bất kỳ:
./asrp scan --project my-app --source "C:\Path\To\SourceCode"
```

### 🔎 Kiểm tra Hồ sơ & Rules:
```bash
asrp validate --project cleverdent    # Kiểm tra hợp lệ Profile Layer 1 & Human Gate
asrp rules list                       # Xem danh mục 21 Rules trong Rule Library
asrp status --project cleverdent      # Xem điểm số và đường dẫn báo cáo mới nhất
```

---

## 📄 3. Xem Báo Cáo Kết Quả
Mở tệp HTML Báo cáo Executive Dashboard sinh ra tại:  
`1. Projects Registry/{project_id}/runs/run-*/security_review_report.html` (Mở bằng Chrome/Edge/Firefox).
