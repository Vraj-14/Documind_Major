import json
import glob

INPUT_FOLDER = r"E:\8th Sem\MAJOR\Documind\data\entity_text_NER"
OUTPUT_FILE = "data/ner_dataset_final.json"

INPUT_FILES = glob.glob(INPUT_FOLDER + r"\*.json")

final_dataset = []
skipped = 0

for input_file in INPUT_FILES:
    print(f"Processing: {input_file}")

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        text = item["text"]
        entities = []
        valid = True

        for entity_text, label in item["entities"]:

            # FIX: find all occurrences, not just the first one.
            # If an entity appears more than once, add a span for each occurrence.
            start = 0
            found = False

            while True:
                pos = text.find(entity_text, start)
                if pos == -1:
                    break
                found = True
                end = pos + len(entity_text)
                entities.append([pos, end, label])
                start = pos + 1  # move past current match to find next

            if not found:
                # Entity text not found in the sentence — skip this record
                print(f"  WARNING: '{entity_text}' not found in: {text[:80]}")
                valid = False
                break

        if valid:
            final_dataset.append({
                "text": text,
                "entities": entities
            })
        else:
            skipped += 1

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(final_dataset, f, indent=2, ensure_ascii=False)

print(f"\nNER dataset created: {OUTPUT_FILE}")
print(f"Total records: {len(final_dataset)}")
print(f"Skipped (entity not found): {skipped}")