import os
import json
from glob import glob

# Define the directory where JSON files are stored
json_dir = "image_jsons"
output_file = "merged_images.json"

# Get a list of all JSON files in the directory
json_files = glob(os.path.join(json_dir, "*.json"))

# Dictionary to store unique titles with a single .jpg image
unique_images = {}

# Process each JSON file
for json_file in json_files:
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
        for item in data:
            title = item.get("title", "").strip()
            src = item.get("src", "").strip()

            # Skip entries with "Shop on eBay" in the title
            if title.lower() == "shop on ebay":
                continue

            # If the title is already in the dictionary, prioritize .jpg images
            if title in unique_images:
                # Keep .jpg over .webp
                if src.endswith(".jpg") and unique_images[title]["src"].endswith(".webp"):
                    unique_images[title] = {"title": title, "src": src}
            else:
                # Store the first found image (may be .webp initially)
                unique_images[title] = {"title": title, "src": src}

# Convert to a list for JSON output
merged_data = list(unique_images.values())

# Save the cleaned and merged JSON
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(merged_data, file, indent=4)

print(f"Merged JSON saved as {output_file}")
