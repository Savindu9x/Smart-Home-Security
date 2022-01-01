import face_recognition as frec
import cv2
import numpy as np
import time
import os
import glob
import pickle

#  #initialize the list of known encodings and known names
known_encodings = []
known_names = []
 # Get the current directory and Set the path
current_directory = os.getcwd()
path = os.path.join(current_directory, 'Dataset/')

list_of_files = [f for f in glob.glob(path+'*.jpg')]
# Get the length of list of files
number_files = len(list_of_files)
names = list_of_files.copy()
#
 # Training the Image Dataset
for i in range(number_files):
     globals()['image_{}'.format(i)] = frec.load_image_file(list_of_files[i])
     globals()['image_encoding_{}'.format(i)] = frec.face_encodings(globals()['image_{}'.format(i)])[0]
     known_encodings.append(globals()['image_encoding_{}'.format(i)])
     # Create array of known names
     current = "/home/pi/project/Dataset/"
     names[i] = names[i].replace(current, "")
     names[i] = names[i].replace(".jpg", "")
     known_names.append(names[i])
# Convert the trained encodings and known names into python dictionary.
print(known_names)
data = {"encodings": known_encodings, "names": known_names}
# Opening new pickle model to save the trained model
with open('face_model.pkl', 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('face_model.pkl', 'rb') as handle:
        data = pickle.load(handle)

def faceDetect():
    # Import Trained face models
    video_capture = cv2.VideoCapture(0)
    name = "unknown"
    #name = "pasan"
    process_this_frame = True
    known_encodings = data.get('encodings')
    known_names = data.get('names')
    boxes = []
    encodings = []
    face_names = []
    while True:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        if process_this_frame:
            boxes = frec.face_locations(rgb_small_frame)
            # compute the facial embedding for the face
            encodings = frec.face_encodings(rgb_small_frame, boxes)
            face_names = []
            for face_encoding in encodings:
                # check each small frame for matching faces.
                matches = frec.compare_faces(known_encodings, face_encoding)
                face_distances = frec.face_distance(known_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]
                face_names.append(name)

        process_this_frame = not process_this_frame
        # Display the results
        for (top, right, bottom, left), name in zip(boxes, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            # Input text label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)
        if (cv2.waitKey(1)) & (name != "unknown"):
             time.sleep(10)
             break
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    return name

faceDetect()