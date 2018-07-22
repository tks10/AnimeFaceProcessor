import os
import shutil
import cv2
from util import detect
from PIL import Image
import glob
from scipy import ndimage


def video_2_frames(video_file='./IMG_2140.MOV', image_dir='./image_dir/', image_file='img_%s.png', sampling=5):
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
        for j in range(sampling-1):
            flag, frame = cap.read()
        if flag == False:  # Is a frame left?
            break

        frame = cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2))  # Resize to half
        frame = ndimage.rotate(frame, 90, reshape=True)

        cv2.imwrite(image_dir+image_file % str(i).zfill(6), frame)  # Save a frame
        print('Save', image_dir+image_file % str(i).zfill(6))
        i += sampling

    cap.release()  # When everything done, release the capture


def extract_faces(image_dir, cascade=None):
    if cascade is None:
        faces = detect.detect(image_dir)
    else:
        faces = detect.detect(image_dir, cascade_file=cascade)

    image = Image.open(image_dir)
    idx = 0
    for face in faces:
        x, y, w, h = face
        face = (x, y, x+w, y+h)
        cropped = image.crop(face)
        image_dir_ = "../faces/" + str(idx) + image_dir.split("/")[-1]
        cropped.save(image_dir_, "PNG", quality=100, optimize=100)
        idx += 1
        print("Saved", image_dir_)


def extract_all_faces(src):
    dirs = glob.glob(src)
    for d in dirs:
        try:
            extract_faces(d)
        except Exception as e:
            print(e)


def extract_smiles(src):
    dirs = glob.glob(src)
    cascade = "../haarcascade_smile.xml"
    for d in dirs:
        try:
            extract_faces(d, cascade)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    # extract_smiles(src="../ClassifyTest_Cropped/*")
     extract_all_faces(src="../images/*")
    # video_2_frames(video_file="../video.MOV", image_dir="../images/", image_file="img_%s.png")
