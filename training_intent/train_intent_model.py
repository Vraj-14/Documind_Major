import torch
import joblib
from datasets import Dataset
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments
)

from dataset_loader import load_dataset
from label_encoder import encode_labels
from split_dataset import split_dataset


DATA_PATH = "data/intent_dataset.csv"
MODEL_OUTPUT = "models/intent_classifier"


# ------------------------------------------------
# Load dataset
# ------------------------------------------------

df = load_dataset(DATA_PATH)

df, encoder, label_map = encode_labels(df)

train_df, val_df, test_df = split_dataset(df)


# ------------------------------------------------
# Convert to HuggingFace datasets
# ------------------------------------------------

train_dataset = Dataset.from_pandas(train_df[["text", "label_id"]]).rename_column("label_id", "labels")
val_dataset = Dataset.from_pandas(val_df[["text", "label_id"]]).rename_column("label_id", "labels")
test_dataset = Dataset.from_pandas(test_df[["text", "label_id"]]).rename_column("label_id", "labels")


# ------------------------------------------------
# Tokenizer
# ------------------------------------------------

tokenizer = DistilBertTokenizerFast.from_pretrained(
    "distilbert-base-uncased"
)


def tokenize(batch):
    return tokenizer(
        batch["text"],
        padding=True,
        truncation=True
    )


train_dataset = train_dataset.map(tokenize, batched=True)
val_dataset = val_dataset.map(tokenize, batched=True)
test_dataset = test_dataset.map(tokenize, batched=True)


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


# ------------------------------------------------
# Model
# ------------------------------------------------

num_labels = len(label_map)

model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=num_labels
)


# ------------------------------------------------
# Training arguments
# ------------------------------------------------

training_args = TrainingArguments(
    output_dir="models/training_output",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=6,
    eval_strategy="epoch",
    save_strategy="epoch",
    logging_dir="models/logs"
)


# ------------------------------------------------
# Trainer
# ------------------------------------------------

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)


# ------------------------------------------------
# Train model
# ------------------------------------------------

trainer.train()


# ------------------------------------------------
# Save model + tokenizer
# ------------------------------------------------

model.save_pretrained(MODEL_OUTPUT)
tokenizer.save_pretrained(MODEL_OUTPUT)


# ------------------------------------------------
# Save label encoder
# ------------------------------------------------

joblib.dump(encoder, f"{MODEL_OUTPUT}/label_encoder.pkl")

print("\nModel and label encoder saved successfully.")