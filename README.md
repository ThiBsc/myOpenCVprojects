# My OpenCV projects
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/mit)
[![openCV version](https://img.shields.io/badge/openCV-%3E%3D%204.2-green)](https://img.shields.io/badge/openCV-%3E%3D%204.2-green)  
A repository of my opencv projects

## The projects

| Project | Description | Preview |
--- | --- |:---:|
[moveTracking](moveTracking) | A program to track movement using openCV (only CPU) and send notifications via Telegram | <img alt="movetracking_preview" src="moveTracking/screenshot/road_capture.png" width="200px"/>
[double game](doublegame) | A program to find the common element on the double's game | <img alt="doublegame_preview" src="doublegame/screenshot/result.png" width="200px"/>
[digit recognition](digit_recognition) | A program to recognize handwritten number digit | <img alt="digit_preview" src="digit_recognition/screenshot/result.png" width="200px"/>
[playing cards recognition](card_recognition) | A script to recognize playing cards | <img alt="playingcards_preview" src="card_recognition/screenshot/result.png" width="200px"/>
[scanner](scanner) | A script to make a scanner like render | <img alt="scanner_processing" src="scanner/screenshot/processing.png" width="200px"/>

## OpenCV configuration

I compiled OpenCV 4.2 from source with the `opencv_contrib` and `NONFREE algorithms`, so to have the same configuration as me, follow these commands:

```sh
mkdir opencv_src && cd opencv_src
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git
mkdir build && cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_GENERATE_PKGCONFIG=ON \
      -D OPENCV_ENABLE_NONFREE=ON \
      -D OPENCV_EXTRA_MODULES_PATH=~/opencv_src/opencv_contrib/modules ../opencv
# find out number of CPU cores in your machine
nproc # return 12 for me
make -j12
sudo make install
pkg-config --modversion opencv4
python3 -c "import cv2; print(cv2.__version__)"
```