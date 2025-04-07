# Overview
This project aims to predict next week's Hass avocado prices across multiple regions in the US.

# Dataset
In this project, I combined multiple datasets to build price prediction models:
* Avocado price data: [Hass Avocado Board](https://hassavocadoboard.com/category-data/?region=Total%20U.S.&y=2022)
* Avocado production volume data: [Hass Avocado Board](https://hassavocadoboard.com/volume-data-projections/)
* Weekly Economic Index: [FRED Economic Data](https://fred.stlouisfed.org/series/WEI)
* Gasoline price: [US Energy Information Administration](https://www.eia.gov/petroleum/gasdiesel/)
* US public holidays: [Kaggle](https://www.kaggle.com/datasets/jeremygerdes/us-federal-pay-and-leave-holidays-2004-to-2100-csv)

# Exploratory Data Analysis

### Average selling price distribution

![image](https://github.com/user-attachments/assets/eada70ae-fb15-4059-8d4c-8dd56554a594)

### Observations
* Price looks normally distributed
* Organic avocados tend to be more expensive than conventional avocados

### Production volumes and economic indicator distributions
![image](https://github.com/user-attachments/assets/0e46cbdd-b6ca-4e7b-9417-19ce6178baff)
![image](https://github.com/user-attachments/assets/b11fe119-1120-4946-99b2-17620bb3c696)
![image](https://github.com/user-attachments/assets/29a13cdf-c83c-40e4-b3d5-46b58d2d9a85)
![image](https://github.com/user-attachments/assets/fde797be-8053-488b-b72d-25de807cce99)
![image](https://github.com/user-attachments/assets/a20d79ce-36a2-4f27-8c21-9e65e68c2b7f)

### Observations
* Except for total production volume and Mexico's production volume, the other volume distributions are right-skewed, as most regions can only grow avocados during specific times of the year.
* Mexico can produce avocados all year round.
* Outliers are present in most of the variables

### Avocado price trend vs sales volume trend
![image](https://github.com/user-attachments/assets/073ea929-6d4f-4d29-9e3b-9f71ed07de89)

### Observations
* Avocado prices have fluctuated over the years, making it challenging for price prediction models to identify a clear pattern.
* Spikes in sales volume often correspond with dips in price.

### Avocado price trend vs total production volume trend
![image](https://github.com/user-attachments/assets/3e32f3ec-cd39-4c4b-9612-77b1a498f781)

### Observations
* Total production volume also negatively correlates with the price,  production volume going up often makes the price go down.


### Correlation matrix between numerical variables

![image](https://github.com/user-attachments/assets/9373b3e1-e4eb-4656-97d6-cf6430eec225)

### Observations
* Sales volume columns are highly correlated with one another, we should only keep one of them to avoid multicollinearity.
* The weekly economic indicator and gas price variables show a positive correlation with the price, though the strength of the relationship is moderate(0.26 and 0.27 respectively).
* Mexico's production volume negatively correlates with the average price, primarily because 90% of U.S. avocado imports come from Mexico.
* California production volume positively correlates with the average price, possibly because avocados from this region are more expensive.
* Chile and the Dominican Republic's production volume show almost no correlation with the price, they should be removed.
* Total production volume and Mexico's production volume exhibit a moderate positive correlation, indicating redundancy.


