from dotenv import load_dotenv
import psycopg2

"""Needs to be setup in a way that allows specific table names to be entered??"""

connection = psycopg2.connect(
    database="postgres",
    host="192.168.8.139",
    user="postgres",
    password="postgres",
    port="5433"
)

load_dotenv()

maskable = []


def main(table_name: str):
    cursor = connection.cursor()

    cursor.execute(f"""
        SELECT
            column_name,
            data_type
        FROM
            information_schema.columns
        WHERE
            table_name = '{table_name}';
    """)

    columns = [col[0] for col in cursor.fetchall()]

    maskable.append(columns[3])

    cursor.execute(f"""
        SELECT
            {columns[3]},
            {columns[4]}
        FROM
            {table_name}
    """)

    result = cursor.fetchall()
    print(mask_result(result, columns[3], [columns[4]]))


def mask_result(result, *column):

    columns = list(column)
    mask = [True if col in maskable else False for col in columns]
    return mask


if __name__ == "__main__":
    main("shipments")

mask_result("hey", "two", 1)
