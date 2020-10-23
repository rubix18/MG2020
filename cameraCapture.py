import cv2
import numpy as np
import findAffineMatrix as am



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

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,",",y)
        params[1].append([x,y])
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY = str(x)+", "+str(y)
        cv2.circle(params[0], (x,y), 2 , (0,0,255), 2)
        cv2.putText(params[0], strXY, (x+5,y), font, 0.5, (255,255,0), 2)
        cv2.imshow("image", params[0])


def click_event_2(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,",",y)
        params[1].append([x,y])
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY = str(x)+", "+str(y)
        cv2.circle(params[0], (x,y), 2 , (0,0,255), 2)
        cv2.putText(params[0], strXY, (x+5,y), font, 0.5, (255,255,0), 2)
        cv2.imshow("field_image", params[0])




