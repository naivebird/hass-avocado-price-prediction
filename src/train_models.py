import pickle
from os import makedirs
from os.path import join, dirname, exists

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor


def split_by_region(df, target, test_size=0.2):
    train_list = []
    test_list = []

    for region, region_df in df.groupby("region"):
        region_df = region_df.sort_values("date")
        X = region_df.loc[:, df.columns != target]
        y = region_df[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, shuffle=False)

        train_list.append(pd.concat([X_train, y_train], axis=1))
        test_list.append(pd.concat([X_test, y_test], axis=1))

    train_df = pd.concat(train_list).reset_index(drop=True)
    test_df = pd.concat(test_list).reset_index(drop=True)

    return train_df, test_df


def split_data(df):
    target = "next_week_average_selling_price"

    df.sort_values(["region", "type", "date"], inplace=True)

    df[target] = df.groupby(["region", "type"])["average_selling_price"].shift(-1)

    df.dropna(inplace=True)

    train_df, test_df = split_by_region(df, target)

    train_df.drop(columns=['date', 'region', 'type', 'year_week'], inplace=True)

    features = [col for col in train_df.columns if col != target]
    X_train, y_train = train_df[features], train_df[target]
    X_test, y_test = test_df[features], test_df[target]
    return X_train, X_test, y_train, y_test


def train_models(df):
    X_train, X_test, y_train, y_test = split_data(df)

    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'XGBoost': XGBRegressor(n_estimators=100, random_state=42)
    }

    results = {
        'Model': [],
        'MAE': [],
        'RMSE': [],
        'R^2': []
    }
    predictions = {}

    for name, model in models.items():
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        predictions[name] = y_pred

        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        results['Model'].append(name)
        results['MAE'].append(mae)
        results['RMSE'].append(rmse)
        results['R^2'].append(r2)

        print(f"{name} - MAE: {mae:.2f}, RMSE: {rmse:.2f}, R^2: {r2:.2f}")

        if not exists(join(dirname(__file__), "models")):
            makedirs(join(dirname(__file__), "models"))

        with open("models/{}.pkl".format(name.replace(" ", "_").lower()), "wb") as f:
            pickle.dump(model, f)
    best_model_index = results['R^2'].index(max(results['R^2']))
    print("The best model is: ", results['Model'][best_model_index])
