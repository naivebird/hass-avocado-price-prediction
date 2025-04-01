from src.collect_data import download_data
from src.process_data import preprocess_data
from src.train_models import train_models


def main():
    download_data()
    df = preprocess_data()
    train_models(df)


if __name__ == '__main__':
    main()
