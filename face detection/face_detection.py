import cv2
import os


# loading face cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

this_folder = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(this_folder, "news.jpg")
img = cv2.imread(my_file)

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

# detecting image
faces = face_cascade.detectMultiScale(gray_img, 
scaleFactor=1.1,
minNeighbors=5)

# drawing rectange around face in image
for x, y, w, h in faces:
    img = cv2.rectangle(img, (x, y),(x + w, y + h), (0,255,0), 3)


print(type(faces))
print(faces)

resized = cv2.resize(img, (int(img.shape[1]/3), int(img.shape[0]/3)))


cv2.imshow("Detected", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()