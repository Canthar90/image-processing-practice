import cv2, time, pandas
from datetime import datetime


first_frame = None
status_list = [None, None]
video = cv2.VideoCapture(0)
rec_times = []
time.sleep(5) #delay for me to hide from camera :]
flag = False
delay_cycles_nr = 0
df = pandas.DataFrame(columns=["Start", "End"])

while True:
    
    check, frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0) #blurring removing the noise from image
    
    # below section is all about delay i use droid cam and there is delay with first frames from camera
    # 20 seems to work fine
    if first_frame is None:
        if flag and delay_cycles_nr < 20:
            delay_cycles_nr += 1
            continue
        elif flag and delay_cycles_nr >= 20:
            first_frame = gray
            continue
        flag = True
        continue
    
    delta_frame = cv2.absdiff(first_frame, gray)  #comparing frames
    
    thresh_delta = cv2.threshold(delta_frame, 50, 255, cv2.THRESH_BINARY)[1]
    thresh_delta = cv2.dilate(thresh_delta, None, iterations=3)
    
    (cnts, _) =cv2.findContours(thresh_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #creating contures
    
    for contour in cnts:
        if cv2.contourArea(contour) < 1500:
            continue
        status = 1
        
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
    
    status_list.append(status)
    if status_list[-1] == 1 and status_list[-2] ==0: # rising edge detection
        rec_times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-1] == 1: # falling edge detection
        rec_times.append(datetime.now())
        
    cv2.imshow("Delta frame" ,delta_frame)
    cv2.imshow("first frame", first_frame)
    cv2.imshow("treshold frame", thresh_delta)
    
    cv2.imshow("Capturing", frame)
    
    
    key = cv2.waitKey(1)
    if key==ord('q'):
        if status == 1:
            rec_times.append(datetime.now())
        break
    
print(status_list)
print(rec_times)

for i in range(0, len(rec_times)-1, 2):
    print(i)
    print(i+1)
    print(len(rec_times))
    df = df.append({"Start": rec_times[i], "End": rec_times[i+1]}, ignore_index=True)    
df.to_csv("Times.csv")
video.release()

cv2.destroyAllWindows()