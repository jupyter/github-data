---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# {{ org }}

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
tags: [remove-cell]
---
import pandas as pd
import sqlite3
import pooch
from markdown import markdown
```

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
tags: [remove-cell]
---
org = "{{ org }}"
# If the template has been converted to pages, then org will not have { org } structure
if "{ org }" in org:
    org = "jupyter-book"
```

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
tags: [remove-cell]
---
# Download latest release data for Jupyter Book
file_path = pooch.retrieve(
    # URL to one of Pooch's test files
    url=f"https://github.com/choldgraf/os-issues/releases/download/latest/{org}.db",
    known_hash=None,
)
```

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
tags: [remove-cell]
---
def df_from_sql(query, db):
    con = sqlite3.connect(db)
    return pd.read_sql(query, con)
    con.close()
```

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
tags: [remove-cell]
---
repos = df_from_sql("SELECT * FROM repos;", file_path).set_index("id")
issues = df_from_sql("SELECT * FROM issues;", file_path)
issues = issues.query("state == 'open'")

# Add some metadata that will make the outputs nicer
for ix, irow in issues.iterrows():
    # Add number of positive reactions
    positive = 0
    for ii in ["+1", "heart", "hooray"]:
        positive += eval(irow["reactions"])[ii]
    issues.loc[ix, 'positive'] = int(positive)

    # Add the repository
    url_repo = repos.loc[irow["repo"]]["html_url"]
    url_repo_parts = url_repo.split("/")[-1]
    issues.loc[ix, "repo"] = f"[{url_repo_parts}]({url_repo})"
    
    # Add the URL of each issue
    url = f"{url_repo}/issues/{irow['number']}"
    issues.loc[ix, "mdtitle"] = f"[{irow['title']}]({url})"

# Add a short body
issues["bodyshort"] = issues["body"].map(lambda a: a.replace("#", "")[:400] if a else '')
```

+++ {"editable": true, "slideshow": {"slide_type": ""}}

A table of all the open issues in the [`jupyer-book` github organization](https://github.com/jupyter-book), sorted by the number of 👍 and ❤️ reactions.

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
tags: [remove-input]
---
issues_sorted = issues.sort_values("positive", ascending=False).head(100)[["mdtitle", "repo", "bodyshort", "positive"]]
issues_sorted = issues_sorted.rename(columns={"bodyshort": "body", "mdtitle": "title", "positive": "👍"})

def render_markdown(text):
    if isinstance(text, str): # Ensure the cell content is a string
        return markdown(text)
    return text
md_cols = ["title", "body", "repo"]
styledict = {ii: render_markdown for ii in md_cols}
df_style = issues_sorted
styled_df = issues_sorted.style.format(styledict | {"👍": int}).hide(axis="index")
styled_df
```

```{code-cell} ipython3

```
