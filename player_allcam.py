#!/usr/bin/env python3

import cv2
import argparse

def display_video_feed(rtsp_address, window_name):
    cap = cv2.VideoCapture(rtsp_address)
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow(window_name, frame)
        else:
            print(f"Unable to open camera on address {rtsp_address}")
            break

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyWindow(window_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rtsp_address", required=True, help="RTSP address of the video stream")
    parser.add_argument("--window_title", required=True, help="Title for the window")
    args = parser.parse_args()

    cv2.namedWindow(args.window_title, cv2.WINDOW_NORMAL)
    display_video_feed(args.rtsp_address, args.window_title)
