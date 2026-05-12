import pandas as pd

import panel as pn
pn.extension()

def load_data():
    df = pd.read_csv('./../3-data-analysis/titanic.csv')
    return df

if __name__ == '__main__':
    df = load_data()
    print(df.head())
    print(df.info())
    print(df.describe())
    print(df.isnull().sum())
    print(df.columns)