import cv2
import os 

 
files = os.walk("to_be_resized", topdown=False)
list_to_resize = os.listdir("to_be_resized")
print(list_to_resize)

for name in list_to_resize:
    name_path = "to_be_resized/" + name
    img = cv2.imread(name_path, 1)
    resized_img = cv2.resize(img, (100, 100))
    ref_name =  name.replace(".jpg", "")
    final_name = f"resized/{ref_name}_resized.jpg"
    cv2.imwrite(final_name, resized_img)