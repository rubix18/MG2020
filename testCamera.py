import cv2

#image_file = 'line.jpg'
#img = cv2.imread(image_file)

print("Started")
cap = cv2.VideoCapture(-1)

while True:
	print("Captured video")
	ret, img = cap.read()

	print("Here 1")
	cv2.imshow("image", img)

	if cv2.waitKey(1 == 27):
		break

cv2.destroyAllWindows()

print("Here 3")
cap.release()
