import cv2
import numpy as np
import findAffineMatrix as am

image_file = 'line.jpg'
field_file = 'field.jpg'

point_list = []
field_point = []

def affineMatrix(in_points, map_to_points) :

    # calculations
    l = len(in_points)
    B = np.vstack([np.transpose(in_points), np.ones(l)])
    D = 1.0 / np.linalg.det(B)
    entry = lambda r,d: np.linalg.det(np.delete(np.vstack([r, B]), (d+1), axis=0))
    M = [[(-1)**i * D * entry(R, i) for i in range(l)] for R in np.transpose(map_to_points)]
    A, t = np.hsplit(np.array(M), [l-1])
    t = np.transpose(t)[0]

    # output
    print("Affine transformation matrix:\n", A)
    print("Affine transformation translation vector:\n", t)
    # unittests
    print("TESTING:")
    for p, P in zip(np.array(in_points), np.array(map_to_points)):
      image_p = np.dot(A, p) + t
      result = "[OK]" if np.allclose(image_p, P) else "[ERROR]"
      print(p, " mapped to: ", image_p, " ; expected: ", P, result)

    return A, t

def click_event(event, x, y, flags, img):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,",",y)
        point_list.append([x,y])
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY = str(x)+", "+str(y)
        cv2.circle(img, (x,y), 2 , (0,0,255), 2)
        cv2.putText(img, strXY, (x+5,y), font, 0.5, (255,255,0), 2)
        cv2.imshow("image", img)


def click_event_2(event, x, y, flags, f_img):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,",",y)
        field_point.append([x,y])
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY = str(x)+", "+str(y)
        cv2.circle(f_img, (x,y), 2 , (0,0,255), 2)
        cv2.putText(f_img, strXY, (x+5,y), font, 0.5, (255,255,0), 2)
        cv2.imshow("field_image", f_img)


# img = 0
# field_img = 0

# def getMatrices():
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
test_img = cv2.imread(image_file)
cv2.imshow("image", test_img)

#calling the mouse click event
cv2.setMouseCallback("image", click_event, test_img)
cv2.waitKey(0)

field_img = cv2.imread(field_file)
cv2.imshow("field_image", field_img)

#calling the mouse click event
cv2.setMouseCallback("field_image", click_event_2, field_img)
cv2.waitKey(0)

cv2.destroyAllWindows()
A_matrix, translation_vector = affineMatrix(point_list, field_point)

print("Transform new point:")
test_point = [625, 200]
image_p = np.dot(A_matrix, test_point) + translation_vector
print(test_point, " mapped to: ", image_p)
image = cv2.circle(field_img, (int(image_p[0]), int(image_p[1])), 2, (0, 0, 255), 10)

# # test_point = [[881, 273], [234, 456], [457, 389]]
# for p in np.array(test_point):
#   image_p = np.dot(A_matrix, p) + translation_vector
#   print(p, " mapped to: ", image_p)
#   image = cv2.circle(field_img, (image_p[0], image_p[1]), 1, (0, 0, 255), 1)

cv2.imshow("adjusted_image", image)
cv2.waitKey(0)
#print("Here 3")
# cap.release()

# return A_matrix, translation_vector

