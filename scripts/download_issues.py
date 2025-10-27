"""Download GitHub data for Jupyter organizations to SQLite databases.

This script uses github-to-sqlite to fetch repository metadata, issues, pull
requests, contributors, and comments from GitHub organizations. The data is
stored in SQLite databases and published as GitHub release artifacts.

See: https://github.com/dogsheep/github-to-sqlite

Re-download Logic:
------------------
This script filters at the repository level to minimize API calls, then
github-to-sqlite handles the rest by fetching all data and replacing existing
records in the database.

1. Repositories: Downloads ALL repos in the org, but only processes those
   updated in the last year for subsequent operations. This is the main
   efficiency mechanism - inactive repos are skipped entirely.

2. Issues & PRs: For active repos, github-to-sqlite fetches ALL issues/PRs
   via the GitHub API and uses replace=True to update existing database records.
   While all data is fetched, GitHub's API pagination makes this relatively fast.
   See: https://github.com/dogsheep/github-to-sqlite/blob/main/github_to_sqlite/utils.py

3. Comments: Downloads all comments for active repositories. github-to-sqlite
   replaces existing comment records with fresh data from the API.

The script is designed to be run daily.
"""
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
    """Download contributor data for the given repositories to SQLite database."""
    repos_str = " ".join(repos)
    cmd = (
        f"github-to-sqlite contributors {db} "
        f"{repos_str}"
    )
    print(cmd)
    run(cmd.split())


def load_repos_data(db):
    """Load and filter repository list from SQLite database.

    Returns only repositories updated in the last year to avoid processing
    archived/inactive repos. This significantly reduces API calls and
    processing time for large organizations.
    """
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


def download_prs_data(org, db):
    # Get list of repositories
    repos = load_repos_data(db)

    # For each repository, download its issues
    print(f"Downloading PRs from {len(repos)} repositories...")
    for repo in track(repos):
        cmd = f"github-to-sqlite pull-requests {db} {repo}"
        print(cmd)
        run(cmd.split())
    print(f"Finished loading new PRs to {db}")


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
    
    # Get list of repositories for subsequent operations
    repos = load_repos_data(path_out)
    
    print(f"Downloading contributor data for: {org}")
    download_contributors_data(repos, path_out)

    print(f"Downloading issues for: {org}")
    download_issues_data(org, path_out)

    print(f"Downloading PRs for: {org}")
    download_prs_data(org, path_out)

    print(f"Downloading comments for: {org}")
    download_comments_data(org, path_out)


if __name__ == "__main__":
    main()
