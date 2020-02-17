# ![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png) Identifying Informal Settlements Using Real-Estate Data

## Table of Contents
  - [Problem Statement](#Problem-Statement)
  - [Data Collection](#Data-Collection)
  - [Executive Summary](#)
----

- [ ] Problem Statement
- [ ] A succinct formulation of the question your analysis seeks to answer.
- [ ] A table of contents, which should indicate which notebook or sipts a stakeholder should start with and a link to an exectuvie summary. 
- [ ] A paragraph description of the data you used, plus your data aquisition, ingestion, and cleaning steps. 

---
## Problem Statement   

Mapping of informal settlements with satellite imagery is a long-standing practice, but such methods could be enhanced through web-scraped real-estate data. This project would build a web scraper to house and apartment adverts for a selected city in Africa/Latin America/Middle East. The scraper should download all adverts in the city during a recent period (ideally 3 years or more); and map all the adverts. The project should test the feasibility of estimating informal tenure from this information. Using gridded population estimates (e.g. from Facebook), the team would calculate the ratio of real estate adverts with population density. This ratio could serve as an input to machine learning models aimed at mapping informal settlements.

Is it possible to identify informal settlements using real estate data and population estimates rather than relying on satelitte imagery?

---  
  
## Data Collection
To collect the data, we searched through global real estate listing websites, but quickly found a lack of consistency in the number of listings in different cities or countries. It became clear that different nations had didfferent ways of listing their properties online, if they even posted them online. To circumvent this problem we decided to perform a case study on Brazil where there was real estate data readily available through Kaggle.

Preliminary EDA showed that the data was consistent and no clear outliers were present. However, due to the nature of the project we required price, and geo spatial data to be avalable and left out any observations that contained null values in either of these columns making this a complete case analysis. 

The population data was gathered through...


Once all the datasets were ready to be used we fed them through a geoprocessing pipeline that would be able to assign each listing to a shapefile/sub district allowing us to see the nearest listing to a certain shapefile and its rent price. These two features proved to be the most telling when trying to identify whether a subdistrict contained an informal settlement or not. 

[Insert Visualization]
---
## Executive Summary


---
## Conclusions and Recommendations