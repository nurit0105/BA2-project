# README
This Project is done by Laura Nurit Davidowicz in partial fulfillment of the requirements for the degree
of Bachelor of Science in Engineering to the University of Applied Sciences FH
Campus Wien. 

Bachelor Degree Program: Computer Science and Digital Communications

It was developed using PyCharm Professional: https://www.jetbrains.com/pycharm/ and the Interpreter Version Python 3.12

## Dependencies
To run this project successfully after cloning it these steps are recommended
to be followed beforehand. 

1. Create and activate the .venv directory. Depending on your OS the commands might be different.
Here is a link on how to do it: https://python.land/virtual-environments/virtualenv

2. Run **pip install -r requirements.txt**

Here is an explanation how to do it in Windows:
```shell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Caution
It can be possible to run both Systems simultaneously, but when you only have one camera available there could be
some blockage. Please run either of the systems but not both at the same time. 

## The Project
This Project shows two implementation. One with MediaPipe and OpenCV developed in Python 
and one with TensorFlow.js Handpose model developed in Javascript. 

Both include a life Hand Gesture Recognition Detection System via Vision and
a Test Performance Run.

### Function of Recognition Detection
The Recognition System can detect one to four fingers showing up in front of the Camera. 
Next to the Video Stream are two Circles simulating Smart Home Devices, for example some type of LEDs. 

* one finger selects the first Circle.
* two fingers selects the second Circle. 
* three fingers turn the Circle Green (ON)
* four fingers turn the Circle Red (OFF)

### Performance Test

When clicking the Performance Testing Buttons in either application the Test-Set gets run
through the System. The Test set includes 7 people of different age, hand size and skin colour.
All pictures of the hand are with different backgrounds and different lighting conditions. 

After the System has run through the Pictures the Interface provides the Information
of the Expected and the Predicted fingers. If those match the Prediction is viewed as correct.
If those do not match it is viewed as incorrect. 


