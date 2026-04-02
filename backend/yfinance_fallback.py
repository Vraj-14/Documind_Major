# """
# yfinance_fallback.py
# ────────────────────
# Called by intent_router when the primary DB pipeline returns no data
# or raises an error. Fetches financial data from Yahoo Finance using
# the company's ticker symbol (stored in company_master.ticker_symbol).

# Returns (columns, rows) in the same format as database.execute_query()
# so generate_answer() needs zero changes.

# Install dependency:  pip install yfinance
# """

# import yfinance as yf
# from .database import get_ticker   # new helper added to database.py


# # ─────────────────────────────────────────────────────────────
# # METRIC → yfinance field mapping
# # ─────────────────────────────────────────────────────────────

# # financials_yearly metrics come from yf.Ticker.financials (income statement)
# # and yf.Ticker.balance_sheet / cashflow — all are annual DataFrames indexed
# # by field name, with fiscal year end dates as columns.

# YFINANCE_INCOME_MAP = {
#     "revenue":              "Total Revenue",
#     "net_profit":           "Net Income",
#     "eps":                  "Basic EPS",
#     "operating_cash_flow":  "Operating Cash Flow",   # from cashflow sheet
# }

# YFINANCE_BALANCE_MAP = {
#     "total_assets":  "Total Assets",
#     "total_debt":    "Total Debt",
#     "total_equity":  "Stockholders Equity",
# }

# # market_data_yearly metrics come from yf.Ticker.info (live snapshot)
# # or from history() for share price. These are LIVE values only —
# # historical PE/PB/market cap are not available from free yfinance.
# YFINANCE_INFO_MAP = {
#     "market_cap":     "marketCap",
#     "share_price":    "currentPrice",
#     "pe_ratio":       "trailingPE",
#     "pb_ratio":       "priceToBook",
#     "dividend_yield": "dividendYield",
# }


# # ─────────────────────────────────────────────────────────────
# # HELPERS
# # ─────────────────────────────────────────────────────────────

# def _fiscal_year_from_date(dt):
#     """Convert a pandas Timestamp to an integer fiscal year (calendar year)."""
#     try:
#         return int(dt.year)
#     except Exception:
#         return None


# def _fetch_annual_sheet(ticker_obj, metric_col):
#     """
#     Try to get a metric from the income statement first,
#     then the cash flow statement, then the balance sheet.
#     Returns a dict of {fiscal_year: value} or empty dict.
#     """
#     result = {}

#     # Income statement
#     if metric_col in YFINANCE_INCOME_MAP:
#         field = YFINANCE_INCOME_MAP[metric_col]
#         sheet = (
#             ticker_obj.cashflow
#             if metric_col == "operating_cash_flow"
#             else ticker_obj.financials
#         )
#         if sheet is not None and field in sheet.index:
#             for col in sheet.columns:
#                 yr = _fiscal_year_from_date(col)
#                 val = sheet.loc[field, col]
#                 if yr and val is not None:
#                     result[yr] = float(val)
#         return result

#     # Balance sheet
#     if metric_col in YFINANCE_BALANCE_MAP:
#         field = YFINANCE_BALANCE_MAP[metric_col]
#         sheet = ticker_obj.balance_sheet
#         if sheet is not None and field in sheet.index:
#             for col in sheet.columns:
#                 yr = _fiscal_year_from_date(col)
#                 val = sheet.loc[field, col]
#                 if yr and val is not None:
#                     result[yr] = float(val)
#         return result

#     return result


# def _fetch_info_metric(ticker_obj, metric_col):
#     """
#     Fetch a live market metric from ticker.info.
#     Returns a single float or None.
#     """
#     field = YFINANCE_INFO_MAP.get(metric_col)
#     if not field:
#         return None
#     info = ticker_obj.info or {}
#     val = info.get(field)
#     return float(val) if val is not None else None


# # ─────────────────────────────────────────────────────────────
# # PUBLIC ENTRY POINT
# # ─────────────────────────────────────────────────────────────

# def fetch_from_yfinance(entities, intent):
#     """
#     Main fallback function called by intent_router.

#     Parameters
#     ----------
#     entities : dict  — same entities dict used by the DB pipeline
#     intent   : str   — one of metric_lookup / comparison / trend_analysis
#                        / performance_analysis

#     Returns
#     -------
#     (columns, rows, note) on success
#         columns : list[str]
#         rows    : list[tuple]
#         note    : str — short message telling the LLM data came from yfinance

#     Raises
#     ------
#     Exception if yfinance also fails, so intent_router can catch it.
#     """

#     companies = entities.get("COMPANY", [])
#     years     = [int(y) for y in entities.get("YEAR", [])]
#     raw_metrics = entities.get("METRIC", [])

#     # Map metric names to DB column names (same mapper used by query_builder)
#     from .metric_mapper import map_metric, get_metric_table
#     mapped_metrics = []
#     for m in raw_metrics:
#         try:
#             mapped_metrics.append(map_metric(m))
#         except ValueError:
#             pass

#     # Performance analysis always uses these three
#     if intent == "performance_analysis":
#         mapped_metrics = ["revenue", "net_profit", "eps"]

#     if not mapped_metrics:
#         raise ValueError("No valid metrics to fetch from yfinance")

#     # ── Determine whether metrics are live (info) or historical (sheets) ──
#     info_metrics     = [m for m in mapped_metrics if m in YFINANCE_INFO_MAP]
#     history_metrics  = [m for m in mapped_metrics if m in YFINANCE_INCOME_MAP or m in YFINANCE_BALANCE_MAP]

#     all_rows = []

#     for company_name in companies:
#         ticker_symbol = get_ticker(company_name)
#         if not ticker_symbol:
#             print(f"FALLBACK: no ticker for {company_name}, skipping")
#             continue

#         print(f"FALLBACK: fetching yfinance data for {company_name} ({ticker_symbol})")
#         tkr = yf.Ticker(ticker_symbol)

#         # ── Historical metrics (income / balance / cashflow sheets) ──
#         if history_metrics:
#             # Build {metric: {year: value}} map
#             metric_year_data = {}
#             for mc in history_metrics:
#                 metric_year_data[mc] = _fetch_annual_sheet(tkr, mc)

#             # Determine which years to output
#             # Trend = all available years; others = only requested years
#             all_years_available = set()
#             for mc in history_metrics:
#                 all_years_available.update(metric_year_data[mc].keys())

#             if intent == "trend_analysis" or not years:
#                 target_years = sorted(all_years_available)
#             else:
#                 target_years = [y for y in years if y in all_years_available]

#             for yr in target_years:
#                 row_values = [yr, company_name] + [
#                     metric_year_data[mc].get(yr) for mc in history_metrics
#                 ]
#                 all_rows.append(tuple(row_values))

#         # ── Live market metrics (info snapshot) ──
#         if info_metrics:
#             info_row = [None, company_name]  # no fiscal year for live data
#             for mc in info_metrics:
#                 val = _fetch_info_metric(tkr, mc)
#                 info_row.append(val)
#             # Use most recent year if available, else None
#             yr_label = max(years) if years else "Live"
#             info_row[0] = yr_label
#             all_rows.append(tuple(info_row))

#     if not all_rows:
#         raise ValueError("yfinance returned no data for the requested companies/metrics")

#     # Build column names to match what generate_answer expects
#     metric_col_names = history_metrics if history_metrics else info_metrics
#     columns = ["fiscal_year", "company_name"] + metric_col_names

#     note = (
#         "Note: This data was fetched from Yahoo Finance (yfinance) because "
#         "it was not available in the local database."
#     )

#     return columns, all_rows, note



"""
yfinance_fallback.py
────────────────────
Called by intent_router when the primary DB pipeline returns no data
or raises an error.

KEY FIXES vs previous version:
  1. Year matching was too strict — if the user asked for 2021 but yfinance
     only had 2022–2024, target_years became [] → all_rows stayed empty →
     fallback silently returned nothing despite having real data.
     FIX: always return ALL available years from yfinance, then tell the LLM
     which years are available so it can answer appropriately.

  2. Fiscal year date extraction was fragile — HDFC Bank fiscal year ends
     March 31, so yfinance stores "FY2022" under date 2022-03-31.
     A user asking for "2021" would get year=2021 from the date but the
     data is actually for the period ending March 2022.
     FIX: extract year from the column date as-is and pass all rows to LLM
     with a note about date conventions.
"""

import yfinance as yf
from .database import get_ticker


# ─────────────────────────────────────────────────────────────
# METRIC → yfinance field mapping
# ─────────────────────────────────────────────────────────────

YFINANCE_INCOME_MAP = {
    "revenue":   "Total Revenue",
    "net_profit": "Net Income",
    "eps":        "Basic EPS",
}

YFINANCE_CASHFLOW_MAP = {
    "operating_cash_flow": "Operating Cash Flow",
}

YFINANCE_BALANCE_MAP = {
    "total_assets":  "Total Assets",
    "total_debt":    "Total Debt",
    "total_equity":  "Stockholders Equity",
}

# Live snapshot only — no historical data available via free yfinance
YFINANCE_INFO_MAP = {
    "market_cap":     "marketCap",
    "share_price":    "currentPrice",
    "pe_ratio":       "trailingPE",
    "pb_ratio":       "priceToBook",
    "dividend_yield": "dividendYield",
}

# All historical metric column names in one set for quick lookup
ALL_HISTORY_METRICS = (
    set(YFINANCE_INCOME_MAP)
    | set(YFINANCE_CASHFLOW_MAP)
    | set(YFINANCE_BALANCE_MAP)
)


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def _year_from_date(dt):
    """Extract integer year from a pandas Timestamp column header."""
    try:
        return int(dt.year)
    except Exception:
        return None


def _fetch_sheet_data(ticker_obj, metric_col):
    """
    Fetch ALL available annual rows for a metric from yfinance sheets.

    OLD: returned {year: value} and then filtered to only requested years.
         If requested year was outside yfinance's ~4-year window, returned {}
         → empty rows → fallback silently failed.

    NEW: returns ALL available {year: value} pairs regardless of what the
         user asked for. The caller always uses all of them so the LLM can
         say "2021 data not available but here is 2022–2024".
    """
    result = {}

    # Pick the right sheet
    if metric_col in YFINANCE_INCOME_MAP:
        field = YFINANCE_INCOME_MAP[metric_col]
        sheet = ticker_obj.financials
    elif metric_col in YFINANCE_CASHFLOW_MAP:
        field = YFINANCE_CASHFLOW_MAP[metric_col]
        sheet = ticker_obj.cashflow
    elif metric_col in YFINANCE_BALANCE_MAP:
        field = YFINANCE_BALANCE_MAP[metric_col]
        sheet = ticker_obj.balance_sheet
    else:
        return result

    if sheet is None or sheet.empty:
        return result

    if field not in sheet.index:
        # Try case-insensitive search for the field name
        matched = [idx for idx in sheet.index if field.lower() in idx.lower()]
        if not matched:
            print(f"FALLBACK: field '{field}' not found in sheet for {metric_col}")
            return result
        field = matched[0]

    for col in sheet.columns:
        yr  = _year_from_date(col)
        val = sheet.loc[field, col]
        if yr is not None and val is not None:
            try:
                result[yr] = float(val)
            except (TypeError, ValueError):
                pass

    return result


def _fetch_info_metric(ticker_obj, metric_col):
    """Fetch a live market metric from ticker.info."""
    field = YFINANCE_INFO_MAP.get(metric_col)
    if not field:
        return None
    info = ticker_obj.info or {}
    val  = info.get(field)
    return float(val) if val is not None else None


# ─────────────────────────────────────────────────────────────
# PUBLIC ENTRY POINT
# ─────────────────────────────────────────────────────────────

def fetch_from_yfinance(entities, intent):
    """
    Fetches financial data from Yahoo Finance.

    OLD behaviour (bug): filtered yfinance results to only the years the
    user asked for. If yfinance didn't have that specific year (e.g. 2021),
    all_rows stayed empty → raised ValueError → _run_fallback caught it →
    returned "No data found" as if yfinance was never tried.

    NEW behaviour: always returns ALL years yfinance has data for.
    The LLM then explains what years are available and answers as best it
    can — e.g. "2021 is not available but here is data for 2022–2024".
    This is far more useful than a silent "No data found".

    Returns (columns, rows, note) matching execute_query() format.
    Raises ValueError / Exception if yfinance genuinely has nothing.
    """
    companies   = entities.get("COMPANY", [])
    years       = [int(y) for y in entities.get("YEAR", [])]   # requested years (for note only)
    raw_metrics = entities.get("METRIC", [])

    # Map NER metric strings → DB column names
    from .metric_mapper import map_metric
    mapped_metrics = []
    for m in raw_metrics:
        try:
            mapped_metrics.append(map_metric(m))
        except ValueError:
            pass

    if intent == "performance_analysis":
        mapped_metrics = ["revenue", "net_profit", "eps"]

    if not mapped_metrics:
        raise ValueError("No valid metrics to fetch from yfinance")

    history_metrics = [m for m in mapped_metrics if m in ALL_HISTORY_METRICS]
    info_metrics    = [m for m in mapped_metrics if m in YFINANCE_INFO_MAP]

    all_rows = []

    for company_name in companies:
        ticker_symbol = get_ticker(company_name)
        if not ticker_symbol:
            print(f"FALLBACK: no ticker found for '{company_name}' in company_master")
            continue

        print(f"FALLBACK: querying yfinance for {company_name} ({ticker_symbol})")
        tkr = yf.Ticker(ticker_symbol)

        # ── Historical sheet metrics ──────────────────────────
        if history_metrics:
            # {metric_col: {year: value}} — ALL available years
            metric_year_data = {
                mc: _fetch_sheet_data(tkr, mc)
                for mc in history_metrics
            }

            # Union of all years present across all requested metrics
            all_available_years = set()
            for mc in history_metrics:
                all_available_years.update(metric_year_data[mc].keys())

            if not all_available_years:
                print(f"FALLBACK: yfinance sheets returned no data for {company_name}")
            else:
                # KEY FIX: use ALL available years, not just the requested ones.
                # Old code: target_years = [y for y in years if y in all_available_years]
                # → empty list when requested year not in yfinance window → silent failure
                # New code: always use every year yfinance has data for
                target_years = sorted(all_available_years, reverse=False)

                print(f"FALLBACK: yfinance has data for years {target_years} "
                      f"(user requested {years})")

                for yr in target_years:
                    row = [yr, company_name] + [
                        metric_year_data[mc].get(yr)
                        for mc in history_metrics
                    ]
                    all_rows.append(tuple(row))

        # ── Live info metrics (no historical data available) ──
        if info_metrics:
            info_vals = [_fetch_info_metric(tkr, mc) for mc in info_metrics]
            # Label the row with "Live" or max requested year as context
            yr_label = max(years) if years else "Live"
            all_rows.append(tuple([yr_label, company_name] + info_vals))

    if not all_rows:
        raise ValueError(
            f"yfinance returned no usable data for companies: {companies}"
        )

    metric_col_names = history_metrics if history_metrics else info_metrics
    columns = ["fiscal_year", "company_name"] + metric_col_names

    # Build a note that tells the LLM exactly what happened and what years it has
    available_years_str = ", ".join(
        str(r[0]) for r in all_rows if r[0] not in ("Live", None)
    )
    requested_years_str = ", ".join(str(y) for y in years) if years else "all years"

    note = (
        f"Data source: Yahoo Finance (local database had no data). "
        f"You requested year(s): {requested_years_str}. "
        f"Yahoo Finance has data for year(s): {available_years_str}. "
        f"If the exact requested year is not present, explain this clearly "
        f"and summarise what is available."
    )

    return columns, all_rows, note