import config


class Validator:
    # Checks if value is an integer with option to be within a range
    @staticmethod
    def is_valid_integer(value, min_value=None, max_value=None):
        try:
            int_value = int(value)
            if (min_value is not None and int_value < min_value) or (max_value is not None and int_value > max_value):
                raise ValueError(f"Value must be between {min_value} and {max_value}.")
            return int_value  # Return the valid integer
        except ValueError:
            raise ValueError("Invalid input: Must be an integer.")

    # Checks is value is a float with option to be within a range
    @staticmethod
    def is_valid_float(value, min_value=None, max_value=None):
        try:
            float_value = float(value)
            if ((min_value is not None and float_value < min_value)
                    or (max_value is not None and float_value > max_value)):
                raise ValueError(f"Value must be between {min_value} and {max_value}.")
            return float_value  # Return the valid float
        except ValueError:
            raise ValueError("Invalid input: Must be a numeric value.")

    # Checks if value is not an empty string
    @staticmethod
    def is_non_empty_string(value):
        if not value.strip():
            raise ValueError("Input cannot be empty.")
        return value.strip()

    # Checks is the test is in the valid_tests list
    @staticmethod
    def is_valid_test_name(test_name):
        if test_name not in config.valid_tests:  # Assume valid_tests is a list of known tests
            raise ValueError(f"Invalid test name: {test_name}.")
        return test_name

    # Checks if value is a valid float and not negative
    @staticmethod
    def is_valid_ph_moisture_result(value):
        value = Validator.is_valid_float(value, min_value=0)  # Chemistry values cannot be negative
        return round(value, 1)  # Ensure it's 1 decimal place
