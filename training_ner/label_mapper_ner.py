def get_label_list():

    labels = [
        "O",
        "B-COMPANY",
        "I-COMPANY",
        "B-METRIC",
        "I-METRIC",
        "B-YEAR",
        "I-YEAR",
        "B-TIMERANGE",
        "I-TIMERANGE"
    ]

    label2id = {label: i for i, label in enumerate(labels)}
    id2label = {i: label for i, label in enumerate(labels)}

    return labels, label2id, id2label  