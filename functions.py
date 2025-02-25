import database

#Gets the test list from the SQL database
def set_test_list():
    full_test_list = database.get_test_list()
    test_list_options = []
    for key in full_test_list:
        test_list_options.append(key)
    return test_list_options

#Converts string of tests selected to SQL codes
def convert_to_sql_test_list(sample_test_list):
    full_test_list = database.get_test_list()       #Get test list from SQL database
    temp_sql_test_list = []     #Empty list

    #Iterate through list to convert to SQL code
    for test in sample_test_list:
        value = full_test_list[test]
        temp_sql_test_list.append(value)
    temp_sql_test_list.sort()       #Sort the list
    sql_test_list = list(set(temp_sql_test_list))       #Store only unique values
    return sql_test_list

#Stores the selected test for each sample
def store_selected_tests(test_results, sample_id, selected_tests):
    test_results[sample_id] = selected_tests
