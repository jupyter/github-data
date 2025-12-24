# Issue tables for open source projects

This repository is an attempt at making GitHub issue data in the Jupyter ecosystem more accessible and useful. It primarily does two things:

1. **Publishes issue data**. A GitHub workflow runs each day, scrapes the latest GitHub issues from a number of Jupyter sub-projects, and publishes them into a public location.
2. **Shows issue tables**. A MyST website uses this data to display tables of issue metadata, sorted by sorted by community engagement (👍 and ❤️ reactions).

**🔗 View the live site:** <https://jupyter.org/github-data/>

_🚨 This is not an official Jupyter service, it is just an experiment at making issue data more useful to the community._

## How this works

### Data collection and release workflow

1. **GitHub Workflow** (`.github/workflows/release.yml`): Runs periodically to download fresh issue data
2. **Download Script** (`scripts/download_issues.py`): Uses [`github-to-sqlite`](https://github.com/dogsheep/github-to-sqlite) to fetch issues, PRs, and comments from Jupyter organizations
3. **SQLite Database**: Stores data in `data/*.db` files
4. **GitHub Releases**: Publishes database files as release assets for public access

### Website with issue tables

1. **Page Generator** (`scripts/generate_pages.py`): Creates a page for each organization from a template
2. **MyST Markdown Book**: Pages have code cells that use the SQLite databases for subproject-specific issues, and render issue tables
3. **GitHub Pages**: Automatically builds and deploys the website on every push to `main`

## Local development

Build and preview the book locally:

```bash
nox -s docs-live
```

Launch JupyterLab in the same environment used to build the book (for debugging):

```bash
nox -s lab
```

## History

This repository was originally built by [@choldgraf](https://github.com/choldgraf) before being moved to the Jupyter org so it could be used and maintained by more people.
