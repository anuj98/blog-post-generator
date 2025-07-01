
<div>
  <h1>Blog Generation and Deployment Automation</h1>
  <p><strong>Project Status</strong></p>
  <p>
    <img src=".github/badges/coverage.svg" alt="Coverage badge" id="coverage-badge"/>
  </p>
</div>


## Features
- Reads blog ideas from a Google Sheet (queue)
- Uses a local Ollama LLM for content generation (no paid API required)
- Fetches relevant images from Unsplash
- Saves blog drafts as Markdown files in a GitHub repository for manual review
- Marks processed ideas in the Google Sheet
- Automated publishing to Dev.to via GitHub Actions


## Starter Kit / Prerequisites

To get started, you need the following installed on your local machine:

- **Python 3.12**
- **Ollama** (for local LLM inference)
  - Install from https://ollama.com/download
  - Pull a model, e.g. `ollama pull llama2`
  - Open Command line and run `ollama run llama2`
- **pip** (Python package manager)
- **Git**

Install required Python packages:

```sh
pip install -r requirements.txt
```

You will also need:
- Google Sheets API credentials (service account JSON)
- Unsplash API key
- GitHub personal access token (for committing drafts)
- Dev.to integration token (for publishing)

## Setup
1. Set up Google Sheets API access:
   - Go to https://console.cloud.google.com/apis/library/sheets.googleapis.com and enable the Google Sheets API for your project.
   - Create a service account in the Google Cloud Console and download the JSON credentials file.
   - In your Google Sheet, click "Share" and add the service account email (from the JSON file) with Editor access.
   - Place the JSON credentials file in your project and reference it in your environment/config.
2. Obtain API keys for Unsplash.
3. Set up a GitHub repository with a personal access token for file commits.
4. Set up Dev.to integration token (see Settings > Extension > API Keys).
5. Install and run Ollama locally, and ensure the desired model is available (e.g. llama2).
6. Set up GitHub Actions for automated publishing to Dev.to.


## Blog Generation & Publishing Process

1. Blog ideas are read from a Google Sheet.
2. Blog content is generated using a local Ollama LLM.
3. Relevant images are fetched from Unsplash.
4. Drafts are saved as Markdown files in a GitHub repository for manual review.
5. When ready, a GitHub Actions workflow can be triggered to publish a selected draft to Dev.to.
6. The workflow checks out the blog repo, runs a Python script to publish the draft to Dev.to using your integration token, and prints the published URL.

## Manual Review
Drafts are saved in the repository for manual review and approval before publishing.

---

For more details, see the code and comments in the main script and the `publish_to_medium.py` file.
