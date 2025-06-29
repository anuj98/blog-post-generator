# Blog Generation and Deployment Automation

This project automates the process of generating blog posts from ideas stored in a Google Sheet, fetching relevant images, saving drafts to GitHub for review, and is designed to be deployed as a Google Cloud Function. The workflow is triggered via GitHub Actions on a 24-hour schedule.

## Features
- Reads blog ideas from a Google Sheet (queue)
- Uses a free Hugging Face Inference API for content generation
- Fetches relevant images from Unsplash
- Saves blog drafts as Markdown files in a GitHub repository for manual review
- Marks processed ideas in the Google Sheet
- Deployable as a Google Cloud Function
- Automated scheduling via GitHub Actions

## Setup
1. Configure Google Sheets API access and share the sheet with your service account.
2. Obtain API keys for Hugging Face Inference API and Unsplash.
3. Set up a GitHub repository with a personal access token for file commits.
4. Deploy the script as a Google Cloud Function.
5. Set up GitHub Actions to trigger the function every 24 hours.

## Manual Review
Drafts are saved in the repository for manual review and approval before publishing.

---

For more details, see the code and comments in the main script.
