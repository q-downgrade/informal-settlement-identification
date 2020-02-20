# Executive Summary

This project is being developed for New Light Technologies  a small, award-winning organization based in Washington, D.C. that provides solutions to government, commercial, and non-profit clients. The main objective of this project is to Improve Slum Area Identification through Real-Estate Data. We found during research that around 25% of the world’s urban population lives in informal settlements, areas that are cut off from basic services and city infrastructure. Mapping these locations can dramatically help aid and non-government organizations better serve those in need. Our team intent to develope a machine learning-based tool that can automatically classify informal settlements using freely available population density data, real estate listing, satellite and aerial imagery. Our first strategy is to finalize a good data source forbuild a web scraper to house and apartment adverts for a selected city in Africa/Latin America/Middle East.


After extracting the data next decision we had to make was what column or columns needs to be our X. We found apartment_near_dist, ph_near_dist, store_near_dist, house_near_dist, ph_near_angle, apartment_near_angle seemed to be having more correlation in identifying the slum area. 
 

EDA helped us set up a preprocessing plan for our model. For preprocessing, we had created a fucntion that used regex, lemmatizatizer which removed punctuation and stopwords. For modeling, I used  TFIDF and Count vetorizers. They brought context of word choices into play, which will give us a better understanding of the group of words used in a reddit blog post about the sports we are analyzing.
 
Machines had no problem understanding the real estat data, after the initial EDA.

Source : https://www.habitatireland.ie/2018/01/1-billion-people-live-slums/

# Problem Statement


 # Conclusion and Recommendation
 
## Conclusions : 
Using ________'s API we have successfully collected data from ______. After doing the initial cleanup we have concatenated the dataframes to be used for training the model. During the EDA we were able to find the most correlated features. Using NLP we have trained our classifiers. We have calaculated Base Line Score , Logistic Regression Model score (Section 5.2 and 5.3), Gaussian NB Model (Section 5.4), Multinomial NB (Section 5.5) and Random Forest Model(Section 5.6) during our modeling process. We have used Count Vectorizer and TFIDF Vectorizer in our models.

All the models we have trained outperformed the Base Line model. TFIDF vector with Logostics Regression had the best Train and Test score. The scores were 0.92 on the Train Score and 0.88 on the Test score.

## Recommendations :

While our mdel trained on Logistic Rgression with TFIDF vectorizer performed better than other models we still think there is a scope of improvement in the accuracy of the models. The present model is also slightly overfit. If we can get more data with different source other than Reddit we will be able to better train our classifiers. We will also like to train our models on other classifiers like Decision tree and Support Vector machines.

https://www.habitatireland.ie/2018/01/1-billion-people-live-slums/