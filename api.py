import json
import requests
import urllib.parse
import tweepy
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
GENERATIVE_API_URL = "https://generative.mdzaiduiux.workers.dev/?prompt="

# Verify that all credentials are loaded
if not all([TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET]):
    raise ValueError("One or more Twitter API credentials are missing from the .env file.")

def read_prompts(file_path="prompts.json"):
    """Read prompts from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            return [data]
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}.")
        return []

def generate_image(prompt):
    """Send prompt to generative API and get image data."""
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"{GENERATIVE_API_URL}{encoded_prompt}"
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Error generating image for prompt '{prompt}': {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error generating image for prompt '{prompt}': {e}")
        return None

def upload_media_and_tweet(image_data, prompt_id, description):
    """Upload image to Twitter v1.1 and post tweet with media using v2."""
    # Initialize OAuth 1.0a for v1.1 media upload
    auth = tweepy.OAuth1UserHandler(
        consumer_key=TWITTER_CONSUMER_KEY,
        consumer_secret=TWITTER_CONSUMER_SECRET,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
    )
    client_v1 = tweepy.API(auth)
    
    # Initialize v2 client
    client_v2 = tweepy.Client(
        consumer_key=TWITTER_CONSUMER_KEY,
        consumer_secret=TWITTER_CONSUMER_SECRET,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
    )
    
    # Save image temporarily
    temp_file = f"temp_image_{prompt_id}.png"
    try:
        with open(temp_file, 'wb') as f:
            f.write(image_data)
        
        # Upload media using v1.1 API
        media = client_v1.media_upload(filename=temp_file)
        media_id = media.media_id_string
        
        # Post tweet with media using v2 API immediately
        tweet_response = client_v2.create_tweet(
            text=description,
            media_ids=[media_id]
        )
        
        if tweet_response.data.get('id'):
            print(f"Successfully posted tweet for prompt {prompt_id}: {tweet_response.data['id']}")
            return True
        else:
            print(f"Error posting tweet for prompt {prompt_id}: {tweet_response.errors}")
            return False
            
    except Exception as e:
        print(f"Error processing prompt {prompt_id}: {e}")
        return False
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

def main():
    prompts = read_prompts()
    if not prompts:
        print("No prompts to process. Exiting.")
        return

    for prompt_data in prompts:
        prompt_id = prompt_data.get("prompt_id")
        description = prompt_data.get("description")
        if not prompt_id or not description:
            print("Skipping prompt: Missing prompt_id or description.")
            continue
            
        print(f"Processing prompt {prompt_id}: {description} (Posting immediately)")
        
        image_data = generate_image(description)
        if not image_data:
            print(f"Failed to generate image for prompt {prompt_id}. Skipping.")
            continue
            
        success = upload_media_and_tweet(image_data, prompt_id, description)
        if not success:
            print(f"Failed to post tweet for prompt {prompt_id}.")

if __name__ == "__main__":
    main()