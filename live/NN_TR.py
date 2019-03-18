import face_recognition
import cv2 as cv2
import os
import sys
import dlib

import math
from sklearn import neighbors
import os
import sys
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
from pymongo import MongoClient
import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
dir_ = "combined_test"
path_inc = "knn_mod_2_45_bt.clf"

def train(tr_dir, mod_sp=None, nn_int= None, k_build='ball_tree', flag=True):

    X = []
    y = []

    # Loop through each entry in the training set
    for class_dir in os.listdir(tr_dir):
        entry = class_dir
        if not os.path.isdir(os.path.join(tr_dir, class_dir)):
            continue

        # init_db_entry(person)

        # Loop through each training image for the current person
        for img_path in image_files_in_folder(os.path.join(tr_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            obj_face_bound_out = face_recognition.face_locations(image)

            if len(obj_face_bound_out) != 1:
                if len(obj_face_bound_out)>1:
                    bound_next = obj_face_bound_out[0]
                    # must select the larger bounding box
                    area = 0
                    for size in obj_face_bound_out:
                        new_area = abs(size[2]-size[0])*abs(size[1]-size[3])
                        if new_area >= area:
                            area = new_area
                            bound_next = [size]
                    X.append(face_recognition.face_encodings(image, known_face_locations=bound_next)[0])
                    y.append(class_dir)
                    print("Image {} has more than one face for training: {} - {}".format(img_path, "selecting face with area one face", area))

                # if flag:
                    # print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(obj_face_bound_out) < 1 else "Found more than one face"))
            else:
                # Add face encoding for current image to the training set
                X.append(face_recognition.face_encodings(image, known_face_locations=obj_face_bound_out)[0])
                y.append(class_dir)

    # Determine how many neighbors to use for weighting in the KNN classifier
    if nn_int is None:
        nn_int = int(round(math.sqrt(len(X))))
        if flag:
            print("Chose n automatically:", nn_int)

    # part for adressing the classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=nn_int, algorithm=k_build, weights='distance')
    knn_clf.fit(X, y)

    # Save the trained KNN classifier
    if mod_sp is not None:
        with open(mod_sp, 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf

if __name__ == "__main__":

    # function call for train() activity
    print("Training KNN classifier...")
    classifier = train(dir_, mod_sp=path_inc, nn_int=2)
    print("Training complete!")


