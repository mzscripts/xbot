import tweepy
import json
import os
import requests
from urllib.parse import quote
from io import BytesIO
import logging
from time import sleep

# === Setup Logging ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# === Load Environment Variables ===
try:
    API_KEY = os.environ["API_KEY"]
    API_SECRET = os.environ["API_SECRET"]
    ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
except KeyError as e:
    logger.error(f"Missing environment variable: {e}")
    raise

# === Initialize Tweepy APIs ===
try:
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api_v1 = tweepy.API(auth, wait_on_rate_limit=True)
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    logger.info("Tweepy APIs initialized successfully")
except tweepy.TweepyException as e:
    logger.error(f"Failed to initialize Tweepy: {e}")
    raise

# === Load Prompts ===
try:
    with open("IgPrompts900.json", "r", encoding="utf-8") as f:
        prompts = json.load(f)
        if not prompts:
            logger.error("No prompts available in InstagramPrompts.json")
            raise ValueError("Empty prompts list")
except FileNotFoundError:
    logger.error("InstagramPrompts.json not found")
    raise
except (ValueError, KeyError) as e:
    logger.error(f"Invalid prompt data: {e}")
    raise

# === Load Last Used Prompt Index ===
last_prompt_file = "last_prompt.txt"

if not os.path.exists(last_prompt_file):
    with open(last_prompt_file, "w") as f:
        f.write("0")

with open(last_prompt_file, "r") as f:
    last_index = int(f.read().strip())

# === Get Next Prompt ===
next_index = last_index + 1

if next_index >= len(prompts):
    logger.info("All prompts have been used. Resetting to start.")
    next_index = 0

selected_prompt = prompts[next_index]
prompt_id = selected_prompt["prompt_id"]
description = selected_prompt["description"]

logger.info(f"Using prompt {next_index + 1} (Prompt ID: {prompt_id}): {description[:50]}...")

# === Prepare Tweet Text ===
tweet_text = f"({next_index + 1}) {description}"
if len(tweet_text) > 280:
    tweet_text = tweet_text[:277] + "..."

# === Generate Image ===
try:
    encoded_prompt = quote(description)
    image_url = f"https://generative.mdzaiduiux.workers.dev/?prompt={encoded_prompt}"
    response = requests.get(image_url, timeout=30)
    response.raise_for_status()
    img_data = response.content
    logger.info(f"Image data retrieved for prompt {prompt_id}")
except requests.RequestException as e:
    logger.error(f"Failed to download image for prompt {prompt_id}: {e}")
    raise

# === Upload Media ===
for attempt in range(3):
    try:
        img_file = BytesIO(img_data)
        img_file.name = f"{prompt_id}.png"
        media = api_v1.media_upload(filename=img_file.name, file=img_file)
        logger.info("Media uploaded successfully")
        break
    except tweepy.TweepyException as e:
        logger.warning(f"Media upload attempt {attempt + 1} failed: {e}")
        if attempt == 2:
            logger.error("Max retries reached for media upload")
            raise
        sleep(5)

# === Post Tweet ===
try:
    response = client.create_tweet(text=tweet_text, media_ids=[media.media_id_string])
    tweet_url = f"https://x.com/i/status/{response.data['id']}"
    logger.info(f"Tweet posted: {tweet_url}")
except tweepy.TweepyException as e:
    logger.error(f"Failed to post tweet: {e}")
    raise

# === Update Last Used Prompt ===
with open(last_prompt_file, "w") as f:
    f.write(str(next_index))

logger.info("Script execution finished successfully")
