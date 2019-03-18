import face_recognition
import cv2 as cv2
import os
import sys
import dlib

import math
import os.path
import pickle
import json
from PIL import Image, ImageDraw
from face_recognition.face_recognition_cli import image_files_in_folder
import time

import json


# assumes that the person has either entered the name or pressed ask a question button

def detect_face(X_img, name):
    # saves the detected face under given name

    # Load image file and find face locations
    X_face_locations = face_recognition.face_locations(X_img)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return [0, 0]
    elif len(X_face_locations) != 1:
        return [0, 0]
    else:

        # Find encodings for faces in the test iamge
        faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)
        return [X_face_locations, faces_encodings]

#if __name__ == "__main__":
def saveface(name):

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    # processing the frame initiated
    process_this_frame = True


    while True:

        time.sleep(0.5)
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        height, width = frame.shape[:2]


        # Only process every other frame of video to save time
        if process_this_frame:
            [location, encodings] = detect_face(rgb_small_frame, name)
            if location != 0:
                for (coor_t, coor_r, coor_b, coor_l) in location :
                    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    coor_t *= 4
                    coor_r *= 4
                    coor_b *= 4
                    coor_l *= 4

                im = frame[max(coor_l - 100,1):min(coor_r + 100,width-1), max(coor_t - 100,1):min(coor_b + 100,height)]


                os.chdir('unknown')
                cv2.imwrite( name + '.jpg', im)
                os.chdir('..')


                process_this_frame = False

                video_capture.release()
                break


# if __name__ == "__main__":
#
#     saveface("Ram")