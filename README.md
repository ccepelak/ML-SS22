# Using Satellite Images to Predict Poverty

Poverty is a multifaceted problem manifested by conditions such as malnutrition, homelessness, lack of access to clean water, low educational achievement, and the like (UN 2005). It continues to be one the world’s most pressing issues and it has only been exacerbated by the economic effects of the COVID-19 pandemic. It follows that poverty statistics are among the most important and most widely used data in the economic and policy research sphere. Ironically, the most vulnerable economies in need of extensive and up-to-date poverty data are also those who lack the capacity to compile them. Our project attempts to contribute to the existing body of research by leverging technological advances in machine learning to make use of existing satellite imagery. 

# Project Summary 
We used day time satellite imagery for Ethiopia, Mali, Nigeria, and Malawi from 2015, combined with economic indicators from survey data, to train machine learning models. We planned to use Linear Regression, Random Forest, and Convolutional Neural Networks (CNN) to improve accuracy in poverty prediction, but also ended up including Support Vector Machines and Transfer Learning models. Our work is inspired by past projects which have pushed the evolution of this work from using only nighttime satellite imagery to a combination of the two, along with application of CNN to countries from around the world. By training multiple models on a cluster of countries in Africa (which have not been included before), we hope that our work can continue to advance this mission and encourage countries without consistent poverty data to invest in the development of this data.

![Nighttime Satellite Images](https://github.com/ccepelak/ML-SS22/blob/main/images/night_satellite.jpg "Nighttime Satellite Images")

# Data Sources
1. We are using satellite images from private satellite company, Planet, which shared images from Africa for [public use](https://www.kaggle.com/datasets/sandeshbhat/satellite-images-to-predict-povertyafrica?resource=download&select=Mali_archive). 
2. Economic indicators from the [Demographic and Health Surveys (DHS) Program](https://dhsprogram.com/)

# Hardware and Software Requirements
This code was tested on a system with the following specifications:
<br>
<br>
GPU: 4 x NVIDIA A100 40GB HBM2 <br>
CPU: AMD EPYC 7742 (64 cores, Rome, 2.25 GHz) <br>
RAM: 512 GB (8 x 64GB) ECC DDR4 3200 Mhz <br>
SSD: 2,5” 3,8 TB U.2 NVMe TLC <br>
Network: 1 x 10 GbE SFP+, 2x 1 GbE RJ45, 1 x IPMI Lan <br>
OS: Ubuntu 20.04 LTS + Tensorflow, PyTorch and MxNet with Docker Container for Versions Management <br>

# Results

Linear Regression (3.76% score) & Random Forest (61.8%) set a rough baseline.

Despite having server issues which only allowed us to run the CNN 50 epochs, this model rendered a 57.1% accuracy rate. 
![CNN Training Curve](https://github.com/ccepelak/ML-SS22/blob/main/images/cnn_training.png "CNN Training Curve")
![CNN Prediction Outcome](https://github.com/ccepelak/ML-SS22/blob/main/images/final_outcome.png "CNN Prediction Outcome")

SVM (60.8%) and Transfer Learning, applied to CNN (56.4%), were both included as a means to circumvent server issues.

# Next Steps & Future Work 

*Improving current work:* 
We saw improvement with hyper parameter tuning, further compression of files, and longer training times; and believe that with more time, the CNN's output can be greatly improved. 

*Future projects & applications:* 
Taking lessons from this project, we'd like to apply this model to more up-to-date satellite images. Our ultimate goal is to use these models to support prediction efforts for countries with NO poverty data (i.e. Afghanistan, Somalia), so including countries nearby which can lead to more accurate prediction is another goal. 

