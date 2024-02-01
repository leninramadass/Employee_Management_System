import mysql.connector

def connect_to_mysql():
    try:
        # Connection to MySQL database
        connection = mysql.connector.connect(host="localhost",
                                             user="root",
                                             password="password",
                                             database="Employee_db")
        # Check if the connection is successful
        if connection.is_connected():
            print("MySQL Connected")
        # Create a cursor to execute SQL queries
        cursor = connection.cursor()
        # Call a create_table
        create_table(connection, cursor)

        return connection, cursor

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL:{e}")

def create_table(connection, cursor):
    # SQL query to create the table if it doesn't exist
    create_table_query = """CREATE TABLE IF NOT EXISTS EMPLOYEE_MANAGEMENT_SYSTEM(
                            EMP_ID TEXT,
                            FULL_NAME TEXT,
                            GENDER TEXT,
                            EMAIL_ID TEXT,
                            CONTACT_NUMBER TEXT,
                            DOJ TEXT,
                            DEPARTMENT TEXT,
                            ADDRESS TEXT)"""
    cursor.execute(create_table_query)
    connection.commit()

def insert_data(connection, cursor, data_to_insert):
    # SQL query to insert data into the table
    insert_data_query = """INSERT INTO EMPLOYEE_MANAGEMENT_SYSTEM
                           (EMP_ID,FULL_NAME,GENDER,EMAIL_ID,CONTACT_NUMBER,DOJ,DEPARTMENT,ADDRESS)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""
    cursor.execute(insert_data_query, data_to_insert)
    connection.commit()

def fetch_data(cursor):
    # SQL query to fetch all data from the table
    fetch_data_query = """SELECT * FROM EMPLOYEE_MANAGEMENT_SYSTEM"""
    cursor.execute(fetch_data_query)
    datas = cursor.fetchall()
    return datas

def update_data(connection, cursor, data_to_insert, EMP_ID):
    # SQL query to update data in the table based on EMP_ID
    update_data_query = """UPDATE EMPLOYEE_MANAGEMENT_SYSTEM 
                        SET EMP_ID=%s,
                        FULL_NAME=%s,
                        GENDER=%s,
                        EMAIL_ID=%s,
                        CONTACT_NUMBER=%s,
                        DOJ=%s,DEPARTMENT=%s,
                        ADDRESS=%s 
                        WHERE EMP_ID=%s """
    cursor.execute(update_data_query, data_to_insert + (EMP_ID,))
    connection.commit()

def remove_data(connection, cursor, EMP_ID):
    # SQL query to remove data from the table based on EMP_ID
    remove_data_query = """DELETE FROM EMPLOYEE_MANAGEMENT_SYSTEM WHERE EMP_ID=%s"""
    cursor.execute(remove_data_query, (EMP_ID,))
    connection.commit()

def close_connection(connection, cursor):
    # Close the cursor and the database connection
    if connection.is_connected():
        cursor.close()
        connection.close()
