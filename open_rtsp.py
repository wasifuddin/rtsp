#!/usr/bin/env python3

import cv2
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--rtsp_address", required=True, help="RTSP address of the video stream")
parser.add_argument("--window_title", required=True, help="Title for the window")
args = parser.parse_args()

# Open the RTSP stream
cv2.namedWindow(args.window_title, cv2.WINDOW_NORMAL)
cap = cv2.VideoCapture(args.rtsp_address)

while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow(args.window_title, frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    else:
        print(f"Unable to open camera at {args.rtsp_address}")
        break

cap.release()
cv2.destroyAllWindows()
