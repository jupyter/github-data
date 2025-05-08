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


def download_repos_data(org, db):
    """Download repository data from GitHub to SQLite database."""
    cmd = f"github-to-sqlite repos {db} {org}"
    print(cmd)
    run(cmd.split())


def download_contributors_data(repos, db):
    """Download repository data from GitHub to SQLite database."""
    cmd = f"github-to-sqlite contributors {db} {" ".join(repos)}"
    print(cmd)
    run(cmd.split())


def load_repos_data(db):
    """Load and filter repository list from SQLite database. Only if updated in the last year."""
    query = """
        SELECT * FROM repos 
        WHERE datetime(updated_at) > datetime('now', '-1 year')
    """
    repos = df_from_sql(query, db)
    repos = repos.set_index("id")
    return repos["full_name"].tolist()


def download_issues_data(org, db):
    # Get list of repositories
    repos = load_repos_data(db)
    
    # For each repository, download its issues
    print(f"Downloading issues from {len(repos)} repositories...")
    for repo in track(repos):
        cmd = f"github-to-sqlite issues {db} {repo}"
        print(cmd)
        run(cmd.split())
    print(f"Finished loading new issues to {db}")


def download_comments_data(org, db):
    # Get list of repositories
    repos = load_repos_data(db)
    
    # For each repository, download its comments
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
    
    # Download repository data once
    print(f"Downloading repository data for: {org}")
    download_repos_data(org, path_out)

    print(f"Downloading contributor data for: {org}")
    download_contributors_data(org, path_out)

    print(f"Downloading issues for: {org}")
    download_issues_data(org, path_out)

    print(f"Downloading comments for: {org}")
    download_comments_data(org, path_out)


if __name__ == "__main__":
    main()
