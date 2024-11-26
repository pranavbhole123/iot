import cv2
import os
import urllib.request

# Download Haar Cascade if not present
haar_url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
haar_path = "haarcascade_frontalface_default.xml"

if not os.path.exists(haar_path):
    print("Downloading Haar Cascade...")
    urllib.request.urlretrieve(haar_url, haar_path)
    print("Download complete.")

# Initialize the Haar Cascade classifier
face_cascade = cv2.CascadeClassifier(haar_path)

# Initialize camera
cap = cv2.VideoCapture(0)  # 0 for default camera

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Face Detection', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
