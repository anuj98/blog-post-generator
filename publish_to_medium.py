import os
import requests

def publish_to_medium(blog_file, medium_token):
    with open(blog_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    title = lines[0].lstrip('#').strip()
    content = ''.join(lines[1:]).strip()

    headers = {
        'Authorization': f'Bearer {medium_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    user_resp = requests.get('https://api.medium.com/v1/me', headers=headers)
    user_resp.raise_for_status()
    user_id = user_resp.json()['data']['id']
    post_data = {
        'title': title,
        'contentFormat': 'markdown',
        'content': content,
        'publishStatus': 'public'
    }
    resp = requests.post(f'https://api.medium.com/v1/users/{user_id}/posts', headers=headers, json=post_data)
    resp.raise_for_status()
    print('Published to Medium:', resp.json()['data']['url'])

if __name__ == '__main__':
    blog_file = os.environ['BLOG_FILE']
    medium_token = os.environ['MEDIUM_TOKEN']
    publish_to_medium(blog_file, medium_token)
