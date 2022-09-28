import os
import psycopg2
from psycopg2 import sql

def Access_heroku():
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

def data_get(table_name):
    conn = Access_heroku()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT * From {};'.format(table_name))

    # 擷取的資料存於data中
    # data中的資料型態為tuple
    data = []
    while True:
        temp = cursor.fetchone()
        if temp:
            data.append(temp)
        else:
            break

    cursor.close()
    conn.close()

    return data

# tablename為string
# data為tuple，tuple內的資料型態為string
def data_insert(tablename, data):
    try:
        conn = Access_heroku()
        cursor = conn.cursor()

        col_name = get_Column(tablename, cursor)

        sql_command = f'INSERT INTO {tablename} ('
        for i in col_name:
            sql_command += (i + ',')
        sql_command = sql_command[:-1] + ') VALUES ('

        for i in range(0, len(col_name)):
            sql_command += '%s,'
        sql_command = sql_command[:-1] + ')'

        cursor.executemany(sql_command, data)
        conn.commit()
    except(Exception, psycopg2.Error) as error:
        print("\nexecute_sql() error", error)
        conn.rollback()
    cursor.close()
    conn.close()

#tablename, col, value為string
def data_del(tablename, col, value):
    conn = Access_heroku()
    cursor = conn.cursor()

    sql_command = f"DELETE FROM {tablename} WHERE {col} = '{value}';"
    cursor.execute(sql_command)
    conn.commit()

    cursor.close()
    conn.close()
    
def get_Column(tablename, cursor):
    col = []
    sql_string = f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{tablename}';"
    sql_object = sql.SQL(sql_string).format(sql.Identifier(tablename))
    cursor.execute(sql_object)
    tmp = cursor.fetchall()
    for tup in tmp:
        col.append(tup[0])
    return col