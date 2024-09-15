import sqlite3
from typing import Dict, List, Tuple


def insert(database: str, table: str, column_values: Dict):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        columns = ", ".join(column_values.keys())
        values = [tuple(column_values.values())]
        placeholders = ", ".join("?" * len(column_values.keys()))
        query = f"INSERT INTO {table} "\
                f"({columns}) "\
                f"VALUES ({placeholders})"
        cursor.executemany(query, values)
        conn.commit()


def insert_many(database: str, table: str, column_values: List):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        columns = ", ".join(column_values[0].keys())
        placeholders = ", ".join(':' + key for key in column_values[0].keys())
        query = f"INSERT INTO {table} "\
                f"({columns}) "\
                f"VALUES ({placeholders})"
        cursor.executemany(query, column_values)
        conn.commit()


def update(database: str, table: str, column_values: Dict, where=None):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        placeholders = []
        for key in column_values:
            placeholders.append(f"{key} = :{key}")
        values = ", ".join(placeholders)
        if where:
            query = f"UPDATE {table} SET {values} WHERE {where}"
        else:
            query = f"UPDATE {table} SET {values}"
        cursor.execute(query, column_values)
        conn.commit()


def fetchall(database: str, table: str, columns: List[str], where=None) -> List:
    result = []
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        columns_joined = ", ".join(columns)
        if where:
            query = f"SELECT {columns_joined} FROM {table} WHERE {where}"
        else:
            query = f"SELECT {columns_joined} FROM {table}"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            dict_row = {}
            for index, column in enumerate(columns):
                dict_row[column] = row[index]
            result.append(dict_row)

    return result


def main():
    pass


if __name__ == '__main__':
    main()
