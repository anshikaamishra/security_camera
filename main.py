import datetime
import winsound

import cv2
from twilio.rest import Client

cam = cv2.VideoCapture(0)

def change_res(width, height):
    cam.set(3, width)
    cam.set(4, height)

change_res(5000,3000)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt_tree.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

recording = True
if recording is True:
    print("Recording Started")

frame_size = (int(cam.get(3)), int(cam.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
out = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20, frame_size)

fps = 0

with open('credentials.txt', 'r') as myfile:
    data = myfile.read()

info_dict = eval(data)

def send_message(body, info_dict):
    # Your Account SID from twilio.com/console
    account_sid = info_dict['account_sid']

    # Your Auth Token from twilio.com/console
    auth_token = info_dict['auth_token']

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        messaging_service_sid='account_sid',
        body= body,
        to='+91123456789'
    )
    print(message.sid)

while cam.isOpened():
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()


    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = body_cascade.detectMultiScale(gray, 1.3, 5)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
    for c in contours:
        if cv2.contourArea(c) < 30000:
            continue
        x, y, w, h, = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        winsound.Beep(500, 200)
        entry_time = datetime.datetime.now().strftime("%A, %I-%M-%S %p %d %B %Y")
        body2 = "Alert: Some movement detected in the Room at {}".format(entry_time)
        send_message(body2, info_dict)

    cv2.putText(frame1, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame1.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 1)

    out.write(frame1)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Recording Stopped")
        break
    cv2.imshow('Security Cam', frame1)

out.release()
cam.release()
cv2.destroyAllWindows()
