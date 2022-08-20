
!git clone https://github.com/geohot/twitchslam

!cd twitcslam
!pip install pygame

!git clone https://github.com/uoip/pangolin

!ls
!sudo apt-get install libglew-dev
#!cd pangolin
#!mkdir pangolin/build
!cd content/pangolin/build
!cmake /content/pangolin/
#!make -j8
#!cd ..
#!python setup.py install

!sudo apt-get install libeigen3-dev
!make -j8
#!cd ..
#!python setup.py install

!gcc --version
!g++ --version

