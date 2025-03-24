import pyodbc
from datetime import date
import config
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


# Database connection
def get_database_connection():
    return pyodbc.connect(connection_string)


# Gets the test list from the SQL table
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


# Gets the list of possible status
def get_status_list():
    with get_database_connection() as conn:
        cursor = conn.cursor()
        query = """SELECT Status 
                    FROM Status_LU"""
        cursor.execute(query)
        status_list = []
        for status in cursor.fetchall():
            status_list.append(status[0])
        return status_list


def get_test_id_by_test_name(test_name):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        query = """SELECT Test_LU.Test_ID 
                    FROM Test_LU
                    WHERE Test = ?"""
        cursor.execute(query, test_name)
        test_id = cursor.fetchone()[0]
        return test_id


# Returns current project number from the SQL table
def get_current_project_number():
    with get_database_connection() as conn:
        cursor = conn.cursor()                          # Create cursor
        query = """SELECT TOP 1 Project_ID              
                    FROM Project 
                    ORDER BY Project_ID DESC"""         # SQL query to get list of Project_IDs, descending order by the Project_ID
        cursor.execute(query)                           # Run query
        current_project_number = cursor.fetchone()[0]   # Set current_project_number to the top most value from query results
        return current_project_number                   # Return current_project_number


# Function to get the last sample number to create a new project
def get_current_sample_number():
    with get_database_connection() as conn:
        cursor = conn.cursor()                          # Create cursor
        query = """SELECT TOP 1 Sample_Number              
                    FROM Sample
                    ORDER BY Sample_ID DESC"""         # SQL query to get list of Sample_Numbers, descending order by the Sample_ID
        cursor.execute(query)                          # Run query
        current_sample_number = cursor.fetchone()[0]   # Set current_sample_number to the top most value from query results
        return current_sample_number                   # Return current_sample_number


# Function to get the last sample number to create a new project
def get_current_sample_id():
    with get_database_connection() as conn:
        cursor = conn.cursor()                         # Create cursor
        query = """SELECT TOP 1 Sample_ID              
                    FROM Sample
                    ORDER BY Sample_ID DESC"""         # SQL query to get list of Sample_Numbers, descending order by the Sample_ID
        cursor.execute(query)                          # Run query
        current_sample_number = cursor.fetchone()[0]   # Set current_sample_number to the top most value from query results
        return current_sample_number                   # Return current_sample_number


# Submits the project and samples into the database
def submit_project_creation(project_number, ui_test_dict):
    sql_status = 1      # Set status to open for initial entry
    creation_date = date.today()        # Set creation date to today
    sample_number = get_current_sample_number() + 1     # Gets the most recently used sample number and adds one
    sample_id = get_current_sample_id() + 1     # Gets the most recently used sample ID and adds one
    with get_database_connection() as conn:
        cursor = conn.cursor()                                    # Create cursor
        project_insert_query = "INSERT INTO Project (Project_ID, Status, Date_Created) VALUES(?, ?, ?)"  # SQL query to insert new project info
        cursor.execute(project_insert_query, (project_number, sql_status, creation_date))  # Run project_insert_query with project info
        test_list_all = list(ui_test_dict.values())     # Gets all values from ui_tst_dict and puts them into a list
        sample_id_counter = sample_id
        for sample in test_list_all:        # Goes through each 'sample' which corresponds to a list of tests in test_list_all
            sample = functions.convert_to_sql_test_list(sample)     # Converts the list of tests to SQL codes
            for test in sample:     # Goes through each test within the list
                sample_insert_query = "INSERT INTO Sample (Sample_ID, Project_ID, Sample_Number, Test, Sample_Complete) VALUES(?, ?, ?, ?, 0)"  # SQL query to insert each sample
                cursor.execute(sample_insert_query, sample_id_counter, project_number, sample_number, test)     # Run query
                sample_id_counter += 1      # Increase sample_id_counter (SQL PK)
            sample_number += 1      # Increase sample_number once all tests submitted for the sample

        conn.commit()                                             # Commit insert into SQL


# Pull the projects and their status from database
def get_all_projects_list():
    with get_database_connection() as conn:
        cursor = conn.cursor()
        query = """SELECT project.Project_ID, status.Status 
                    FROM Project AS project 
                    JOIN Status_LU AS status ON project.Status=status.Status_ID 
                    ORDER BY project.Project_ID"""
        cursor.execute(query)
        total_projects_list = cursor.fetchall()     # Puts data into a list
        return total_projects_list


# Pull project information based on filters
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


# Gets project status from database
def get_project_status(project_id):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        query_status = """SELECT project.Project_ID, status.Status 
                        FROM Project AS project 
                        JOIN Status_LU AS status ON project.Status=status.Status_ID 
                        WHERE project.Project_ID=?"""
        cursor.execute(query_status, project_id)
        project_status = cursor.fetchone()[1]
        return project_status


# Gets project details from database
def get_project_details(project_id):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        project_status = get_project_status(project_id)
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
        return project_details


# Gets all tests selected for all samples on a project
def get_test_profile_tests_only(project_id):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        query = """SELECT DISTINCT Test_LU.Test FROM Sample
                    Join Test_LU ON Sample.Test = Test_LU.Test_ID
                    WHERE Sample.Project_ID = ?"""
        cursor.execute(query, project_id)
        results = cursor.fetchall()
        tests = []
        for test in results:
            tests.append(test[0])
        return tests


# Gets all sample numbers for a project
def get_sample_nums_for_project(project_id):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        query = """SELECT DISTINCT Sample.Sample_Number FROM Sample 
                    WHERE Sample.Project_ID = ?"""
        cursor.execute(query, project_id)
        results = cursor.fetchall()
        samples = []
        for sample in results:
            samples.append(sample[0])
        return samples


# Gets samples to enter based on project ID and selected test
def get_samples_to_enter(project_id, test):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        query = """SELECT Sample.Sample_ID, Sample.Sample_Number FROM Sample
                    WHERE Sample.Project_ID = ? AND Sample.Test = ?"""
        cursor.execute(query, project_id, test)
        results = cursor.fetchall()
        results.sort()
        sample_id_list = []
        sample_number_list = []
        for values in results:
            sample_id_list.append(values[0])
            sample_number_list.append(values[1])
        return sample_id_list, sample_number_list


# Checks to see if all samples have a result entered
def check_all_samples_entered(project_id):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        query = """SELECT Sample.Sample_Complete FROM Sample
                WHERE Sample.Project_ID = ?"""
        cursor.execute(query, project_id)
        returned_list = cursor.fetchall()
        completed_list = []
        for check in returned_list:
            completed_list.append(check[0])
        if all(completed_list):
            change_project_status(project_id, "Review")
        else:
            change_project_status(project_id, "In Progress")


# Changes project status
def change_project_status(project_id, change_status_to):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        current_status = get_project_status(project_id)
        if current_status == "Open" and change_status_to == "In Progress":
            query = """UPDATE Project SET Status = 2
                        WHERE Project_ID = ?"""
            cursor.execute(query, project_id)
        elif current_status == "In Progress" and change_status_to == "Review":
            query = """UPDATE Project SET Status = 3
                        WHERE Project_ID = ?"""
            cursor.execute(query, project_id)
        elif current_status == "Review" and change_status_to == "Closed":
            query = """UPDATE Project SET Status = 4
                        WHERE Project_ID = ?"""
            cursor.execute(query, project_id)
        else:
            return


# Submits sample results to database
def submit_results_for_test(results_list, sql_test, project_id):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        if sql_test in config.petrifilm_tests or sql_test in config.chemistry_tests:
            query = """UPDATE Sample SET Result_Num = ?, Sample_Complete = 1
                        WHERE Sample_Number = ? AND Test = ?"""
        elif sql_test in config.pathogen_tests:
            query = """UPDATE Sample SET Result_Non_Num = ?, Sample_Complete = 1
                        WHERE Sample_Number = ? AND Test = ?"""
        else:
            raise ValueError(f"Unknown test type: '{sql_test}'")
        for sample in results_list:
            cursor.execute(query, sample[1], sample[0], sql_test)
    check_all_samples_entered(project_id)


# Returns a list of tests still needed to be entered for a project
def check_entry_complete_for_test(project_id):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        # Get SQL test codes for a project
        test_query = """SELECT DISTINCT Sample.Test FROM Sample
                        WHERE Sample.Project_ID = ?"""
        cursor.execute(test_query, project_id)
        results = cursor.fetchall()
        # Put the codes into a list
        sql_test_ids = []
        final_test_list = []
        for test in results:
            sql_test_ids.append(test[0])
        # For each test in sql_test_list, get sample_complete bool value for each sample with that test
        for test in sql_test_ids:
            check_query = """SELECT Sample.Sample_Complete FROM Sample
                        WHERE Sample.Project_ID = ? and Sample.Test = ?"""
            cursor.execute(check_query, project_id, test)
            returned_list = cursor.fetchall()
            completed_list = []
            for check in returned_list:
                completed_list.append(check[0])
            # If all samples with that test have a result entered, remove test from list
            if not all(completed_list):
                final_test_list.append(test)

        # Convert remaining tests from final_test_list's to string names
        values = ", ".join(["?" for _ in final_test_list])
        test_names_query = f"""SELECT Test_LU.Test FROM Test_LU
                                WHERE Test_ID IN ({values})"""
        cursor.execute(test_names_query, final_test_list)
        results = cursor.fetchall()
        tests_list = []
        for test in results:
            tests_list.append(test[0])
        return tests_list


def get_results_for_project(project_id):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        query = """SELECT Sample.Sample_Number, Sample.Test, Sample.Result_Num, Sample.Result_Non_Num FROM Sample
                    WHERE Sample.Project_ID = ?"""
        cursor.execute(query, project_id)
        results = cursor.fetchall()
        return results


def sample_profile_information(project_id, sample_number):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        query = """SELECT Sample.Sample_Number, Test_LU.Test FROM Sample
                    JOIN Test_LU ON Test_LU.Test_ID = Sample.Test
                    WHERE Sample.Project_ID = ? AND Sample.Sample_Number = ?"""
        cursor.execute(query, project_id, sample_number)
        profile_all = cursor.fetchall()
        tests = []
        for pair in profile_all:
            tests.append(pair[1])
        profile = [sample_number, tests]
        return profile


# Takes new results and updates the database
def submit_edited_results(sample_num, test_id, new_result):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        query = """UPDATE Sample SET Result_Num = ? 
                    WHERE Sample_Number = ? AND Test = ?"""
        cursor.execute(query, (new_result, sample_num, test_id))
        conn.commit()  # Save changes
