import os
import json
import numpy as np
import networkx as nx
import shutil
from scipy.spatial import distance_matrix
import subprocess

# Paths
file_path = "./Datast_T-SEE/TSNE_positions.json"
image_folder = "./Dataset"
output_folder = "./Data_TSEE"

# Ensure output folder exists (remove if it already exists to avoid old files)
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)  # Remove existing directory
os.makedirs(output_folder)

# Load TSNE data
with open(file_path, "r") as f:
    tsne_data = json.load(f)

# Extract image names and positions
image_names = list(tsne_data.keys())
positions = np.array([[tsne_data[img]["x"], tsne_data[img]["y"]] for img in image_names])

# Compute distance matrix
dist_matrix = distance_matrix(positions, positions)
print("Finished computing distance matrix.")

# Create a weighted graph
G = nx.Graph()
for i in range(len(image_names)):
    for j in range(i + 1, len(image_names)):  # Avoid duplicate edges
        G.add_edge(image_names[i], image_names[j], weight=dist_matrix[i, j])

print("Finished creating graph.")

# Solve TSP using Christofides algorithm (1.5x optimal)
tsp_path = nx.approximation.christofides(G)
print("Finished solving TSP.")

# Rename images in numerical order and move them
renamed_images = []
for i, img_name in enumerate(tsp_path):
    img_ext = os.path.splitext(img_name)[-1] or ".png"
    new_name = f"{i:04d}{img_ext}"  # Rename numerically (0001.png, 0002.png, etc.)
    new_path = os.path.join(output_folder, new_name)

    # Move and rename the file from `image_folder`
    original_path = os.path.join(image_folder, img_name)

    if os.path.exists(original_path):
        shutil.copy(original_path, new_path)
        renamed_images.append(new_name)
    else:
        print(f"Warning: {original_path} not found, skipping.")

print(f"Images have been renamed and saved in: {output_folder}")

# Generate FFmpeg JSON structure for video frames
ffmpeg_json = {
    "frames": [{"image": img_name, "time": i} for i, img_name in enumerate(renamed_images)]
}

# Save FFmpeg JSON output
ffmpeg_json_path = "./output/ffmpeg_tsp_path.json"
with open(ffmpeg_json_path, "w") as f:
    json.dump(ffmpeg_json, f, indent=4)

print(f"Saved FFmpeg JSON: {ffmpeg_json_path}")

# Run FFmpeg to create a video from the ordered images
output_video = "./output/output.mp4"  # Save video inside `output` folder
ffmpeg_command = [
    "ffmpeg",
    "-framerate", "30",  # Set frame rate (adjust as needed)
    "-i", os.path.join(output_folder, "%04d.png"),  # Pattern for numbered images
    "-c:v", "libx264",
    "-crf", "23",
    "-preset", "fast",
    output_video
]

subprocess.run(ffmpeg_command)

print(f"Video created successfully: {output_video}")
