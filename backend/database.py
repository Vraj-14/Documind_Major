# import psycopg2


# def get_connection():

#     conn = psycopg2.connect(
#         host="localhost",
#         database="Documind",
#         user="postgres",
#         password="vraj1410",
#         port=5432
#     )

#     return conn


# def execute_query(query):

#     conn = get_connection()

#     cursor = conn.cursor()

#     cursor.execute(query)

#     rows = cursor.fetchall()

#     columns = [desc[0] for desc in cursor.description]

#     cursor.close()
#     conn.close()

#     return columns, rows










# 2-4-26



import psycopg2


def get_connection():

    conn = psycopg2.connect(
        host="localhost",
        database="Documind",
        user="postgres",
        password="vraj1410",
        port=5432
    )

    return conn


def execute_query(query):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()

    return columns, rows


# ─────────────────────────────────────────────────────────────
# NEW: ticker resolver for yfinance fallback
#
# OLD: no ticker resolution existed — the fallback had no way to
#      call yfinance without knowing the ticker symbol.
#
# NEW: looks up ticker_symbol from company_master using the exact
#      company name string. Returns None if not found so the
#      fallback can skip that company gracefully.
# ─────────────────────────────────────────────────────────────

def get_ticker(company_name):
    """
    Returns the ticker_symbol string for a given company_name,
    or None if the company is not found in company_master.

    Example:
        get_ticker('Infosys Limited') → 'INFY.NS'
    """
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT ticker_symbol FROM company_master WHERE company_name = %s LIMIT 1",
            (company_name,)
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row[0] if row else None
    except Exception as e:
        print(f"get_ticker error for '{company_name}': {e}")
        return None