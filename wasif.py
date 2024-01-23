#!/usr/bin/env python3

import cv2
import argparse
import numpy as np
active_dev = []
file_path = 'valid_camport.txt'
dev_list = []

with open(file_path, 'r') as file:
    for line in file:
        line = line.strip()
        cap = cv2.VideoCapture(str(line.strip()))
        ret, frame = cap.read()
        if ret:
            dev_list.append(str(line))
        # else:
        #     print("Fail")

# lines_list now contains all lines from the file
print(dev_list)

def display_video_feed():

    global dev_list
    # cap2 = cv2.VideoCapture("rtsp://192.168.23.176:8567/video_stream")
    i = 8567
    while True:
        i = i+1
        print(i)
        cap1 = cv2.VideoCapture(f"rtsp://192.168.23.176:{i}/video_stream")
        # cap2 = cv2.VideoCapture(dev_list[1])   # cap1 = cv2.VideoCapture("rtsp://192.168.23.176:8567/video_stream")
        # cap2 = cv2.VideoCapture("rtsp://192.168.23.176:8569/video_stream")
        try:
            while True:
                ret1, frame1 = cap1.read()
                # ret2, frame2 = cap2.read()
                if ret1:
                    # frame2 = cv2.resize(frame2, (frame1.shape[1], frame2.shape[0]))
                    # com_frame = np.hstack((frame1,frame2))
                    cv2.imshow("69", frame1)
                #
                # elif ret2:
                #     # frame2 = cv2.resize(frame2, (frame1.shape[1], frame2.shape[0]))
                #     # com_frame = np.hstack((frame1,frame2))
                #     cv2.imshow("67", frame2)
                else:
                    # print(f"Unable to open camera on address {rtsp_address1}")
                    break

                key = cv2.waitKey(1)
                if key == ord('q'):
                    break

            cap1.release()
        except:
            print("Retreat", i)
            continue
    # cap2.release()

if __name__ == "__main__":


    # display_video_feed()
    pass