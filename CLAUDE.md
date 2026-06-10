# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NewsHeadliner — a static news site that scrapes headlines daily at 09:00 KST via GitHub Actions and auto-deploys the result.

## Planned Stack

- **Scraper**: Python (requests + BeautifulSoup or feedparser)
- **Site**: Static HTML/CSS (no framework — keep it simple)
- **CI/CD**: GitHub Actions (cron schedule, deploy to GitHub Pages)

## Build & Run

> Commands will be added as the project is set up.

## Architecture (planned)

```
NewsHeadliner/
├── .github/workflows/      # GitHub Actions: scrape + deploy
├── scraper/                # Python scraper script
│   └── scrape.py
├── site/                   # Generated static site output
│   └── index.html
├── templates/              # HTML template(s) for site generation
└── CLAUDE.md
```

### Data flow

1. GitHub Actions cron triggers `scraper/scrape.py` at 09:00 KST daily.
2. Scraper fetches news feeds → writes `site/index.html` from a template.
3. Actions commits the updated `site/` and pushes to `gh-pages` branch (or uses `actions/deploy-pages`).
