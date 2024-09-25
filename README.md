# Webcam calibration with Kalibr

### Deps

docker, python3, python-opencv, git

### Step 1: Measure display data

Display `april_6x6_80x80cm_A0.pdf`

Adjust details the display of `data_inside_container/april_6x6_80x80cm.yaml`.

The values you should put there are literal physical measurements you take from your screen while displaying the pdf.

### Step 2: Collect images

Using the board `april_6x6_80x80cm_A0.pdf` displayed at your screen, without any measument modification since last step...

Run `sudo python takes_pictures_with_computer_camera.py`

Press 's' to take a picture of the board

Point your camera towards the board and take pictures:
- roll to side to side
- move angles
- zoom in and out
- get weird angles from the board
- do a close up to get the distortions that happen for things too close to camera

Press 'esc' to end

### Step 3: Build kalibr

Build image
```
git clone https://github.com/ethz-asl/kalibr.git
cd kalibr
docker build -t kalibr -f Dockerfile_ros1_20_04 .
```

Give screen access to docker container
```
xhost +local:root
```

### Step 4: Create bag file from images

Terminal 1 - Run Kalibr container with roscore
```
sudo docker run -it -e "DISPLAY" -e "QT_X11_NO_MITSHM=1" \
    -v "/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    -v "data_inside_container:/data" kalibr

roscore
```

**PLEASE GET CONTAINER ID TO USE BELOW:**

Terminal 2 - Open kalibr container and run bag creator
```
sudo docker exec -it <container-id> /bin/bash
cd /data
source /opt/ros/noetic/setup.bash
rosbag record -O calibration.bag /camera/image_raw
```

Terminal 3 - Open kalibr container and run image topic publisher
```
sudo docker exec -it <container-id> /bin/bash
cd /data
source /opt/ros/noetic/setup.bash
python3 publish_images_to_ros_topic.py
```

This will create `data_inside_container/calibration.bag` file containing your pictures in format kalibr want them.


### Step 5: Calibrate


standard lens is typical for webcams
fisheye/wide-angle lens common in action cameras or special sensors

Standard Lenses: Use `pinhole-radtan` or `pinhole-equi`.
Fisheye/Wide-Angle Lenses: Use `pinhole-equi` or `kannala-brandt`.
Catadioptric or Omnidirectional Lenses: Use `omni`.


Assuming your `docker run` command is still running,  
```
sudo docker exec -it <container-id> /bin/bash
cd /data
source /catkin_ws/devel/setup.bash
rosrun kalibr kalibr_calibrate_cameras \
    --bag /data/calibration.bag --target /data/april_6x6.yaml \
    --models pinhole-radtan \
    --topics /camera/image_raw
```

File `data_inside_container/calibration-results-cam.txt` will contain your calibration data.

## Sources

- https://github.com/ethz-asl/kalibr/wiki/installation
