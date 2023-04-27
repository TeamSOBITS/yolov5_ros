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

sobit_common(2023/3/1時点ではbranchをfeature/box_to_tfを使用してください。)のインストール
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
python3 -m pip uninstall utils
```
## 使用するmessage(sobit_common内にあります。)
BoundingBox, BoundingBoxes, StringArray, ObjectPose, ObjectPoseArray, Image, CompressedImage,




# Usage
 
YOLOv5 
 
```bash
# azure_kinect
roslaunch yolov5_ros azure_yolov5.launch
# realsense
roslaunch yolov5_ros realsense2_yolov5.launch
```
 
YOLOv5 + PCL
 
```bash
# azure_kinect
roslaunch yolov5_ros azure_yolov5_with_tf.launch
# realsense
roslaunch yolov5_ros realsense2_yolov5_with_tf.launch

```

# Note

## 学習時コマンド
```bash 
python3 train.py --imgsz 640 --batch 8 --epochs 300 --data '/home/sobits/catkin_ws/src/yolov5_ros/src/yolov5/datasets/shelf_ak/train.yaml' --weights yolov5s.pt
```

##学習経過確認
```bash
python3 -m tensorboard.main --logdir=runs/train/
```

## Node Parameters
* **'weights`**
    weightファイルのファイルパス

* **'confidence_threshold`**
    認識のスコアのしきい値

* **'iou_threshold`**
    iouのしきい値

* **'inference_size_h`**
    入力画像の幅

* **'inference_size_w`**
    入力画像の横

* **'input_image_topic`**(/rgb/image_raw)
    入力画像のtopic
* **'output_topic`**(objects_rect)
    yolov5の推論結果
* **'`**
## Subscribe Topics
* **'/camera/rgb/image_raw`** (sensor_msgs/Image)

    YOLOv5の入力画像

* **'/camera/depth/points`** (sensor_msgs/PointCloud2)
    ポイントクラウドの入力

## Publish Topics
* **'output_image_topic`**(/yolov5/image_out)
    yolov5の推論結果を画像
