# METRIC_MAP = {

#     "revenue": "revenue",
#     "net profit": "net_profit",
#     "eps": "eps",
#     "total assets": "total_assets",
#     "total debt": "total_debt",
#     "total equity": "total_equity",
#     "operating cash flow": "operating_cash_flow",

#     "market cap": "market_cap",
#     "share price": "share_price",
#     "pe ratio": "pe_ratio",
#     "pb ratio": "pb_ratio",
#     "dividend yield": "dividend_yield"
# }


# def map_metric(metric):

#     metric = metric.lower().strip()

#     if metric in METRIC_MAP:
#         return METRIC_MAP[metric]

#     raise ValueError(f"Metric not supported: {metric}")



METRIC_MAP = {
    "revenue": "revenue",
    "net profit": "net_profit",
    "eps": "eps",
    "total assets": "total_assets",
    "total debt": "total_debt",
    "total equity": "total_equity",
    "operating cash flow": "operating_cash_flow",

    "market cap": "market_cap",
    "share price": "share_price",
    "pe ratio": "pe_ratio",
    "pb ratio": "pb_ratio",
    "dividend yield": "dividend_yield"
}

# NEW: tells query_builder which table each mapped DB column lives in
METRIC_TABLE_MAP = {
    "revenue":              "financials_yearly",
    "net_profit":           "financials_yearly",
    "eps":                  "financials_yearly",
    "total_assets":         "financials_yearly",
    "total_debt":           "financials_yearly",
    "total_equity":         "financials_yearly",
    "operating_cash_flow":  "financials_yearly",

    "market_cap":           "market_data_yearly",
    "share_price":          "market_data_yearly",
    "pe_ratio":             "market_data_yearly",
    "pb_ratio":             "market_data_yearly",
    "dividend_yield":       "market_data_yearly",
}


def map_metric(metric):
    metric = metric.lower().strip()
    if metric in METRIC_MAP:
        return METRIC_MAP[metric]
    raise ValueError(f"Metric not supported: {metric}")


def get_metric_table(db_column):
    """
    Given a mapped DB column name (e.g. 'pe_ratio'),
    returns the table it belongs to.
    Defaults to financials_yearly if unknown.
    """
    return METRIC_TABLE_MAP.get(db_column, "financials_yearly")