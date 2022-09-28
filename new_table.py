import os
import json
import sys
import psycopg2

if len(sys.argv) < 2:
    print('no argument')
    sys.exit()

table_name = sys.argv[1]  # ex 勞保局服務事項

# Read JSON #
with open('{}.json'.format(table_name), encoding='utf-8') as json_data:
    record_list = json.load(json_data)

if type(record_list) == list:
    first_record = record_list[0]

    columns = list(first_record.keys())
    # print("\ncolmn names:", columns)
else:
    print("Needs to be an array of JSON objects")
    sys.exit()

#'''CREATE TABLE <JSON NAME> (<PROPERTY 1> VARCHAR(500),<PROPERTY 2> VARCHAR(500)...);'''
sql_string = "CREATE TABLE {} (".format(table_name)
for i in range(0, len(columns)):
    sql_string += (columns[i] + ' VARCHAR(500)')
    if i != len(columns) - 1:
        sql_string += ','

sql_string += ');'
sql_string += '\nINSERT INTO {}'.format(table_name)
sql_string += "(" + ','.join(columns) + ")\nVALUES"

for i, record_dict in enumerate(record_list):

    values = []
    for col_names, val in record_dict.items():

        if type(val) == str:
            val = val.replace("'", "''")
            val = "'" + val + "'"

        values += [str(val)]

    sql_string += "(" + ','.join(values) + "),\n"

sql_string = sql_string[:-2] + ";"

# Connect Heroku database #
try:
    DATABASE_URL = os.popen(
        'heroku config:get DATABASE_URL -a laoli113138').read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    print("\ncreated cusor object", cursor)

except(Exception, psycopg2.Error) as err:
    print("\npsycopg2 connect error", err)
    conn = None
    cursor = None

# Access Database #
if cursor != None:

    try:
        cursor.execute(sql_string)
        conn.commit()
        print('\nfinished INSERT INTO execution')
    except(Exception, psycopg2.Error) as error:
        print("\nexecute_sql() error", error)
        conn.rollback()

    cursor.close()
    conn.close()
