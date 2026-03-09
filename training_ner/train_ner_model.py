import torch
from transformers import (
    AutoTokenizer,
    BertForTokenClassification,
    Trainer,
    TrainingArguments
)
from datasets import Dataset, Features, Sequence, Value

from dataset_loader_ner import load_dataset
from split_dataset_ner import split_dataset
from label_mapper_ner import get_label_list
from tokenize_align_ner import align_labels


DATA_PATH = "data/ner_dataset_final.json"
MODEL_OUTPUT = "models/ner_model"
BASE_MODEL = "dslim/bert-base-NER"

# -----------------------------
# Load dataset
# -----------------------------

df = load_dataset(DATA_PATH)

train_df, val_df, test_df = split_dataset(df)

# Reset index so iloc lookups are safe after split
train_df = train_df.reset_index(drop=True)
val_df = val_df.reset_index(drop=True)
test_df = test_df.reset_index(drop=True)

# -----------------------------
# Tokenizer
# -----------------------------

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

labels, label2id, id2label = get_label_list()

# -----------------------------
# Tokenization function
# -----------------------------

def tokenize_function(example):
    import json as _json
    text = example["text"]
    # Deserialize from JSON string → [[start, end, label], ...]
    entities = [tuple(e) for e in _json.loads(example["entities_json"])]

    tokenized = align_labels(
        text,
        entities,
        tokenizer,
        label2id
    )

    return tokenized


# -----------------------------
# Convert to HF Dataset
# -----------------------------

# PyArrow cannot infer the schema of entities because each span is [int, int, str]
# — a mixed-type list. We convert each span to a dict and declare an explicit
# Features schema so PyArrow knows exactly what types to expect.

def df_to_hf_dataset(dataframe):
    """
    Store entities as a JSON string to avoid PyArrow mixed-type issues entirely.
    We parse it back inside tokenize_function.
    """
    import json as _json

    records = []
    for _, row in dataframe.iterrows():
        records.append({
            "text": row["text"],
            "entities_json": _json.dumps(row["entities"])  # serialize to plain string
        })

    return Dataset.from_list(records)


train_dataset = df_to_hf_dataset(train_df)
val_dataset   = df_to_hf_dataset(val_df)
test_dataset  = df_to_hf_dataset(test_df)

train_dataset = train_dataset.map(tokenize_function)
val_dataset = val_dataset.map(tokenize_function)
test_dataset = test_dataset.map(tokenize_function)

train_dataset.set_format(
    type="torch",
    columns=["input_ids", "attention_mask", "labels"]
)
val_dataset.set_format(
    type="torch",
    columns=["input_ids", "attention_mask", "labels"]
)
test_dataset.set_format(
    type="torch",
    columns=["input_ids", "attention_mask", "labels"]
)

# Quick sanity check — print one sample before training
print("Sample training record:")
print(train_dataset[0])

# -----------------------------
# Model
# -----------------------------

model = BertForTokenClassification.from_pretrained(
    BASE_MODEL,
    num_labels=len(labels),
    id2label=id2label,
    label2id=label2id,
    ignore_mismatched_sizes=True  # needed since we replace the classifier head
)

# -----------------------------
# Training arguments
# -----------------------------

training_args = TrainingArguments(
    output_dir="models/ner_training_output",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=5,          # increase from 2 — NER needs more epochs
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True, # keep best checkpoint
    logging_dir="models/ner_logs",
    logging_steps=10,
)

# -----------------------------
# Trainer
# -----------------------------

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# -----------------------------
# Train
# -----------------------------

trainer.train()

# -----------------------------
# Save model
# -----------------------------

model.save_pretrained(MODEL_OUTPUT)
tokenizer.save_pretrained(MODEL_OUTPUT)

print("NER model trained and saved successfully.")