import face_recognition
import cv2
import os 
import numpy as np

def find_faces(college_name : str, course_name: str, target_img : str):
    image_list_path = './images/iitism/bss/'
    image_file_name_list = [(os.path.join(image_list_path, fname), fname) for fname in os.listdir(image_list_path)]
    known_face_encodings = []
    known_face_names = []
    for image_path in image_file_name_list:
        known_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(image_path[0]))[0])
        known_face_names.append(image_path[1][:-5])
    frame = cv2.imread(target_img)
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        if name != "Unknown" and name not in face_names:
            face_names.append(name)
    return face_names