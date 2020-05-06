# Teal-Titan-Automation
### A Custom Convolutional Neural Network Architecture based Machine Automation for Titan Engineering and Automation Limited (TEAL)

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

## CNN Architecture

We define the architecture by defining the skeleton of the network.  We first add the convolution layer. In our architecture we have three convolutional layer with the first and the last layer having 32 filters and the middle layer having 64 filters. The kernel size of the filter in all three layers is ```[3x3]```.  We also Batch Normalize after every convolution layer followed by MaxPooling with pool size ```[2x2]``` and 2 strides.
We then flatten the output of these convolution layer, as an input the fully connected layer.
After several combinations of layers and neurons in layers, we concluded the following to be the most efficient and accurate network architecture for the created dataset.
We have three layer neural network with one hidden layer. The input and the hidden layer have a sixteen neurons each. We have Leaky ReLU as activation function for input and hidden layer with ```α = 0.02``` and ```α = 0.005``` respectively, instead of ReLU function to avoid the dying ReLU problem.

Before compiling the skeleton, i.e is the model before training, we define the optimizer function. We here use, Nadam (Nesterov Adam optimizer). Much like Adam Optimizer is essentially RMSprop with momentum, Nadam Optimizer is Adam RMSprop with Nesterov momentum. We set the learning rate to 0.0001 and leave rest of the parameters like ```beta_1=0.04```, ```beta_2=0.009```, ```epsilon=None```, and ```schedule_decay=0.004``` to their default values.
We compile the network and before training, we rescale the RGB values of the image from 0-255 to 0-1, since those values are too high for the models to process. We set a ```shear_range=0.2``` and ```zoom_range=0.2```. We then train with batch_size=16 and input ```target_size=(64,64)``` and 250 epochs.

## Accuracy

We saw an average pickup success rate of 60-65% in case of using the learnt model in comparison to the success rate of 20% without learning, showing a 40-45% increase in performance in the former case. For comparison, human's success rate in picking is generally about 90%.
