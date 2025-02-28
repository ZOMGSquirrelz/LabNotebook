import pyodbc
from datetime import date
import functions
from dotenv import load_dotenv
import os

load_dotenv()

UID = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

# Database connection string
connection_string = f"""DRIVER={{ODBC Driver 18 for SQL Server}};
                    SERVER=127.0.0.1,1433;
                    DATABASE=LabNotebook;
                    UID={UID};
                    PWD={password};
                    TrustServerCertificate=yes"""

#Database connection
def get_database_connection():
    return pyodbc.connect(connection_string)

#Gets the test list from the SQL table
def get_test_list():
    with get_database_connection() as conn:
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

#Gets the list of possible status
def get_status_list():
    with get_database_connection() as conn:
        cursor = conn.cursor()
        query = """SELECT Status FROM Status_LU"""
        cursor.execute(query)
        status_list = []
        for status in cursor.fetchall():
            status_list.append(status[0])
        return status_list

#Returns current project number from the SQL table
def get_current_project_number():
    with get_database_connection() as conn:
        cursor = conn.cursor()                          #Create cursor
        query = """SELECT TOP 1 Project_ID              
                    FROM Project 
                    ORDER BY Project_ID DESC"""         #SQL query to get list of Project_IDs, descending order by the Project_ID
        cursor.execute(query)                           #Run query
        current_project_number = cursor.fetchone()[0]   #Set current_project_number to the top most value from query results
        return current_project_number                   #Return current_project_number

#Function to get the last sample number to create a new project
def get_current_sample_number():
    with get_database_connection() as conn:
        cursor = conn.cursor()                          #Create cursor
        query = """SELECT TOP 1 Sample_Number              
                    FROM Sample
                    ORDER BY Sample_ID DESC"""         #SQL query to get list of Sample_Numbers, descending order by the Sample_ID
        cursor.execute(query)                           #Run query
        current_sample_number = cursor.fetchone()[0]   #Set current_sample_number to the top most value from query results
        return current_sample_number                   #Return current_sample_number

#Function to get the last sample number to create a new project
def get_current_sample_id():
    with get_database_connection() as conn:
        cursor = conn.cursor()                          #Create cursor
        query = """SELECT TOP 1 Sample_ID              
                    FROM Sample
                    ORDER BY Sample_ID DESC"""         #SQL query to get list of Sample_Numbers, descending order by the Sample_ID
        cursor.execute(query)                           #Run query
        current_sample_number = cursor.fetchone()[0]   #Set current_sample_number to the top most value from query results
        return current_sample_number                   #Return current_sample_number


#Submits the project and samples into the database
def submit_project_creation(project_number, ui_test_dict):
    sql_status = 1      #Set status to open for initial entry
    creation_date = date.today()        #Set creation date to today
    sample_number = get_current_sample_number() + 1     #Gets the most recently used sample number and adds one
    sample_id = get_current_sample_id() + 1     #Gets the most recently used sample ID and adds one
    with get_database_connection() as conn:
        cursor = conn.cursor()                                    #Create cursor
        project_insert_query = "INSERT INTO Project (Project_ID, Status, Date_Created) VALUES(?, ?, ?)"  #SQL query to insert new project info
        cursor.execute(project_insert_query,(project_number, sql_status, creation_date))  #Run project_insert_query with project info
        test_list_all = list(ui_test_dict.values())     #Gets all values from ui_tst_dict and puts them into a list
        sample_id_counter = sample_id
        for sample in test_list_all:        #Goes through each 'sample' which corresponds to a list of tests in test_list_all
            sample = functions.convert_to_sql_test_list(sample)     #Converts the list of tests to SQL codes
            for test in sample:     #Goes through each test within the list
                sample_insert_query = "INSERT INTO Sample (Sample_ID, Project_ID, Sample_Number, Test) VALUES(?, ?, ?, ?)"  #SQL query to insert each sample
                cursor.execute(sample_insert_query, sample_id_counter, project_number, sample_number, test)     #Run query
                sample_id_counter += 1      #Increase sample_id_counter (SQL PK)
            sample_number += 1      #Increase sample_number once all tests submitted for the sample

        #conn.commit()                                             #Commit insert into SQL

#Pull the projects and their status from database
def get_all_projects_list():
    with get_database_connection() as conn:
        cursor = conn.cursor()
        query = """SELECT project.Project_ID, status.Status 
                    FROM Project AS project 
                    JOIN Status_LU AS status ON project.Status=status.Status_ID 
                    ORDER BY project.Project_ID"""
        cursor.execute(query)
        total_projects_list = cursor.fetchall()     #Puts data into a list
        for p in total_projects_list:
            print(f'Project: {p[0]} | Status: {p[1]}')          #Debugging
        return total_projects_list

#Pull project information based on filters
def get_filtered_projects_list(status_list):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        filters = ', '.join(['?' for x in status_list])
        query = f"""SELECT project.Project_ID, status.Status 
                    FROM Project AS project 
                    JOIN Status_LU AS status ON project.Status=status.Status_ID 
                    WHERE status.Status IN ({filters})
                    ORDER BY project.Project_ID"""
        cursor.execute(query, tuple(status_list))
        filtered_projects_list = cursor.fetchall()
        print(filtered_projects_list)
        return filtered_projects_list

#Gets project details from database
def get_project_details(project_id):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        query_status = """SELECT project.Project_ID, status.Status 
                        FROM Project AS project 
                        JOIN Status_LU AS status ON project.Status=status.Status_ID 
                        WHERE project.Project_ID=?"""
        cursor.execute(query_status, project_id)
        project_status = cursor.fetchone()[1]
        query_details = """SELECT project.Project_ID, project.Date_Created, count(DISTINCT sample.Sample_Number) as 'Sample Count'
                        FROM Project as project
                        JOIN  Sample as sample ON project.Project_ID=sample.Project_ID
                        WHERE project.Project_ID = ?
                        GROUP BY project.Project_ID, project.Date_Created"""
        cursor.execute(query_details, project_id)
        details = cursor.fetchone()
        project_creation_date = details[1].strftime("%Y-%m-%d")
        project_sample_count = details[2]
        project_details = [project_id, project_status, project_creation_date, project_sample_count]
        print(f'Project: {project_id}, status: {project_status}, date: {project_creation_date}, samples: {project_sample_count}')       #Debugging
        return project_details
