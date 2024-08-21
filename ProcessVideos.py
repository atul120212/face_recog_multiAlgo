import os
from GetVFrams import get_frams
from AppConstants import *

source_folder = os.path.join('PreprocessedVideos')
destination_folder = os.path.join('database')
preprocessed_vid_dir = os.listdir(source_folder)

for n, subdir in enumerate(preprocessed_vid_dir, start=1):
    subdirectory = os.path.join(source_folder, subdir)
    files = os.listdir(subdirectory)
    extensions = ('.mp4')  # Add more extensions if needed
    vfiles = [f for f in files if f.lower().endswith(extensions)]
    for i, filename in enumerate(vfiles, start=1):
        print(filename)
        dir = os.path.join(destination_folder, subdir)
        if not os.path.exists(dir):
            os.mkdir(dir)
        filepath = os.path.join(source_folder, subdir, filename)
        get_frams(filepath, SAMPLE_COUNT, dir)
        # vidcap = cv2.VideoCapture(filepath)
        # success, image = vidcap.read()
        # count = 0
        # while success:
        #     nfilename = os.path.join(dir, generate_uuid() + '.jpg')
        #     cv2.imwrite(nfilename, image)  # save frame as JPEG file
        #     success, image = vidcap.read()
        #     print('Read a new frame ' + str(count) + '.jpg from: ' + dir, success)
        #     count += 1
        #     if count > 60:
        #         break
