from sqlite3 import connect, Row

database: str = "db/school.db"


def getprocess(sql: str, vals: list) -> list:
    conn = connect(database)
    conn.row_factory = Row
    cursor = conn.cursor()
    cursor.execute(sql, vals)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def postprocess(sql: str, vals: list) -> bool:
    try:
        conn = connect(database)
        cursor = conn.cursor()
        cursor.execute(sql, vals)
        conn.commit()
        result = cursor.rowcount > 0
    except Exception as e:
        print(f"Error: {e}")
        result = False
    finally:
        cursor.close()
        conn.close()
    return result


def getall(table: str) -> list:
    sql = f"SELECT * FROM {table}"
    return getprocess(sql, [])


def getrecord(table: str, **kwargs) -> list:
    keys = list(kwargs.keys())
    vals = list(kwargs.values())
    fields = " AND ".join([f"{k} = ?" for k in keys])
    sql = f"SELECT * FROM {table} WHERE {fields}"
    return getprocess(sql, vals)


def addrecord(table: str, **kwargs) -> bool:
    keys = list(kwargs.keys())
    vals = list(kwargs.values())
    placeholders = ",".join(["?"] * len(keys))
    fields = ",".join(keys)
    sql = f"INSERT INTO {table} ({fields}) VALUES ({placeholders})"
    return postprocess(sql, vals)


def deleterecord(table: str, **kwargs) -> bool:
    keys = list(kwargs.keys())
    vals = list(kwargs.values())
    fields = " AND ".join([f"{k} = ?" for k in keys])
    sql = f"DELETE FROM {table} WHERE {fields}"
    return postprocess(sql, vals)


def updaterecord(table: str, **kwargs) -> bool:
    keys = list(kwargs.keys())
    vals = list(kwargs.values())

    if not keys:
        return False

    set_fields = ",".join([f"{k} = ?" for k in keys[1:]])
    sql = f"UPDATE {table} SET {set_fields} WHERE {keys[0]} = ?"

    reordered = vals[1:] + [vals[0]]
    return postprocess(sql, reordered)
