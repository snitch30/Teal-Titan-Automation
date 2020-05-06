# Teal-Titan-Automation
### A custom Convolutional Neural Network Architecture based solution Machine Automation for Teal, Titan

## Introduction
This project aims at replacing vibratory bowl feeders in industry production lines with a vision guided robot. This project we use VGR in the form a cobot arm equipped with an external camera and using the input/feedback from the camera, we uses various algorithms to help the cobot pick the component from the bin successfully.

## Assumptions
We assume that the bin is continuously been filled as the objects are removed from it. Although the refilling need not necessarily be equal to the number of components removed from the bin, we assume that bin gets the filled by 15 ± x, where |x| < 5 after 15 components are filled. This way we are making it more randomised and not controlling the setup too much.

We’ve also assumed the component for phase 1 to be a simple, uniform and almost symmetrical component to avoid complications. Having the component simple in the initial phase, allows us to understand any prerequisites and methods to tackle basic obstacles for future phases. 
