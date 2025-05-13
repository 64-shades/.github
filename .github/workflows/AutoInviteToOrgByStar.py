#!/usr/bin/env python3
"""
Auto-invite GitHub user to organization team when they star the repo.

Author: Max Base
Sponsor: John Bampton
Date: 2025-05-09
"""

import os
import sys
import json
import requests

def log_env_info():
    print("🔍 Environment Info:")
    print("CI Environment:", "GitHub Actions" if os.getenv('CI') else "Local")
    print("Python Prefix:", sys.prefix)

def load_event_data():
    event_path = os.getenv('GITHUB_EVENT_PATH')
    if not event_path or not os.path.isfile(event_path):
        raise FileNotFoundError("GITHUB_EVENT_PATH is missing or invalid.")
    
    with open(event_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def send_github_invite(username, team_id, token):
    url = f'https://api.github.com/teams/{team_id}/memberships/{username}'
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {token}'
    }

    print(f"📨 Sending invite to @{username}...")
    response = requests.put(url, headers=headers)
    
    if response.status_code == 200:
        print("✅ User already a member.")
    elif response.status_code == 201:
        print("🎉 Invite sent successfully.")
    else:
        print(f"⚠️ Failed to send invite. Status Code: {response.status_code}")
        print(response.text)

def main():
    print("👋 Hello, GitHub Actions!")

    log_env_info()

    try:
        github_token = os.environ['MY_GITHUB_KEY']
        team_id = os.environ['COMMUNITY_TEAM_ID']
    except KeyError as e:
        print(f"❌ Missing environment variable: {e}")
        sys.exit(1)

    try:
        event_data = load_event_data()
        username = event_data['sender']['login']
        send_github_invite(username, team_id, github_token)
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
