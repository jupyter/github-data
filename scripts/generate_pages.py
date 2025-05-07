from pathlib import Path
orgs = ["jupyter", "jupyterlab", "jupyter-book", "jupyter-server", "jupyterhub"]

here = Path(__file__).parent
path_template = here / ".." / "templates" / "table.md"
text = path_template.read_text()
for org in orgs:
    text_org = text.replace("{{ org }}", org)
    path_org = here / ".." / "book" / "org" / f"{org}.md"
    path_org.parent.mkdir(parents=True, exist_ok=True)
    path_org.write_text(text_org)
print(f"Finished generating {len(orgs)} org pages...")
