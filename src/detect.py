#!/usr/bin/env python3

import rospy
import cv2
import torch
import torch.backends.cudnn as cudnn
import numpy as np
from cv_bridge import CvBridge
from pathlib import Path
import os
import sys
import sensor_msgs
from sobit_common_msg.srv import RunCtrl, RunCtrlResponse
from std_msgs.msg import Bool
from rostopic import get_topic_type

from sensor_msgs.msg import Image, CompressedImage
# from detection_msgs.msg import BoundingBox, BoundingBoxes
from sobit_common_msg.msg import BoundingBox, BoundingBoxes, StringArray, ObjectPose, ObjectPoseArray

# add yolov5 submodule to path
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0] / "yolov5"
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative path

# import from yolov5 submodules
from models.common import DetectMultiBackend
from utils.general import (
    check_img_size,
    check_requirements,
    non_max_suppression,
    scale_coords
)
from utils.plots import Annotator, colors
from utils.torch_utils import select_device
from utils.augmentations import letterbox


@torch.no_grad()
class Yolov5Detector:
    def __init__(self):
        self.conf_thres = rospy.get_param("~confidence_threshold")
        self.iou_thres = rospy.get_param("~iou_threshold")
        self.agnostic_nms = rospy.get_param("~agnostic_nms")
        self.max_det = rospy.get_param("~maximum_detections")
        self.classes = rospy.get_param("~classes", None)
        self.line_thickness = rospy.get_param("~line_thickness")
        self.view_image = rospy.get_param("~view_image")
        self.can_predict = rospy.get_param("~initial_predict", True)
        # Initialize weights 
        weights = rospy.get_param("~weights")
        # Initialize model
        self.device = select_device(str(rospy.get_param("~device","")))
        self.model = DetectMultiBackend(weights, device=self.device, dnn=rospy.get_param("~dnn"), data=rospy.get_param("~data"))
        self.stride, self.names, self.pt, self.jit, self.onnx, self.engine = (
            self.model.stride,
            self.model.names,
            self.model.pt,
            self.model.jit,
            self.model.onnx,
            self.model.engine,
        )
#publisherの定義
        self.pub_result_img = rospy.Publisher("detect_result", sensor_msgs.msg.Image, queue_size=10)
        self.pub_detect_list = rospy.Publisher("detect_list", StringArray, queue_size=10)
        self.pub_detect_poses = rospy.Publisher("detect_poses", ObjectPoseArray, queue_size=10)

        # Setting inference size
        self.img_size = [rospy.get_param("~inference_size_w", 640), rospy.get_param("~inference_size_h",480)]
        self.img_size = check_img_size(self.img_size, s=self.stride)
        self.height = self.img_size[0]
        self.width = self.img_size[1]

        # Half
        self.half = rospy.get_param("~half", False)
        self.half &= (
            self.pt or self.jit or self.onnx or self.engine
        ) and self.device.type != "cpu"  # FP16 supported on limited backends with CUDA
        if self.pt or self.jit:
            self.model.model.half() if self.half else self.model.model.float()
        bs = 1  # batch_size
        cudnn.benchmark = True  # set True to speed up constant image size inference
        self.model.warmup()  # warmup        
        
        # Initialize subscriber to Image/CompressedImage topic
        input_image_type, input_image_topic, _ = get_topic_type(rospy.get_param("~input_image_topic"), blocking = True)
        self.compressed_input = input_image_type == "sensor_msgs/CompressedImage"

        self.server = rospy.Service("run_ctrl", RunCtrl, self.run_ctrl_server)
        self.sub_run_ctrl = rospy.Subscriber("run_ctrl", Bool, self.run_ctrl_callback)

        if self.compressed_input:
            self.image_sub = rospy.Subscriber(
                input_image_topic, CompressedImage, self.callback, queue_size=1
            )
        else:
            self.image_sub = rospy.Subscriber(
                input_image_topic, Image, self.callback, queue_size=1
            )
        # Initialize prediction publisher
        self.pred_pub = rospy.Publisher(
            rospy.get_param("~output_topic"), BoundingBoxes, queue_size=10
        )
        # Initialize image publisher
        self.publish_image = rospy.get_param("~publish_image")
        if self.publish_image:
            self.image_pub = rospy.Publisher(
                rospy.get_param("~output_image_topic"), Image, queue_size=10
            )
        # Initialize CV_Bridge
        self.bridge = CvBridge()



    def run_ctrl_server(self, msg):
        if msg.request:
            self.can_predict = True
        else:
            self.can_predict = False
        return RunCtrlResponse(True)

    def run_ctrl_callback(self, msg):
        self.can_predict = msg.data
        rospy.loginfo("run ctrl -> {}".format(self.can_predict))

    def callback(self, data):
        """adapted from yolov5/detect.py"""
        # print(data.header)
        if not self.can_predict:
            return

        if self.compressed_input:
            im = self.bridge.compressed_imgmsg_to_cv2(data, desired_encoding="bgr8")
        else:
            im = self.bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")
        
        im, im0 = self.preprocess(im)
        # Run inference
        im = torch.from_numpy(im).to(self.device) 
        im = im.half() if self.half else im.float()
        im /= 255
        if len(im.shape) == 3:
            im = im[None]

        pred = self.model(im, augment=False, visualize=False)
        pred = non_max_suppression(
            pred, self.conf_thres, self.iou_thres, self.classes, self.agnostic_nms, max_det=self.max_det
        )

        ### To-do move pred to CPU and fill BoundingBox messages
        
        # Process predictions 
        det = pred[0].cpu().numpy()

        bounding_boxes = BoundingBoxes()
        bounding_boxes.header = data.header
        # bounding_boxes.image_header = data.header
        
        annotator = Annotator(im0, line_width=self.line_thickness, example=str(self.names))
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

            # Write results
            for *xyxy, conf, cls in reversed(det):
                bounding_box = BoundingBox()
                detect_list = StringArray()
                detect_poses = ObjectPoseArray()                
                c = int(cls)
                dist_list = []
                # Fill in bounding box message
                bounding_box.Class = self.names[c]
                bounding_box.probability = conf 
                bounding_box.xmin = int(xyxy[0])
                bounding_box.ymin = int(xyxy[1])
                bounding_box.xmax = int(xyxy[2])
                bounding_box.ymax = int(xyxy[3])

                bounding_boxes.bounding_boxes.append(bounding_box)
                # Annotate the image
                if self.publish_image or self.view_image:  # Add bbox to image
                      # integer class
                    label = f"{self.names[c]} {conf:.2f}"
                    annotator.box_label(xyxy, label, color=colors(c, True))       
                detect_list.data.append(label)
                
                obj_pose = ObjectPose()
                obj_pose.Class = label
                obj_pose.pose.position.x = int(xyxy[0] + (xyxy[2] - xyxy[0]) / 2)
                obj_pose.pose.position.y = int(xyxy[1] + (xyxy[3] - xyxy[1]) / 2)
                obj_pose.pose.position.z = -1
                detect_poses.object_poses.append(obj_pose)
                p = np.array((obj_pose.pose.position.y, obj_pose.pose.position.x))
                center = np.array((self.height/2,self.width/2))
                dist = np.linalg.norm(p-center)
                dist_list.append(dist)
                ### POPULATE THE DETECTION MESSAGE HERE
            detect_poses.header = data.header
            # Stream results
            im0 = annotator.result()
        # Publish prediction
        self.pred_pub.publish(bounding_boxes)
        try:
            self.pub_detect_poses.publish(detect_poses)
            self.pub_detect_list.publish(detect_list)
        except UnboundLocalError:
            pass
        # Publish & visualize images
        if self.view_image:
            cv2.imshow(str(0), im0)
            cv2.waitKey(1)  # 1 millisecond
        if self.publish_image:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(im0, "bgr8"))


    def preprocess(self, img):
        """
        Adapted from yolov5/utils/datasets.py LoadStreams class
        """
        img0 = img.copy()
        img = np.array([letterbox(img, self.img_size, stride=self.stride, auto=self.pt)[0]])
        # Convert
        img = img[..., ::-1].transpose((0, 3, 1, 2))  # BGR to RGB, BHWC to BCHW
        img = np.ascontiguousarray(img)

        return img, img0 

if __name__ == "__main__":

    check_requirements(exclude=("tensorboard", "thop"))

    rospy.init_node("yolov5", anonymous=True)
    detector = Yolov5Detector()
    
    rospy.spin()