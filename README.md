# RTSP streaming using GStreamer

Python implementation to stream camera feed from OpenCV videoCapture via RTSP server using GStreamer 1.0.

## Installation

This implementation has been developed and tested on Ubuntu 16.04 and 18.04. So the installation steps are specific to debian based linux distros.

### Step-1 Install GStreamer-1.0 and related plugins
sudo apt-get install gstreamer1.0-plugins-ugly
### Step-2 Install RTSP server
    sudo apt-get install libglib2.0-dev libgstrtspserver-1.0-dev gstreamer1.0-rtsp
### Requirement
- Python 3.x
- Opencv 3.x or above ( pip install opencv-python )
- pip install cvzone
  
  #install v4l-utils
  sudo apt-get install v4l-utils


### Usage
> Run stream.py with required arguments to start the rtsp server
##### Sample 
    python stream.py --device_id 0 --fps 30 --image_width 640 --image_height 480 --port 8554 --stream_uri /video_stream

    or

    python3 stream.py --device_id 2 --fps 20 --image_width 640 --image_height 480 --port 8554 --stream_uri /video_stream
    
### Visualization

You can view the video feed on `rtsp://server-ip-address:8554/stream_uri`

e.g: `rtsp://192.168.1.12:8554/video_stream`

You can either use any video player which supports rtsp streaming like VLC player or you can use the `open-rtsp.py` script to view the video feed.

Check ip address-ip add

on other side (Ground Station terminal give this command)-

ffplay -fflags nobuffer -flags low_delay -framedrop -strict experimental -rtsp_transport tcp rtsp://me-ubuntu.local:8554/video_stream



### small change by Mehedi Ahamed (For easy use)
#stream.bash- this one serves one cam video feed




#stream_allcam.bash- adjust port no and total device number to serve all cam feed




#player_allcam.py- this is configured for to be used by cli/player_allcam.bash



#player_allcam.bash- adjust port no and total device number to show all cam feed


