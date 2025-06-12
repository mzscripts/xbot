import tweepy
import json
import os
import requests
import random
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

# === Load and Pick Random Prompt ===
try:
    with open("InstagramPrompts.json", "r", encoding="utf-8") as f:
        prompts = json.load(f)
        if not prompts:
            logger.error("No prompts available in InstagramPrompts.json")
            raise ValueError("Empty prompts list")
        selected_prompt = random.choice(prompts)
        prompt_id = selected_prompt["prompt_id"]
        description = selected_prompt["description"]
        if not (prompt_id and description):
            logger.error("Selected prompt missing prompt_id or description")
            raise ValueError("Invalid prompt structure")
        logger.info(f"Selected prompt {prompt_id}: {description[:50]}...")
except FileNotFoundError:
    logger.error("InstagramPrompts.json not found")
    raise
except (ValueError, KeyError) as e:
    logger.error(f"Invalid prompt data: {e}")
    raise

# === Prepare Tweet Text ===
tweet_text = description
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

logger.info("Script execution finished successfully")