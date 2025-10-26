# ❓ What is this site?

## How this works

- Every night, [this GitHub Action](https://github.com/jupyter/issue-data/blob/main/.github/workflows/release.yml) scrapes GitHub all issues information across a number of Jupyter organizations.
  - It uses the [github-to-sqlite](https://datasette.io/tools/github-to-sqlite) project to scrape issue metadata and return it in a `.sqlite` database.
  - It uses a matrix job in GitHub actions to do this for many GitHub organizations at once. Then it bundles each `.db` file into and makes a "release" with each attached. [Here's the release I update each time](https://github.com/jupyter/issue-data/releases/tag/latest).
- I then [generate a MyST site from this book](https://github.com/jupyter/issue-data/blob/main/book) that displays a sorted table for each organization.
  - In the [`templates/` folder](https://github.com/jupyter/issue-data/tree/main/templates) there'a [markdown page](https://github.com/jupyter/issue-data/blob/main/templates/table.md) meant to display the `github-to-sqlite` tables.
  - I generate one page for each GitHub organization using that template.
  - Each page downloads the `.db` file for that organization in the latest release of this repository (with the excellent [Pooch package](https://github.com/fatiando/pooch)). It then sorts the issues by the number of "👍" and "❤️" reactions, and displays the resulting table.
  - It uses the [MyST Document Engine](https://mystmd.org) to build the book in [this GitHub Action](https://github.com/jupyter/issue-data/blob/main/.github/workflows/book.yml) and hosts it online with GitHub Pages.

## Why is this interesting?

A lot of open source projects use GitHub issues for both describing and tracking interest around issues. Many users report their interest with an issue using these emojis. This is a way to quickly scan the issues that get a lot of love across an entire GitHub organization, which could help contributors identify high-value targets for development.

More generally, it's useful to have access to a lot of issue metadata for many reasons. However, it's not always easy and quick to get access to that issue data. You've got to remember the GitHub API, wait for downloads to happen, etc. This repository shows how you can easily scrape all the issues for a repository and package them in a way that they can be almost immediately downloaded.

## To preview the site locally

Download `nox`:

```bash
pip install nox
```

Run the MyST server with `nox`:

```bash
nox -s docs-live
```
