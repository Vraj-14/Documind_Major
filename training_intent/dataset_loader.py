import pandas as pd


def load_dataset(path):
    df = pd.read_csv(path)

    # Validate required columns
    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError("Dataset must contain 'text' and 'label' columns")

    # Remove empty rows
    df = df.dropna()

    return df