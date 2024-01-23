#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import necessary argumnets
import gi
import cv2
import argparse
import numpy as np
import cvzone
import threading
# import required library like Gstreamer and GstreamerRtspServer
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib

dev_list = []
check_state = 0
cam_restart = 0
def valid_port():
    global dev_list, port_initialise, check_state, cam_restart
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
    port_initialise = threading.Thread(target=valid_port)
    cam_restart = 1
    check_state = 0
    dev_list = list(set(dev_list))
    print("THE LIST   ::::::::: ", dev_list)
port_initialise = threading.Thread(target=valid_port)
valid_port()
# Sensor Factory class which inherits the GstRtspServer base class and add
# properties to it.
class SensorFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, **properties):
        print("init")
        super(SensorFactory, self).__init__(**properties)
        self.cap1 = cv2.VideoCapture(dev_list[0])
        self.cap2 = cv2.VideoCapture(dev_list[1])
        self.cap3 = cv2.VideoCapture(dev_list[2])
        # self.valid_ports = ["/dev/video0", "/dev/video2", "/dev/video4"]  # Initialize the list of valid ports
        self.number_frames = 0
        self.fps = opt.fps
        self.duration = 1 / self.fps * Gst.SECOND  # duration of a frame in nanoseconds
        self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                             'caps=video/x-raw,format=BGR,width={},height={},framerate={}/1 ' \
                             '! videoconvert ! video/x-raw,format=I420 ' \
                             '! x264enc speed-preset=ultrafast tune=zerolatency ' \
                             '! rtph264pay config-interval=1 name=pay0 pt=96' \
            .format(opt.image_width, opt.image_height, self.fps)

    # method to capture the video feed from the camera and push it to the
    # streaming buffer.




    def on_need_data(self, src, length):
        global dev_list, check_state, cam_restart, loop
        if self.cap1.isOpened():
            print("on_need_read_data")
            ret1, frame1 = self.cap1.read()
            ret2, frame2 = self.cap2.read()
            ret3, frame3 = self.cap3.read()
            img_list = []
            print("Img List populate")
            if ret1 or ret2 or ret3:

                if ret1:
                    # It is better to change the resolution of the camera
                    # instead of changing the image shape as it affects the image quality.
                    frame1 = cv2.resize(frame1, (opt.image_width, opt.image_height), interpolation=cv2.INTER_LINEAR)
                    frame1 = cv2.putText(frame1, "1", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                                         cv2.LINE_AA)
                    img_list.append(frame1)

                if ret2:
                    frame2 = cv2.resize(frame2, (opt.image_width, opt.image_height), interpolation=cv2.INTER_LINEAR)
                    frame2 = cv2.putText(frame2, "2", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                                         cv2.LINE_AA)
                    img_list.append(frame2)
                if ret3:
                    frame3 = cv2.resize(frame3, (opt.image_width, opt.image_height), interpolation=cv2.INTER_LINEAR)
                    frame3 = cv2.putText(frame3, "3", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                                         cv2.LINE_AA)
                    img_list.append(frame3)
                print("THE IMG  ::::::::: ", len(img_list))

                frame = cvzone.stackImages(img_list, 1, 0.5)
                frame = cv2.resize(frame, (opt.image_width, opt.image_height))

                if cam_restart ==1 and check_state == 0 and len(img_list)<3:
                    print("camera restart")
                    self.cap1 = cv2.VideoCapture(dev_list[0])
                    self.cap2 = cv2.VideoCapture(dev_list[1])
                    self.cap3 = cv2.VideoCapture(dev_list[2])
                    cam_restart = 0


                print("THE LESR", len(img_list))
                if len(img_list) != 3 and check_state ==0:
                    print("Cam Disconneted")
                    check_state =1
                    port_initialise.start()


                    loop.run()


                print("Data Passed to Remote")
                data = frame.tostring()
                buf = Gst.Buffer.new_allocate(None, len(data), None)
                buf.fill(0, data)
                buf.duration = self.duration
                timestamp = self.number_frames * self.duration
                buf.pts = buf.dts = int(timestamp)
                buf.offset = timestamp
                self.number_frames += 1
                retval = src.emit('push-buffer', buf)
                print('pushed buffer, frame {}, duration {} ns, durations {} s'.format(self.number_frames,
                                                                                       self.duration,
                                                                                       self.duration / Gst.SECOND))
                if retval != Gst.FlowReturn.OK:
                    print(retval)

    # attach the launch string to the override method
    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)

    # attaching the source element to the rtsp media
    def do_configure(self, rtsp_media):
        self.number_frames = 0
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)


# Rtsp server implementation where we attach the factory sensor with the stream uri
class GstServer(GstRtspServer.RTSPServer):
    def __init__(self, **properties):
        super(GstServer, self).__init__(**properties)
        self.factory = SensorFactory()
        self.factory.set_shared(True)
        self.set_service(str(opt.port))
        self.get_mount_points().add_factory(opt.stream_uri, self.factory)
        self.attach(None)


# getting the required information from the user
parser = argparse.ArgumentParser()
parser.add_argument("--device_id", required=True, help="device id for the \
                video device or video file location")
parser.add_argument("--fps", required=True, help="fps of the camera", type=int)
parser.add_argument("--image_width", required=True, help="video frame width", type=int)
parser.add_argument("--image_height", required=True, help="video frame height", type=int)
parser.add_argument("--port", default=8554, help="port to stream video", type=int)
parser.add_argument("--stream_uri", default="/video_stream", help="rtsp video stream uri")
opt = parser.parse_args()

try:
    opt.device_id = int(opt.device_id)

except ValueError:
    pass

# initializing the threads and running the stream on loop.
# GLib.threads_init()
Gst.init(None)
server = GstServer()
# loop = GObject.MainLoop()
loop = GLib.MainLoop()

loop.run()