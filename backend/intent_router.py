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








# import sys
# import os

# # Add parent directory to Python path
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from inference.intent_predictor import predict_intent
# from inference.ner_predictor import predict_entities

# from .query_builder import build_query
# from .database import execute_query
# from .llm_generator import generate_answer


# def process_question(question):

#     intent = predict_intent(question)

#     entities = predict_entities(question)

#     query = build_query(intent, entities)

#     columns, rows = execute_query(query)

#     answer = generate_answer(question, columns, rows)

#     entities = predict_entities(question)
#     print("ENTITIES:", entities) 

#     return {
#         "intent": intent,
#         "entities": entities,
#         "query": query,
#         "data": rows,
#         "answer": answer
#     }


    














# import sys
# import os
# import re

# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from inference.intent_predictor import predict_intent
# from inference.ner_predictor import predict_entities

# from .query_builder import build_query
# from .database import execute_query
# from .llm_generator import generate_answer


# # ─────────────────────────────────────────────────────────────
# # NER REPAIR LAYER
# # ─────────────────────────────────────────────────────────────

# def _repair_years(entities, original_question):
#     """
#     The NER model frequently mis-tokenises years, producing:
#         YEAR: ['202']   TIMERANGE: ['4 and 2025']
#     instead of:
#         YEAR: ['2024', '2025']

#     OLD behaviour: broken year tokens were passed directly to the query
#     builder, generating  AND fiscal_year = 202  which matches nothing,
#     causing empty DB results and LLM hallucination.

#     NEW behaviour:
#       1. Extract ALL 4-digit years directly from the raw question using
#          a simple regex — completely bypassing the NER year output.
#       2. Replace entities['YEAR'] with the regex-extracted list.
#       3. Drop the spurious TIMERANGE key so it doesn't confuse anything
#          downstream.

#     This is intentionally simple and robust: a regex on the question
#     is far more reliable than the NER model for pure digit patterns.
#     """
#     # Find every 4-digit number that looks like a plausible fiscal year
#     years_in_question = re.findall(r'\b(19\d{2}|20\d{2})\b', original_question)

#     if years_in_question:
#         # Deduplicate while preserving order
#         seen = set()
#         unique_years = []
#         for y in years_in_question:
#             if y not in seen:
#                 seen.add(y)
#                 unique_years.append(y)
#         entities['YEAR'] = unique_years
#     else:
#         # If no year found in question, keep whatever NER gave (may be empty)
#         pass

#     # Remove TIMERANGE — it was only ever produced as a side-effect of
#     # the NER model mis-splitting years and is never used by query_builder
#     entities.pop('TIMERANGE', None)

#     return entities


# def _validate_entities(entities, intent):
#     """
#     Lightweight sanity check before hitting the DB.
#     Returns a string error message if something critical is missing,
#     or None if everything looks okay.
#     """
#     company = entities.get('COMPANY', [])
#     year    = entities.get('YEAR', [])
#     metric  = entities.get('METRIC', [])

#     if not company or company[0] is None:
#         return "I couldn't identify a company name in your question. Please mention the full company name."

#     if intent in ('metric_lookup', 'comparison', 'performance_analysis'):
#         if not year:
#             return "I couldn't identify a year in your question. Please specify a fiscal year (e.g. 2024)."
#         # Extra guard: reject any year token that is not exactly 4 digits
#         for y in year:
#             if not re.fullmatch(r'19\d{2}|20\d{2}', str(y)):
#                 return (
#                     f"The year '{y}' doesn't look right. "
#                     "Please use a 4-digit fiscal year like 2024 or 2025."
#                 )

#     if intent == 'metric_lookup' and not metric:
#         return "I couldn't identify a financial metric in your question."

#     return None  # all good


# # ─────────────────────────────────────────────────────────────
# # MAIN ENTRY POINT
# # ─────────────────────────────────────────────────────────────

# def process_question(question):

#     # 1. Intent + NER
#     intent   = predict_intent(question)
#     entities = predict_entities(question)

#     # 2. Repair NER year extraction (the main bug fix)
#     entities = _repair_years(entities, question)

#     print("ENTITIES (after repair):", entities)

#     # 3. Validate before touching the DB
#     validation_error = _validate_entities(entities, intent)
#     if validation_error:
#         return {
#             "intent":   intent,
#             "entities": entities,
#             "query":    None,
#             "data":     [],
#             "answer":   validation_error
#         }

#     # 4. Build SQL and execute
#     try:
#         query = build_query(intent, entities)
#         columns, rows = execute_query(query)
#     except ValueError as ve:
#         # Unsupported intent / metric mapping failure
#         return {
#             "intent":   intent,
#             "entities": entities,
#             "query":    None,
#             "data":     [],
#             "answer":   f"Sorry, I couldn't process that question: {str(ve)}"
#         }
#     except Exception as db_err:
#         # DB-level error (column doesn't exist, connection issue, etc.)
#         print("DB ERROR:", db_err)
#         return {
#             "intent":   intent,
#             "entities": entities,
#             "query":    str(db_err),
#             "data":     [],
#             "answer":   (
#                 "I ran into a database error while fetching your data. "
#                 "The metric you asked about may not be available in the database."
#             )
#         }

#     # 5. Guard against empty results — do NOT send empty data to the LLM
#     #    OLD: empty rows were passed to generate_answer which caused the
#     #         LLM to hallucinate placeholder values like [insert value, e.g., 20.50]
#     #    NEW: return a clear "no data" message immediately
#     if not rows:
#         companies = ", ".join(entities.get("COMPANY", []))
#         years     = ", ".join(str(y) for y in entities.get("YEAR", []))
#         return {
#             "intent":   intent,
#             "entities": entities,
#             "query":    query,
#             "data":     [],
#             "answer":   (
#                 f"No data found for {companies} "
#                 f"{'in ' + years if years else ''}. "
#                 "Please check that the company name and fiscal year exist in the database."
#             )
#         }

#     # 6. Generate natural-language answer from real DB data
#     answer = generate_answer(question, columns, rows)

#     return {
#         "intent":   intent,
#         "entities": entities,
#         "query":    query,
#         "data":     rows,
#         "answer":   answer
#     }




















# import sys
# import os
# import re

# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from inference.intent_predictor import predict_intent
# from inference.ner_predictor import predict_entities

# from .query_builder import build_query
# from .database import execute_query
# from .llm_generator import generate_answer


# # ─────────────────────────────────────────────────────────────
# # STEP 1 — YEAR REPAIR
# # Regex replaces the NER model's broken year tokens entirely.
# # e.g.  YEAR:['202']  TIMERANGE:['4 and 2025']  →  YEAR:['2024','2025']
# # ─────────────────────────────────────────────────────────────

# def _repair_years(entities, question):
#     years = re.findall(r'\b(19\d{2}|20\d{2})\b', question)
#     seen, unique = set(), []
#     for y in years:
#         if y not in seen:
#             seen.add(y)
#             unique.append(y)
#     if unique:
#         entities['YEAR'] = unique
#     entities.pop('TIMERANGE', None)
#     return entities


# # ─────────────────────────────────────────────────────────────
# # STEP 2 — INTENT OVERRIDE
# #
# # The trained intent model makes two recurring mistakes:
# #
# #   A) Trend questions ("PE ratio trend", "share price over the years")
# #      → model predicts metric_lookup instead of trend_analysis
# #      FIX: if no year found in question AND trend keywords present
# #           → force trend_analysis
# #
# #   B) Comparison questions with market metrics ("compare PE ratio of X and Y")
# #      → model predicts metric_lookup instead of comparison
# #      FIX: if 2+ companies found AND compare keywords present
# #           → force comparison
# #
# #   C) Multi-year single-company questions ("revenue in 2024 and 2025")
# #      → model predicts metric_lookup (correct) but we also check
# #        if it wrongly says comparison when only one company is present
# #      FIX: if only 1 company → can't be comparison → force metric_lookup
# #
# # Rule priority: trend > comparison > model output
# # ─────────────────────────────────────────────────────────────

# TREND_KEYWORDS = re.compile(
#     r'\b(trend|over the years|over years|historical|history|'
#     r'year.on.year|yoy|across years|past years|growth over|'
#     r'how has .+ changed|how did .+ change|progression)\b',
#     re.IGNORECASE
# )

# COMPARE_KEYWORDS = re.compile(
#     r'\b(compare|comparison|vs\.?|versus|between|which is (higher|better|more|greater)|'
#     r'who has (more|higher|better)|difference between)\b',
#     re.IGNORECASE
# )


# def _override_intent(predicted_intent, entities, question):
#     """
#     Returns the corrected intent string.

#     OLD behaviour: raw intent model output was used directly, causing
#     market-metric trend and comparison questions to be misrouted to
#     metric_lookup → wrong SQL → wrong or hallucinated answers.

#     NEW behaviour: lightweight keyword + entity signal rules correct
#     the model before it reaches the query builder.
#     """
#     years     = entities.get('YEAR', [])
#     companies = entities.get('COMPANY', [])

#     # ── Rule 1: Trend override ───────────────────────────────
#     # "show pe ratio trend" / "over the years" → no year in question
#     # The model often predicts metric_lookup here and the year repair
#     # finds no year → validation would reject it.  Force trend_analysis.
#     if not years and TREND_KEYWORDS.search(question):
#         print(f"INTENT OVERRIDE: {predicted_intent} → trend_analysis (trend keyword, no year)")
#         return 'trend_analysis'

#     # ── Rule 2: Comparison override ──────────────────────────
#     # "compare PE ratio of Infosys and Wipro" → model predicts metric_lookup
#     # because it hasn't seen enough market-metric comparison training examples.
#     if len(companies) >= 2 and COMPARE_KEYWORDS.search(question):
#         print(f"INTENT OVERRIDE: {predicted_intent} → comparison (compare keyword, 2+ companies)")
#         return 'comparison'

#     # ── Rule 3: Guard — can't be comparison with 1 company ──
#     # Multi-year single-company questions ("revenue in 2024 and 2025")
#     # should stay metric_lookup, not comparison.
#     if predicted_intent == 'comparison' and len(companies) < 2:
#         print(f"INTENT OVERRIDE: comparison → metric_lookup (only {len(companies)} company found)")
#         return 'metric_lookup'

#     return predicted_intent


# # ─────────────────────────────────────────────────────────────
# # STEP 3 — VALIDATION
# # Checks all required entities are present before hitting the DB.
# # ─────────────────────────────────────────────────────────────

# def _validate_entities(entities, intent):
#     company = entities.get('COMPANY', [])
#     year    = entities.get('YEAR', [])
#     metric  = entities.get('METRIC', [])

#     if not company or company[0] is None:
#         return "I couldn't identify a company name. Please use the full company name (e.g. 'Infosys Limited')."

#     # trend_analysis fetches ALL years — no year needed in the question
#     if intent in ('metric_lookup', 'comparison', 'performance_analysis'):
#         if not year:
#             return "I couldn't identify a year. Please specify a fiscal year like 2024 or 2025."
#         for y in year:
#             if not re.fullmatch(r'19\d{2}|20\d{2}', str(y)):
#                 return f"The year '{y}' doesn't look right. Please use a 4-digit fiscal year."

#     if intent in ('metric_lookup', 'trend_analysis', 'comparison') and not metric:
#         return "I couldn't identify a financial metric in your question."

#     return None


# # ─────────────────────────────────────────────────────────────
# # MAIN ENTRY POINT
# # ─────────────────────────────────────────────────────────────

# def process_question(question):

#     # 1. NER + intent from models
#     intent   = predict_intent(question)
#     entities = predict_entities(question)

#     # 2. Repair broken year tokens from NER
#     entities = _repair_years(entities, question)

#     # 3. Correct the intent model's known mis-classifications
#     intent = _override_intent(intent, entities, question)

#     print(f"INTENT: {intent}  |  ENTITIES: {entities}")

#     # 4. Validate before touching the DB
#     error = _validate_entities(entities, intent)
#     if error:
#         return {"intent": intent, "entities": entities,
#                 "query": None, "data": [], "answer": error}

#     # 5. Build SQL and execute
#     try:
#         query = build_query(intent, entities)
#         columns, rows = execute_query(query)
#     except ValueError as ve:
#         return {"intent": intent, "entities": entities,
#                 "query": None, "data": [],
#                 "answer": f"Sorry, I couldn't process that question: {ve}"}
#     except Exception as db_err:
#         print("DB ERROR:", db_err)
#         return {"intent": intent, "entities": entities,
#                 "query": str(db_err), "data": [],
#                 "answer": (
#                     "I ran into a database error while fetching your data. "
#                     "The metric or company may not be available."
#                 )}

#     # 6. Guard empty results — never send empty rows to the LLM
#     if not rows:
#         companies = ", ".join(entities.get("COMPANY", []))
#         years     = ", ".join(str(y) for y in entities.get("YEAR", []))
#         return {"intent": intent, "entities": entities,
#                 "query": query, "data": [],
#                 "answer": (
#                     f"No data found for {companies}"
#                     f"{' in ' + years if years else ''}. "
#                     "Please verify the company name and fiscal year exist in the database."
#                 )}

#     # 7. Generate answer from real DB data
#     answer = generate_answer(question, columns, rows)

#     return {
#         "intent":   intent,
#         "entities": entities,
#         "query":    query,
#         "data":     rows,
#         "answer":   answer
#     }













# 2-4-26

import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.intent_predictor import predict_intent
from inference.ner_predictor import predict_entities

from .query_builder import build_query
from .database import execute_query
from .llm_generator import generate_answer
from .yfinance_fallback import fetch_from_yfinance


# ─────────────────────────────────────────────────────────────
# STEP 1 — YEAR REPAIR
# ─────────────────────────────────────────────────────────────

def _repair_years(entities, question):
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', question)
    seen, unique = set(), []
    for y in years:
        if y not in seen:
            seen.add(y)
            unique.append(y)
    if unique:
        entities['YEAR'] = unique
    entities.pop('TIMERANGE', None)
    return entities


# ─────────────────────────────────────────────────────────────
# STEP 2 — INTENT OVERRIDE  (expanded keyword + entity rules)
#
# OLD: ~6 keyword phrases, no entity-only signal, returns str
# NEW: 20+ phrases, entity-signal rule, returns (intent, reason, confidence)
# ─────────────────────────────────────────────────────────────

TREND_KEYWORDS = re.compile(
    r'\b(trend|trend analysis|over the years|over years|historical|history|'
    r'year.on.year|yoy|across years|past years|growth over|'
    r'how has|how did .+ change|progression|trajectory|'
    r'year by year|over time|since \d{4}|from \d{4})\b',
    re.IGNORECASE
)

COMPARE_KEYWORDS = re.compile(
    r'\b(compare|comparison|vs\.?|versus|between|'
    r'which is (higher|better|more|greater|lower)|'
    r'who has (more|higher|better)|difference between|'
    r'rank|ranking|better than|higher than|lower than|'
    r'which company|who performed)\b',
    re.IGNORECASE
)

PERF_KEYWORDS = re.compile(
    r'\b(perform|performance|overall|how did|how is|'
    r'financial health|results)\b',
    re.IGNORECASE
)


def _override_intent(predicted_intent, model_confidence, entities, question):
    """
    Returns: (final_intent, override_reason, display_confidence)

    override_reason values (internal — not sent to UI):
        'model'                  — no rule fired, model output accepted
        'rule_trend'             — trend keyword detected, no year
        'rule_compare_keyword'   — compare keyword + 2+ companies
        'rule_entity_signal'     — 2 companies + year, no keyword needed
        'rule_guard_trend'       — trend + specific year → metric_lookup
        'rule_guard_comparison'  — comparison with only 1 company
        'rule_performance'       — performance keyword detected
    """
    years     = entities.get('YEAR', [])
    companies = entities.get('COMPANY', [])

    # Rule 1: trend keyword + no year in question
    if not years and TREND_KEYWORDS.search(question):
        print(f"INTENT OVERRIDE: {predicted_intent} → trend_analysis (rule_trend)")
        return 'trend_analysis', 'rule_trend', 0.90

    # Rule 2a: compare keyword + 2+ companies
    if len(companies) >= 2 and COMPARE_KEYWORDS.search(question):
        print(f"INTENT OVERRIDE: {predicted_intent} → comparison (rule_compare_keyword)")
        return 'comparison', 'rule_compare_keyword', 0.92

    # Rule 2b: 2 companies + year present — entity signal alone is enough
    if len(companies) >= 2 and years:
        print(f"INTENT OVERRIDE: {predicted_intent} → comparison (rule_entity_signal)")
        return 'comparison', 'rule_entity_signal', 0.80

    # Rule 3: trend predicted but a specific year was given → metric_lookup
    if predicted_intent == 'trend_analysis' and len(years) == 1:
        print(f"INTENT OVERRIDE: trend_analysis → metric_lookup (rule_guard_trend)")
        return 'metric_lookup', 'rule_guard_trend', 0.85

    # Rule 4: comparison predicted but only 1 company found
    if predicted_intent == 'comparison' and len(companies) < 2:
        print(f"INTENT OVERRIDE: comparison → metric_lookup (rule_guard_comparison)")
        return 'metric_lookup', 'rule_guard_comparison', 0.85

    # Rule 5: performance keywords + single company + year
    if PERF_KEYWORDS.search(question) and len(companies) == 1 and years:
        print(f"INTENT OVERRIDE: {predicted_intent} → performance_analysis (rule_performance)")
        return 'performance_analysis', 'rule_performance', 0.78

    # No rule fired — trust the model
    return predicted_intent, 'model', model_confidence


# ─────────────────────────────────────────────────────────────
# STEP 3 — VALIDATION
# ─────────────────────────────────────────────────────────────

def _validate_entities(entities, intent):
    company = entities.get('COMPANY', [])
    year    = entities.get('YEAR', [])
    metric  = entities.get('METRIC', [])

    if not company or company[0] is None:
        return "I couldn't identify a company name. Please use the full company name (e.g. 'Infosys Limited')."

    if intent in ('metric_lookup', 'comparison', 'performance_analysis'):
        if not year:
            return "I couldn't identify a year. Please specify a fiscal year like 2024 or 2025."
        for y in year:
            if not re.fullmatch(r'19\d{2}|20\d{2}', str(y)):
                return f"The year '{y}' doesn't look right. Please use a 4-digit fiscal year."

    if intent in ('metric_lookup', 'trend_analysis', 'comparison') and not metric:
        return "I couldn't identify a financial metric in your question."

    return None


# ─────────────────────────────────────────────────────────────
# STEP 4 — FALLBACK RUNNER
# ─────────────────────────────────────────────────────────────

def _run_fallback(question, intent, entities):
    try:
        print("FALLBACK: DB had no data — trying yfinance...")
        columns, rows, note = fetch_from_yfinance(entities, intent)

        if not rows:
            print("FALLBACK: yfinance also returned no data")
            return None

        answer = generate_answer(
            question + f"\n\n[{note}]",
            columns,
            rows
        )

        return {
            "intent":      intent,
            "entities":    entities,
            "query":       "yfinance_fallback",
            "data":        rows,
            "answer":      f"{answer}\n\n_{note}_",
            # confidence / intent debug fields preserved
            "predicted_intent":   intent,
            "final_intent":       intent,
            "confidence":         None,
            "override_fired":     False,
        }

    except Exception as fb_err:
        print(f"FALLBACK ERROR: {fb_err}")
        return None


# ─────────────────────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────────────────────

def process_question(question):

    # 1. NER + intent (now returns label + confidence)
    predicted_intent, model_confidence = predict_intent(question)
    entities = predict_entities(question)

    # 2. Repair broken year tokens from NER
    entities = _repair_years(entities, question)

    # 3. Override layer — returns (final_intent, reason, confidence)
    final_intent, override_reason, confidence = _override_intent(
        predicted_intent, model_confidence, entities, question
    )

    override_fired = (final_intent != predicted_intent)

    print(f"PREDICTED: {predicted_intent} ({model_confidence:.0%})  "
          f"FINAL: {final_intent} ({confidence:.0%})  "
          f"REASON: {override_reason}")

    # 4. Validate before touching the DB
    error = _validate_entities(entities, final_intent)
    if error:
        return {
            "intent":           final_intent,
            "entities":         entities,
            "query":            None,
            "data":             [],
            "answer":           error,
            "predicted_intent": predicted_intent,
            "final_intent":     final_intent,
            "confidence":       round(confidence * 100, 1),
            "override_fired":   override_fired,
        }

    # 5. Build SQL and execute
    db_ok   = False
    columns = []
    rows    = []
    query   = None

    try:
        query = build_query(final_intent, entities)
        columns, rows = execute_query(query)
        db_ok = True
    except ValueError as ve:
        print(f"DB ValueError: {ve} — trying fallback")
    except Exception as db_err:
        print(f"DB ERROR: {db_err} — trying fallback")
        query = str(db_err)

    # 6. Empty rows → trigger fallback
    if db_ok and not rows:
        print("DB returned empty rows — trying fallback")
        db_ok = False

    # 7. If DB failed → yfinance fallback
    if not db_ok:
        fallback_result = _run_fallback(question, final_intent, entities)
        if fallback_result:
            fallback_result["predicted_intent"] = predicted_intent
            fallback_result["final_intent"]     = final_intent
            fallback_result["confidence"]       = round(confidence * 100, 1)
            fallback_result["override_fired"]   = override_fired
            return fallback_result

        companies = ", ".join(entities.get("COMPANY", []))
        years     = ", ".join(str(y) for y in entities.get("YEAR", []))
        return {
            "intent":           final_intent,
            "entities":         entities,
            "query":            query,
            "data":             [],
            "answer":           (
                f"No data found for {companies}"
                f"{' in ' + years if years else ''}. "
                "The data is not available in the local database or Yahoo Finance."
            ),
            "predicted_intent": predicted_intent,
            "final_intent":     final_intent,
            "confidence":       round(confidence * 100, 1),
            "override_fired":   override_fired,
        }

    # 8. DB succeeded — generate answer
    answer = generate_answer(question, columns, rows)

    return {
        "intent":           final_intent,
        "entities":         entities,
        "query":            query,
        "data":             rows,
        "answer":           answer,
        "predicted_intent": predicted_intent,
        "final_intent":     final_intent,
        "confidence":       round(confidence * 100, 1),
        "override_fired":   override_fired,
    }