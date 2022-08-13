# Security Camera Alert
The presence of a human safety officer is not an effective process of security and is not reliable. In such scenarios, this framework provides proper interloper detection and protects the owner's property.

The proposed system uses a webcam and python code for detecting the intruder and sending an alert SMS. On the client-side, the video is captured continuously and filtered. The filtered information is sent to the server-side. And it displays the status of the interloper with a time and date stamp. It starts recording the current frame. After the movement is detected in the current frame the framework alerts the user or owner by sending an alert message using a Twilio API and saves the recorded footage into the local storage. 

## Requirements
Make sure you have 'OpenCV' installed in your Python IDLE:
```
import cv2 as cv
```

Install twilio from PyPi using pip, a package manager for Python.
```
pip install twilio
```

Sign up https://www.twilio.com/try-twilio
