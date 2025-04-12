from io import BytesIO

import kagglehub
import pandas as pd
import requests

WEI_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=WEI&scale=left&cosd=2008-01-05&coed=2025-03-22&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Weekly%2C%20Ending%20Saturday&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-03-30&revision_date=2025-03-30&nd=2008-01-05"
GAS_URL = "https://www.eia.gov/petroleum/gasdiesel/xls/pswrgvwall.xls"
HOLIDAY_DATASET_NAME = "jeremygerdes/us-federal-pay-and-leave-holidays-2004-to-2100-csv"
HOLIDAY_DATASET_PATH = "400_Years_of_Generated_Dates_and_Holidays.csv"

WEI_PATH = "avocado-data/raw_data/WEI.csv"
GASOLINE_PRICE_PATH = "avocado-data/raw_data/gasoline_price.csv"
US_HOLIDAYS_PATH = "avocado-data/raw_data/us_holidays.csv"
AVOCADO_PRICE_PATH = "avocado-data/raw_data/{year}-plu-total-hab-data.csv"
AVOCADO_PRODUCTION_VOLUME_PATH = "avocado-data/raw_data/Volume Data  Projections - Hass Avocado Board {year}.csv"


def download_wei_data(url, output_path):
    response = requests.get(url)
    with open(output_path, "wb") as f:
        f.write(response.content)


def download_gasoline_price_data(url, output_path):
    response = requests.get(url)
    df = pd.read_excel(BytesIO(response.content), sheet_name="Data 1", skiprows=2)
    df.rename(
        columns={
            "Weekly U.S. Regular Conventional Retail Gasoline Prices  (Dollars per Gallon)": "gasoline_price"
        },
        inplace=True
    )
    df = df[["Date", "gasoline_price"]]
    df.to_csv(output_path, index=False)


def download_us_holiday_data(dataset_name, dataset_path, output_path):
    path = kagglehub.dataset_download(dataset_name, dataset_path)
    with open(path, "r") as f:
        with open(output_path, "w") as out:
            out.write(f.read())


def download_data():
    download_wei_data(WEI_URL, WEI_PATH)
    download_gasoline_price_data(GAS_URL, GASOLINE_PRICE_PATH)
    download_us_holiday_data(HOLIDAY_DATASET_NAME, HOLIDAY_DATASET_PATH, US_HOLIDAYS_PATH)
