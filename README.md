# santiwari07.github.io

Personal site of **Sanskar Tiwari (santiwari07)**: an index of my projects with one page per project.

Live at **https://santiwari07.github.io**

## How it updates itself

A GitHub Action (`.github/workflows/sync.yml`) runs every day at 07:00 IST, on every push, and on demand
from the Actions tab. It:

1. Lists my public repos and gives a page to every new one that is **not a fork** and **has a description**.
   The page uses the repo description, the first paragraphs and feature bullets of its README, its topics,
   its website link and the first screenshot in the README.
2. Rebuilds every page and the sitemap and deploys to GitHub Pages. Nothing is committed back to the repo.

So for a new project to appear: make the repo public, give it a description (and ideally topics and a
screenshot in the README). It shows up by the next morning, or straight away if you run the workflow.

## Editing by hand

- `_build/projects.json` holds the hand-written project pages. These always win over automatic ones.
  To polish an automatic page, copy its entry from `_build/auto.json` into `projects.json` and edit it.
- Add a repo name to `"ignore"` in `projects.json` to keep it off the site.
- Set `"featured": true` on a project to show it as a card at the top of the home page.

Local build: `python _build/sync.py` then `python _build/build.py` (Python 3.8+, no packages needed).
