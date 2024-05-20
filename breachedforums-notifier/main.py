import sys
from parse import parse_page
import time
import requests

if len(sys.argv) != 3:
    exit("senfou")

with open(sys.argv[1]+".last.txt") as fp:
    prev_id = int(fp.read())
next_id = prev_id

content = requests.get("https://breached.vc/Forum-"+sys.argv[1])

def post_to_embed(post):
    return {
        "title": post["title"],
        "type": "rich",
        "thumbnail": {"url": "https://breached.vc/images/default_avatar.png"},
        "author": {"name": post["author"], "link": "https://breached.vc/User-"+post["author"]},
        #"provider": {"name": "breachedforums", "link": "https://breached.vc/"},
        "description": post["posted_at"],
        "url": post["link"]
    }

ret = parse_page(content)
embeds = []
for t in ret[::-1]:
    if t["id"] > prev_id:
        embeds.append(post_to_embed(t))
        if next_id < t["id"]:
            next_id = t["id"]

for i in range(0, len(embeds), 10):
    tmp = embeds[i:i+10]
    if i:
        time.sleep(10)
    requests.post(sys.argv[2], headers={"Content-Type": "application/json"}, json={"embeds": tmp})

with open(sys.argv[1]+".last.txt", "w") as fp:
    fp.write(str(next_id))