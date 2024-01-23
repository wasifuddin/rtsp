#!/bin/bash

launch_python_script() {
    python3 stream.py \
        --device_id "${1}" \
        --fps 20 \
        --image_width 640 \
        --image_height 480 \
        --port "${2}" \
        --stream_uri "${3}" &
    sleep 5  # Add a delay to allow the stream to initialize
}

video_devices=($(v4l2-ctl --list-devices | grep -oP '/dev/video\K\d+'))

cleanup_and_exit() {
    echo "Cleaning up and exiting..."
    pkill -P $$
    exit 0
}

# Trap Ctrl+C and call the cleanup function
trap cleanup_and_exit SIGINT

if [ ${#video_devices[@]} -eq 0 ]; then
    echo "No video devices found."
    exit 1
fi

# Set base port number
base_port=8554

for device in "${video_devices[@]}"; do
    device_id=$(echo "${device}" | grep -oP '\d+')
    stream_uri="/video_stream"
    echo "xxxxxx ---- $device_id"
    launch_python_script "$device_id" "$base_port" "$stream_uri"
    ((base_port++))
done

# Wait for all background processes to finish
wait
