import os
import subprocess

# Define paths
output_folder = "./Data_TSEE2"
output_video_10 = "./video/outOrig_new.mp4"
output_video_21 = "./video/outOrig_new2.mp4"

# Ensure the output directory exists
os.makedirs("./video", exist_ok=True)

# Set the desired output resolution (change as needed)
resolution = "1920:1080"  # Change to preferred resolution (e.g., "1280:720")

# First FFmpeg command: Normal video at 10 FPS (with resizing)
ffmpeg_command_1 = [
    "ffmpeg",
    "-framerate", "10",
    "-i", os.path.join(output_folder, "%04d.png"),
    "-vf", f"scale={resolution}:force_original_aspect_ratio=decrease,pad={resolution}:-1:-1:color=black",
    "-c:v", "libx264",
    "-crf", "23",
    "-preset", "fast",
    output_video_10
]

# Second FFmpeg command: Morphing effect using minterpolate (with resizing)
ffmpeg_command_2 = [
    "ffmpeg",
    "-framerate", "5",
    "-i", os.path.join(output_folder, "%04d.png"),
    "-vf", f"scale={resolution}:force_original_aspect_ratio=decrease,pad={resolution}:-1:-1:color=black,minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=30'",
    "-c:v", "libx264",
    "-crf", "18",
    "-preset", "slow",
    output_video_21
]

# Run first command
print("Generating normal 10 FPS video with resized images...")
subprocess.run(ffmpeg_command_1)

# Run second command
print("Generating morphing transition video with resized images...")
subprocess.run(ffmpeg_command_2)

print("Video creation completed successfully!")
