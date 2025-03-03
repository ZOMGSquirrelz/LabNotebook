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

#Converts string of a selected test to the SQL code
def convert_to_sql_single_test(test):
    full_test_list = database.get_test_list()
    sql_value = full_test_list[test]
    return sql_value

#Takes a list of values and makes them into an integer
def make_list_into_int(value_list):
    new_number = 0
    while len(value_list) != 0:
        new_number += int(value_list[0])
        value_list.pop(0)
        if len(value_list) == 0:
            break
        else:
            new_number *= 10
    return new_number

#Takes a count and creates a list of values
#If count is over 100, makes any value past the third digit 0
#Example: 12545 becomes [1, 2, 3, 0, 0]
def dilute_count(count):
    count_list = []
    for number in count:
        if len(count_list) > 2:
            count_list.append("0")
        else:
            count_list.append(int(number))
    return count_list

#Takes the result and performs rounding rules to the value
def result_rounding(result):
    if int(result) < 100:
        rounded_result = result
        return rounded_result
    else:
        result_list = dilute_count(result)
        if result_list[2] < 5 or (result_list[2] == 5 and result_list[1] % 2 == 0):
            result_list[2] = 0
        elif result_list[2] > 5 or (result_list[2] == 5 and result_list[1] % 2 != 0):
            result_list[1] = result_list[1] + 1
            result_list[2] = 0
        rounded_result = make_list_into_int(result_list)

        return rounded_result

#Calculation for when multiple dilution counts are within the countable range of the plate type
def multiple_in_range_calc(result_stats):
    diluted_values = []
    for dil, result in result_stats:
        result *= (10 ** dil)
        diluted_values.append(result)
    dil_values_length = len(diluted_values)
    total = 0
    for values in diluted_values:
        total += values
    averaged_result = total/dil_values_length
    return averaged_result


#Stores the selected test for each sample
def store_selected_tests(test_results, sample_id, selected_tests):
    test_results[sample_id] = selected_tests
