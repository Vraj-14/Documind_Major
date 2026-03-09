# import torch
# from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification


# MODEL_PATH = "models/intent_classifier"


# tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_PATH)

# model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)

# model.eval()


# labels = [
#     "metric_lookup",
#     "trend_analysis",
#     "comparison",
#     "performance_analysis"
# ]


# def predict_intent(text):

#     inputs = tokenizer(
#         text,
#         return_tensors="pt",
#         truncation=True,
#         padding=True
#     )

#     with torch.no_grad():
#         outputs = model(**inputs)

#     logits = outputs.logits

#     pred = torch.argmax(logits, dim=1).item()
    
#     return labels[pred]


# # test example
# if __name__ == "__main__":

#     q = "I'm looking for the performance summary of Bajaj Finserv Ltd"

#     intent = predict_intent(q)

#     print("Predicted intent:", intent)













import torch
import joblib
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification


MODEL_PATH = "models/intent_classifier"


# ------------------------------------------------
# Load model
# ------------------------------------------------

tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_PATH)

model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)

encoder = joblib.load(f"{MODEL_PATH}/label_encoder.pkl")

model.eval()


# ------------------------------------------------
# Prediction function
# ------------------------------------------------

def predict_intent(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True
    )

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits

    pred_id = torch.argmax(logits, dim=1).item()

    label = encoder.inverse_transform([pred_id])[0]

    return label


# ------------------------------------------------
# Test
# ------------------------------------------------

if __name__ == "__main__":

    q = "What is the revenue of HDFC Bank Limited in 2024?"

    intent = predict_intent(q)

    print("Predicted intent:", intent)