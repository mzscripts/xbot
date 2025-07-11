import tweepy
import json
import os
import requests
from urllib.parse import quote
from io import BytesIO
import logging
from time import sleep
from supabase import create_client
from PIL import Image, ImageEnhance

# === Setup Logging ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# === Load Environment Variables ===
try:
    API_KEY = os.environ["API_KEY"]
    API_SECRET = os.environ["API_SECRET"]
    ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
    SUPABASE_URL = os.environ["SUPABASE_URL"]
    SUPABASE_KEY = os.environ["SUPABASE_KEY"]
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

# === Initialize Supabase Client ===
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# === Load Prompts ===
try:
    with open("IgPrompts900.json", "r", encoding="utf-8") as f:
        prompts = json.load(f)
        if not prompts:
            logger.error("No prompts available in IgPrompts900.json")
            raise ValueError("Empty prompts list")
except Exception as e:
    logger.error(f"Failed to load prompts: {e}")
    raise

# === Load Last Used Prompt Index from Supabase ===
try:
    response = supabase.table('tweet_prompt_state').select('id', 'last_prompt_index').limit(1).execute()
    if not response.data:
        logger.error("No state row found in Supabase")
        raise ValueError("State row missing")

    state_row = response.data[0]
    state_id = state_row['id']
    last_index = state_row['last_prompt_index']
    logger.info(f"Fetched last index {last_index} from Supabase")
except Exception as e:
    logger.error(f"Error fetching state from Supabase: {e}")
    raise

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

# === Image Enhancement Function ===
def enhance_image(input_path, output_path, upscale_factor=2):
    img = Image.open(input_path)
    new_size = (img.width * upscale_factor, img.height * upscale_factor)
    upscaled_img = img.resize(new_size, Image.LANCZOS)
    sharp_img = ImageEnhance.Sharpness(upscaled_img).enhance(2.0)
    final_img = ImageEnhance.Contrast(sharp_img).enhance(1.3)
    final_img.save(output_path)

# === Generate & Enhance Image ===
try:
    encoded_prompt = quote(description)
    image_url = f"https://generative.mdzaiduiux.workers.dev/?prompt={encoded_prompt}"
    response = requests.get(image_url, timeout=30)
    response.raise_for_status()

    # Save original image
    orig_path = f"/tmp/{prompt_id}_orig.png"
    with open(orig_path, "wb") as f:
        f.write(response.content)

    # Enhance image
    enhanced_path = f"/tmp/{prompt_id}_enhanced.png"
    enhance_image(orig_path, enhanced_path, upscale_factor=2)
    logger.info(f"Enhanced image saved at: {enhanced_path}")

except Exception as e:
    logger.error(f"Image generation or enhancement failed: {e}")
    raise

# === Upload Media ===
for attempt in range(3):
    try:
        with open(enhanced_path, "rb") as f:
            img_file = BytesIO(f.read())
            img_file.name = f"{prompt_id}_enhanced.png"
            media = api_v1.media_upload(filename=img_file.name, file=img_file)
            logger.info("Enhanced media uploaded successfully")
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

# === Update Supabase Index ===
try:
    supabase.table('tweet_prompt_state').update({'last_prompt_index': next_index}).eq('id', state_id).execute()
    logger.info(f"Updated Supabase index to {next_index}")
except Exception as e:
    logger.error(f"Failed to update Supabase state: {e}")
    raise

logger.info("Script execution finished successfully")
