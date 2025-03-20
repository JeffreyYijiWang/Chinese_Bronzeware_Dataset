import os
import json
import requests

# Define file paths
json_file = "merged_images.json"
updated_json_file = "merged_images_with_id.json"
image_folder = r"C:\Users\Jeffr\OneDrive\Documents\GitHub\Chinese_Bronzeware_Dataset\Ebay_dataset"

# Create directory if it doesn't exist
os.makedirs(image_folder, exist_ok=True)

# Load JSON data
with open(json_file, "r", encoding="utf-8") as file:
    image_data = json.load(file)

# Assign unique IDs to each image
for index, item in enumerate(image_data, start=1):
    item["id"] = index  # Incremental ID

# Save the updated JSON with IDs
with open(updated_json_file, "w", encoding="utf-8") as file:
    json.dump(image_data, file, indent=4)

print(f"Updated JSON with IDs saved as '{updated_json_file}'")

# Function to clean filenames
def clean_filename(title):
    return "".join(c if c.isalnum() or c in " _-" else "_" for c in title).strip().replace(" ", "_")

# Download images
for item in image_data:
    img_id = item["id"]
    title = item.get("title", "unknown")
    img_url = item.get("src")

    if not img_url:
        continue  # Skip if no image URL

    # Generate a clean filename with ID
    img_filename = f"{img_id}_{clean_filename(title)}.jpg"
    img_path = os.path.join(image_folder, img_filename)

    # Download and save image
    try:
        response = requests.get(img_url, stream=True)
        response.raise_for_status()

        with open(img_path, "wb") as img_file:
            for chunk in response.iter_content(1024):
                img_file.write(chunk)

        print(f"Downloaded: {img_filename}")

    except Exception as e:
        print(f"Error downloading {img_url}: {e}")

print(f"All images saved in '{image_folder}'")
