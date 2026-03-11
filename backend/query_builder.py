from .metric_mapper import map_metric

def build_query(intent, entities):
    """
    Main router for SQL query creation
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
        raise ValueError("Unsupported intent")


# --------------------------------
# Metric Lookup
# --------------------------------

# def metric_lookup_query(entities):

#     company = entities.get("COMPANY", [None])[0]
#     metric = entities.get("METRIC", [None])[0]
#     year = entities.get("YEAR", [None])[0]

#     query = f"""
#     SELECT {metric}
#     FROM financials_yearly
#     JOIN company_master USING(company_id)
#     WHERE company_name = '{company}'
#     AND fiscal_year = {year};
#     """

#     return query

def metric_lookup_query(entities):

    company = entities.get("COMPANY", [None])[0]
    metric = entities.get("METRIC", [None])[0]
    year = entities.get("YEAR", [None])[0]

    metric = map_metric(metric)

    query = f"""
    SELECT {metric}
    FROM financials_yearly
    JOIN company_master USING(company_id)
    WHERE company_name = '{company}'
    AND fiscal_year = {year};
    """

    return query


# --------------------------------
# Comparison
# --------------------------------

# def comparison_query(entities):

#     companies = entities.get("COMPANY", [])
#     metric = entities.get("METRIC", [None])[0]
#     year = entities.get("YEAR", [None])[0]

#     company_list = ",".join([f"'{c}'" for c in companies])

#     query = f"""
#     SELECT company_name, {metric}
#     FROM financials_yearly
#     JOIN company_master USING(company_id)
#     WHERE company_name IN ({company_list})
#     AND fiscal_year = {year};
#     """

#     return query

def comparison_query(entities):

    companies = entities.get("COMPANY", [])
    metric = entities.get("METRIC", [None])[0]
    year = entities.get("YEAR", [None])[0]

    metric = map_metric(metric)

    company_list = ",".join([f"'{c}'" for c in companies])

    query = f"""
    SELECT company_name, {metric}
    FROM financials_yearly
    JOIN company_master USING(company_id)
    WHERE company_name IN ({company_list})
    AND fiscal_year = {year};
    """

    return query


# --------------------------------
# Trend Analysis
# --------------------------------

# def trend_analysis_query(entities):

#     company = entities.get("COMPANY", [None])[0]
#     metric = entities.get("METRIC", [None])[0]

#     query = f"""
#     SELECT fiscal_year, {metric}
#     FROM financials_yearly
#     JOIN company_master USING(company_id)
#     WHERE company_name = '{company}'
#     ORDER BY fiscal_year;
#     """

#     return query

def trend_analysis_query(entities):

    company = entities.get("COMPANY", [None])[0]
    metric = entities.get("METRIC", [None])[0]

    metric = map_metric(metric)

    query = f"""
    SELECT fiscal_year, {metric}
    FROM financials_yearly
    JOIN company_master USING(company_id)
    WHERE company_name = '{company}'
    ORDER BY fiscal_year;
    """

    return query

# --------------------------------
# Performance Analysis
# --------------------------------

def performance_query(entities):

    company = entities.get("COMPANY", [None])[0]
    year = entities.get("YEAR", [None])[0]

    query = f"""
    SELECT revenue, net_profit, eps
    FROM financials_yearly
    JOIN company_master USING(company_id)
    WHERE company_name = '{company}'
    AND fiscal_year = {year};
    """

    return query