# ❓ What is this site?

## How this works

Every night a GitHub workflow scrapes the issues, pull requests, and comments from several Jupyter organizations and publishes them as SQLite databases in a [GitHub release](https://github.com/jupyter/github-data/releases/tag/latest).
This site reads those databases and shows, for each organization, the open issues sorted by "👍" and "❤️" reactions.

The [repository README](https://github.com/jupyter/github-data#how-this-works) describes the workflows, the scripts, and how to build the site locally.

## Why is this interesting?

A lot of open source projects use GitHub issues for both describing and tracking interest around issues. Many users report their interest with an issue using these emojis. This is a way to quickly scan the issues that get a lot of love across an entire GitHub organization, which could help contributors identify high-value targets for development.

More generally, it's useful to have access to a lot of issue metadata for many reasons. However, it's not always easy and quick to get access to that issue data. You've got to remember the GitHub API, wait for downloads to happen, etc. This repository shows how you can easily scrape all the issues for a repository and package them in a way that they can be almost immediately downloaded.

## History of this project

This was originally created by [`@choldgraf`](https://github.com/choldgraf), as part of [2i2c's work to better-support upstream projects](https://2i2c.org/blog/2025/foundational-contributions/). It was donated to Jupyter in October 2025 so that the community could collectively maintain and improve this.
