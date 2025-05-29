import os
from pathlib import Path
from instagrapi import Client
from PIL import Image
import logging
import tempfile

# === Setup Logging ===
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# === Instagram Credentials ===
USERNAME = "gen.art.mz"  # Replace with your Instagram username
PASSWORD = "#uwiJu?Rome8W-thE7Pe"  # Replace with your Instagram password

# === Image Directory ===
IMG_DIR = "img"
Path(IMG_DIR).mkdir(parents=True, exist_ok=True)

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
        client.login(USERNAME, PASSWORD)
        logger.info("✅ Successfully logged in to Instagram")
        return client
    except Exception as e:
        logger.error(f"❌ Failed to login: {e}")
        return None

# === Post Image to Instagram ===
def post_image(client, image_path, caption="Posted via instagrapi"):
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
        return

    # Get the first PNG file in the img directory
    image_path = next(Path(IMG_DIR).glob("*.png"), None)
    if not image_path:
        logger.warning("⚠️ No PNG images found in img folder")
        return

    logger.info(f"📤 Processing image: {image_path}")
    # Convert PNG to JPEG
    jpeg_path = convert_png_to_jpeg(str(image_path))
    if jpeg_path:
        if post_image(client, jpeg_path):
            # Delete the original PNG after successful posting
            try:
                os.remove(image_path)
                logger.info(f"🗑️ Deleted original PNG: {image_path}")
                # Delete the temporary JPEG
                os.remove(jpeg_path)
                logger.info(f"🗑️ Deleted temporary JPEG: {jpeg_path}")
            except Exception as e:
                logger.error(f"❌ Failed to delete files for {image_path}: {e}")
        else:
            # Clean up temporary JPEG if posting failed
            try:
                os.remove(jpeg_path)
                logger.info(f"🗑️ Deleted temporary JPEG: {jpeg_path}")
            except Exception as e:
                logger.error(f"❌ Failed to delete temporary JPEG {jpeg_path}: {e}")

    logger.info("✅ Finished processing one image")

if __name__ == "__main__":
    main()