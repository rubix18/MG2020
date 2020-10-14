import numpy as np
import cv2
import cameraCapture as cc

A,t = cc.getMatrices()

# input data
# ins = [[1, 1], [2, 3], [3, 2]]  # <- points
# out = [[0, 2], [1, 2], [-2, -1]] # <- mapped to
#
# srcTri = np.float32(ins)
# dstTri = np.float32(out)
# A1 = cv2.getAffineTransform(srcTri, dstTri)
# # output
# print("Affine transformation matrix1:\n", A1)
#
# # calculations
# l = len(ins)
# B = np.vstack([np.transpose(ins), np.ones(l)])
# D = 1.0 / np.linalg.det(B)
# entry = lambda r,d: np.linalg.det(np.delete(np.vstack([r, B]), (d+1), axis=0))
# M = [[(-1)**i * D * entry(R, i) for i in range(l)] for R in np.transpose(out)]
# A, t = np.hsplit(np.array(M), [l-1])
# t = np.transpose(t)[0]
#
# # output
# print("Affine transformation matrix:\n", A)
# print("Affine transformation translation vector:\n", t)
# # unittests
# print("TESTING:")
# for p, P in zip(np.array(ins), np.array(out)):
#   image_p = np.dot(A, p) + t
#   result = "[OK]" if np.allclose(image_p, P) else "[ERROR]"
#   print(p, " mapped to: ", image_p, " ; expected: ", P, result)
