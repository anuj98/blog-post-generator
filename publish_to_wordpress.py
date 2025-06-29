import os
import markdown as mdlib
import requests

def markdown_to_html(md_content):
    return mdlib.markdown(md_content)

def publish_to_wordpress(title, md_content, wp_access_token, wp_site_id):
    html_content = markdown_to_html(md_content)
    url = f"https://public-api.wordpress.com/rest/v1.1/sites/{wp_site_id}/posts/new"
    headers = {
        "Authorization": f"Bearer {wp_access_token}"
    }
    data = {
        "title": title,
        "content": html_content,
        "status": "publish"
    }
    resp = requests.post(url, headers=headers, data=data)
    if resp.status_code == 201:
        print("Published to WordPress:", resp.json().get('URL'))
    else:
        print("Failed to publish to WordPress:", resp.text)

def main():
    blog_file = os.environ['BLOG_FILE']
    wp_access_token = os.environ['WP_ACCESS_TOKEN']
    wp_site_id = os.environ['WP_SITE_ID']
    with open(blog_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    title = lines[0].lstrip('#').strip()
    md_content = ''.join(lines)
    publish_to_wordpress(title, md_content, wp_access_token, wp_site_id)

if __name__ == "__main__":
    main()
