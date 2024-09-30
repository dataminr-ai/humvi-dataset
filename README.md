# HumVI Dataset
The HumVI dataset includes news articles about different types of violent incidents categorized by what type of humanitarian sector it can potentially affect, e.g. aid protection, food insecurity, healthcare security, education protection, and/or internally displaced people (IDP) protection. 

The dataset comprises articles in three languages (English, French, and Arabic) from multiple different sources. We partnered with a data-backed humanitarian organization - [anonymous organization] to obtain real world ground truth labels for these datasets. 

### Table of Contents
- [HumVI Dataset](#humvi-dataset)
    - [Table of Contents](#table-of-contents)
- [Data Description](#data-description)
- [Data Collection](#data-collection)

# Data Description
The dataset includes the following splits:
- Core
    - Train: `data/humvi_core_train.csv`
    - Test: `data/humvi_core_test.csv`
- Expansion 
    - Train:  `data/humvi_expansion_train.csv`
    - Test: `data/humvi_expansion_test.csv`
- Unlabeled


# Data Collection
### Scraping URLs
The dataset does not include article titles & full text due to TOS limitations. To hydrate the dataset you may scrape the URLs by running `data_collection/web_scrape.py`

### GDelt Data Collection
Run `data_collection/scrape_gdelt_articles.py` to collect the last N hours of GDelt articles, filter by country & scrape the webpage content.

```
python data_collection/scrape_gdelt_articles.py \
    --collect_n_hours 1
```
