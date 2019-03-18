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

import json

import fnlp
import ftexttospeech

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
path_inc = "knn_mod_2_45_bt.clf"
mod_cf = 'names.cf'

def predict(X_img, knn_clf=None, model_path=None, distance_threshold=0.9):

    if knn_clf is None and model_path is None:
        raise Exception("need knn classifier")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # Load image file and find face locations
    # X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(X_img)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=2)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

# def init_db_entry(name):
#     # initiate db
#     json_obj = {}
#     json_obj['_id'] = str(name)
#     json_obj['freq'] = 1
#     json_obj['time'] = datetime.datetime.now()
#     test_col.insert_one(json_obj)

#if __name__ == "__main__":
def runface(video_capture):

    dist_threshold = 0.45

    update = {}

    # Get a reference to webcam #0 (the default one)
    # video_capture = cv2.VideoCapture(0)
    #video_capture = cv2.VideoCapture(1)

    # processing the frame initiated
    process_this_frame = True

    # system total for current run
    unknown_count = 0
    # system flag for current unknown run
    current_unknown_flag = False
    # system list for live predictions
    liveList = []


    while True:

        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            predictions = predict(rgb_small_frame, model_path = path_inc, distance_threshold=dist_threshold)

        process_this_frame = not process_this_frame

        dl = []

        for face,(coor_t, coor_r, coor_b, coor_l) in predictions:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            coor_t *= 4
            coor_r *= 4
            coor_b *= 4
            coor_l *= 4
            im = frame[coor_l:coor_r, coor_t:coor_b]
            dl.append(face)

            if 'unknown' in face :

                if 'unknown' not in update:
                    update[face] = 10
                    # if known immediately flag updates
                    current_unknown_flag = False

                # to change unknown count delay
                if update[face] > 30:
                    if current_unknown_flag == False :
                        unknown_count = unknown_count + 1

                        # directs to the application
                        ##############################
                        print("greet stranger")




                        ##############################

                        current_unknown_flag = True

                        video_capture.release()
                        cv2.destroyAllWindows()

                        return "unknown"

                # elif update[face] <=30:
                #     prob_measure += 1

            else:

                # if known the flag updates
                current_unknown_flag = False
                if face not in update:
                    print('in condition')
                    print(face)
                    update[face] = 10

                    ##############
                    # nlp_output = fnlp.nlpname(face)
                    # ftexttospeech.texttospeech(nlp_output)
                    #######RAM




                if update[face] > 15 :
                    if face not in liveList :
                        print('greet with name '+ face)
                        liveList.append(face)

                        video_capture.release()
                        cv2.destroyAllWindows()

                        return face
                        # result_freq = test_col.update({'_id': face}, {'$inc': {'freq': 1}})
                        # result_datetime = test_col.update({'_id': face}, {'$set': {'time': datetime.datetime.now()}})

        # elif len(predictions) >1:
        #     print('do something')


        # Display the results
        for name,(coor_t, coor_r, coor_b, coor_l)in predictions:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            coor_t *= 4
            coor_r *= 4
            coor_b *= 4
            coor_l *= 4

            # box drawn
            cv2.rectangle(frame, (coor_l, coor_t), (coor_r, coor_b), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (coor_l, coor_b - 35), (coor_r, coor_b), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (coor_l + 6, coor_b - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)
        print(update)
        # print(liveList)


        update = {k : v for k,v in  update.items() if v}
        for entries in liveList:
            if entries not in update:
                liveList.remove(entries)
        for pivot in update:
            if pivot in dl:
                update[pivot] = update[pivot]+1
            else :
                update[pivot] -= 1
                if update[pivot] < 0:
                    update.pop(pivot)
        with open(mod_cf, 'w') as f:
            json.dump(update, f)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # cursor = test_col.find({})
            # for document in cursor:
            #         print(document)
            #break
            video_capture.release()
            cv2.destroyAllWindows()
            return "0"


    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

