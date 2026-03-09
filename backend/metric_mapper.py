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


def map_metric(metric):

    metric = metric.lower().strip()

    if metric in METRIC_MAP:
        return METRIC_MAP[metric]

    raise ValueError(f"Metric not supported: {metric}")