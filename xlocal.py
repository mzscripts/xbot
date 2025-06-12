import tweepy
import json
import os
from dotenv import load_dotenv
import requests
import random
from urllib.parse import quote
from pathlib import Path

# === Setup ===
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# Authenticate for v1.1 API (for media upload)
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api_v1 = tweepy.API(auth)

# Initialize Tweepy client for v2 API (for tweeting)
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Test authentication
try:
    user = client.get_me()
    print(f"✅ Authenticated as: {user.data.username}")
except tweepy.TweepyException as e:
    print(f"❌ Authentication failed: {e}")
    exit(1)

# === Prepare image directory ===
IMG_DIR = "img"
Path(IMG_DIR).mkdir(parents=True, exist_ok=True)

# === Load and pick 1 random prompt ===
try:
    with open("girl.json", "r", encoding="utf-8") as f:
        prompts = json.load(f)
        selected_prompt = random.choice(prompts)
except FileNotFoundError:
    print("❌ prompts.json not found.")
    exit(1)
except ValueError:
    print("❌ No prompts available.")
    exit(1)

# === Process the selected prompt ===
prompt_id = selected_prompt["prompt_id"]
description = selected_prompt["description"]
tweet_text = f"{description}"

if len(tweet_text) > 280:
    tweet_text = tweet_text[:277] + "..."

print(f"📤 Processing prompt {prompt_id}: {description[:50]}...")

# === Image generation ===
try:
    encoded_prompt = quote(description)
    image_url = f"https://generative.mdzaiduiux.workers.dev/?prompt={encoded_prompt}"
    img_data = requests.get(image_url).content
    img_filename = os.path.join(IMG_DIR, f"{prompt_id}.png")

    with open(img_filename, 'wb') as handler:
        handler.write(img_data)
    print(f"🖼️ Image saved: {img_filename}")
except Exception as e:
    print(f"❌ Failed to download image for prompt {prompt_id}: {e}")
    exit(1)

# === Upload media using v1.1 API ===
try:
    media = api_v1.media_upload(img_filename)
except Exception as e:
    print(f"❌ Failed to upload media: {e}")
    exit(1)

# === Post tweet using v2 API ===
try:
    response = client.create_tweet(text=tweet_text, media_ids=[media.media_id_string])
    print(f"✅ Tweet posted: https://twitter.com/{user.data.username}/status/{response.data['id']}")
except Exception as e:
    print(f"❌ Failed to post tweet: {e}")
    exit(1)

print("✅ Finished posting prompt.")