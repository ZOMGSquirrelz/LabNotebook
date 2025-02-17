from datetime import date
import pyodbc

#Information needed to connect to SQL database
connection_string = """DRIVER={ODBC Driver 18 for SQL Server};
                    SERVER=127.0.0.1,1433;
                    DATABASE=LabNotebook;
                    UID=econard;
                    PWD=Freeze*6;
                    TrustServerCertificate=yes"""

#Connect to SQL database
conn = pyodbc.connect(connection_string)

#Function to create a simple menu for testing
def display_main_menu():
    print("""Create new project?
    1 - Yes
    2 - No
    3 - Test
    4 - Exit""")

#Function to get number of samples for testing
def get_sample_total():
    while True:
        try:
            number_of_samples = int(input("Enter the number of samples: "))
            break
        except:
            print("Value must be an integer")
    return number_of_samples

#Function to get list of possible tests
def display_test_list():
    cursor = conn.cursor()                          #Create cursor
    query = """SELECT Count(*) FROM Test_LU"""      #SQL query to get count of test list
    cursor.execute(query)                           #Run query
    list_length = int(cursor.fetchone()[0])         #Set result to list_length
    test_query = "SELECT Test FROM Test_LU"         #SQL query to get list of tests
    cursor.execute(test_query)                      #Run test_query
    test_list = cursor.fetchall()                   #Set result to test_list
    current_list_spot = 0                           #Int for list iteration
    while current_list_spot != list_length:         #Display list as 'Spot - Test'
        print(f'{current_list_spot + 1} - {test_list[current_list_spot][0]}')
        current_list_spot += 1                      #Increase current_list_spot by 1
    return test_list                                #Return the test_list

#Function to get the last project number to create a new project
def get_current_project_number():
    cursor = conn.cursor()                          #Create cursor
    query = """SELECT TOP 1 Project_ID              
                FROM Project 
                ORDER BY Project_ID DESC"""         #SQL query to get list of Project_IDs, descending order by the Project_ID
    cursor.execute(query)                           #Run query
    current_project_number = cursor.fetchone()[0]   #Set current_project_number to the top most value from query results
    return current_project_number                   #Return current_project_number

#Function to get the last sample number to create a new project
def get_current_sample_number():
    cursor = conn.cursor()                          #Create cursor
    query = """SELECT TOP 1 Sample_Number              
                FROM Sample
                ORDER BY Sample_ID DESC"""         #SQL query to get list of Sample_Numbers, descending order by the Sample_ID
    cursor.execute(query)                           #Run query
    current_sample_number = cursor.fetchone()[0]   #Set current_sample_number to the top most value from query results
    return current_sample_number                   #Return current_sample_number

# with pyodbc.connect(connection_string) as conn:
#     choice = ""
#     display_main_menu()
#     while choice != 0:
#         choice = input("Choice: ")
#         if choice == '1':
#             project_number = get_current_project_number() + 1         #Set project number to 1 more than current_project_number
#             creation_date = date.today()                              #Set creation_date to today's date
#             status = "Open"                                           #Set status to 'Open' for display purposes only
#             sql_status = 1                                            #Set sql_status to 1 to represent 'Open' in database
#
#             print(f'Project Number: {project_number}')                #Display project info
#             print(f'Date created: {creation_date}')
#             print(f'Status: {status}')
#
#             insert_query = "INSERT INTO Project (Project_ID, Status, Date_Created) VALUES(?, ?, ?)"   #SQL query to insert new project info
#             cursor = conn.cursor()                                    #Create cursor
#             cursor.execute(insert_query,(project_number, sql_status, creation_date))  #Run insert_query with project info
#             conn.commit()                                             #Commit insert into SQL
#             conn.close()                                              #Close connection
#             # sample_count = get_sample_total()
#             # print(f'Total number of samples on project: {sample_count}')
#             # print("Project Created")
#             break
#         elif choice == '2':
#             print("Cancel project creation")
#             break
#         elif choice == '3':
#             number_of_samples = get_sample_total()
#             sample_list = []
#             sample_and_test_list = []
#             current_sample_number = get_current_sample_number()
#             sample_counter = 0
#             while sample_counter != number_of_samples:
#                 sample_list.append(current_sample_number + 1)
#                 current_sample_number += 1
#                 sample_counter += 1
#             for sample in sample_list:
#                 sample_test_list = []
#                 selection = -1
#                 while selection != 0:
#                     display_test_list()               #Call display_test_list function
#                     print('''Enter the number associated with the test you want to add.
# To complete test addition, enter 0''')
#                     while True:
#                         try:
#                             selection = int(input(f'Choose a test to be added for sample {sample}: '))
#                             break
#                         except:
#                             print("Value must be an integer")
#                     if selection in sample_test_list:
#                         print('Invalid entry - Test already selected for this sample')
#                     else:
#                         sample_test_list.append(selection)
#                 sample_and_test_list.append([sample, sample_test_list])
#
#         elif choice == '4':                   #Exit program
#             break
#         else:                                 #If entry is anything but a selectable menu item, try again
#             print("Invalid Entry")
