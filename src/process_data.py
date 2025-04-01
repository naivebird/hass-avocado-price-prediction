from datetime import datetime

import pandas as pd
from sklearn.preprocessing import StandardScaler

from collect_data import AVOCADO_PRICE_PATH, AVOCADO_PRODUCTION_VOLUME_PATH, GASOLINE_PRICE_PATH, US_HOLIDAYS_PATH, \
    WEI_PATH

YEARS = [2022, 2023, 2024, 2025]


def load_price_data():
    price_dataframes = []
    for year in YEARS:
        price_dataframes.append(pd.read_csv(AVOCADO_PRICE_PATH.format(year=year)))

    price_df = pd.concat(price_dataframes, ignore_index=True)

    price_df.dropna(subset=['Current Year Week Ending'], inplace=True)

    price_df["year_week"] = price_df["Current Year Week Ending"].apply(
        lambda x: x[:4] + '-' + str(datetime.strptime(x, "%Y-%m-%d %H:%M:%S").isocalendar()[1]))

    price_df.rename(columns={
        "ASP Current Year": "average_selling_price",
        "Geography": "region",
        "Current Year Week Ending": "date",
        "Type": "type",
        "Total Bulk and Bags Units": "total_sales_volume",
        "4046 Units": "4046_units",
        "4225 Units": "4225_units",
        "4770 Units": "4770_units",
        "TotalBagged Units": "total_bagged_units"
    }, inplace=True)

    price_df.drop(columns=["Timeframe", "SmlBagged Units", "LrgBagged Units", "X-LrgBagged Units"], inplace=True)

    return price_df


def load_production_volume_data():
    prod_volume_dataframes = []
    for year in YEARS:
        prod_volume_dataframes.append(pd.read_csv(AVOCADO_PRODUCTION_VOLUME_PATH.format(year=year)))
    prod_volume_df = pd.concat(prod_volume_dataframes, ignore_index=True)

    prod_volume_df = prod_volume_df[prod_volume_df["Status"] == "Actual"]

    prod_volume_df.fillna(0, inplace=True)

    prod_volume_df["year_week"] = prod_volume_df.apply(lambda x: str(x["Year"]) + "-" + str(x["Week Number"]), axis=1)

    prod_volume_df.drop(columns=["Status", "Year", "Week Number", "Week Ending"], inplace=True)

    prod_volume_df.rename(columns={
        "Total Volume": "total_prod_volume",
        "California": "california_prod_volume",
        "Chile": "chile_prod_volume",
        "Mexico": "mexico_prod_volume",
        "Peru": "peru_prod_volume",
        "Colombia": "colombia_prod_volume",
        "Dominican Republic": "dominican_republic_prod_volume"
    }, inplace=True)

    volume_cols = ['total_prod_volume', 'california_prod_volume',
                   'chile_prod_volume', 'mexico_prod_volume', 'peru_prod_volume',
                   'colombia_prod_volume', 'dominican_republic_prod_volume']

    for col in volume_cols:
        prod_volume_df[col] = prod_volume_df[col].apply(lambda x: str(x).replace(",", ""))
        prod_volume_df[col] = prod_volume_df[col].astype(float)

    return prod_volume_df


def load_wei_data():
    wei_df = pd.read_csv(WEI_PATH)
    wei_df["year_week"] = wei_df["observation_date"].apply(
        lambda x: x[:4] + '-' + str(datetime.strptime(x, "%Y-%m-%d").isocalendar()[1]))
    return wei_df[['year_week', 'WEI']]


def load_gas_price_data():
    gas_price_df = pd.read_csv(GASOLINE_PRICE_PATH)
    gas_price_df["year_week"] = gas_price_df["Date"].apply(
        lambda x: x[:4] + '-' + str(datetime.strptime(x, "%Y-%m-%d").isocalendar()[1]))
    return gas_price_df[["year_week", "gasoline_price"]]


def load_holidays_data():
    holiday_df = pd.read_csv(US_HOLIDAYS_PATH)

    holiday_df["year_week"] = holiday_df["A_DATE"].apply(
        lambda x: x[-4:] + '-' + str(datetime.strptime(x, "%m/%d/%Y").isocalendar()[1]))

    holiday_df.fillna({"IS_HOLIDAY": 0}, inplace=True)
    holiday_df.rename(columns={"IS_HOLIDAY": "is_holiday"}, inplace=True)
    holiday_df = holiday_df[holiday_df["is_holiday"] == 1]

    return holiday_df[["year_week", "is_holiday"]]


def merge_datasets():
    merged_df = load_price_data()
    for dataset in [load_production_volume_data(), load_wei_data(), load_gas_price_data(), load_holidays_data()]:
        merged_df = pd.merge(merged_df, dataset, on="year_week", how="left")
    merged_df.fillna({"is_holiday": 0}, inplace=True)
    return merged_df


def remove_multi_collinear_features(df):
    columns_to_remove = ["4046_units", "4225_units", "4770_units", "total_bagged_units", "total_prod_volume"]
    df.drop(columns=columns_to_remove, inplace=True)
    return df


def remove_weak_predictors(df):
    columns_to_remove = ["chile_prod_volume", "dominican_republic_prod_volume", "is_holiday"]
    df.drop(columns=columns_to_remove, inplace=True)
    return df


def remove_outliers(df, columns):
    for column in columns:
        if column != "price":
            q1 = df[column].quantile(0.25)
            q3 = df[column].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 3 * iqr
            upper_bound = q3 + 3 * iqr

            df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    return df


def encode_categorical_features(df):
    df = df.dropna().reset_index(drop=True)
    categorical_df = pd.get_dummies(df[['type', 'region']], drop_first=True)
    df = pd.concat([df, categorical_df], axis=1)
    df.drop(columns=['type', 'region'], inplace=True)
    return df


def scale_numerical_features(df, num_cols):
    scaler = StandardScaler()
    df[num_cols] = scaler.fit_transform(df[num_cols])
    return df


def preprocess_data():

    df = merge_datasets()

    df = remove_multi_collinear_features(df)

    df = remove_weak_predictors(df)

    num_cols = [col for col in df.columns if df[col].dtype in ['int64', 'float64'] and col != 'average_selling_price']

    df = remove_outliers(df, num_cols)

    df = scale_numerical_features(df, num_cols)

    return df