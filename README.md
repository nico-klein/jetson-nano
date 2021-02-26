# jetson-nano
Here are my my samples and tests with the jetson nano. 
I'm in an early phase. not to much here.

## tests
### camera-test.ipynb
* test 2 connected cameras on the jetson (USB camera support will be added later)
###m otor-test.ipynb
* drive forward, beackward
### gamepad-test.ipynb
* test all buttons and analog sticks (the 4 buttons on the left dont't work...)

## remote_controlled_car
* drive the robot with a PS5 gamepad

## predict_with_vgg16.ipynb
* predict image from internet, from file and live from camera with imagenet vgg16

## folder images
* sample images for image recognition

## folder utils
libs to use the hardware of the jetson nano 
*  camera (up to 2 internal cameras. USB cam will be added later)  
*  PS5 gamepad
*  motors
I write my own because the already existing did not implement everything I need 
