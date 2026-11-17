"""Regenerate privacy/index.html and terms/index.html from the source Markdown.

Run from the repo root:

    pip install markdown
    python3 scripts/convert_legal.py

The source of truth is docs/legal/privacy_policy.md and terms_of_service.md
in the main onus repo (private). This script assumes that repo is checked
out as a sibling directory: ../onus relative to this repo's root.
"""
import markdown
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_REPO = os.path.join(ROOT, "..", "onus", "docs", "legal")

PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — On/Us</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<header><a class="brand" href="/">On/Us</a></header>
<main>
{body}
</main>
<footer>
<a href="/privacy">Privacy Policy</a> · <a href="/terms">Terms of Service</a> · <a href="/support">Support</a>
</footer>
</body>
</html>
"""


def convert(md_path, title, out_path):
    with open(md_path, encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r"^# .+\n", "", text, count=1)
    # python-markdown only starts a list block on a blank line before it; a
    # few source lines open a list right after a paragraph with no blank
    # line. Insert it so those bullets render as <ul>, not literal "- " text.
    # Whitespace-only: does not change any word of the legal text.
    lines = text.split("\n")
    fixed = []
    for line in lines:
        if line.startswith("- ") and fixed and fixed[-1].strip() != "" and not fixed[-1].startswith("- "):
            fixed.append("")
        fixed.append(line)
    text = "\n".join(fixed)
    body = markdown.markdown(text, extensions=["tables"])
    body = f"<h1>{title}</h1>\n" + body
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(PAGE_TEMPLATE.format(title=title, body=body))


if __name__ == "__main__":
    convert(
        os.path.join(SOURCE_REPO, "privacy_policy.md"),
        "Privacy Policy",
        os.path.join(ROOT, "privacy", "index.html"),
    )
    convert(
        os.path.join(SOURCE_REPO, "terms_of_service.md"),
        "Terms of Service",
        os.path.join(ROOT, "terms", "index.html"),
    )
    print("Regenerated privacy/index.html and terms/index.html")
