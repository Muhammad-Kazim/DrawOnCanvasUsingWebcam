import cv2
import numpy as np

def empty():
    pass

# path = 'Picture/Stylus.jpg'
frameWidth = 600
frameHeight = 400

cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 640, 250)
cv2.createTrackbar("Hue Min", "Trackbars", 102, 179, empty)
cv2.createTrackbar("Hue Max", "Trackbars", 142, 179, empty)
cv2.createTrackbar("Sat Min", "Trackbars", 25, 255, empty)
cv2.createTrackbar("Sat Max", "Trackbars", 153, 255, empty)
cv2.createTrackbar("Val Min", "Trackbars", 0, 255, empty)
cv2.createTrackbar("Val Max", "Trackbars", 255, 255, empty)

while True:
    # img = cv2.imread(path)
    success, imgResize = cap.read()

    # imgResize = cv2.resize(img, (300, 500))
    imgHSV = cv2.cvtColor(imgResize, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("Hue Min", "Trackbars")
    h_max = cv2.getTrackbarPos("Hue Max", "Trackbars")
    s_min = cv2.getTrackbarPos("Sat Min", "Trackbars")
    s_max = cv2.getTrackbarPos("Sat Max", "Trackbars")
    v_min = cv2.getTrackbarPos("Val Min", "Trackbars")
    v_max = cv2.getTrackbarPos("Val Max", "Trackbars")
    print(h_min, h_max, s_min, s_max, v_min, v_max)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(imgResize, imgResize, mask=mask)

    #0, 179, 0, 171, 0, 28 stylus
    #0, 7, 165, 255, 81, 255 #red marker

    stack = np.hstack((imgResize, imgResult))

    cv2.imshow('Original', stack)
    # cv2.imshow('Original HSV', imgHSV)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break