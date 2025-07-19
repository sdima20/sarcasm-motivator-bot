import json
import random

def get_random_post():
    with open("content/posts.json", "r", encoding="utf-8") as f:
        posts = json.load(f)
    return random.choice(posts)