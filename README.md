# AdvsOrganic
Title: Prediction of Ad vs organic viewership of YT videos

Objective: Brands are interested in knowing their expenditure spent on Advertisements on various YT videos and also they are interested to
           find out how their competitors are promoting their products through various advertisement campaigns and their expenditure. As 
           this information is not provided by the YT, we need an algorithm which could predict the advertisement viewership and organic 
           viewership of the videos
           
Technology: Python

Model: SVM (linear kernel) both for classification and regression

Process:
1. Training data consisting videos of both brands and creators were collected from Signedup channels (~ 3000 videos)
2. Data cleaning needed to be extensive as the data contained lot of skewness, new features were engineered
3. Classification model was built to classify the videos as ad videos and non ad videos
4. Regression models were built to estimate the Ad per and organic per respectively
5. API was built to provide access to the data team

Accuracy:

 Classification model was showing 95% accuracy on test data
 
 Ad_per and organic_per models were giving close prediction values on test data
 
 
 
