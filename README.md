# Overview
This project aims to predict next week's Hass avocado prices across multiple regions in the US using historical price data, production volume data, and other economic indicators. In this project, you can run this notebook: `src/hass_avocado_price_prediction.ipynb` to see my exploratory data analysis, feature engineering, and model training processes. There are also some other Python files including the `src/main.py` file which you can run to quickly achieve the same things (without data visualization) at your terminal as an alternative.

# Dataset
In this project, I combined multiple datasets to build price-prediction models. All raw datasets are stored in the `src/avocado-data/raw_data` directory. You can also find the combined dataset in `src/avocado-data/combined_data`, and train and test data in `src/avocado-data/train_and_test_data`.

### Avocado price data 
Link: [Hass Avocado Board](https://hassavocadoboard.com/category-data/?region=Total%20U.S.&y=2022) (login required).

Columns:
* `ASP Current Year`: average selling price
* `Geography`: the city or region of the observation
* `Current Year Week Ending`: the date of the observation
* `Type`: the type of avocado, conventional or organic
* `Total Bulk and Bags Units`: total number of avocados sold
* `4046 Units`: total number of avocados with PLU 4046 sold
* `4225 Units`: total number of avocados with PLU 4225 sold
* `4770 Units`: total number of avocados with PLU 4770 sold
* `TotalBagged Units`: total number of bags sold

### Avocado production volume data
Link: [Hass Avocado Board](https://hassavocadoboard.com/volume-data-projections/) (login required).

Columns:
* `Year`: the year of the observation
* `Week Number`: the week number of the observation
* `Status`: the status of the record, Actual or Projected
* `Total Volume`: total avocado production volume in California and other South American countries combined
* `California`: California production volume
* `Chile`: Chile's production volume
* `Mexico`: Mexico's production volume
* `Peru`: Peru's production volume
* `Colombia`: Colombia's production volume
* `Dominican Republic`: Dominican Republic's production volume

### Weekly Economic Index
Link: [FRED Economic Data](https://fred.stlouisfed.org/series/WEI)

Columns:
* `WEI`: the value of the index
* `observation_date`: the date of the observation

### Gasoline price
Link: [US Energy Information Administration](https://www.eia.gov/petroleum/gasdiesel/)

Columns:
* `Date`: the date of the observation
* `gasoline_price`: the price of gasoline


### US public holidays
Link: [Kaggle](https://www.kaggle.com/datasets/jeremygerdes/us-federal-pay-and-leave-holidays-2004-to-2100-csv)

Columns:
* `A_DATE`: the date of the observation
* `IS_HOLIDAY`: a flag to indicate if the date is a holiday

# Reproduction Steps

### Install required packages
Clone the repository:
```bash
git clone https://github.com/naivebird/hass-avocado-price-prediction.git
```

Navigate to the project directory:
```bash
cd hass-avocado-price-prediction
```

Setup your virtual environment
```bash
python -m venv env
env\Scripts\activate
```
Install poetry
```bash
pip install poetry
```
Install the dependencies
```bash
poetry install
```
### Run the notebook
This notebook is important as it has all my observations and explanations for feature engineering and model selection decisions.
```bash
jupyter notebook src/hass_avocado_price_prediction.ipynb
```
### Run the Python script
This is an alternative way to run the project at your terminal.
```bash
cd src
python main.py
```
