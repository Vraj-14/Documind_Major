import json
import pandas as pd


def load_dataset(path):

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    return df