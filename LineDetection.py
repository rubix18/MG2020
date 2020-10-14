import os
import cv2
import numpy as np
import math

import LineCluster as Cluster

def LineDetection(file, imageShow = False):
    #Read image
    image = cv2.imread(file, cv2.IMREAD_COLOR)

    #Split channels
    b, g, r = cv2.split(image)

    #Find green parts
    ones = np.ones(g.shape) / 1000000
    a = g.astype(np.float64) / (r.astype(np.float64) + b.astype(np.float64) + g.astype(np.float64) + ones)
    green = (255 * (a > 0.41)).astype(np.uint8)

    #Erode and dilate
    kernel = np.ones((13,13), np.uint8)
    opening = cv2.morphologyEx(green, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=5)

    morphology = cv2.merge((closing, closing, closing))

    gray = cv2.cvtColor(morphology, cv2.COLOR_BGR2GRAY)
    (thresh, bnw) = cv2.threshold(gray, 127, 1, cv2.THRESH_BINARY)

    #Gaussian blur
    gauss = cv2.GaussianBlur(image, (3,3), 0)

    # Find the edges using canny detector
    edges = cv2.Canny(gauss, 50, 100)

    #edges in green ground
    ground = edges * bnw

    #Hough Transform
    hough_image = image.copy()
    lines = cv2.HoughLinesP(ground, 1, np.pi/180, 115, minLineLength=100, maxLineGap=50)

    if lines is None:
        return []

    lines = [_[0] for _ in lines]

    if imageShow:
        cv2.imshow("Original Image", image)
        #cv2.waitKey(0)

        cv2.imshow("Black and white", bnw * 255)
        #cv2.waitKey(0)

        cv2.imshow("Edge", edges)
        #cv2.waitKey(0)

        cv2.imshow("Ground", ground)
        #cv2.waitKey(0)

        for line in lines:
            x1, y1, x2, y2 = line
            cv2.line(hough_image, (x1, y1), (x2, y2), (0, 255, 255), 1)

        cv2.imshow("Hough transform", hough_image)
        #cv2.waitKey(0)

    return lines

if __name__ == "__main__":
    file = 'line.jpg'
    lines = LineDetection(file, True)
    lines = Cluster.LineCluster(lines)

    image = cv2.imread(file)
    for line in lines:
        x1, y1, x2, y2 = [int(_) for _ in line]
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Show cluster result
    cv2.imshow("Line cluster", image)
    cv2.waitKey(0)