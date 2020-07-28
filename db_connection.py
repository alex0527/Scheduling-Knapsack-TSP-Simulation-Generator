import mysql.connector as db
from mysql.connector import errorcode
import db_tables
import pandas as pd

HOST = "xxx"
USER = "xxx"
PASSWORD = "xxx"
PORT = 3306
DB_NAME = 'xxx'

TABLES_CREATE = db_tables.create()

def connect_database(HOST, PORT, USER, PASSWORD, DB_NAME):
    cnx = db.connect(host=HOST, port=PORT, user=USER, passwd=PASSWORD, database=DB_NAME)
    cursor = cnx.cursor()
    return cnx, cursor

def drop_database():
    cnx = db.connect(host=HOST, port=PORT,user=USER, passwd=PASSWORD)
    cursor = cnx.cursor()
    cursor.execute('SHOW DATABASES')
    db_list = cursor.fetchall()
    for i in range(len(db_list)):
        if DB_NAME in db_list[i]:
            print("Database {} exists.".format(DB_NAME))
            cursor.execute("DROP DATABASE {}".format(DB_NAME))
            cnx.commit()
            print("Database {} is dropped.".format(DB_NAME))
    cursor.close()
    cnx.close()

def create_database():
    cnx = db.connect(host=HOST, port=PORT,user=USER, passwd=PASSWORD)
    cursor = cnx.cursor()
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except db.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            try:
                cursor.execute(
                    "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
                cnx.commit()
            except db.Error as err:
                print("Failed creating database: {}".format(err))
                exit(1)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)
    cursor.close()
    cnx.close()

def create_tables(TABLES_CREATE):
    cnx, cursor = connect_database(HOST, PORT, USER, PASSWORD, DB_NAME)
    for table_name in TABLES_CREATE:
        table_description = TABLES_CREATE[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
            cnx.commit()
        except db.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("Successfully!")
    cursor.close()
    cnx.close()

def csv_insert_tables(df, sql_part):
    cnx, cursor = connect_database(HOST, PORT, USER, PASSWORD, DB_NAME)
    count = 0
    for index, row in df.iterrows():
        row_val = row.values
        comms = '{}'.format("")
        for key in range(len(row_val)):
            if row_val[key] == True:
                comms += str(row_val[key]) + ","
            else:
                row_val[key] = str(row_val[key]).replace('\'','')
                row_val[key] = str(row_val[key]).replace('\\','\\\\')
                if key != len(row_val)-1:
                    comms += "'" + str(row_val[key]) + "',"
                if key == len(row_val)-1:
                    comms += "'" + str(row_val[key]) + "'"
        sql= sql_part + """
        values
        ({})""".format(comms)
        try:
            cursor.execute(sql)
            cnx.commit()
        except db.Error as err:
            print('failed -- {} -- {}'.format(index, sql))
            # print(err.msg)
    cursor.close()
    cnx.close()

if __name__ == '__main__':
    drop_database()
    create_database()
    create_tables(TABLES_CREATE)

    sql = {
        'users': '(`user_id`, `password`, `first_name`, `last_name`, `email_address`, `phone_number`, `address`)',
        'tracking': '(`tracking_id`, `status`, `created_at`, `estimated_delivered_at`, `delay`, `previous_destination`, `previous_destination_start_time`)',
        'station': '(`station_id`, `drone_num`, `robot_num`, `address`, `lon`, `lat`)',
        'machine': '(`machine_id`, `station_id`, `machine_type`, `available`, `height_limit`, `weight_limit`, `unit_price_per_mile_per_kg`)',
        'contact': '(`contact_id`, `first_name`, `last_name`, `phone_number`, `email_address`, `address`)',
        'orders': '(`order_id`, `user_id`, `tracking_id`, `station_id`, `machine_id`, `active`, `sender_id`, `recipient_id`, `package_weight`, `package_height`, `package_fragile`, `package_length`, `package_width`, `carrier`, `total_cost`, `appointment_time`)'
    }
    for sheetname in pd.ExcelFile('dispatch_db.xlsx').sheet_names:
        df = pd.read_excel('dispatch_db.xlsx', sheet_name = sheetname)
        sql_part = 'Insert into {} {}'.format(sheetname, sql[sheetname])
        csv_insert_tables(df, sql_part)


