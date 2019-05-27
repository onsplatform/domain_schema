from django.db import connection


def table_exists(table_schema, table_name):
    """
    check if a table exists in the database
    """
    with connection.cursor() as cursor:
        query = f"""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = '{table_schema}' AND table_name = '{table_name}'
        """
        cursor.execute(query)
        ret = cursor.fetchone()
        return ret[0] > 0


def table_columns(table_schema, table_name) :
    """
    lists all table columns
    """
    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT *
            FROM "information_schema"."columns"
            WHERE table_schema='{table_schema}' AND table_name = '{table_name}'
        """)

        columns = [col[0] for col in cursor.description]
        table_name_index = columns.index('column_name')
        return {row[table_name_index]: dict(zip(columns, row)) for row in cursor.fetchall()}
