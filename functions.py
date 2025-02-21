import customtkinter as ctk
import database

class TestGrid:
    def __init__(self, master, sample_count):
        self.master = master
        self.sample_count = sample_count
        self.test_list = set_test_list()
        self.next_database_sample = database.get_current_sample_number() + 1
        self.current_sample = 1  # Track which sample we're on
        self.row_count = 0  # Start at row 3
        self.test_column_count = 2  # Test dropdown starts at column 2
        self.test_column_count_max = 0
        self.submit_flags = [False] * sample_count  # Track row completion
        self.test_selections = []  # Track test option menus for current row
        self.sample_results = {}  # Store selected tests per sample
        self.project_tests = []

        self.create_row(self.current_sample, self.next_database_sample)

    def create_row(self, sample_id, sql_sample_id):
        """Creates a new row for a sample with test selection."""
        label_sample_id = ctk.CTkLabel(self.master, text=str(sql_sample_id))
        label_sample_id.grid(row=self.row_count, column=1, padx=0, pady=5)

        # First test dropdown
        test_var = ctk.StringVar(value=self.test_list[0])  # Default selection
        options_test_list = ctk.CTkOptionMenu(self.master, values=self.test_list, variable=test_var)
        options_test_list.grid(row=self.row_count, column=self.test_column_count, padx=5, pady=5)

        self.test_selections.append(test_var)  # Store reference to selected option

        # + Button to add another test
        button_add_test = ctk.CTkButton(self.master, text="+", width=10,
                                        command=lambda: self.add_another_test(self.row_count, button_add_test, button_submit))
        button_add_test.grid(row=self.row_count, column=self.test_column_count + 1, padx=5, pady=5)

        # Submit button to finalize the row
        button_submit = ctk.CTkButton(self.master, text="Submit",
                                      command=lambda: self.finalize_row(sample_id,button_add_test, button_submit))
        button_submit.grid(row=self.row_count, column=self.test_column_count + 2, padx=5, pady=5)

    def add_another_test(self, row, add_button, submit_button):
        """Adds a new test dropdown and shifts buttons right."""
        new_test_column = self.test_column_count + 1

        # Create new test dropdown
        test_var = ctk.StringVar(value=self.test_list[0])  # Default selection
        options_test_list = ctk.CTkOptionMenu(self.master, values=self.test_list, variable=test_var)
        options_test_list.grid(row=row, column=new_test_column, padx=5, pady=5)

        self.test_selections.append(test_var)  # Store reference to selected option

        # Move buttons to the right
        add_button.grid(row=row, column=new_test_column + 1, padx=5, pady=5)
        submit_button.grid(row=row, column=new_test_column + 2, padx=5, pady=5)

        self.test_column_count += 1  # Update column tracker

    def finalize_row(self, sample_id, button1, button2):
        """Marks the current row as completed and moves to the next sample."""
        selected_tests = [var.get() for var in self.test_selections]  # Get selected values
        self.sample_results[sample_id] = selected_tests  # Store them

        print(f"Sample {sample_id} tests: {selected_tests}")  # Debugging output
        sql_sample_test_list = convert_to_sql_test_list(selected_tests)
        self.sample_results[sample_id] = sql_sample_test_list
        self.project_tests.append(self.sample_results)

        button1.destroy()
        button2.destroy()

        self.submit_flags[sample_id - 1] = True  # Mark this sample as complete

        if self.current_sample < self.sample_count:
            self.current_sample += 1
            self.next_database_sample += 1
            self.row_count += 1  # Move to the next row
            if self.test_column_count_max < self.test_column_count:
                self.test_column_count_max = self.test_column_count - 1
            self.test_column_count = 2  # Reset column count
            self.test_selections = []  # Reset selections for new row
            self.sample_results = {}    # Reset selections for new row
            self.create_row(self.current_sample, self.next_database_sample)  # Start new sample row
        else:
            button_final_submit = ctk.CTkButton(self.master, text="Submit") #, command=lambda: self.submit_test_list)
            button_final_submit.grid(row=self.row_count+1, column=2)

    def submit_test_list(self):
        return self.project_tests


def set_test_list():
    full_test_list = database.get_test_list()
    test_list_options = []
    for key in full_test_list:
        test_list_options.append(key)
    return test_list_options

def convert_to_sql_test_list(sample_test_list):
    full_test_list = database.get_test_list()
    temp_sql_test_list = []
    for test in sample_test_list:
        value = full_test_list[test]
        temp_sql_test_list.append(value)
    temp_sql_test_list.sort()
    sql_test_list = list(set(temp_sql_test_list))
    return sql_test_list

