# Security Playground OS

Repository notes inspired by a **Knowledge Graph** learning loop:

`Learn → Build → Break → Fix → Automate → Share`

## Top-level structure
- `apps/`: demo applications (web/mobile/desktop/ai).
- `labs/`: hands-on labs (networking, OS, web, application/platform/cloud/offensive/ai security, reverse engineering).
- `knowledge/`: Knowledge Base, organized by topic families:
  - `foundations/`, `networking/`, `web/`
  - `application-security/`, `platform-security/`, `cloud-security/`
  - `offensive-security/`, `secure-engineering/`, `ai-security/`
  - `research/`, `glossary/`
- `tools/`: security tools.
- `packages/`: shared libraries.
- `infrastructure/`: shared infrastructure.
- `datasets/`: payloads / samples / PCAPs.
- `automation/`: scripts & automation.
- `docs/`: repository documentation (roadmap, templates, references, research).

## Vai trò của từng thư mục
`security-playground/` là một “học theo vòng lặp” dựa trên concept graph:
`Learn → Build → Break → Fix → Automate → Share`

Mỗi thư mục có vai trò rõ ràng để đảm bảo: một khái niệm chỉ tồn tại một lần (One Concept = One Home).

- `knowledge/`: Knowledge Base. Một khái niệm chỉ tồn tại một lần (One Concept = One Home).
- `labs/`: Bài thực hành, PoC, walkthrough, CTF, môi trường kiểm thử.
- `apps/`: Ứng dụng mẫu để học và kiểm thử bảo mật.
- `tools/`: Công cụ tự viết (scanner, parser, analyzer...).
- `packages/`: Thư viện dùng chung giữa `apps/` và `tools/`.
- `infrastructure/`: Docker, Kubernetes, Terraform, Monitoring và các thành phần hạ tầng dùng chung.
- `datasets/`: Payloads, PCAP, wordlists, mẫu dữ liệu phục vụ nghiên cứu.
- `automation/`: Script build, generate docs, validate links, export...
- `docs/`: Tài liệu về chính repository (architecture, contribution, standards...).

## Cấu trúc tham chiếu
```text
security-playground/
├── knowledge/                     # Knowledge Base
│   ├── foundations/
│   ├── networking/
│   ├── web/
│   ├── application-security/
│   ├── platform-security/
│   ├── cloud-security/
│   ├── offensive-security/
│   ├── secure-engineering/
│   ├── ai-security/
│   ├── research/
│   ├── glossary/
│   ├── TAXONOMY.md
│   └── README.md
│
├── labs/                          # Hands-on Labs
│   ├── networking/
│   ├── web/
│   ├── application-security/
│   ├── platform-security/
│   ├── cloud-security/
│   ├── offensive-security/
│   └── ai-security/
│
├── apps/                          # Demo Applications
│   ├── web/
│   ├── mobile/
│   ├── desktop/
│   ├── api/
│   └── ai/
│
├── tools/                         # Security Tools
│
├── packages/                      # Shared Libraries
│
├── infrastructure/                # Shared Infrastructure
│   ├── docker/
│   ├── kubernetes/
│   ├── terraform/
│   ├── monitoring/
│   └── local/
│
├── datasets/                      # Payloads / PCAP / Wordlists
│
├── automation/                    # Scripts & Automation
│
├── docs/                          # Repository Documentation
│
├── .github/
├── .vscode/
│
├── README.md
├── ROADMAP.md
├── CONTRIBUTING.md
├── LICENSE
│
├── package.json
├── pnpm-workspace.yaml
├── turbo.json
└── tsconfig.base.json
```

## Start here
1. Read `[docs/roadmap/Application-Security-Overview.md](docs/roadmap/Application-Security-Overview.md)`.
2. Read the topic template: `[docs/KB_TOPIC_TEMPLATE.md](docs/KB_TOPIC_TEMPLATE.md)`.
3. Pick a topic in `knowledge/` (example: `knowledge/networking/tcp.md`).
4. Follow the lifecycle headings inside each topic.
