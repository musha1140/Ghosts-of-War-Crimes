import pandas as pd

def test_no_missing_values():
    df = pd.read_csv("data/processed_data/processed_data.csv")
    assert df.isnull().sum().sum() == 0, "No missing values in processed data"
