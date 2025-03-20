import os
import json
import numpy as np
import networkx as nx
import shutil
from scipy.spatial import distance_matrix
import subprocess
from PIL import Image  # Import for image conversion

# Paths
file_path = "./Datast_T-SEE/TSNE_positions.json"
image_folder = "./Dataset"
output_folder = "./Data_TSEE2"
output_video_folder = "./video"
output_video = os.path.join(output_video_folder, "output.mp4")
ffmpeg_json_path = "./Datast_T-SEE/ffmpeg_tsp_path.json"

# Ensure output folders exist
for folder in [output_folder, output_video_folder]:
    os.makedirs(folder, exist_ok=True)

# Load TSNE data
with open(file_path, "r") as f:
    tsne_data = json.load(f)

# Extract image names and positions
image_names = list(tsne_data.keys())
positions = np.array([[tsne_data[img]["x"], tsne_data[img]["y"]] for img in image_names])

# Compute distance matrix
dist_matrix = distance_matrix(positions, positions)
print("Finished computing distance matrix.")

# Create a graph with nodes as images and edges weighted by distance
G = nx.Graph()
for i, img1 in enumerate(image_names):
    for j, img2 in enumerate(image_names):
        if i != j:
            G.add_edge(img1, img2, weight=dist_matrix[i, j])

print("Finished creating graph.")

# Solve TSP using Nearest Neighbor heuristic
tsp_path = list(nx.approximation.traveling_salesman_problem(G, cycle=False))
print("Finished solving TSP.")

# Rename images in numerical order and convert to PNG
renamed_images = []
for i, img_name in enumerate(tsp_path):
    new_name = f"{i:04d}.png"  # Ensure all images are saved as PNG
    new_path = os.path.join(output_folder, new_name)

    # Move and convert image to PNG
    original_path = os.path.join(image_folder, img_name)

    if os.path.exists(original_path):
        try:
            img = Image.open(original_path).convert("RGB")  # Convert to RGB mode
            img.save(new_path, "PNG")  # Save as PNG
            renamed_images.append(new_name)
        except Exception as e:
            print(f"Error converting {original_path}: {e}")
    else:
        print(f"Warning: {original_path} not found, skipping.")

print(f"Images have been renamed and saved in: {output_folder}")

# Generate FFmpeg JSON structure for video frames
ffmpeg_json = {
    "frames": [{"image": img_name, "time": i} for i, img_name in enumerate(renamed_images)]
}

# Save FFmpeg JSON output
with open(ffmpeg_json_path, "w") as f:
    json.dump(ffmpeg_json, f, indent=4)

print(f"Saved FFmpeg JSON: {ffmpeg_json_path}")

# Run FFmpeg to create a video from the ordered PNG images
ffmpeg_command = [
    "ffmpeg",
    "-framerate", "30",
    "-i", os.path.join(output_folder, "%04d.png"),  # Process PNG images
    "-c:v", "libx264",
    "-crf", "23",
    "-preset", "fast",
    output_video
]

subprocess.run(ffmpeg_command)

print(f"Video created successfully: {output_video}")
