"""Write one page per organization into book/org/, from templates/table.md.

The site's myst.yml picks up every file in book/org/. That folder is
generated and not committed, so run this before building the site.
"""
import tomllib
from pathlib import Path

here = Path(__file__).parent
orgs = tomllib.loads((here / ".." / "orgs.toml").read_text())["orgs"]

path_template = here / ".." / "templates" / "table.md"
text = path_template.read_text()
for org in orgs:
    text_org = text.replace("{{ org }}", org)
    path_org = here / ".." / "book" / "org" / f"{org}.md"
    path_org.parent.mkdir(parents=True, exist_ok=True)
    path_org.write_text(text_org)
print(f"Finished generating {len(orgs)} org pages...")
