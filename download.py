import json
from bs4 import BeautifulSoup

# Correct file path for Windows
html_file = r"C:\Users\Jeffr\OneDrive\Documents\GitHub\Chinese_Bronzeware_Dataset\ebay_page.html"

# Load the HTML file
with open(html_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Find all image elements with data-defer-load
image_data = []
for img in soup.find_all("img"):
    defer_load = img.get("src")  # Get image URL
    alt_text = img.get("alt")  # Get title
    
    if defer_load and alt_text:
        image_data.append({"src": defer_load, "title": alt_text})

# Save to JSON file
output_file = "extracted_images10.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(image_data, f, indent=4, ensure_ascii=False)

print(f"Extracted image data saved to {output_file}")
