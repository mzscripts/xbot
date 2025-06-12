import os
import json
import random
from pathlib import Path
from instagrapi import Client
from PIL import Image
import logging
import tempfile

# === Setup Logging ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_poster.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# === Instagram Credentials (Loaded from Environment Variables) ===
USERNAME = os.getenv("INSTA_USERNAME")
PASSWORD = os.getenv("INSTA_PASSWORD")
SESSION_FILE = "session.json"

# === Directories and Files ===
IMG_DIR = "img"
CAPTION_FILE = "instagram_captions.json"
Path(IMG_DIR).mkdir(parents=True, exist_ok=True)

# === Load Captions from JSON ===
def load_captions():
    try:
        if not os.path.exists(CAPTION_FILE):
            logger.error(f"❌ Caption file not found: {CAPTION_FILE}")
            return None
        with open(CAPTION_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            captions = data.get('captions', [])
            if not captions:
                logger.warning("⚠️ No captions found in the file")
                return None
            if len(captions) < 5:
                logger.warning(f"⚠️ Only {len(captions)} captions left, please add more")
            return captions
    except UnicodeDecodeError as e:
        logger.error(f"❌ Encoding error in {CAPTION_FILE}: {e}")
        try:
            with open(CAPTION_FILE, 'r', encoding='utf-8', errors='replace') as f:
                data = json.load(f)
                captions = data.get('captions', [])
                logger.warning("⚠️ Loaded captions with replacement characters due to encoding issues")
                return captions
        except Exception as e2:
            logger.error(f"❌ Fallback failed: {e2}")
            return None
    except Exception as e:
        logger.error(f"❌ Failed to load captions from {CAPTION_FILE}: {e}")
        return None

# === Save Updated Captions to JSON ===
def save_captions(captions):
    try:
        with open(CAPTION_FILE, 'w', encoding='utf-8') as f:
            json.dump({"captions": captions}, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Updated caption file: {CAPTION_FILE}")
    except Exception as e:
        logger.error(f"❌ Failed to save captions to {CAPTION_FILE}: {e}")

# === Get Random Caption and Hashtags ===
def get_random_caption():
    captions = load_captions()
    if not captions:
        return None, None
    selected = random.choice(captions)
    caption_text = selected.get('caption', '')
    hashtags = selected.get('hashtags', [])
    full_caption = f"{caption_text} {' '.join(hashtags)}"
    return full_caption, selected

# === Remove Used Caption ===
def remove_caption(used_caption):
    captions = load_captions()
    if captions and used_caption in captions:
        captions.remove(used_caption)
        save_captions(captions)
        logger.info("🗑️ Removed used caption from file")
    else:
        logger.warning("⚠️ Caption not found in file or already removed")

# === Convert PNG to JPEG ===
def convert_png_to_jpeg(png_path):
    try:
        with Image.open(png_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            temp_jpeg = os.path.join(tempfile.gettempdir(), f"{os.path.basename(png_path)}.jpg")
            img.save(temp_jpeg, 'JPEG', quality=95)
            logger.info(f"🔄 Converted {png_path} to {temp_jpeg}")
            return temp_jpeg
    except Exception as e:
        logger.error(f"❌ Failed to convert {png_path} to JPEG: {e}")
        return None

# === Initialize Instagram Client ===
def initialize_client():
    try:
        client = Client()
        # Load session if exists
        if os.path.exists(SESSION_FILE):
            client.load_settings(SESSION_FILE)
            logger.info("✅ Loaded session from file")
            try:
                client.get_timeline_feed()  # Test session
                logger.info("✅ Session is valid, no login required")
                return client
            except Exception as e:
                logger.warning(f"⚠️ Invalid session: {e}, attempting login")
        # Login if no valid session
        if not USERNAME or not PASSWORD:
            logger.error("❌ Instagram credentials not provided")
            return None
        client.login(USERNAME, PASSWORD)
        client.dump_settings(SESSION_FILE)
        logger.info("✅ Successfully logged in and saved session")
        return client
    except Exception as e:
        logger.error(f"❌ Failed to initialize client: {e}")
        return None

# === Post Image to Instagram ===
def post_image(client, image_path, caption):
    try:
        if not os.path.exists(image_path):
            logger.error(f"❌ Image not found: {image_path}")
            return False
        media = client.photo_upload(image_path, caption)
        logger.info(f"🖼️ Successfully posted image: {image_path} (Media ID: {media.id})")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to post image {image_path}: {e}")
        return False

# === Main Function ===
def main():
    client = initialize_client()
    if not client:
        logger.error("❌ Client initialization failed, aborting")
        return

    # Get all PNG files in the img directory
    image_paths = list(Path(IMG_DIR).glob("*.png"))
    if not image_paths:
        logger.warning("⚠️ No PNG images found in img folder")
        return
    image_path = random.choice(image_paths)  # Randomly select one image

    # Get random caption
    caption, selected_caption = get_random_caption()
    if not caption:
        logger.error("❌ No valid caption available, aborting post")
        return

    logger.info(f"📤 Processing image: {image_path} with caption: {caption}")
    # Convert PNG to JPEG
    jpeg_path = convert_png_to_jpeg(str(image_path))
    if jpeg_path:
        if post_image(client, jpeg_path, caption):
            # Delete the original PNG and used caption after successful posting
            try:
                os.remove(image_path)
                logger.info(f"🗑️ Deleted original PNG: {image_path}")
                remove_caption(selected_caption)
            except Exception as e:
                logger.error(f"❌ Failed to delete files or caption for {image_path}: {e}")
        else:
            logger.warning("⚠️ Post failed, keeping original PNG and caption")
        
        # Clean up temporary JPEG
        try:
            os.remove(jpeg_path)
            logger.info(f"🗑️ Deleted temporary JPEG: {jpeg_path}")
        except Exception as e:
            logger.error(f"❌ Failed to delete temporary JPEG {jpeg_path}: {e}")

    logger.info("✅ Finished processing one image")

if __name__ == "__main__":
    main()