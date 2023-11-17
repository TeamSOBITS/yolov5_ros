<a name="readme-top"></a>

[JP](README.md) | [EN](template_readme_en.md)

[![Contributors][contributors-shield]][chttps://github.com/TeamSOBITS/yolov5_ros/graphs/contributors]
[![Forks][forks-shield]][https://github.com/TeamSOBITS/yolov5_ros/forks]
[![Stargazers][stars-shield]][https://github.com/TeamSOBITS/yolov5_ros/stargazers]
[![Issues][issues-shield]][https://github.com/TeamSOBITS/yolov5_ros/issues]
<!-- [![MIT License][license-shield]][license-url] -->

# レポジトリ名

<!-- 目次 -->
<details>
  <summary>目次</summary>
  <ol>
    <li>
      <a href="#概要">概要</a>
    </li>
    <li>
      <a href="#環境構築">環境構築</a>
      <ul>
        <li><a href="#環境条件">環境条件</a></li>
        <li><a href="#インストール方法">インストール方法</a></li>
      </ul>
    </li>
    <li><a href="#実行・操作方法">実行・操作方法</a></li>
    <li><a href="#マイルストーン">マイルストーン</a></li>
    <li><a href="#変更履歴">変更履歴</a></li>
    <!-- <li><a href="#contributing">Contributing</a></li> -->
    <!-- <li><a href="#license">License</a></li> -->
    <li><a href="#参考文献">参考文献</a></li>
  </ol>
</details>



<!-- レポジトリの概要 -->
## 概要

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

ここで本レポジトリの目的や解決する課題を中心にアピールしてください．
YOLOv5をROS上で実行するROSパッケージです．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>



<!-- セットアップ -->
## セットアップ

### 環境条件

* OS: Ubuntu20.04
* ROS distribution: noetic
* Python: 3.8.10
* Pytorch: 1.13.1
* Package: sobit_common
### インストール方法

1. yolov5_rosをworkspace上にclone
   ```
   cd catkin_ws/src/
   git clone https://github.com/TeamSOBITS/yolov5_ros.git
   ```
2. sobit_commonのインストール
   ```
   cd catkin_ws/src/
   git clone https://github.com/TeamSOBITS/sobit_common.git
   ```
3. yolov5_ros/srcにyolov5の公式パッケージをインストール
   ```
   cd catkin_ws/src/
   git clone https://github.com/ultralytics/yolov5.git
   ```
4. 必要なpythonモジュールをインストール
   ```
   cd catkin_ws/src/yolov5_ros/src/yolov5
   python3 -m pip install --upgrade pip
   python3 -m pip install -r requirements.txt
   python3 -m pip uninstall utils
   ```



<p align="right">(<a href="#readme-top">上に戻る</a>)</p>



<!-- 実行・操作方法 -->
## 実行・操作方法

<!-- デモの実行方法やスクリーンショットがあるとわかりやすくなるでしょう -->
### 実行方法
* YOLOv5
   ```
   roslaunch yolov5_ros yolov5.launch
   ```
   
* YOLOv5 with TF
   ```
   roslaunch yolov5_ros yolov5_with_tf.launch
   ```
   
* 実行時の引数
   ```
   weights: weightファイルのパス
   confidence_threshold: 認識のスコアの閾値
   iou_threshold: IoUの閾値
   inference_size_h: 推論する画像の縦幅
   inference_size_w: 推論する画像の横幅
   input_image_topic: 入力画像のtopic
   output_topic: yolov5による推論結果
   ```

   
### 使用Topic
* 使用msg一覧
   ```
   Boundingbox (sobit_common)
   BoundingBoxes (sobit_common)
   StringArray 
   ObjectPose 
   ObjectPoseArray 
   Image (sensor_msgs)
   CompressedImage 
   ```

* Subscribe Topics
   ```
   '/camera/rgb/image_raw'(sensor_msgs/Image): YOLOv5への入力画像
   'camera/depth/points'(sensor_msgs/PointCloud2): ポイントクラウドの入力
   ```
   
* Publish Topics
   ```
   'output_image_topic'(yolov5/image_out): YOLOv5の推論結果の画像
   ```

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>



<!-- マイルストーン -->
## マイルストーン

- [ ] OSS化
   - [ ] msgの更新(vision_msgsか，jsk_recognition_msgsを推奨します) ．
- [ ] README.mdの更新
    - [ ] launch実行の際の引数や具体的な使用方法について説明が必要です．
    - [ ] READMEの英語版の作成が必要です． 

現時点のバッグや新規機能の依頼を確認するために[Issueページ](https://github.com/TeamSOBITS/yolov5_ros/issues) をご覧ください．

<p align="right">(<a href="#readme-top">上に</a>)</p>



<!-- 変更履歴 -->
## 変更履歴

- 1.0: 2023/11/17 OSS UPDATE
   - Merge branch(origin/handyman_2023をnoetic_develに統一)
   - Update README.md


<!-- CONTRIBUTING -->
<!-- ## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">上に戻る</a>)</p> -->



<!-- LICENSE -->
<!-- ## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">上に戻る</a>)</p> -->



<!-- 参考文献 -->
## 参考文献

* Jocher, G. (2020). YOLOv5 by Ultralytics (Version 7.0) [Computer software]. https://doi.org/10.5281/zenodo.3908559
* mats-robotics. yolov5_ros. https://github.com/mats-robotics/yolov5_ros
* []()

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
<!-- [license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt -->
