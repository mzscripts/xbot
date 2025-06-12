import json
import os
from dotenv import load_dotenv
import requests
import threading
from urllib.parse import quote
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

# === Setup ===
load_dotenv()

# === Prepare image directory ===
IMG_DIR = "31-5-25"
Path(IMG_DIR).mkdir(parents=True, exist_ok=True)

# === Load prompts ===
try:
    with open("wallprompts.json", "r", encoding="utf-8") as f:
        prompts = json.load(f)
except FileNotFoundError:
    print("❌ prompts.json not found.")
    exit(1)

# === Function to save updated prompts to JSON ===
# def save_prompts(prompts_list, filename="prompts_2000.json"):
#     try:
#         with open(filename, "w", encoding="utf-8") as f:
#             json.dump(prompts_list, f, indent=4)
#         print(f"📝 Updated prompts saved to {filename}")
#     except Exception as e:
#         print(f"❌ Failed to save prompts to {filename}: {e}")

# === Function to crop image to mobile aspect ratio (9:16) ===
def crop_to_mobile_aspect(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            target_aspect = 9 / 16
            current_aspect = width / height

            if abs(current_aspect - target_aspect) > 0.01:  # If not already in 9:16
                if current_aspect > target_aspect:  # Image is too wide
                    new_width = int(height * target_aspect)
                    left = (width - new_width) // 2
                    img_cropped = img.crop((left, 0, left + new_width, height))
                else:  # Image is too tall
                    new_height = int(width / target_aspect)
                    top = (height - new_height) // 2
                    img_cropped = img.crop((0, top, width, top + new_height))
                img_cropped.save(image_path, quality=95)
                print(f"🖌️ Cropped image to 9:16 aspect ratio: {image_path}")
    except Exception as e:
        print(f"❌ Failed to crop image {image_path}: {e}")

# === Function to generate and save image for a single prompt ===
def generate_image(prompt, prompts_list):
    prompt_id = prompt["prompt_id"]
    description = prompt["description"]
    print(f"📤 Processing prompt {prompt_id}: {description[:50]}...")
    try:
        encoded_prompt = quote(description)
        # Add width and height parameters for mobile aspect ratio (1080x1920)
        image_url = f"https://generative.mdzaiduiux.workers.dev/?prompt={encoded_prompt}&width=1080&height=1920"
        img_data = requests.get(image_url, timeout=30).content
        img_filename = os.path.join(IMG_DIR, f"{description[:50].replace(' ', '_')}.png")
        with open(img_filename, 'wb') as handler:
            handler.write(img_data)
        
        # Crop image to ensure 9:16 aspect ratio
        crop_to_mobile_aspect(img_filename)
        
        print(f"🖼️ Image saved: {img_filename}")
        
        # Remove the prompt from the prompts list
        # prompts_list[:] = [p for p in prompts_list if p["prompt_id"] != prompt_id]
        # Save the updated prompts list to the JSON file
        # save_prompts(prompts_list)
        # print(f"🗑️ Prompt {prompt_id} removed from prompts_2000.json")
        
        return True
    except Exception as e:
        print(f"❌ Failed to download or process image for prompt {prompt_id}: {e}")
        return False

# === Process prompts in batches of 50 ===
BATCH_SIZE = 10
total_prompts = len(prompts)
print(f"📋 Total prompts to process: {total_prompts}")

for i in range(0, total_prompts, BATCH_SIZE):
    batch_prompts = prompts[i:i + BATCH_SIZE]
    print(f"📦 Processing batch {i // BATCH_SIZE + 1} with {len(batch_prompts)} prompts...")
    
    try:
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_prompt = {executor.submit(generate_image, prompt, prompts): prompt for prompt in batch_prompts}
            for future in as_completed(future_to_prompt):
                prompt = future_to_prompt[future]
                try:
                    future.result()  # Ensure exceptions are caught
                except Exception as e:
                    print(f"❌ Exception for prompt {prompt['prompt_id']}: {e}")
    except Exception as e:
        print(f"❌ Threading error in batch {i // BATCH_SIZE + 1}: {e}")
        continue

print("✅ Finished processing all prompts.")