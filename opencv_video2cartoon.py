import cv2
import numpy as np


def cartoonize_frame(frame, k):
    data = np.float32(frame).reshape((-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    result = centers[labels.flatten()]
    cartoon_frame = result.reshape(frame.shape)
    return cartoon_frame


cap = cv2.VideoCapture('./PETS09-S2L1-raw.webm')

fourcc = cv2.VideoWriter.fourcc(*'XVID')
out = cv2.VideoWriter('cartoonized_video.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    cartoon_frame = cartoonize_frame(frame, 10)
    out.write(cartoon_frame)
    cv2.imshow('Frame', cartoon_frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
