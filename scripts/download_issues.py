from subprocess import run
import pandas as pd
import sqlite3
from rich.progress import track
from pathlib import Path
import sys

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
    query = """
        SELECT * FROM repos 
        WHERE datetime(updated_at) > datetime('now', '-1 year')
    """
    repos = df_from_sql(query, db)
    repos = repos.set_index("id")
    
    # For each repository, download its issues
    repos = repos["full_name"].tolist()
    print(f"Downloading issues from {len(repos)} repositories...")
    for repo in track(repos):
        cmd = f"github-to-sqlite issues {db} {repo}"
        print(cmd)
        run(cmd.split())
    print(f"Finished loading new issues to {db}")


def download_comments_data(org, db):
    # Load all repositories in a local DB
    cmd = f"github-to-sqlite comments {db} {org}"
    print(cmd)
    run(cmd.split())
    query = """
        SELECT * FROM repos 
        WHERE datetime(updated_at) > datetime('now', '-1 year')
    """
    repos = df_from_sql(query, db)
    repos = repos.set_index("id")
    
    # For each repository, download its issues
    repos = repos["full_name"].tolist()
    print(f"Downloading comments from {len(repos)} repositories...")
    for repo in track(repos):
        cmd = f"github-to-sqlite issue-comments {db} {repo}"
        print(cmd)
        run(cmd.split())
    print(f"Finished loading new comments to {db}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python download_issues.py <organization>")
        sys.exit(1)
    
    org = sys.argv[1]
    path_out = (here / ".." / "data" / f"{org}.db").resolve()
    print(f"Downloading to {path_out}")
    
    print(f"Downloading issues for: {org}")
    download_issues_data(org, path_out)

    print(f"Downloading comments for: {org}")
    download_comments_data(org, path_out)


if __name__ == "__main__":
    main()
