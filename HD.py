import os
import subprocess

# CONFIGURE THESE
INPUT_FOLDER = "31-5-25"
OUTPUT_FOLDER = "HD-31-5-25"

def enhance_images():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            input_path = os.path.join(INPUT_FOLDER, filename)
            output_path = os.path.join(OUTPUT_FOLDER, filename)

            command = [
                "python", "-m", "realesrgan",
                "-i", input_path,
                "-o", output_path,
                "-n", "RealESRGAN_x4plus"
            ]

            print(f"Enhancing: {filename}")
            subprocess.run(command, check=True)

if __name__ == "__main__":
    enhance_images()
