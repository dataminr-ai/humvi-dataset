# davinci-dataset
The DaVINCI dataset includes news articles about different types of violent incidents categorized by what type of humanitarian sector it can potentially affect, e.g. aid protection, food insecurity, healthcare security, education protection, and/or internally displaced people (IDP) protection. 

The dataset comprises articles in three languages (English, French, and Arabic) from multiple different sources. We partnered with a data-backed humanitarian organization - [anonymous organization] to obtain real world ground truth labels for these datasets. 

### Table of Contents
- [davinci-dataset](#davinci-dataset)
    - [Table of Contents](#table-of-contents)
- [Scraping URLs](#scraping-urls)
- [Data Description](#data-description)

# Scraping URLs
The dataset does not include the article titles & full text due to TOS limitations. To hydrate the dataset you may scrape the URLs by running `scrape.py`

# Data Description
The dataset includes the following splits:
- Vanilla
    - Train
    - Test:
- Full 
    - Train: 
    - Test
- Unlabeled