import os
from dotenv import load_dotenv
import requests
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from github import Github

load_dotenv()
# Environment variables (set these in your cloud function, CI/CD, or .env file)
GOOGLE_SHEET_ID = os.environ.get('GOOGLE_SHEET_ID')
GOOGLE_SERVICE_ACCOUNT_JSON = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')  # Path or JSON string
UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_ACCESS_KEY')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GITHUB_REPO = os.environ.get('GITHUB_REPO')  # e.g. 'username/repo'


# Google Sheets setup
def get_gsheet_client():
    if GOOGLE_SERVICE_ACCOUNT_JSON.endswith('.json'):
        creds = Credentials.from_service_account_file(GOOGLE_SERVICE_ACCOUNT_JSON, scopes=[
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive',
        ])
    else:
        import json
        creds = Credentials.from_service_account_info(json.loads(GOOGLE_SERVICE_ACCOUNT_JSON), scopes=[
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive',
        ])
    return gspread.authorize(creds)


def get_next_idea(sheet):
    rows = sheet.get_all_records()
    for idx, row in enumerate(rows, start=2):  # skip header
        if row.get('Status', '').lower() not in ['in progress', 'done']:
            return idx, row['Idea']
    return None, None


def mark_idea_status(sheet, row_idx, status):
    sheet.update_cell(row_idx, 2, status)  # 'Status' is column B


def generate_blog_content(idea):
    prompt = f"Write a detailed, engaging blog post about: {idea}. Include practical examples, tips, and a conclusion. Avoid using formal or overly academic phrases such as 'it is worth noting,' 'furthermore,' 'consequently,' 'in terms of,' 'one may argue,' 'it is imperative,' 'this suggests that,' 'thus,' 'it is evident that,' 'notwithstanding,' 'pertaining to,' 'therein lies,' 'utilize,' 'be advised,' 'hence,' 'indicate,' 'facilitate,' 'subsequently,' 'moreover,' and 'it can be seen that.'"
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama2",  # Change to your preferred local model if needed
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
    except Exception as e:
        print(f"Local LLM failed: {e}")
        raise


def fetch_image_url(query):
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_ACCESS_KEY}"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        return data['urls']['regular']
    return None


def save_draft_to_github(title, content):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(GITHUB_REPO)
    date_str = datetime.utcnow().strftime('%Y-%m-%d')
    filename = f"drafts/{date_str}-{title.replace(' ', '_')}.md"
    repo.create_file(filename, f"Add draft: {title}", content, branch="main")


def main():
    # Google Sheets
    gc = get_gsheet_client()
    sh = gc.open_by_key(GOOGLE_SHEET_ID)
    worksheet = sh.sheet1
    row_idx, idea = get_next_idea(worksheet)
    if not idea:
        print("No new ideas in the queue.")
        return 'No new ideas.'
    mark_idea_status(worksheet, row_idx, 'In Progress')
    # Generate blog
    blog_content = generate_blog_content(idea)
    # Fetch image
    image_url = fetch_image_url(idea)
    # Format markdown
    md_content = f"# {idea}\n\n![]({image_url})\n\n{blog_content}\n"
    # Save to GitHub
    save_draft_to_github(idea, md_content)
    mark_idea_status(worksheet, row_idx, 'Done')
    print(f"Draft for '{idea}' saved.")
    return f"Draft for '{idea}' saved."


if __name__ == "__main__":
    main()
