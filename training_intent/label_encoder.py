from sklearn.preprocessing import LabelEncoder


def encode_labels(df):
    # Create encoder
    encoder = LabelEncoder()

    # Encode labels into integers
    df["label_id"] = encoder.fit_transform(df["label"])

    # Create mapping: label -> id
    label_map = dict(
        zip(
            encoder.classes_,
            encoder.transform(encoder.classes_)
        )
    )

    return df, encoder, label_map