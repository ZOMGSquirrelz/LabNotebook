import database
import config

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

#Convert a SQL test id to the test name
def convert_to_test_name_from_sql_code(sql_test_id):
    test_dict = database.get_test_list()
    for test_name, test_id in test_dict.items():
        if test_id == sql_test_id:
            return test_name

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
#Example: 12545 becomes [1, 2, 5, 0, 0]
def remove_excess_from_count(count):
    count_list = []
    for number in count:
        if len(count_list) > 2:
            count_list.append(0)
        else:
            count_list.append(int(number))
    return count_list

#Takes the result and performs rounding rules to the value
def result_rounding(result):
    if int(result) < 100:           #If result is less than 100, no rounding is needed
        rounded_result = result
        return rounded_result
    else:
        result_list = remove_excess_from_count(result)          #Creates a list of numbers with zeroes after the third digit
        if result_list[2] < 5 or (result_list[2] == 5 and result_list[1] % 2 == 0):
            result_list[2] = 0
        elif result_list[2] > 5 or (result_list[2] == 5 and result_list[1] % 2 != 0):
            result_list[1] = result_list[1] + 1
            result_list[2] = 0
        rounded_result = make_list_into_int(result_list)

        return rounded_result

def single_count_calculation(dil_count_list):
    dilution = dil_count_list[0]
    count = dil_count_list[1]
    diluted_result = count * (10 ** dilution)
    return diluted_result

#Calculation for when multiple dilution counts are within the countable range of the plate type
def multiple_in_range_calc(result_stats):
    diluted_values = []
    for dil, result in result_stats:
        result *= (10 ** dil)           #Dilutes the result based on the dilution entered
        diluted_values.append(result)       #Addes result to the diluted_values list
    dil_values_length = len(diluted_values)
    total = 0
    for values in diluted_values:
        total += values
    averaged_result = total/dil_values_length       #Averages the diluted values
    return averaged_result

#Compares the results to the specifc countable range for the test and outputs the final result
def compare_to_countable_range(test_name, values_list):
    under_range_list = []
    in_range_list = []
    over_range_list = []

    if test_name in config.countable_ranges:
        lower_limit, upper_limit = config.countable_ranges[test_name]       #Sets lower and upper limits based on test and config table
        for dil, entry in values_list:                  #For each set in values_list...
            if lower_limit <= entry <= upper_limit:     #If entry is within the range,add to in_range_list
                in_range_list.append([dil, entry])
            elif entry < lower_limit:                   #If entry is less than lower limit, add to under_range_list
                under_range_list.append([dil, entry])
            elif upper_limit < entry:                   #If entry is more than upper limit, add to over_range_list
                over_range_list.append([dil, entry])
        if len(in_range_list) != 0:         #If there are any in the in_range_list, conduct calculations on them
            result = multiple_in_range_calc(in_range_list)
        elif len(under_range_list) != 0 and len(over_range_list) == 0:      #If there are any in the under_range_list, but not over_range_list,
            result = single_count_calculation(under_range_list[0])          #Do calculations on the least diluted entry
        elif len(over_range_list) != 0 and len(under_range_list) == 0:                      #If there are any in the over_range_list, but none in under_range_list,
            result = single_count_calculation(over_range_list[len(over_range_list)-1])      #Do calculations on the one closer to the upper limit (likely the most diluted)
        elif len(under_range_list) != 0 and len(over_range_list) != 0:      #If there are any in both under_range_list and over_range_list,
            result = single_count_calculation(over_range_list[0])           #Do calculations on the least dilute in the over_range_list
    else:
        result = values_list[0][1]
    final_result = result_rounding(str(int(result)))        #Conduct rounding rules on the result from calculations
    return final_result

#Perfomr rounding rules to chemistry result entries
def chemistry_rounding(value):
    value = round(float(value), 2)      #Round to 2 decimal places

    #Extract the decimal values
    first_decimal = int(value * 10) % 10
    second_decimal = int(value * 100) % 10

    #Rounding rules
    if second_decimal < 5 or (second_decimal == 5 and first_decimal % 2 == 0):
        result = round(value, 1)
    else:
        result = round(value + 0.01, 1)

    #Convert to float with 1 decimal place
    result = float(f"{result:.1f}")
    return result


#Stores the selected test for each sample
def store_selected_tests(test_results, sample_id, selected_tests):
    test_results[sample_id] = selected_tests
