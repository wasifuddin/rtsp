#!/bin/bash

base_ip="192.168.23.176"
base_port=8554
max_feeds=500

for ((i=0; i<max_feeds; i++)); do
    current_port=$((base_port + i))
    rtsp_address="rtsp://${base_ip}:${current_port}/video_stream"

    # Check if the port is valid
    if nc -zv $base_ip $current_port; then
        echo "Launching stream for address ${rtsp_address}"
        
        # Call your Python script with the dynamic arguments
        python3 player_allcam.py \
            --rtsp_address "${rtsp_address}" \
            --window_title "RTSP View - Port ${current_port}" &
    else
        echo "Skipping port ${current_port} as it is not available."
    fi
done

# Wait for all background processes to finish
wait
