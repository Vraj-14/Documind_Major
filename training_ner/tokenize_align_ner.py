# def align_labels(text, entities, tokenizer, label2id):

#     tokenized = tokenizer(
#         text,
#         truncation=True,
#         return_offsets_mapping=True
#     )

#     offsets = tokenized["offset_mapping"]

#     labels = ["O"] * len(offsets)

#     for start, end, entity in entities:

#         for i, (token_start, token_end) in enumerate(offsets):

#             if token_start >= start and token_end <= end:

#                 if token_start == start:
#                     labels[i] = f"B-{entity}"
#                 else:
#                     labels[i] = f"I-{entity}"

#     labels = [label2id[label] for label in labels]

#     tokenized["labels"] = labels

#     return tokenized





# def align_labels(text, entities, tokenizer, label2id):

#     tokenized = tokenizer(
#         text,
#         truncation=True,
#         padding="max_length",
#         max_length=64,
#         return_offsets_mapping=True
#     )

#     offsets = tokenized["offset_mapping"]

#     labels = []

#     for token_start, token_end in offsets:

#         label = "O"

#         for start, end, entity in entities:

#             if token_start >= start and token_end <= end:

#                 if token_start == start:
#                     label = f"B-{entity}"
#                 else:
#                     label = f"I-{entity}"

#         labels.append(label)

#     labels = [label2id[label] for label in labels]

#     # ignore padding tokens
#     labels = [
#         label if offset != (0, 0) else -100
#         for label, offset in zip(labels, offsets)
#     ]

#     tokenized["labels"] = labels

#     tokenized.pop("offset_mapping")

#     return tokenized











def align_labels(text, entities, tokenizer, label2id):
    """
    Tokenize `text` and align BIO labels from character-span `entities`.

    entities: list of [start, end, label]  (character offsets, end is exclusive)
    Returns a dict with input_ids, attention_mask, labels (no offset_mapping).
    """

    tokenized = tokenizer(
        text,
        truncation=True,
        padding="max_length",
        max_length=128,
        return_offsets_mapping=True
    )

    offsets = tokenized["offset_mapping"]
    labels = []

    for token_start, token_end in offsets:

        # Special tokens ([CLS], [SEP], [PAD]) have offset (0, 0) — ignore them
        if token_start == 0 and token_end == 0:
            labels.append(-100)
            continue

        assigned_label = "O"

        for start, end, entity in entities:
            # Token overlaps with this entity span
            if token_start < end and token_end > start:
                if token_start == start:
                    assigned_label = f"B-{entity}"
                else:
                    assigned_label = f"I-{entity}"
                break  # first matching entity wins

        labels.append(label2id[assigned_label])

    tokenized["labels"] = labels
    tokenized.pop("offset_mapping")

    return tokenized