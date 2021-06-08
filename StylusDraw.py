import cv2
import numpy as np

frameWidth = 640
frameHeight = 580

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

myColors = [[0, 0, 0, 179, 171, 28],    #stylus
            [0, 165, 81, 7, 255, 255]]  #red marker
myColName = ['Stylus', 'Red Marker']

colId = [[0, 0, 0],
         [0, 0, 255]]

# myPoints = [] #[x, y, colId]

def findColor(img, myColor):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    newPoints = []
    for ij, color in enumerate(myColor):
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        # cv2.imshow(myColName[ij], mask)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x,y), 10, colId[ij], cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x, y, colId[ij]])
    return newPoints

def getContours(img):
    contours, heirarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y

def drawOnCanvas(point):
    for pnt in point:
        cv2.circle(imgResult, (pnt[0], pnt[1]), 10, (pnt[2], pnt[3], pnt[4]), cv2.FILLED)

myPoint = []

while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors)

    if len(newPoints) != 0:
        for newP in newPoints:
            myPoint.append([newP[0], newP[1], newP[2][0], newP[2][1], newP[2][2]])
    if len(myPoint) != 0:
        drawOnCanvas(myPoint)

    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break