# import sys
# import os

# # Add parent directory to Python path
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from inference.intent_predictor import predict_intent


# from inference.intent_predictor import predict_intent
# from inference.ner_predictor import predict_entities

# from backend.query_builder import build_query
# from backend.database import execute_query


# def process_question(question):

#     intent = predict_intent(question)

#     entities = predict_entities(question)

#     query = build_query(intent, entities)

#     columns, rows = execute_query(query)

#     return {
#         "intent": intent,
#         "entities": entities,
#         "query": query,
#         "columns": columns,
#         "data": rows
#     }

import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.intent_predictor import predict_intent
from inference.ner_predictor import predict_entities

from .query_builder import build_query
from .database import execute_query
from .llm_generator import generate_answer


def process_question(question):

    intent = predict_intent(question)

    entities = predict_entities(question)

    query = build_query(intent, entities)

    columns, rows = execute_query(query)

    answer = generate_answer(question, columns, rows)

    entities = predict_entities(question)
    print("ENTITIES:", entities) 

    return {
        "intent": intent,
        "entities": entities,
        "query": query,
        "data": rows,
        "answer": answer
    }


    