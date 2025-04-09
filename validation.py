import config
from customtkinter import CTkToplevel, CTkLabel, CTkButton
from datetime import datetime


class Validator:

    @staticmethod
    def show_error_popup(message):
        popup = CTkToplevel()
        popup.title("Error")
        popup.geometry("300x150")

        label_warning = CTkLabel(popup, text=message, text_color="red")
        label_warning.pack(pady=10)

        close_button = CTkButton(popup, text="OK", command=popup.destroy)
        close_button.pack(pady=10)

        popup.grab_set()

    # Checks if value is an integer with option to be within a range
    @staticmethod
    def is_valid_integer(value, min_value=None, max_value=None):
        try:
            int_value = int(value)
            if (min_value is not None and int_value < min_value) or (max_value is not None and int_value > max_value):
                message = f"Value must be between {min_value} and {max_value}."
                Validator.show_error_popup(message)
                raise ValueError(message)
            return int_value  # Return the valid integer
        except ValueError:
            raise ValueError("Invalid input: Must be an integer.")

    # Checks is value is a float with option to be within a range
    @staticmethod
    def is_valid_float(value, min_value=None, max_value=None):
        try:
            float_value = float(value)
            if (min_value is not None and float_value < min_value) or (max_value is not None and float_value > max_value):
                message = f"Value must be between {min_value} and {max_value}."
                Validator.show_error_popup(message)
                raise ValueError(message)
            return float_value  # Return the valid float
        except ValueError:
            raise ValueError("Invalid input: Must be a numeric value.")

    @staticmethod
    def is_valid_date(date_string, input_format="%m/%d/%Y",  output_format="%Y-%m-%d"):
        try:
            formatted_date = datetime.strptime(date_string, input_format)
            return formatted_date.strftime(output_format)
        except ValueError:
            print(f"Invalid date: {date_string}")
            return None

    @staticmethod
    def is_valid_date_order(start_date, end_date):
        try:
            if start_date < end_date:
                return True
        except ValueError:
            print(f"Date error: Start date {start_date} comes after end date {end_date}")

    # Checks if value is a valid float and not negative
    @staticmethod
    def is_valid_ph_moisture_result(value):
        value = Validator.is_valid_float(value, min_value=0)  # Chemistry values cannot be negative
        return round(value, 1)  # Ensure it's 1 decimal place

    # Checks if entry is valid pathogen result
    @staticmethod
    def is_valid_pathogen_result(value):
        test_value = value.lower()
        if test_value != "absence" and test_value != "presence":
            message = "Invalid Entry: Must be 'Absence' or 'Presence'."
            Validator.show_error_popup(message)
            raise ValueError(message)
        return test_value.capitalize()
