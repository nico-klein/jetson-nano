# my jetson nano and jetbot
Here are my my samples and tests with the jetson nano. I'm in an early phase and some filies are in experimetal state.
I use tensorflow and a bit pytorch. Thats why didtn't use the jetbot images with pytorch dockers only.

# Software
## play in python with hardware addons
* PWM cooling fan (also servivce for automatic speed depending on temperature)
* OLED Displays SSD1306 128x32 and 128x64 (also service for status and custom infos)
* USB Gamepads from Xbox and PS5
* Battery voltage (jetbot)
* motors (jetbot)
* cameras

# predict images
* predict images from internet, from file and live from camera 
* pretrained nets on imagenet
* pytorch and tensorflow

# setup my jetson and jetbot
## general
###get Jetpack Version 
    sudo apt-cache show nvidia-jetpack

### get CUDNN Version 
	old: cat /usr/include/cudnn.h | grep CUDNN_MAJOR -A 2
	new: cat /usr/include/cudnn_version.h 

### get CUDA Version 
	/usr/local/cuda/bin/nvcc -V

### set powermode check (m 1: 5W power mode, m 0: MAXN)  
	sudo nvpmodel -m 1
	sudo tegrastats
	sudo nvpmodel -q

### test fan (if is installed. e.g. from noctua)
	sudo jetson_clocks 
	power off after test

### reset cams
	sudo systemctl restart nvargus-daemon

### jetson stats (installs also jetson_stats.service)
	sudo -H pip3 install -U jetson-stats
	reboot
	call from terminal: jtop

## install
### prepare  sd card on a mac
	sudo diskutil unmount /dev/diskxsy
	sudo dd bs=1m if=/Users/.../jetson_451.img of=/dev/diskx

### swap default 2GB -> 4GB (better)
	check with 	free -m
	option 1
		check with: zramctl
		change divisor 2 -> 1 : sudo vi /etc/systemd/nvzramconfig.sh
	option 2
		sudo systemctl disable nvzramconfig
		sudo fallocate -l 4G /mnt/4GB.swap
		sudo chmod 600 /mnt/4GB.swap
		sudo mkswap /mnt/4GB.swap
		sudo echo "/mnt/4GB.swap swap swap defaults 0 0" >> /etc/fstab

### no UI
	sudo systemctl set-default multi-user
	# on with sudo systemctl set-default graphical.target

### wifi
	easy way: setup in in UI
	nmcli connection show
	sudo iw dev wlan0 set power_save off

### gamepad
	maybe needed:  sudo chmod oua+rw /dev/input/event*
	?? xbox controller bluetooth 
		sudo apt-get install xboxdrv

### github (password or no password possible)
	ssh-keygen -t ed25519 -C "<email address>"
	git clone git@github.com:nico-klein/jetson-nano.git


### service for automatic cooler fan
	see services/cooling_fan_service.py

### service for oled display (stats and custum outputs)
	maybe needed: sudo pip3 install Adafruit_SSD1306 Adafruit_GPIO
    see services/oled_service.py

## python base + jupyter
	sudo apt install nodejs npm
	sudo apt install python3-pip
	sudo apt-get install libffi-dev
	sudo pip3 install jupyter jupyterlab
	sudo pip3 install traitlets ipywidgets smbus
	sudo pip3 install evdev
	DO NOT !!! sudo apt-get install python3-opencv
	sudo apt-get install python3-matplotlib
	pip3 install Cython
	use remote (with no security !) :  jupyter notebook --no-browser --ip=0.0.0.0 --NotebookApp.token=''

## jupyter as service (not user root or sudo)
### /etc/systemd/system/jupyter.service 
	[Unit]
	After=network.service

	[Service]
	ExecStart=/usr/bin/sudo /home/jetbot/.local/bin/jupyter lab  --config=/home/jetbot/.jupyter/jupyter_notebook_config.py
	??? Environment="PATH=/home/jetbot/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"
	User=jetbot
	WorkingDirectory=/home/jetbot

	[Install]
	WantedBy=default.target

### commands
    sudo systemctl enable jupyter.service 	# activate initial
    sudo systemctl daemon-reload 			# only needed after changes 
    sudo systemctl start jupyter.service 	# only needed after daemon-reload
    systemctl status jupyter.service 		# show log

## tensorflow
    see https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html
	sudo apt-get update
	sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran
	sudo pip3 install -U pip testresources setuptools==49.6.0 
	# ??? sudo pip3 install image
	sudo pip3 install -U numpy==1.16.1 future==0.18.2 mock==3.0.5 h5py==2.10.0 keras_preprocessing==1.1.1 keras_applications==1.0.8 gast==0.2.2 futures protobuf pybind11
	check jetpack : sudo apt-cache show nvidia-jetpack (info: 09.06.2020 waa V44 / 22.02.2021 was V45) 
	sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v45 tensorflow
	test: python3 / import tensorflow. if crash with "Illegal instruction" =>
		export OPENBLAS_CORETYPE=ARMV8 (add in .bashrc)

## pytorch
	# PyTorch v1.7 - torchvision v0.8.1  for jetpack 4.4 and higher
	mkdir installs
	cd installs
	wget https://nvidia.box.com/shared/static/cs3xn3td6sfgtene6jdvsxlr366m2dhq.whl -O torch-1.7.0-cp36-cp36m-linux_aarch64.whl
	sudo apt-get install libopenblas-base libopenmpi-dev 
	pip3 install ?numpy? torch-1.7.0-cp36-cp36m-linux_aarch64.whl

	sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev libavcodec-dev libavformat-dev libswscale-dev
	git clone --branch release/0.8.0 https://github.com/pytorch/vision torchvision   # see below for version of torchvision to download
	cd torchvision
	export BUILD_VERSION=0.8.0  # where 0.x.0 is the torchvision version  
	python3 setup.py install --user
	# cd ../  # attempting to load torchvision from build dir will result in import error
	# pip install 'pillow<7' # always needed for Python 2.7, not needed torchvision v0.5.0+ with Python 3.6

## jetbot 
    I use a normal jetson image and no setup from nvidia or waveshare 

### motor driver
	pip3 install Adafruit_MotorHAT

### nvidia git - I use only to read in files and do not execute setup.py
	mkdir nvidia
	cd nvidia
	git clone https://github.com/NVIDIA-AI-IOT/jetbot
	# in notebooks opt: 	import sys	sys.path.append('../')


### waveshare git  - I use only to read in files and do not execute setup.py
	see https://www.waveshare.com/wiki/JetBot_AI_Kit
	mkdir waveshare
	cd waveshare
	git clone https://github.com/waveshare/jetbot
	# opt: cd jetbot and sudo python3 setup.py install
	# in notebooks opt: 	import sys	sys.path.append('../')

##  jetson inference
	# https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md
	sudo apt-get update
	sudo apt-get install git cmake libpython3-dev python3-numpy
	git clone --recursive https://github.com/dusty-nv/jetson-inference
	cd jetson-inference
	mkdir build
	cd build
	cmake ../
	make -j$(nproc)
	sudo make install
	sudo ldconfig
	# executables in jetson-inference/build/aarch64/bin

## docker (I dont use anymore for jetson)

	sudo docker images
	sudo docker container list

	pip3 install pandas requests


	load images
		see https://ngc.nvidia.com/catalog/containers/nvidia:l4t-tensorflow
		tf : sudo docker pull nvcr.io/nvidia/l4t-tensorflow:r32.5.0-tf2.3-py3
		torch: sudo docker pull nvcr.io/nvidia/l4t-pytorch:r32.5.0-pth1.7-py3
	start interactive
		sudo docker run -it --rm --runtime nvidia --network host nvcr.io/nvidia/l4t-pytorch:r32.5.0-pth1.7-py3
	start batch remote

	# pytorch docker
	# https://ngc.nvidia.com/catalog/containers/nvidia:l4t-pytorch
	# sudo docker pull nvcr.io/nvidia/l4t-pytorch:r32.5.0-pth1.7-py3

