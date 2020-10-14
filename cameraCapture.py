import cv2
import numpy as np
import findAffineMatrix as am

image_file = 'line.jpg'
field_file = 'field.jpg'

point_list = []
field_point = []


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

#image_file = 'line.jpg'
#img = cv2.imread(image_file)

# print("Started")
# cap = cv2.VideoCapture(-1)
#
# img = cap.read() # Initial image
#
# while True:
# 	ret, img = cap.read()
# 	imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# 	cv2.imshow("image", img)
#
# 	if cv2.waitKey(1) & 0xFF == ord('q'):
#         	break
#
#
# cv2.imshow("image", img)
# cv2.waitKey(0)

#Here, you need to change the image name and it's path according to your directory
img = cv2.imread(image_file)
cv2.imshow("image", img)

#calling the mouse click event
cv2.setMouseCallback("image", click_event)
cv2.waitKey(0)

field_img = cv2.imread(field_file)
cv2.imshow("field_image", field_img)

#calling the mouse click event
cv2.setMouseCallback("field_image", click_event_2)
cv2.waitKey(0)

cv2.destroyAllWindows()
A_matrix, translation_vector = am.affineMatrix(point_list, field_point)

print("Transform new point:")
test_point = [[881, 273], [234, 456], [457, 389]]
for p in np.array(test_point):
  image_p = np.dot(A_matrix, p) + translation_vector
  print(p, " mapped to: ", image_p)
  image = cv2.circle(field_img, image_p, 1, )

# image_p = np.dot(A_matrix, test_point) + translation_vector
# print(test_point, " mapped to: ", image_p)

#print("Here 3")
# cap.release()
