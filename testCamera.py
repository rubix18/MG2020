import cv2

#image_file = 'line.jpg'
#img = cv2.imread(image_file)

print("Started")
cap = cv2.VideoCapture(-1)

img = cap.read() # Initial image

while True:
	ret, img = cap.read()
	imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	cv2.imshow("image", img)

	if cv2.waitKey(1) & 0xFF == ord('q'):
        	break


cv2.imshow("image", img)
cv2.waitKey(0)

#cv2.destroyAllWindows()

#print("Here 3")
cap.release()
