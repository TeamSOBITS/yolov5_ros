# YOLOv5 ROS
YOLOv5のROSパッケージ

# Requirement
 
* OS: Ubuntu20.04
* ROS distribution: Noetic
* python : 3.8.10
* pytorch : 1.13.1
* package : sobit_common

## Installation
yolov5_rosのインストール
```bash
cd catkin_ws/src/
git clone https://github.com/TeamSOBITS/yolov5_ros.git
```

sobit_commonのインストール
```bash
cd catkin_ws/src/
git clone https://github.com/TeamSOBITS/sobit_common.git
```

/yolov5_ros/src　のディレクトリにyolov5の公式パッケージをインストールしてください。
```bash
cd yolov5_ros/src/
git clone https://github.com/ultralytics/yolov5.git
```

必要なpython moduleのインストール
```bash
cd yolov5_ros/src/yolov5
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install utils
```
## 使用するmessage(sobit_common内にあります。)
BoundingBox, BoundingBoxes, StringArray, ObjectPose, ObjectPoseArray, Image, CompressedImage

 
# Usage
 
YOLOv5 
 
```bash
roslaunch yolov5_ros yolov5.launch
```
 
YOLOv5 + PCL
 
```bash
roslaunch yolov5_ros yolov5_with_tf.launch
```