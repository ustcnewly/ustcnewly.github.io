cd opencv-2.4.13/build
sudo make uninstall
sudo rm -rf /usr/local/lib/libopencv*
sudo rm -rf /usr/local/share/OpenCV
sudo rm -rf /usr/local/include/opencv2
cd ../../opencv-3.2.0/build
sudo make install
