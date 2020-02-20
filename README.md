# ![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png) Identifying Informal Settlements Using Real-Estate Data

## Table of Contents
  - [Problem Statement](#Problem-Statement)
  - [Data Collection](#Data-Collection)
  - [Executive Summary](#)
----

- [ ] Problem Statement
- [ ] A succinct formulation of the question your analysis seeks to answer.
- [ ] A table of contents, which should indicate which notebook or scipts a stakeholder should start with and a link to an exectuvie summary. 
- [ ] A paragraph description of the data you used, plus your data aquisition, ingestion, and cleaning steps. 

---
## Problem Statement   

Mapping of informal settlements with satellite imagery is a long-standing practice, but such methods could be enhanced through web-scraped real-estate data. This project would build a web scraper to house and apartment adverts for a selected city in Africa/Latin America/Middle East. The scraper should download all adverts in the city during a recent period (ideally 3 years or more); and map all the adverts. The project should test the feasibility of estimating informal tenure from this information. Using gridded population estimates (e.g. from Facebook), the team would calculate the ratio of real estate adverts with population density. This ratio could serve as an input to machine learning models aimed at mapping informal settlements.

### Succent Question Formulation

Is it possible to identify informal settlements using real estate data and population estimates rather than relying on satelitte imagery?

---  

## Notebook Links Table of Contents


* [Exploratory Data Analysis (EDA) Notebook Link - GitHub View](https://git.generalassemb.ly/delta/delta/blob/master/eda/EDA.ipynb)

* [Geoprocessing Notebook Link - GitHub View](https://git.generalassemb.ly/delta/delta/blob/master/geoprocessing/Geoprocessing.ipynb)

* [Modeling Notebook Link - GitHub View](https://git.generalassemb.ly/delta/delta/blob/master/modeling/modeling-notebook.ipynb)

  
## Data Collection
To collect the data, we searched through global real estate listing websites, but quickly found a lack of consistency in the number of listings in different cities or countries. It became clear that different nations had didfferent ways of listing their properties online, if they even posted them online. To circumvent this problem we decided to perform a case study on Brazil where there was real estate data readily available through Kaggle.

Preliminary EDA showed that the data was consistent and no clear outliers were present. However, due to the nature of the project we required price, and geo spatial data to be avalable and left out any observations that contained null values in either of these columns making this a complete case analysis. 

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


---
## Executive Summary


---
## Conclusions and Recommendations