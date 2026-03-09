from sklearn.model_selection import train_test_split


def split_dataset(df):
    # First split: Train (80%) and Temp (20%)
    train_df, temp_df = train_test_split(
        df,
        test_size=0.2,
        stratify=df["label_id"],
        random_state=42
    )

    # Second split: Validation (10%) and Test (10%)
    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.5,
        stratify=temp_df["label_id"],
        random_state=42
    )

    return train_df, val_df, test_df