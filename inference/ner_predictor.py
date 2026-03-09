from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification

MODEL_PATH = "models/ner_model"

# Load tokenizer + model
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForTokenClassification.from_pretrained(MODEL_PATH)

ner = pipeline(
    "token-classification",
    model=model,
    tokenizer=tokenizer,
    aggregation_strategy="simple"  # merges subword tokens into full words
)


def predict_entities(text):
    """
    Run NER on `text` and return a dict of {label: [list of entity strings]}.
    Duplicate values under the same label are deduplicated.
    """

    result = ner(text)

    entities = {}

    for r in result:
        label = r["entity_group"]
        # "word" from aggregation_strategy="simple" may have leading ## artifacts
        # strip whitespace and the Ġ / ## subword prefix chars just in case
        value = r["word"].strip().replace(" ##", "").replace("##", "")

        if not value:
            continue

        if label not in entities:
            entities[label] = []

        if value not in entities[label]:
            entities[label].append(value)

    return entities


def predict_entities_detailed(text):
    """
    Returns full span details: label, word, score, start, end.
    Useful for debugging model output quality.
    """
    result = ner(text)
    return [
        {
            "label": r["entity_group"],
            "word": r["word"].strip(),
            "score": round(r["score"], 4),
            "start": r["start"],
            "end": r["end"],
        }
        for r in result
    ]


if __name__ == "__main__":

    tests = [
        "What is profit of Eicher Motors Limited ?"
    ]

    # import transformers
    # print(transformers.__version__)

    for text in tests:
        print(f"\nInput : {text}")
        print(f"Entities : {predict_entities(text)}")
        print("Detailed:")
        for e in predict_entities_detailed(text):
            print(f"  {e}")