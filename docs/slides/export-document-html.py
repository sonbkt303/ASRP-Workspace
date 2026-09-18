#!/usr/bin/env python3
"""Export document-style markdown companions to standalone HTML."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import markdown

SLIDES_DIR = Path(__file__).resolve().parent
CSS_PATH = SLIDES_DIR / "themes" / "document-style.css"
STYLE_BLOCK = re.compile(r"<style>.*?</style>\s*", re.DOTALL | re.IGNORECASE)
LINK_TAG = re.compile(
    r'<link\s+rel="stylesheet"\s+href="themes/document-style\.css"\s*/>\s*',
    re.IGNORECASE,
)


def export(md_path: Path) -> Path:
    text = md_path.read_text(encoding="utf-8")
    body = STYLE_BLOCK.sub("", text)
    body = LINK_TAG.sub("", body)

    title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else md_path.stem

    html_body = markdown.markdown(
        body,
        extensions=["extra", "tables", "sane_lists", "nl2br"],
    )

    css = CSS_PATH.read_text(encoding="utf-8")
    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
{css}
  </style>
</head>
<body class="document-style">
<article>
{html_body}
</article>
</body>
</html>
"""

    out_path = md_path.with_suffix(".html")
    out_path.write_text(html, encoding="utf-8")
    return out_path


def main() -> int:
    targets = sys.argv[1:] or ["q&a.md", "speaker-script.md"]
    for name in targets:
        md_path = SLIDES_DIR / name
        if not md_path.exists():
            print(f"skip: {md_path} not found", file=sys.stderr)
            continue
        out = export(md_path)
        print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
