import os
import requests


def publish_to_devto(title, md_content, devto_api_key):
    url = "https://dev.to/api/articles"
    headers = {
        "api-key": devto_api_key,
        "Content-Type": "application/json"
    }
    data = {
        "article": {
            "title": title,
            "published": True,
            "body_markdown": md_content
        }
    }
    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code in (200, 201):
        print("Published to dev.to:", resp.json().get('url'))
    else:
        print("Failed to publish to dev.to:", resp.text)


def main():
    blog_file = os.environ['BLOG_FILE']
    devto_api_key = os.environ['DEVTO_API_KEY']
    with open(blog_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    title = lines[0].lstrip('#').strip()
    md_content = ''.join(lines)
    publish_to_devto(title, md_content, devto_api_key)


if __name__ == "__main__":
    main()
