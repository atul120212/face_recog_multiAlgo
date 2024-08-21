import numpy as np
import pickle
import os
import cv2
import time
import imutils
from RecorgOutPut import RecorgoniseObject

curr_path = os.getcwd()

print("Loading face detection model")
proto_path = os.path.join(curr_path, 'model', 'deploy.prototxt')
model_path = os.path.join(curr_path, 'model', 'res10_300x300_ssd_iter_140000.caffemodel')
face_detector = cv2.dnn.readNetFromCaffe(prototxt=proto_path, caffeModel=model_path)

print("Loading face recognition model")
recognition_model = os.path.join(curr_path, 'model', 'openface_nn4.small2.v1.t7')
face_recognizer = cv2.dnn.readNetFromTorch(model=recognition_model)

recognizer = pickle.loads(open('recognizer.pickle', "rb").read())
le = pickle.loads(open('le.pickle', "rb").read())


def Recogonise(identifier):
    print("Starting test video file")
    if(identifier=="0"):
        vs = cv2.VideoCapture(0)
    else:
        temp_folder = os.path.join('Temp')
        vs = cv2.VideoCapture(os.path.join(temp_folder, identifier))
    # vs = cv2.VideoCapture(0)
    time.sleep(1)
    Rec = []

    while True:
        try:
            ret, frame = vs.read()
            # frame = cv2.rotate(frame, cv2.ROTATE_180)  # Rotate fram
            frame = imutils.resize(frame, width=600)

            (h, w) = frame.shape[:2]

            image_blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0),
                                               False,
                                               False)

            face_detector.setInput(image_blob)
            face_detections = face_detector.forward()
            face_count=0
            for i in range(0, face_detections.shape[2]):
                confidence = face_detections[0, 0, i, 2]
                if confidence >= 0.5:
                    if i > 0:
                        face_count += 1
                    box = face_detections[0, 0, i, 3:7] * np.array([w, h, w, h])

                    (startX, startY, endX, endY) = box.astype("int")

                    face = frame[startY:endY, startX:endX]

                    (fH, fW) = face.shape[:2]
                    if fH < 20 or fW < 20:
                        continue  # Skip small faces
                    face_blob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96), (0, 0, 0), True, False)

                    face_recognizer.setInput(face_blob)
                    vec = face_recognizer.forward()

                    preds = recognizer.predict_proba(vec)[0]
                    j = np.argmax(preds)
                    proba = preds[j]
                    name = le.classes_[j]

                    # if(proba * 100)>77:
                    text = "{}: {:.2f}".format(name, proba * 100)
                    # Rec = {proba * 100: name}
                    Rec.append(RecorgoniseObject(Empid=name, confidence=str(proba * 100)))

                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
                    cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)

            # Display the face count on the frame
            face_count_text = f"Faces detected: {face_count+1}"
            if face_count==0:
                cv2.putText(frame, face_count_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
            if face_count > 0:
                cv2.putText(frame, face_count_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break
        except Exception as e:
            print('Somthing went wrong..')
            print(str(e))

            break
    # print(Rec);

    cv2.destroyAllWindows()


#Recogonise('testvideo.mp4')
