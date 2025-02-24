import pyodbc

# Database connection string
connection_string = """DRIVER={ODBC Driver 18 for SQL Server};
                    SERVER=127.0.0.1,1433;
                    DATABASE=LabNotebook;
                    UID=econard;
                    PWD=***********;        
                    TrustServerCertificate=yes"""    #Enter password

def get_db_connection():
    """Returns a database connection."""
    return pyodbc.connect(connection_string)

def get_test_list():
    """Fetches test list from SQL database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()  # Create cursor
        query = """SELECT Count(*) FROM Test_LU"""  # SQL query to get count of test list
        cursor.execute(query)  # Run query
        list_length = int(cursor.fetchone()[0])  # Set result to list_length
        test_query = "SELECT Test FROM Test_LU"  # SQL query to get list of tests
        cursor.execute(test_query)  # Run test_query
        sql_test_list = cursor.fetchall()  # Set result to sql_test_list
        test_list = {}
        current_list_spot = 0  # Int for list iteration
        while current_list_spot != list_length:  # Display list as 'Spot - Test'
            key = sql_test_list[current_list_spot][0]
            test_list[key] = current_list_spot + 1
            current_list_spot += 1  # Increase current_list_spot by 1
        return test_list

def get_current_project_number():
    with get_db_connection() as conn:
        cursor = conn.cursor()                          #Create cursor
        query = """SELECT TOP 1 Project_ID              
                    FROM Project 
                    ORDER BY Project_ID DESC"""         #SQL query to get list of Project_IDs, descending order by the Project_ID
        cursor.execute(query)                           #Run query
        current_project_number = cursor.fetchone()[0]   #Set current_project_number to the top most value from query results
        return current_project_number                   #Return current_project_number

#Function to get the last sample number to create a new project
def get_current_sample_number():
    with get_db_connection() as conn:
        cursor = conn.cursor()                          #Create cursor
        query = """SELECT TOP 1 Sample_Number              
                    FROM Sample
                    ORDER BY Sample_ID DESC"""         #SQL query to get list of Sample_Numbers, descending order by the Sample_ID
        cursor.execute(query)                           #Run query
        current_sample_number = cursor.fetchone()[0]   #Set current_sample_number to the top most value from query results
        return current_sample_number                   #Return current_sample_number


def submit_project_creation(project_number, sql_status, creation_date, sample_id, sample_number, test):
    with get_db_connection() as conn:
        cursor = conn.cursor()                                    #Create cursor
        project_insert_query = "INSERT INTO Project (Project_ID, Status, Date_Created) VALUES(?, ?, ?)"  # SQL query to insert new project info
        cursor.execute(project_insert_query,(project_number, sql_status, creation_date))  #Run project_insert_query with project info
        # sample_insert_query = "INSERT INTO Sample (Sample_ID, Project_ID, Sample_Number, Test) VALUES(?, ?, ?, ?)"
        # cursor.execute(sample_insert_query, )

        #conn.commit()                                             #Commit insert into SQL

