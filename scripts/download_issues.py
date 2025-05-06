from subprocess import run
import pandas as pd
import sqlite3
from rich.progress import track
from pathlib import Path

here = Path(__file__).parent

def df_from_sql(query, db):
    con = sqlite3.connect(db)
    return pd.read_sql(query, con)
    con.close()

def download_issues_data(org, db):
    # Load all repositories in a local DB
    cmd = f"github-to-sqlite repos {db} {org}"
    print(cmd)
    run(cmd.split())
    repos = df_from_sql("SELECT * FROM repos;", db)
    repos = repos.set_index("id")
    
    # For each repository, download its issues
    repos = repos["full_name"].tolist()
    print(f"Downloading issues from {len(repos)} repositories...")
    for repo in track(repos):
        cmd = f"github-to-sqlite issues {db} {repo}"
        print(cmd)
        run(cmd.split())
    print(f"Finished loading new issues to {db}")

path_out = (here / ".." / "data" / "github.db").resolve()
print(f"Downloading to {path_out}")
download_issues_data("jupyter-book", path_out)