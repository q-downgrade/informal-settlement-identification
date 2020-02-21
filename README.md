# ![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png) Identifying Informal Settlements Using Real-Estate Data
By Matteo Cangiano, Q Leedham, and Daniel Sheehan  
  
  
## Table of Contents
  - [Problem Statement](#Problem-Statement)
  - [Notebook Links](#Notebook-Links-Table-of-Contents)
  - [Data Collection](#Data-Collection)
  - [Executive Summary](#Executive-Summary)
  - [Conclusions](#Conclusions)
  - [Recommendations and Limitations](#Recommendations-and-Limitations)

---
## Problem Statement   

Mapping of informal settlements with satellite imagery is a long-standing practice, but such methods could be enhanced through web-scraped real-estate data. This project would build a web scraper to house and apartment adverts for a selected city in Africa/Latin America/Middle East. The scraper should download all adverts in the city during a recent period (ideally 3 years or more); and map all the adverts. The project should test the feasibility of estimating informal tenure from this information. Using gridded population estimates (e.g. from Facebook), the team would calculate the ratio of real estate adverts with population density. This ratio could serve as an input to machine learning models aimed at mapping informal settlements. The team will be using the metric of accuracy for model evaluation. 

### Succinct Question Formulation

Is it possible to identify informal settlements using real estate data and population estimates rather than relying on satelitte imagery?

---  

## Notebook Links Table of Contents


* [Exploratory Data Analysis (EDA) Notebook Link - GitHub View](https://git.generalassemb.ly/delta/delta/blob/master/eda/EDA.ipynb)

* [Geoprocessing Notebook Link - GitHub View](https://git.generalassemb.ly/delta/delta/blob/master/geoprocessing/Geoprocessing.ipynb)

* [Modeling Notebook Link - GitHub View](https://git.generalassemb.ly/delta/delta/blob/master/modeling/modeling-notebook.ipynb)  

  
---

## Data Collection
To collect the data, we searched through global real estate listing websites, but quickly found a lack of consistency in the number of listings in different cities or countries. It became clear that different nations had didfferent ways of listing their properties online, if they even posted them online. To circumvent this problem we decided to perform a case study on Brazil where there was real estate data readily available through Kaggle.

Preliminary EDA showed that the Sao Paulo dataset contained both sale and rent prices. For the purposes of this project the team decided to only include listings that had a rent price as well as geographical location. Making this a Complete Case Analysis will ensure that we have the best possible model we can create, in addition the removal of listings left the team with more than enough data to feed the models.

For population data we leveraged the Gridded Population of the World (GPW) collection fourth version (GPWv4). Read more on GPW data below:

> The Gridded Population of the World (GPW) collection, now in its fourth version (GPWv4), models the distribution of human population (counts and densities) on a continuous global raster surface. Since the release of the first version of this global population surface in 1995, the essential inputs to GPW have been population census tables and corresponding geographic boundaries. The purpose of GPW is to provide a spatially disaggregated population layer that is compatible with data sets from social, economic, and Earth science disciplines, and remote sensing. It provides globally consistent and spatially explicit data for use in research, policy-making, and communications. For GPWv4, population input data are collected at the most detailed spatial resolution available from the results of the 2010 round of Population and Housing Censuses, which occurred between 2005 and 2014. The input data are extrapolated to produce population estimates for the years 2000, 2005, 2010, 2015, and 2020. A set of estimates adjusted to national level, historic and future, population predictions from the United Nation's World Population Prospects report are also produced for the same set of years. The raster data sets are constructed from national or subnational input administrative units to which the estimates have been matched. GPWv4 is gridded with an output resolution of 30 arc-seconds (approximately 1 km at the equator). [https://sedac.ciesin.columbia.edu/data/collection/gpw-v4](https://sedac.ciesin.columbia.edu/data/collection/gpw-v4)

For the purpose of this project, we are classifying the presence of an **Urban Permanent Informal Settlements** in a given geography, in this project's case [Census Tracts from the Brazilian Government](ftp://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_de_setores_censitarios__divisoes_intramunicipais/censo_2010/setores_censitarios_shp/). 

Sao Paulo and Rio De Janiero are Brazil's two largest cities and they both publish datasets regarding the locations and extents of their **[Favelas](https://en.wikipedia.org/wiki/Favela)** (a form of Urban Permanent Informal Settlements). 

Favela Shapefiles:

* [Sao Paulo](http://dados.prefeitura.sp.gov.br/dataset/favelas)

* [Rio De Janiero](http://www.data.rio/datasets/limite-favelas?geometry=-43.381%2C-22.997%2C-43.272%2C-22.970)

We defined our **Study Area** as the Census Tracts inside the Minimum Bounding Geometry as a Circle around the Favela Features and selecting the Census Tracts that overlap with it.

Once all the datasets were ready to be used we fed them through a geoprocessing pipeline that would be able to assign each listing to a shapefile/sub district allowing us to see the nearest listing to a certain shapefile and its rent price. These two features proved to be the most telling when trying to identify whether a subdistrict contained an informal settlement or not. 

For the purpose of this study, we decided to do a complete case analysis keeping only complete real estate data. 

### Data Dictionary

For the variables we created, we have contstructed a [data dictionary](https://git.generalassemb.ly/delta/delta/blob/master/data_dictionary/data_dictionary.md). 

---

## Requirements

We leveraged a standard set of Data Science python libraries as well as Esri's `arcpy` Python package from ArcGIS install (Windows) and `cartopy` and `ipyleaflet` for mapping and visualization. 

See our [requirements.txt](https://git.generalassemb.ly/delta/delta/blob/master/requirements.txt)

---

## Executive Summary

This project is being developed for New Light Technologies  a small, award-winning organization based in Washington, D.C. that provides solutions to government, commercial, and non-profit clients. The main objective of this project is to Improve Slum Area Identification through Real-Estate Data. We found during research that around 25% of the world’s urban population lives in informal settlements, areas that are cut off from basic services and city infrastructure. Mapping these locations can dramatically help aid and non-government organizations better serve those in need. Our team develops a machine learning-based tool that can automatically classify informal settlements using open sourced population density, and real estate data.

The problem statement asked to create web scrapers to scrape real estate listings for a given city and create interaction terms to see the relationship between population estimates and real estate data when predicting an informal settlement. Due to the limited time we decided to forgo the web scrapers as different cities and countries would have different practices when it came to posting listings online such as the use of different websites. 

Instead we found two datasets on real estate listings for Brazil on Kaggle and while this was convenient, gathering geospatial data proved to be more complicated. With the use of the IBGE and the state of São Paulo, who partners with companies such as Dados Aberto to provide data on its region, we were able to gather what we needed in the form of census tracts, population estimates and favela locations. 

Preliminary EDA showed that the Sao Paulo dataset contained both sale and rent prices. For the purposes of this project the team decided to only include listings that had a rent price as well as geographical location. Making this a Complete Case Analysis will ensure that we have the best possible model we can create, in addition the removal of listings left the team with more than enough data to feed the models. However, it wasn’t until the listings were plotted around a known favela (Paraisópolis) that the team discovered the relationship between listings in the area. It was at this point the importance of geospatial data became clear.

Once all the datasets were ready to be used we fed them through a geoprocessing pipeline that would be able to assign each listing to a shapefile/sub district allowing us to see the nearest listing to a certain shapefile and its rent price. These two features proved to be the most telling when trying to identify whether a subdistrict contained an informal settlement or not. However, there should be no decision-making based on our model, even though it performs with an ROC score of ~94%. The output of our model is a mere suggestion of which areas are worth investigating further for the presence of informal settlements. 


Source : [https://www.habitatireland.ie/2018/01/1-billion-people-live-slums/](https://www.habitatireland.ie/2018/01/1-billion-people-live-slums/)

---

## Conclusions

Using real estate listings and population mapped to census tracts we were able to find a few models that predicted the presense or absence of informal settlements in São Paulo with relatively high accuracy. We found that the distance from real estate listings were the biggest indicators of where a favela is present in the city. The price and number of those listings matter much less, however. This method could potentially be expanded to other cities, but would rely on finding the required data. Different cities would likely require different data, however. In Alexandria, Egypt, for example, informal settlements are more likely to [encroach on agricultural land](https://www.sciencedirect.com/science/article/pii/S111001681730279X). All we can say for sure is that the models we used work in São Paulo, and potentially other cities in the region.



## Recommendations and Limitations

As noted in the conclusion, we recommend using different models for different regions. While this model works well for the city we tested in on, it may not work well in less urban environments where informal settlements may be constructed. This method isn't perfect, and will likely work best when used in conjunction with other methods of detecting informal settlements using satellite data. A combination of the two would likely yield better results than these models alone. One limitation is that very small favelas will mark an entire census tract as having an informal settlement within it. Future iterations may want to limit the number of small informal settlements included in the model. Future versions may also want to avoid using census tracts as a geographical unit as they tend to have unusual shapes. Other methods should be considered for geographical mapping.