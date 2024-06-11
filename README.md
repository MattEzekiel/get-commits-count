# 📊 Count Commits GitHub Action

This GitHub Action counts the total number of commits in the repository and generates a badge with the commit count. The workflow runs on a schedule, on push events to the `main` branch, on pull requests targeting the `main` branch, and when manually triggered.

## 📅 Trigger Events

The workflow is triggered by the following events:
- ⏰ Scheduled run at the beginning of each month (`cron: '0 0 1 * *'`).
- 📦 Push events to the `main` branch.
- 📥 Pull request events targeting the `main` branch.
- 🖱️ Manual workflow dispatch.
- ![Endpoint Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FMattEzekiel%2Fget-commits-count%2Fmain%2Fexample.json) ![Commits](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FMattEzekiel%2Fget-commits-count%2Fmain%2Fcommit-count-badge.json&query=message)

## ⚙️ Workflow Details

### 🏗️ Jobs

The workflow defines a single job called `count-commits` that runs on the latest Ubuntu environment (`ubuntu-latest`). This job includes the following steps:

1. **🔄 Checkout repository**
    - Uses the [actions/checkout@v2](https://github.com/actions/checkout) action to checkout the repository.

2. **🔧 Set up Node.js**
    - Uses the [actions/setup-node@v2](https://github.com/actions/setup-node) action to set up Node.js version 22.

3. **📦 Install dependencies**
    - Runs `npm install puppeteer` to install the Puppeteer library, which is used for web scraping.

4. **🔍 Run scraper and generate commit badge**
    - Runs a custom Node.js script (`scraper.js`) to count the total number of commits.
    - Creates a JSON file (`commit-count-badge.json`) with the commit count to be used as a badge.

5. **📤 Upload badge**
    - Uses the [actions/upload-artifact@v2](https://github.com/actions/upload-artifact) action to upload the `commit-count-badge.json` file as an artifact.

6. **📄 Commit and push badge update**
    - Configures Git with a user name and email.
    - Adds the `commit-count-badge.json` file to the repository.
    - Commits the changes with a message "Update commit badge".
    - Pushes the commit to the repository.

## 🔑 Environment Variables

- `GITHUB_TOKEN`: Required to authenticate with the GitHub API. This secret is automatically provided by GitHub Actions.

## 📋 Example Usage

To use this workflow in your repository, create a file named `.github/workflows/count-commits.yml` and add the following content:

```yaml
name: Count Commits

on:
  schedule:
    - cron: '0 0 1 * *'
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
  workflow_dispatch:

jobs:
  count-commits:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      # This code use Node.js
      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '22'

      - name: Install dependencies
        run: npm install puppeteer

      - name: Run scraper and generate commit badge
        id: commit-badge
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          TOTAL_COMMITS=$(node scraper.js)
          echo "Commits: $TOTAL_COMMITS"
          echo '{"schemaVersion": 1, "label": "Commits", "message": "'"$TOTAL_COMMITS"' total", "color": "blue"}' > commit-count-badge.json

      - name: Upload badge
        uses: actions/upload-artifact@v2
        with:
          name: commit-badge
          path: commit-count-badge.json

      - name: Commit and push badge update
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git status
          git add commit-count-badge.json
          git commit -m "Update commit badge"
          git push
```

Ensure you have the scraper.js script in your repository, which should contain the logic to count the commits.
