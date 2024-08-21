import cv2
import os
from Utilities import generate_uuid
from AppConstants import *
from rotate_mp4 import IdentifyFileRotation
from PIL import Image
import numpy as np


def get_frams(video_input_path, num_frames, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    video_capture = cv2.VideoCapture(video_input_path)

    if not video_capture.isOpened():
        print("Error: Could not open video.")
        return

    # Get total number of frames in the video
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the interval between frames to capture
    if total_frames < num_frames:
        print(
            f"Warning: The video only has {total_frames} frames, which is less than the requested {num_frames} frames.")
        num_frames = total_frames

    print('Total Fram: ' + str(total_frames))
    interval = total_frames // num_frames
    frame_count = 0
    captured_frames = 0

    while captured_frames < num_frames:
        # Read the next frame
        ret, frame = video_capture.read()

        if not ret:
            break

        # Save the frame if it's at the correct interval
        if frame_count % interval == 0:
            frame_filename = os.path.join(output_folder, generate_uuid() + '.jpg')
            if not IdentifyFileRotation(filePath=video_input_path, rotation=0) - 1:
                Original_Image = Image.fromarray(frame)
                rotated_image = Original_Image.rotate(IMAGE_ROTATION)
                open_cv_image = np.array(rotated_image)
            cv2.imwrite(frame_filename, open_cv_image)
            captured_frames += 1

        frame_count += 1

    # Release the video capture object
    video_capture.release()
    print(f"Captured {captured_frames} frames and saved them to '{output_folder}'.")


# Example usage
video_path = 'vid.mp4'  # Path to your video file
num_frames = SAMPLE_COUNT  # Number of frames to capture
output_folder = 'output_frames'  # Folder to save captured frames
