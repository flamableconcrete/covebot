#!/usr/bin/python3

import json
import requests

# subreddit url to request, minimum score, title length, and our user agent
gamedeals_top = (
    "https://www.reddit.com/r/gamedeals/top.json?limit=25&t=day"  # today's top 25 posts
)
minimum_score = 200  # integer, the minimum upvotes a post must receive
max_title_length = 90  # integer, the number of characters to display
reddit_user_agent = "covebot_gamedeals:v0.1 (by online-cove.slack.com admin)"

gamedeals_webhook = (
    "https://hooks.slack.com/services/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
)
error_webhook = (
    "https://hooks.slack.com/services/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
)
found = False
try:
    headers = {"User-Agent": reddit_user_agent}
    r = requests.get(gamedeals_top, headers=headers)
    if r.status_code == requests.codes.ok:
        posts = json.loads(r.content)
        for i in range(0, len(posts["data"]["children"])):
            root = posts["data"]["children"][i]["data"]
            if root["score"] >= minimum_score:
                found = True
                link = root["permalink"]
                message = f"{root['score']}: {root['title'][:max_title_length]}\nhttps://old.reddit.com{link}"
                r = requests.post(gamedeals_webhook, json={"text": message})
                if r.ok:
                    print(f"posted okay: {link}")
                else:
                    print(f"posting problem: {r.status_code} - {r.message}")
        if not found:
            message = (
                f"Covebot: no {minimum_score}+ voted links today in r/gamedeals"
            )
            r = requests.post(error_webhook, json={"text": message})
    else:
        message = f"Covebot: Error ({r.status_code}) when retrieving gamedeals top posts :hankey:"
        r = requests.post(error_webhook, json={"text": message})
except:
    # print(f'script error: {r.content}')
    message = f"Covebot: Gamedeals Error :hankey:"
    r = requests.post(error_webhook, json={"text": message})
