# # from .metric_mapper import map_metric

# # def build_query(intent, entities):
# #     """
# #     Main router for SQL query creation
# #     """

# #     if intent == "metric_lookup":
# #         return metric_lookup_query(entities)

# #     elif intent == "comparison":
# #         return comparison_query(entities)

# #     elif intent == "trend_analysis":
# #         return trend_analysis_query(entities)

# #     elif intent == "performance_analysis":
# #         return performance_query(entities)

# #     else:
# #         raise ValueError("Unsupported intent")


# # # --------------------------------
# # # Metric Lookup
# # # --------------------------------

# # # def metric_lookup_query(entities):

# # #     company = entities.get("COMPANY", [None])[0]
# # #     metric = entities.get("METRIC", [None])[0]
# # #     year = entities.get("YEAR", [None])[0]

# # #     query = f"""
# # #     SELECT {metric}
# # #     FROM financials_yearly
# # #     JOIN company_master USING(company_id)
# # #     WHERE company_name = '{company}'
# # #     AND fiscal_year = {year};
# # #     """

# # #     return query

# # def metric_lookup_query(entities):

# #     company = entities.get("COMPANY", [None])[0]
# #     metric = entities.get("METRIC", [None])[0]
# #     year = entities.get("YEAR", [None])[0]

# #     metric = map_metric(metric)

# #     query = f"""
# #     SELECT {metric}
# #     FROM financials_yearly
# #     JOIN company_master USING(company_id)
# #     WHERE company_name = '{company}'
# #     AND fiscal_year = {year};
# #     """

# #     return query


# # # --------------------------------
# # # Comparison
# # # --------------------------------

# # # def comparison_query(entities):

# # #     companies = entities.get("COMPANY", [])
# # #     metric = entities.get("METRIC", [None])[0]
# # #     year = entities.get("YEAR", [None])[0]

# # #     company_list = ",".join([f"'{c}'" for c in companies])

# # #     query = f"""
# # #     SELECT company_name, {metric}
# # #     FROM financials_yearly
# # #     JOIN company_master USING(company_id)
# # #     WHERE company_name IN ({company_list})
# # #     AND fiscal_year = {year};
# # #     """

# # #     return query

# # def comparison_query(entities):

# #     companies = entities.get("COMPANY", [])
# #     metric = entities.get("METRIC", [None])[0]
# #     year = entities.get("YEAR", [None])[0]

# #     metric = map_metric(metric)

# #     company_list = ",".join([f"'{c}'" for c in companies])

# #     query = f"""
# #     SELECT company_name, {metric}
# #     FROM financials_yearly
# #     JOIN company_master USING(company_id)
# #     WHERE company_name IN ({company_list})
# #     AND fiscal_year = {year};
# #     """

# #     return query


# # # --------------------------------
# # # Trend Analysis
# # # --------------------------------

# # # def trend_analysis_query(entities):

# # #     company = entities.get("COMPANY", [None])[0]
# # #     metric = entities.get("METRIC", [None])[0]

# # #     query = f"""
# # #     SELECT fiscal_year, {metric}
# # #     FROM financials_yearly
# # #     JOIN company_master USING(company_id)
# # #     WHERE company_name = '{company}'
# # #     ORDER BY fiscal_year;
# # #     """

# # #     return query

# # def trend_analysis_query(entities):

# #     company = entities.get("COMPANY", [None])[0]
# #     metric = entities.get("METRIC", [None])[0]

# #     metric = map_metric(metric)

# #     query = f"""
# #     SELECT fiscal_year, {metric}
# #     FROM financials_yearly
# #     JOIN company_master USING(company_id)
# #     WHERE company_name = '{company}'
# #     ORDER BY fiscal_year;
# #     """

# #     return query

# # # --------------------------------
# # # Performance Analysis
# # # --------------------------------

# # def performance_query(entities):

# #     company = entities.get("COMPANY", [None])[0]
# #     year = entities.get("YEAR", [None])[0]

# #     query = f"""
# #     SELECT revenue, net_profit, eps
# #     FROM financials_yearly
# #     JOIN company_master USING(company_id)
# #     WHERE company_name = '{company}'
# #     AND fiscal_year = {year};
# #     """

# #     return query


























# # from .metric_mapper import map_metric

# # def build_query(intent, entities):
# #     """
# #     Main router for SQL query creation
# #     """

# #     if intent == "metric_lookup":
# #         return metric_lookup_query(entities)

# #     elif intent == "comparison":
# #         return comparison_query(entities)

# #     elif intent == "trend_analysis":
# #         return trend_analysis_query(entities)

# #     elif intent == "performance_analysis":
# #         return performance_query(entities)

# #     else:
# #         raise ValueError("Unsupported intent")


# # # --------------------------------
# # # Metric Lookup
# # # --------------------------------

# # def metric_lookup_query(entities):

# #     company = entities.get("COMPANY", [None])[0]
# #     year = entities.get("YEAR", [None])[0]

# #     # FIX: get ALL metrics, not just [0]
# #     raw_metrics = entities.get("METRIC", [])

# #     if not raw_metrics:
# #         raise ValueError("No metric found in question")

# #     # Map each metric name to its DB column name
# #     mapped_metrics = [map_metric(m) for m in raw_metrics]

# #     # Build comma-separated column list e.g. "revenue, net_profit, eps"
# #     columns_str = ", ".join(mapped_metrics)

# #     query = f"""
# #     SELECT {columns_str}
# #     FROM financials_yearly
# #     JOIN company_master USING(company_id)
# #     WHERE company_name = '{company}'
# #     AND fiscal_year = {year};
# #     """

# #     return query


# # # --------------------------------
# # # Comparison
# # # --------------------------------

# # def comparison_query(entities):

# #     companies = entities.get("COMPANY", [])
# #     metric = entities.get("METRIC", [None])[0]
# #     year = entities.get("YEAR", [None])[0]

# #     metric = map_metric(metric)

# #     company_list = ",".join([f"'{c}'" for c in companies])

# #     query = f"""
# #     SELECT company_name, {metric}
# #     FROM financials_yearly
# #     JOIN company_master USING(company_id)
# #     WHERE company_name IN ({company_list})
# #     AND fiscal_year = {year};
# #     """

# #     return query


# # # --------------------------------
# # # Trend Analysis
# # # --------------------------------

# # def trend_analysis_query(entities):

# #     company = entities.get("COMPANY", [None])[0]
# #     metric = entities.get("METRIC", [None])[0]

# #     metric = map_metric(metric)

# #     query = f"""
# #     SELECT fiscal_year, {metric}
# #     FROM financials_yearly
# #     JOIN company_master USING(company_id)
# #     WHERE company_name = '{company}'
# #     ORDER BY fiscal_year;
# #     """

# #     return query


# # # --------------------------------
# # # Performance Analysis
# # # --------------------------------

# # def performance_query(entities):

# #     company = entities.get("COMPANY", [None])[0]
# #     year = entities.get("YEAR", [None])[0]

# #     query = f"""
# #     SELECT revenue, net_profit, eps
# #     FROM financials_yearly
# #     JOIN company_master USING(company_id)
# #     WHERE company_name = '{company}'
# #     AND fiscal_year = {year};
# #     """

# #     return query

















# from .metric_mapper import map_metric

# def build_query(intent, entities):
#     """
#     Main router for SQL query creation
#     """

#     if intent == "metric_lookup":
#         return metric_lookup_query(entities)

#     elif intent == "comparison":
#         return comparison_query(entities)

#     elif intent == "trend_analysis":
#         return trend_analysis_query(entities)

#     elif intent == "performance_analysis":
#         return performance_query(entities)

#     else:
#         raise ValueError("Unsupported intent")


# # --------------------------------
# # Metric Lookup
# # --------------------------------

# def metric_lookup_query(entities):

#     company = entities.get("COMPANY", [None])[0]
#     year = entities.get("YEAR", [None])[0]

#     raw_metrics = entities.get("METRIC", [])

#     if not raw_metrics:
#         raise ValueError("No metric found in question")

#     mapped_metrics = [map_metric(m) for m in raw_metrics if m is not None]

#     if not mapped_metrics:
#         raise ValueError("No valid metric found after mapping")

#     columns_str = ", ".join(mapped_metrics)

#     query = f"""
#     SELECT {columns_str}
#     FROM financials_yearly
#     JOIN company_master USING(company_id)
#     WHERE company_name = '{company}'
#     AND fiscal_year = {year};
#     """

#     return query


# # --------------------------------
# # Comparison
# # --------------------------------

# def comparison_query(entities):

#     companies = entities.get("COMPANY", [])
#     year = entities.get("YEAR", [None])[0]

#     raw_metrics = entities.get("METRIC", [])

#     # If no metric extracted, fall back to revenue
#     if not raw_metrics or raw_metrics[0] is None:
#         metric = "revenue"
#     else:
#         metric = map_metric(raw_metrics[0])

#     company_list = ",".join([f"'{c}'" for c in companies])

#     query = f"""
#     SELECT company_name, {metric}
#     FROM financials_yearly
#     JOIN company_master USING(company_id)
#     WHERE company_name IN ({company_list})
#     AND fiscal_year = {year};
#     """

#     return query


# # --------------------------------
# # Trend Analysis
# # --------------------------------

# def trend_analysis_query(entities):

#     company = entities.get("COMPANY", [None])[0]

#     raw_metrics = entities.get("METRIC", [])

#     if not raw_metrics or raw_metrics[0] is None:
#         raise ValueError("No metric found in question")

#     metric = map_metric(raw_metrics[0])

#     query = f"""
#     SELECT fiscal_year, {metric}
#     FROM financials_yearly
#     JOIN company_master USING(company_id)
#     WHERE company_name = '{company}'
#     ORDER BY fiscal_year;
#     """

#     return query


# # --------------------------------
# # Performance Analysis
# # --------------------------------

# def performance_query(entities):

#     company = entities.get("COMPANY", [None])[0]
#     year = entities.get("YEAR", [None])[0]

#     query = f"""
#     SELECT revenue, net_profit, eps
#     FROM financials_yearly
#     JOIN company_master USING(company_id)
#     WHERE company_name = '{company}'
#     AND fiscal_year = {year};
#     """

#     return query













# from .metric_mapper import map_metric, get_metric_table


# def build_query(intent, entities):
#     """
#     Main router for SQL query creation.
#     """
#     if intent == "metric_lookup":
#         return metric_lookup_query(entities)

#     elif intent == "comparison":
#         return comparison_query(entities)

#     elif intent == "trend_analysis":
#         return trend_analysis_query(entities)

#     elif intent == "performance_analysis":
#         return performance_query(entities)

#     else:
#         raise ValueError(f"Unsupported intent: {intent}")


# # ─────────────────────────────────────────────────────────────
# # HELPERS
# # ─────────────────────────────────────────────────────────────

# def _year_filter(years):
#     """
#     OLD: always used a single year → AND fiscal_year = {year}
#          This caused Bug 2 — only the first extracted year was used,
#          so "revenue in 2024 and 2025" silently dropped 2025.

#     NEW: if multiple years are present, use IN (...) so every
#          requested year is included in the result set.
#     """
#     if not years:
#         return ""
#     if len(years) == 1:
#         return f"AND fy.fiscal_year = {years[0]}"
#     year_list = ", ".join(str(y) for y in years)
#     return f"AND fy.fiscal_year IN ({year_list})"


# def _build_from_clause(table):
#     """
#     OLD: every query hard-coded JOIN financials_yearly regardless of metric,
#          so market metrics like pe_ratio caused a 500 UndefinedColumn error.

#     NEW: dynamically selects the correct primary data table and always
#          joins company_master for the company name.
#          When the metric lives in market_data_yearly the alias 'fy' still
#          works because we alias whichever table we pick as 'fy'.
#     """
#     return f"""
#     FROM {table} fy
#     JOIN company_master cm ON cm.company_id = fy.company_id"""


# def _detect_primary_table(mapped_metrics):
#     """
#     Decide which single table to query from.
#     If ALL metrics are from the same table, use that table.
#     If metrics span both tables, default to financials_yearly
#     (mixed-table queries require a more complex JOIN — handle via
#     performance_query which manually selects from both).
#     """
#     tables = {get_metric_table(m) for m in mapped_metrics}
#     if len(tables) == 1:
#         return tables.pop()
#     # Mixed: fall back to financials_yearly (edge case)
#     return "financials_yearly"


# # ─────────────────────────────────────────────────────────────
# # METRIC LOOKUP  (single company, one or more metrics, one or more years)
# # ─────────────────────────────────────────────────────────────

# def metric_lookup_query(entities):
#     """
#     Bug 1 fix: route to the correct table based on the requested metric.
#     Bug 2 fix: support multiple years with IN (...).

#     Example – old query for pe_ratio:
#         SELECT pe_ratio
#         FROM financials_yearly          ← WRONG TABLE → 500 error
#         JOIN company_master USING(company_id)
#         WHERE company_name = 'ICICI Bank Limited'
#         AND fiscal_year = 2026;

#     Example – new query for pe_ratio:
#         SELECT fy.pe_ratio
#         FROM market_data_yearly fy      ← correct table
#         JOIN company_master cm ON cm.company_id = fy.company_id
#         WHERE cm.company_name = 'ICICI Bank Limited'
#         AND fy.fiscal_year = 2026;

#     Example – new query for revenue 2024 + 2025:
#         SELECT fy.fiscal_year, fy.revenue
#         FROM financials_yearly fy
#         JOIN company_master cm ON cm.company_id = fy.company_id
#         WHERE cm.company_name = 'HDFC Bank Limited'
#         AND fy.fiscal_year IN (2024, 2025)
#         ORDER BY fy.fiscal_year;
#     """
#     company = entities.get("COMPANY", [None])[0]
#     years   = entities.get("YEAR", [])

#     raw_metrics = entities.get("METRIC", [])
#     if not raw_metrics:
#         raise ValueError("No metric found in question")

#     mapped_metrics = [map_metric(m) for m in raw_metrics if m is not None]
#     if not mapped_metrics:
#         raise ValueError("No valid metric found after mapping")

#     primary_table = _detect_primary_table(mapped_metrics)
#     from_clause   = _build_from_clause(primary_table)
#     year_filter   = _year_filter(years)

#     # Include fiscal_year in SELECT when multiple years requested so the
#     # LLM can label each row correctly.
#     if len(years) > 1:
#         columns_str = "fy.fiscal_year, " + ", ".join(f"fy.{m}" for m in mapped_metrics)
#         order_clause = "ORDER BY fy.fiscal_year"
#     else:
#         columns_str  = ", ".join(f"fy.{m}" for m in mapped_metrics)
#         order_clause = ""

#     query = f"""
#     SELECT {columns_str}{from_clause}
#     WHERE cm.company_name = '{company}'
#     {year_filter}
#     {order_clause};
#     """
#     return query


# # ─────────────────────────────────────────────────────────────
# # COMPARISON  (multiple companies, one metric, one year)
# # ─────────────────────────────────────────────────────────────

# def comparison_query(entities):
#     """
#     Bug 1 fix: same table-routing logic applied here.

#     Old: metric was always fetched from financials_yearly.
#     New: table is chosen based on the metric requested.
#     """
#     companies = entities.get("COMPANY", [])
#     years     = entities.get("YEAR", [])

#     raw_metrics = entities.get("METRIC", [])
#     if not raw_metrics or raw_metrics[0] is None:
#         metric = "revenue"
#     else:
#         metric = map_metric(raw_metrics[0])

#     primary_table = get_metric_table(metric)
#     from_clause   = _build_from_clause(primary_table)
#     year_filter   = _year_filter(years)
#     company_list  = ", ".join(f"'{c}'" for c in companies)

#     query = f"""
#     SELECT cm.company_name, fy.{metric}{from_clause}
#     WHERE cm.company_name IN ({company_list})
#     {year_filter};
#     """
#     return query


# # ─────────────────────────────────────────────────────────────
# # TREND ANALYSIS  (single company, one metric, all years)
# # ─────────────────────────────────────────────────────────────

# def trend_analysis_query(entities):
#     """
#     No year filter here — fetches all available years for the metric.
#     Bug 1 fix: table routing applied.
#     """
#     company = entities.get("COMPANY", [None])[0]

#     raw_metrics = entities.get("METRIC", [])
#     if not raw_metrics or raw_metrics[0] is None:
#         raise ValueError("No metric found in question")

#     metric        = map_metric(raw_metrics[0])
#     primary_table = get_metric_table(metric)
#     from_clause   = _build_from_clause(primary_table)

#     query = f"""
#     SELECT fy.fiscal_year, fy.{metric}{from_clause}
#     WHERE cm.company_name = '{company}'
#     ORDER BY fy.fiscal_year;
#     """
#     return query


# # ─────────────────────────────────────────────────────────────
# # PERFORMANCE ANALYSIS  (revenue + net_profit + eps, single year)
# # ─────────────────────────────────────────────────────────────

# def performance_query(entities):
#     """
#     These three columns all live in financials_yearly, so no routing change
#     needed here. Bug 2 fix: year handled via _year_filter for consistency.
#     """
#     company = entities.get("COMPANY", [None])[0]
#     years   = entities.get("YEAR", [])

#     year_filter = _year_filter(years)

#     query = f"""
#     SELECT fy.revenue, fy.net_profit, fy.eps
#     FROM financials_yearly fy
#     JOIN company_master cm ON cm.company_id = fy.company_id
#     WHERE cm.company_name = '{company}'
#     {year_filter};
#     """
#     return query











from .metric_mapper import map_metric, get_metric_table


def build_query(intent, entities):
    """
    Main router for SQL query creation.
    """
    if intent == "metric_lookup":
        return metric_lookup_query(entities)

    elif intent == "comparison":
        return comparison_query(entities)

    elif intent == "trend_analysis":
        return trend_analysis_query(entities)

    elif intent == "performance_analysis":
        return performance_query(entities)

    else:
        raise ValueError(f"Unsupported intent: {intent}")


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def _year_filter(years):
    """
    OLD: always used a single year → AND fiscal_year = {year}
         This caused Bug 2 — only the first extracted year was used,
         so "revenue in 2024 and 2025" silently dropped 2025.

    NEW: if multiple years are present, use IN (...) so every
         requested year is included in the result set.
    """
    if not years:
        return ""
    if len(years) == 1:
        return f"AND fy.fiscal_year = {years[0]}"
    year_list = ", ".join(str(y) for y in years)
    return f"AND fy.fiscal_year IN ({year_list})"


def _build_from_clause(table):
    """
    OLD: every query hard-coded JOIN financials_yearly regardless of metric,
         so market metrics like pe_ratio caused a 500 UndefinedColumn error.

    NEW: dynamically selects the correct primary data table and always
         joins company_master for the company name.
         When the metric lives in market_data_yearly the alias 'fy' still
         works because we alias whichever table we pick as 'fy'.
    """
    return f"""
    FROM {table} fy
    JOIN company_master cm ON cm.company_id = fy.company_id"""


def _detect_primary_table(mapped_metrics):
    """
    Decide which single table to query from.
    If ALL metrics are from the same table, use that table.
    If metrics span both tables, default to financials_yearly
    (mixed-table queries require a more complex JOIN — handle via
    performance_query which manually selects from both).
    """
    tables = {get_metric_table(m) for m in mapped_metrics}
    if len(tables) == 1:
        return tables.pop()
    # Mixed: fall back to financials_yearly (edge case)
    return "financials_yearly"


# ─────────────────────────────────────────────────────────────
# METRIC LOOKUP  (single company, one or more metrics, one or more years)
# ─────────────────────────────────────────────────────────────

def metric_lookup_query(entities):
    """
    Bug 1 fix: route to the correct table based on the requested metric.
    Bug 2 fix: support multiple years with IN (...).

    Example – old query for pe_ratio:
        SELECT pe_ratio
        FROM financials_yearly          ← WRONG TABLE → 500 error
        JOIN company_master USING(company_id)
        WHERE company_name = 'ICICI Bank Limited'
        AND fiscal_year = 2026;

    Example – new query for pe_ratio:
        SELECT fy.pe_ratio
        FROM market_data_yearly fy      ← correct table
        JOIN company_master cm ON cm.company_id = fy.company_id
        WHERE cm.company_name = 'ICICI Bank Limited'
        AND fy.fiscal_year = 2026;

    Example – new query for revenue 2024 + 2025:
        SELECT fy.fiscal_year, fy.revenue
        FROM financials_yearly fy
        JOIN company_master cm ON cm.company_id = fy.company_id
        WHERE cm.company_name = 'HDFC Bank Limited'
        AND fy.fiscal_year IN (2024, 2025)
        ORDER BY fy.fiscal_year;
    """
    company = entities.get("COMPANY", [None])[0]
    years   = entities.get("YEAR", [])

    raw_metrics = entities.get("METRIC", [])
    if not raw_metrics:
        raise ValueError("No metric found in question")

    mapped_metrics = [map_metric(m) for m in raw_metrics if m is not None]
    if not mapped_metrics:
        raise ValueError("No valid metric found after mapping")

    primary_table = _detect_primary_table(mapped_metrics)
    from_clause   = _build_from_clause(primary_table)
    year_filter   = _year_filter(years)

    # Include fiscal_year in SELECT when multiple years requested so the
    # LLM can label each row correctly.
    if len(years) > 1:
        columns_str = "fy.fiscal_year, " + ", ".join(f"fy.{m}" for m in mapped_metrics)
        order_clause = "ORDER BY fy.fiscal_year"
    else:
        columns_str  = ", ".join(f"fy.{m}" for m in mapped_metrics)
        order_clause = ""

    query = f"""
    SELECT {columns_str}{from_clause}
    WHERE cm.company_name = '{company}'
    {year_filter}
    {order_clause};
    """
    return query


# ─────────────────────────────────────────────────────────────
# COMPARISON  (multiple companies, one metric, one year)
# ─────────────────────────────────────────────────────────────

def comparison_query(entities):
    """
    Always selects fiscal_year + company_name + metric so the LLM
    knows exactly which value belongs to which company and year.

    OLD query (missing fiscal_year):
        SELECT cm.company_name, fy.revenue
        FROM financials_yearly fy
        JOIN company_master cm ON cm.company_id = fy.company_id
        WHERE cm.company_name IN ('Reliance Industries Limited')
        AND fy.fiscal_year IN (2023, 2024);

        Returned rows: (Reliance, 8778350000000), (Reliance, 9010640000000)
        The LLM had no way to know which row was 2023 and which was 2024,
        so it guessed — and guessed wrong, swapping the values.

    NEW query (fiscal_year always included, ORDER BY year then company):
        SELECT fy.fiscal_year, cm.company_name, fy.revenue
        FROM financials_yearly fy
        JOIN company_master cm ON cm.company_id = fy.company_id
        WHERE cm.company_name IN ('Reliance Industries Limited')
        AND fy.fiscal_year IN (2023, 2024)
        ORDER BY fy.fiscal_year, cm.company_name;

        Returned rows: (2023, Reliance, 8778350000000), (2024, Reliance, 9010640000000)
        Now the LLM can read the year label directly from the data.
    """
    companies = entities.get("COMPANY", [])
    years     = entities.get("YEAR", [])

    raw_metrics = entities.get("METRIC", [])
    if not raw_metrics or raw_metrics[0] is None:
        metric = "revenue"
    else:
        metric = map_metric(raw_metrics[0])

    primary_table = get_metric_table(metric)
    from_clause   = _build_from_clause(primary_table)
    year_filter   = _year_filter(years)
    company_list  = ", ".join(f"'{c}'" for c in companies)

    query = f"""
    SELECT fy.fiscal_year, cm.company_name, fy.{metric}{from_clause}
    WHERE cm.company_name IN ({company_list})
    {year_filter}
    ORDER BY fy.fiscal_year, cm.company_name;
    """
    return query


# ─────────────────────────────────────────────────────────────
# TREND ANALYSIS  (single company, one metric, all years)
# ─────────────────────────────────────────────────────────────

def trend_analysis_query(entities):
    """
    No year filter here — fetches all available years for the metric.
    Bug 1 fix: table routing applied.
    """
    company = entities.get("COMPANY", [None])[0]

    raw_metrics = entities.get("METRIC", [])
    if not raw_metrics or raw_metrics[0] is None:
        raise ValueError("No metric found in question")

    metric        = map_metric(raw_metrics[0])
    primary_table = get_metric_table(metric)
    from_clause   = _build_from_clause(primary_table)

    query = f"""
    SELECT fy.fiscal_year, fy.{metric}{from_clause}
    WHERE cm.company_name = '{company}'
    ORDER BY fy.fiscal_year;
    """
    return query


# ─────────────────────────────────────────────────────────────
# PERFORMANCE ANALYSIS  (revenue + net_profit + eps, single year)
# ─────────────────────────────────────────────────────────────

def performance_query(entities):
    """
    These three columns all live in financials_yearly, so no routing change
    needed here. Bug 2 fix: year handled via _year_filter for consistency.
    """
    company = entities.get("COMPANY", [None])[0]
    years   = entities.get("YEAR", [])

    year_filter = _year_filter(years)

    query = f"""
    SELECT fy.fiscal_year, fy.revenue, fy.net_profit, fy.eps
    FROM financials_yearly fy
    JOIN company_master cm ON cm.company_id = fy.company_id
    WHERE cm.company_name = '{company}'
    {year_filter}
    ORDER BY fy.fiscal_year;
    """
    return query