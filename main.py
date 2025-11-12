import cv2
import numpy as np

# reference document
# file = input("Reference document file name: ")
file = "ref.png"
ref = cv2.imread(file, 1)
ref = cv2.resize(ref, (int(ref.shape[1] / 3),int(ref.shape[0] / 3)))

# scanned document
# file = input("Image to align file name: ")
file = "scan.jpg"
img = cv2.imread(file, 1)
img = cv2.resize(img, (int(img.shape[1] / 3),int(img.shape[0] / 4)))

ref_g = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

MAX_FEATURES = 500
orb = cv2.ORB_create(MAX_FEATURES)
keypoints1, descriptors1 = orb.detectAndCompute(ref_g, None)
keypoints2, descriptors2 = orb.detectAndCompute(img_g, None)

matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
matches = list(matcher.match(descriptors1, descriptors2, None))
matches.sort(key = lambda x: x.distance, reverse = False)

numGoodMatches = int(len(matches) * 0.1)
matches = matches[:numGoodMatches]

points1 = np.zeros((len(matches), 2), dtype=np.float32)
points2 = np.zeros((len(matches), 2), dtype=np.float32)

for i, match in enumerate(matches):
    points1[i, :] = keypoints1[match.queryIdx].pt
    points2[i, :] = keypoints2[match.trainIdx].pt

h, mask = cv2.findHomography(points2, points1, cv2.RANSAC)

height,width,_ = ref.shape
img_scan = cv2.warpPerspective(img, h, (width, height))

#save data
cv2.imwrite("output.png",img_scan)

#optionally show result for user
cv2.imshow("Scanned", img_scan)
cv2.waitKey(0)