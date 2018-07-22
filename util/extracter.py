import os
import shutil
import cv2
from util import detect
from PIL import Image
import glob


def video_2_frames(video_file='./IMG_2140.MOV', image_dir='./image_dir/', image_file='img_%s.png'):
    # Delete the entire directory tree if it exists.
    if os.path.exists(image_dir):
        shutil.rmtree(image_dir)

    # Make the directory if it doesn't exist.
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    # Video to frames
    i = 0
    cap = cv2.VideoCapture(video_file)
    while(cap.isOpened()):
        flag, frame = cap.read()  # Capture frame-by-frame
        if flag == False:  # Is a frame left?
            break
        cv2.imwrite(image_dir+image_file % str(i).zfill(6), frame)  # Save a frame
        print('Save', image_dir+image_file % str(i).zfill(6))
        i += 1

    cap.release()  # When everything done, release the capture


def extract_faces(image_dir):
    faces = detect.detect(image_dir)
    image = Image.open(image_dir)
    idx = 0
    for face in faces:
        x, y, w, h = face
        face = (x, y, x+w, y+h)
        cropped = image.crop(face)
        image_dir_ = "./faces/" + str(idx) + image_dir.split("/")[-1]
        cropped.save(image_dir_, "PNG", quality=100, optimize=100)
        idx += 1
        print("Saved", image_dir_)


if __name__ == "__main__":
    dirs = glob.glob("./images/*")
    for d in dirs:
        try:
            extract_faces(d)
        except Exception as e:
            print(e)
