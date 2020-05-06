# Teal-Titan-Automation
### A custom Convolutional Neural Network Architecture based solution Machine Automation for Teal, Titan

## Introduction
This project aims at replacing vibratory bowl feeders in industry production lines with a vision guided robot. This project we use VGR in the form a cobot arm equipped with an external camera and using the input/feedback from the camera, we uses various algorithms to help the cobot pick the component from the bin successfully.

## Assumptions
We assume that the bin is continuously been filled as the objects are removed from it. Although the refilling need not necessarily be equal to the number of components removed from the bin, we assume that bin gets the filled by 15 ± x, where |x| < 5 after 15 components are filled. This way we are making it more randomised and not controlling the setup too much.

We’ve also assumed the component for phase 1 to be a simple, uniform and almost symmetrical component to avoid complications. Having the component simple in the initial phase, allows us to understand any prerequisites and methods to tackle basic obstacles for future phases. 

## Challenges

### 2D Camera
As of today, most of the industry standard solutions consisting a Vision Guided Robot, involve a 3D camera for the vision system. 3D camera allows the measure the z-axis component/position which otherwise isn’t available without external sensors on using 2D Camera. To decrease the overhead cost we decided to implement this with only a 2D static camera. However in order to tackle it, we used the cobot’s built in pressure sensor using the vacuum grip to detect the object post which the bot tries to pickup instead of moving downwards towards the bin. We could’ve also used external IR/Ultrasonic Sensors to receive the z-axis data.

### Static Camera
We challenged ourselves by using a static camera over the bin, against the industry standard of having a static camera over the bin as well as a camera attached to the arm of the robot in order to make it more accurate while guiding it to the location, as well as easier image capture possible for training.

<p align="center">
  <img src=op/1.png />
</p>

We split the images into ’n’ number of pieces, where ’n’ depends on the size of the components and we assign each piece to a coordinate.
By using this we avoid necessity of two cameras and thus reducing overhead costs.

### Image Distortion Correction
A camera is often modelled as an ideal pin-hole one, which images on the focus plane without distortion. However, lens distortion will make the image distorted from ideal one. Two major distortions are radial distortion and tangential distortion. We use chess board distortion removal using openCV for the same.

<p align="center">
  <img src=op/2.png />
</p>

## Dataset Creation

The dataset is created by randomly picking one of ’n’ number of pieces of the image's part of the bin and the cobot attempting to pick the component, that small image is later stored based on whether it was successfully picked or not.
The component is filled as the emptying is done by cobot in order to create the dataset. This was done over 2-3 days on an average of 7-8 hours a day. We had collected around 6192 images with success being around 1188 images and failure being 5004 images.
It was found on manual checking that, there were around 816 images from the failure cases (5004 images), had less than 20% component, and was filled with the colour of the bin’s base, indicating the absence of component. We had used only 10-15% of the 816 images to remove redundancy and avoid overfitting or misclassification.

## Accuracy

We were able to achieve a success rate of 60-70% consistently on different scenarios. For comparison, human's success rate in picking is generally about 90%.
