
import cv2
import numpy as np
import matplotlib as plt

#In this code, first click 3 points on real image and close it. 
#Then click 3 points on field lines image and close it.

#This will display all the available mouse click events  
#events = [i for i in dir(cv2) if 'EVENT' in i]
#print(events)

#This variable we use to store the pixel location

image_file = 'line.jpg'
field_file = 'field.jpg'


point_list = []
field_point = []
#click event function
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,",",y)
        point_list.append([x,y])
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY = str(x)+", "+str(y)
        cv2.circle(img, (x,y), 2 , (0,0,255), 2)
        cv2.putText(img, strXY, (x+5,y), font, 0.5, (255,255,0), 2)
        cv2.imshow("image", img)


def click_event_2(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,",",y)
        field_point.append([x,y])
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY = str(x)+", "+str(y)
        cv2.circle(field_img, (x,y), 2 , (0,0,255), 2)
        cv2.putText(field_img, strXY, (x+5,y), font, 0.5, (255,255,0), 2)
        cv2.imshow("field_image", field_img)



# Capture image from Webcam
cap = cv2.VideoCapture(-1)
img = cap.read() # Initial image

while True:
        ret, img = cap.read()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        cv2.imshow("image", img)
        if cv2.waitKey(1) & 0xFF == ord('c'):
                break

cv2.imshow("image", img)

#frame = img.copy()
#frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Or use prefill image
#Here, you need to change the image name and it's path according to your directory
#img = cv2.imread(image_file)


#calling the mouse click event
cv2.setMouseCallback("image", click_event)
cv2.waitKey(0)
cap.release()


field_img = cv2.imread(field_file)
cv2.imshow("field_image", field_img)

#calling the mouse click event
cv2.setMouseCallback("field_image", click_event_2)
cv2.waitKey(0)

cv2.destroyAllWindows()

rows,cols,ch = img.shape

srcTri = np.float32(point_list)
dstTri = np.float32(field_point)

warp_mat = cv2.getAffineTransform(srcTri, dstTri)
warp_dst = cv2.warpAffine(img, warp_mat, (img.shape[1], img.shape[0]))
# Rotating the image after Warp
center = (warp_dst.shape[1]//2, warp_dst.shape[0]//2)
angle = -50
scale = 0.6
rot_mat = cv2.getRotationMatrix2D( center, angle, scale )
warp_rotate_dst = cv2.warpAffine(warp_dst, rot_mat, (warp_dst.shape[1], warp_dst.shape[0]))
#cv2.imshow('Source image', field_img)
cv2.imshow('Warp', warp_dst)
#cv2.imshow('Warp + Rotate', warp_rotate_dst)

cv2.waitKey(0)

