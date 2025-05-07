---
title: Creating a list of issue upvotes in Jupyter Book
date: "2025-05-05"
jupytext:
  formats: ipynb,md:myst
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

```{code-cell} ipython3
import pandas as pd
import sqlite3
import pooch
from markdown import markdown
```

```{code-cell} ipython3
file_path = pooch.retrieve(
    # URL to one of Pooch's test files
    url="https://github.com/choldgraf/os-issues/releases/download/latest/github.db",
    known_hash=None,
)
```

```{code-cell} ipython3
def df_from_sql(query, db):
    con = sqlite3.connect(db)
    return pd.read_sql(query, con)
    con.close()
```

```{code-cell} ipython3
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
issues["bodyshort"] = issues["body"].map(lambda a: a.replace("#", "")[:200] if a else '')
```

```{code-cell} ipython3
issues_sorted = issues.sort_values("positive", ascending=False).head(50)[["mdtitle", "repo", "bodyshort", "positive"]]

def render_markdown(text):
    if isinstance(text, str): # Ensure the cell content is a string
        return markdown(text)
    return text
md_cols = ["mdtitle", "bodyshort", "repo"]
styledict = {ii: render_markdown for ii in md_cols}
styled_df = issues_sorted.style.format(styledict | {"positive": int}).hide(axis="index")
styled_df
```
