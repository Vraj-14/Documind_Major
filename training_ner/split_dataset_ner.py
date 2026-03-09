from sklearn.model_selection import train_test_split


def split_dataset(df):

    train_df, temp_df = train_test_split(
        df,
        test_size=0.2,
        random_state=42
    )

    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.5,
        random_state=42
    )

    return train_df, val_df, test_df