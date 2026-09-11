# Issue tables for open source projects

This repository makes GitHub issue data in the Jupyter ecosystem easier to access. It does two things:

1. Publishes issue data. A GitHub workflow runs each night, scrapes issues, pull requests, and comments from several Jupyter organizations, and publishes them as SQLite databases in a GitHub release.
2. Shows issue tables. A MyST website reads that data and shows, for each organization, the open issues sorted by community reactions (👍 and ❤️).

**🔗 View the live site:** <https://jupyter.org/github-data/>

_🚨 This is not an official Jupyter service, it is just an experiment at making issue data more useful to the community._

## Which organizations are included

The list lives in [`orgs.toml`](./orgs.toml).
To add an organization, add it there.
The next nightly run scrapes it and the site gets a page for it.

## How this works

### Collecting and publishing data

[`release.yml`](.github/workflows/release.yml) runs every night.
It reads `orgs.toml`, then runs [`scripts/download_issues.py`](scripts/download_issues.py) once per organization, in parallel.
That script uses [`github-to-sqlite`](https://github.com/dogsheep/github-to-sqlite) to write repositories, issues, pull requests, and comments into `data/<org>.db`.
The workflow then attaches every `.db` file to the [`latest` release](https://github.com/jupyter/github-data/releases/tag/latest).

To download the data yourself:

```bash
gh release download latest --repo jupyter/github-data --pattern "jupyterhub.db"
```

### Building the website

[`book.yml`](.github/workflows/book.yml) builds the site after every nightly release and on every push to `main`.

1. [`scripts/generate_pages.py`](scripts/generate_pages.py) fills in [`templates/table.md`](templates/table.md) once per organization and writes the result to `book/org/`. That folder is generated, not committed.
2. Each generated page downloads its organization's `.db` file from the latest release and renders the issue table.
3. [MyST](https://mystmd.org) builds the site and GitHub Pages hosts it.

## Local development

Preview the site with a live server:

```bash
nox -s docs-live
```

Scrape one organization yourself (needs a `GITHUB_TOKEN` environment variable):

```bash
nox -s download -- jupyter-book
```

Launch JupyterLab in the same environment, for debugging:

```bash
nox -s lab
```

## Notes for maintainers

GitHub disables scheduled workflows in repositories with no commits for 60 days.
If the `latest` release stops updating, check the Actions tab and re-enable the release workflow.

## History

This repository was originally built by [@choldgraf](https://github.com/choldgraf) before being moved to the Jupyter org so it could be used and maintained by more people.
