import cv2
import numpy as np
import matplotlib
from matplotlib.pyplot import imshow
from matplotlib import pyplot as plt
import pandas as pd
from scipy import stats

#Start Function Definitions

def curvedetect():
    x_vals = []
    y_vals = []
    
    for y in range(225):
        for x in range(300):
            if(edges[y][x] == 255):
                x_vals.append(x)
                y_vals.append(300 - y)
    
    global centerX
    global centerY

    for nums in range(len(x_vals)):
        if(x_vals[nums]>140 and x_vals[nums]<160):
            centerX.append(x_vals[nums])
            centerY.append(y_vals[nums])
            
    cutoff_num = round(0.35*len(centerY))
    centerY = centerY[cutoff_num:]
    centerX = centerX[cutoff_num:]



def doItAll(orig_img):
    global edges
    edges = []
    #Pre-Processing of the image
    gray = cv2.cvtColor(orig_img,cv2.COLOR_BGR2GRAY)
    slp_int = [0,0]

    #Gaussian Blur
    kernel_size = 17
    blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

    #Canny edge detection
    low_threshold = 10 #change values later
    high_threshold = 100 #same here
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

    #Hough Line Transform
    rho = 1  # distance resolution in pixels of the Hough grid (1)
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 5  # minimum number of votes (intersections in Hough grid cell) (15) (Experiment with this)
    min_line_length = 100  # minimum number of pixels making up a line (50)
    max_line_gap = 20  # maximum gap in pixels between connectable line segments (20)
    line_image = np.copy(orig_img) * 0  # creating a blank to draw lines on

    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)

    global centerX
    global centerY
    
    centerX = []
    centerY = []

    linesarray = []
    #print(lines)
    #Is it a line?

    try:
        for line in lines:
            for x1,y1,x2,y2 in line:
                linesarray.append(np.sqrt(x1*x1+y1*y1))
        
        biggestnum = linesarray[0]
        indexnum = 0

        for nums in range(len(linesarray)):
            if linesarray[nums] > biggestnum:
                biggestnum = linesarray[nums]
                indexnum = nums
        
        global slp_int
        slp_int = [0,0]

        x1 = lines[indexnum][0][0]
        y1 = lines[indexnum][0][1]
        x2 = lines[indexnum][0][2]
        y2 = lines[indexnum][0][3]
        #print("drawing a line")
        cv2.line(orig_img,(x1,y1),(x2,y2),(255,0,0),5)
        #print("(" + str(x1) + ", " + str(x2) + ")")

        if(x2 == x1):
            slp_int[0] = 1000000 + x2
            slp_int[1] = 1234
        else:
            slp_int[0] = (y2-y1)/(x2-x1)
            slp_int[1] = y1 - (x1)*(y2-y1)/(x2-x1)   
        
    except TypeError:
        #It's a curve
        curvedetect()
        try:
            slope, intercept, r_value, p_value, std_err = stats.linregress(centerX, centerY)
        except ValueError:
            return "straight"
        
        
        slp_int[0] = slope
        slp_int[1] = intercept
        try:
            cv2.line(orig_img,(0,int(225-slp_int[1])),(300,225-(int(300*slp_int[0] + slp_int[1]))),(255,0,0))
        except:
            return "straight"
       
    #Now that we have the slope and intercept, what is the optimal course? 
    mid_val = slp_int[0]*150+slp_int[1]
    if(mid_val < 200 and mid_val > 0):
        turnVal = 1
        if(np.rad2deg(np.arctan(slp_int[0])) > 0):
            turnVal = -1*(90-np.rad2deg(np.arctan(slp_int[0])))
        else:
            turnVal = 1*(90-abs(np.rad2deg(np.arctan(slp_int[0]))))

        if(turnVal >= -20 and turnVal <= 25):
            return("straight")
        else:
            return(str(turnVal))
    else:
        return("straight")


def doSomething():
    print("doing something")

#End Function Definitions 

cap = cv2.VideoCapture('C:\Yash\SciFairVid3.mp4') #input video
global x
x = 0
while cap.isOpened():

    ret,frame = cap.read()
    orig_img = frame
    orig_img = cv2.resize(orig_img,(300,225))
    message = doItAll(orig_img)


    font = cv2.FONT_HERSHEY_SIMPLEX
    try:
        cv2.putText(orig_img, message,(10,100), font, 1,(255,0,0),1,cv2.LINE_AA)
    except ValueError:
        doSomething()
    #cv2.line(orig_img,(xcoor1,int(ycoor1)),(xcoor2,int(ycoor2)),(255,0,0),5)
    list1 = ['CurvedSidewalk',str(x),'.jpg']
    cv2.imwrite("".join(list1),orig_img)
    print("Writing frame " + str(x))
    x = x+1



    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()  # destroy all the opened windows
