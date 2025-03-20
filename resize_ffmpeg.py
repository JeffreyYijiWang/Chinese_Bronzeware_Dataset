import os
import subprocess

# Define source and target directories
directories = {
    "Dataset": "Dataset_128",
    "Ebay_dataset": "Ebay_dataset_128"
}

# Iterate through the directories
for input_dir, output_dir in directories.items():
    # Create source directory if it doesn't exist
    os.makedirs(input_dir, exist_ok=True)
    
    # Create target directory
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over all image files in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):  # Supported formats
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            # FFmpeg command to resize image
            ffmpeg_cmd = [
                "ffmpeg",
                "-i", input_path,      # Input file
                "-vf", "scale=128:128",  # Resize to 128x128
                "-q:v", "2",          # High-quality output
                output_path           # Output file
            ]

            # Run FFmpeg command
            subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            print(f"Resized: {filename} -> {output_path}")

print("✅ All images resized successfully!")
