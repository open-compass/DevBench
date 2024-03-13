# Hybrid Images

## Introduction

**Hybrid images** are static images that change in interpretation as a function of the viewing distance. The basic idea is that high frequency tends to dominate perception when it is available, but, at a distance, only the low frequency (smooth) part of the signal can be seen. By blending the high frequency portion of one image with the low-frequency portion of another, you get a hybrid image that leads to different interpretations at different distances.
Click [here](http://www.cs.cornell.edu/courses/cs5670/2018sp/projects/pa1/index.html) to view projects introduction. 
## Features

* Write an image filtering function and use it to create **hybrid images**
* Using different kind of filters (e.g., Gaussian Blur kernel)
* Get high-pass features and low-pass features of different images and hybrid them into one image

## Structure

| Name          | Function                                                 |
| ------------- | -------------------------------------------------------- |
| resources/    | available images to hybrid                               |
| src/hybrid.py | hybrid program with multiple hybrid algorithms functions |


## Usages

### Requirements

* Linux / Windows / MacOS
* cv2
* numpy
* pandas


## Examples

### Images before hybriding

![cat](https://github.com/ReynoldZhao/Project1_Hybrid_Images/raw/master/resources/cat.jpg)

![dog](https://github.com/ReynoldZhao/Project1_Hybrid_Images/raw/master/resources/dog.jpg)

### Hybrid images

![hybrid](https://github.com/ReynoldZhao/Project1_Hybrid_Images/raw/master/resources/hybrid.png)
