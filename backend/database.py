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