import customtkinter as ctk
from PIL import Image
import database
import functions
import report
import config
from validation import Validator
from functools import partial


# Logo images
main_logo = ctk.CTkImage(light_image=Image.open('images/NotebookLogo.JPG'),
                          dark_image=Image.open('images/NotebookLogo.JPG'),
                          size=(150, 200))

secondary_logo = ctk.CTkImage(light_image=Image.open('images/NotebookLogo.JPG'),
                              dark_image=Image.open('images/NotebookLogo.JPG'),
                              size=(60, 80))


# MainPage configuration
class MainPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.success_window = None

        # Logo creation and placement
        self.label_logo = ctk.CTkLabel(self, image=main_logo, text="")
        self.label_logo.pack(pady=10)

        # Currently a test button
        self.test_button = ctk.CTkButton(self, text="Search for Project", command=self.open_project_search_window)
        self.test_button.pack(pady=5)

        # Button to open the new project creation window - ProjectCreationWindow
        self.create_project_button = ctk.CTkButton(self, text="New Project", command=self.open_project_creation_window)
        self.create_project_button.pack(pady=5)

        # # TEST BUTTON
        # self.create_project_button = ctk.CTkButton(self, text="TEST", command=lambda: self.show_tests())
        # self.create_project_button.pack(pady=5)
        #
        # # Label for the test button output
        # self.label_test_list = ctk.CTkLabel(self, text="")
        # self.label_test_list.pack(pady=5)

        # Store reference to the project window
        self.project_creation_window = None
        self.project_search_window = None

    # # TEST STUFF
    # def show_tests(self):
    #     self.success_window = SubmittedWindow(self, message="This is a test")
    #     self.success_window.grab_set()

    # Open ProjectSearchWindow if it isn't already open
    def open_project_search_window(self):
        if self.project_search_window is None or not self.project_search_window.winfo_exists():
            self.project_search_window = ProjectSearchWindow(self)  # Create new window
            self.project_search_window.grab_set()  # Make other pages unclickable
        else:
            self.project_search_window.focus()  # If already open, bring it to front

    # Open ProjectCreationWindow if it isn't already open
    def open_project_creation_window(self):
        if self.project_creation_window is None or not self.project_creation_window.winfo_exists():
            self.project_creation_window = ProjectCreationWindow(self)  # Create new window
            self.project_creation_window.grab_set()  # Make other pages unclickable
        else:
            self.project_creation_window.focus()  # If already open, bring it to front


class BasePage(ctk.CTkToplevel):
    def __init__(self, parent, title_text):
        super().__init__(parent)

        self.success_window = None

        # Page title creation and window size
        self.title(f"{title_text}")
        self.geometry("1000x750")

        # Set up the top frame of the page
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Set up the bottom frame of the page
        self.frame_middle = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_middle.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Set up the bottom frame of the page
        self.frame_bottom = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_bottom.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        # Logo creation and placement
        self.label_logo = ctk.CTkLabel(self.frame_top, text="", image=secondary_logo)
        self.label_logo.grid(row=0, column=0, padx=10, pady=10)

        # Title for the top of the ProjectCreationWindow
        self.title_label = ctk.CTkLabel(self.frame_top, text=f"{title_text}", font=("", 20))
        self.title_label.grid(row=0, column=1, padx=10, pady=5)


# ProjectSearchWindow configuration
class ProjectSearchWindow(BasePage):
    def __init__(self, parent):
        super().__init__(parent, "Project Search")

        self.project_window = None
        self.results_window = None
        self.review_window = None
        self.report_window = None
        self.selected_search_status = []
        self.list_of_status = database.get_status_list()
        self.status_vars = {}
        self.adv_vars = {}

        self.frame_middle = ctk.CTkScrollableFrame(self, fg_color="transparent", width=950, height=500)
        self.frame_middle.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.frame_advanced = ctk.CTkFrame(self.frame_top, fg_color="transparent")
        self.frame_advanced.grid(row=2, column=0, columnspan=10, sticky="w", padx=5, pady=5)
        self.frame_advanced.grid_remove()

        # Search button creation and placement
        self.button_search = ctk.CTkButton(self.frame_top, text="Search", command=lambda: self.search_projects())
        self.button_search.grid(row=1, column=1, padx=5, pady=5)

        # Set up status filter checkboxes
        filter_start_column = 2
        for status in self.list_of_status:
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(self.frame_top, text=status, variable=var)
            checkbox.grid(row=1, column=filter_start_column, padx=5, pady=5)
            self.status_vars[status] = var
            filter_start_column += 1

    # This chunk is an attempt at adding advanced search filters. Not currently working.
    #     self.advanced_visible = False
    #     self.button_adv_options= ctk.CTkButton(self.frame_top, text="+", width=15, command=lambda: self.toggle_advanced_search())
    #     self.button_adv_options.grid(row=1, column=filter_start_column, padx=5, pady=5)
    #
    # def toggle_advanced_search(self):
    #     if not self.advanced_visible:
    #         self.advanced_visible = True
    #         self.frame_advanced.grid()
    #         self.advanced_search_setup()
    #         self.button_adv_options.configure(text="-")
    #     else:
    #         self.advanced_visible = False
    #         self.frame_advanced.grid_remove()
    #         self.button_adv_options.configure(text="+")
    #
    # def advanced_search_setup(self):
    #     options_list = ["Project Number", "Sample Number", "Start Date", "End Date"]
    #
    #     for widget in self.frame_advanced.winfo_children():
    #         widget.destroy()
    #
    #
    #     options_start_column = 2
    #     for i, option in enumerate(options_list):
    #         label = ctk.CTkLabel(self.frame_advanced, text=option)
    #         label.grid(row=2, column=i + 2, padx=5, pady=5)
    #
    #         var = ctk.StringVar()
    #         entry = ctk.CTkEntry(self.frame_advanced, textvariable=var)
    #         entry.grid(row=3, column=i + 2, padx=5, pady=5)
    #         self.adv_vars[option] = var
    #
    #     # Advanced search functions
    #     self.button_adv_search = ctk.CTkButton(self.frame_advanced, text="Advanced Search", command=lambda: self.adv_search_projects())
    #     self.button_adv_search.grid(row=2, column=1, padx=5, pady=5)
    #
    # def adv_search_projects(self):
    #     project_num = self.adv_vars["Project Number"].get().strip()
    #     if project_num:
    #         Validator.is_valid_integer(int(project_num), min_value=1)
    #     sample_num = self.adv_vars["Sample Number"].get().strip()
    #     if sample_num:
    #         Validator.is_valid_integer(int(sample_num), min_value=1)
    #     start_date = self.adv_vars["Start Date"].get().strip()
    #     if start_date:
    #         Validator.is_valid_date(start_date)
    #     end_date = self.adv_vars["End Date"].get().strip()
    #     if end_date:
    #         Validator.is_valid_date(end_date)
    #     if start_date != None and end_date != None:
    #         Validator.is_valid_date_order(start_date, end_date)
    #
    #     selected_options_list = [option for option, input in self.adv_vars.items() if input.get()]
    #
    #     if len(selected_options_list) == 0:
    #         self.search_projects()
    #     else:
    #         database.get_advanced_filtered_projects_list(self.adv_vars)
    #     print(selected_options_list)
    #     print("Advanced Filters:")
    #     print("Project:", project_num)
    #     print("Sample:", sample_num)
    #     print("Start:", start_date)
    #     print("End:", end_date)

    def search_projects(self):
        self.selected_search_status = [status for status, var in self.status_vars.items() if var.get()]
        if not self.selected_search_status:
            projects = database.get_all_projects_list()
        else:
            projects = database.get_filtered_projects_list(self.selected_search_status)

        # Clears frame when new search is conducted
        for widget in self.frame_middle.winfo_children():
            widget.destroy()

        if projects != None:
            for index, project in enumerate(projects):
                project_id, status = project
                label = ctk.CTkLabel(self.frame_middle, text=f'Project: {project_id} | Status: {status}', font=("TkDefaultFont", 16), justify="left")
                label.grid(row=index, column=0, padx=5, pady=5, sticky="w")

                # Buttons to open various project windows
                button_view = ctk.CTkButton(self.frame_middle, text="View Project", command=lambda p_id=project_id: self.open_project_window(p_id))
                button_view.grid(row=index, column=1, padx=5, pady=5)

                button_enter = ctk.CTkButton(self.frame_middle, text="Enter Results", command=lambda p_id=project_id: self.open_results_window(p_id))
                button_enter.grid(row=index, column=2, padx=5, pady=5)

                button_review = ctk.CTkButton(self.frame_middle, text="Review Project", command=lambda p_id=project_id: self.open_review_window(p_id))
                button_review.grid(row=index, column=3, padx=5, pady=5)

                button_report = ctk.CTkButton(self.frame_middle, text="View Report", command=lambda p_id=project_id: self.open_report_window(p_id))
                button_report.grid(row=index, column=4, padx=5, pady=5)

                # Button state changes based on project status
                if status == "Closed":
                    button_enter.configure(state="disabled")
                    button_review.configure(state="disabled")
                elif status == "In Progress":
                    button_review.configure(state="disabled")
                    button_report.configure(state="disabled")
                elif status == "Review":
                    button_enter.configure(state="disabled")
                    button_report.configure(state="disabled")
                elif status == "Open":
                    button_review.configure(state="disabled")
                    button_report.configure(state="disabled")
        else:
            self.label_project_results = ctk.CTkLabel(self.frame_middle, text="No projects found.")
            self.label_project_results.grid(row=0, column=0, padx=5, pady=5)

    # Open ProjectDetailsWindow if it isn't already open
    def open_project_window(self, project_id):
        if self.project_window is None or not self.project_window.winfo_exists():
            self.project_window = ProjectDetailsWindow(self, project_id)  # Create new window
            self.project_window.grab_set()  # Make other pages unclickable
        else:
            self.project_window.focus()  # If already open, bring it to front

    # Open ResultsEntryWindow if it isn't already open
    def open_results_window(self, project_id):
        if self.results_window is None or not self.results_window.winfo_exists():
            self.results_window = ResultEntryWindow(self, project_id)  # Create new window
            self.results_window.grab_set()  # Make other pages unclickable
        else:
            self.results_window.focus()  # If already open, bring it to front

    # Open ResultReviewWindow if it isn't already open
    def open_review_window(self, project_id):
        if self.review_window is None or not self.review_window.winfo_exists():
            self.review_window = ResultReviewWindow(self, project_id)  # Create new window
            self.review_window.grab_set()  # Make other pages unclickable
        else:
            self.review_window.focus()  # If already open, bring it to front

    # Open ProjectReportWindow if it isn't already open
    def open_report_window(self, project_id):
        if self.report_window is None or not self.report_window.winfo_exists():
            self.report_window = ProjectReportWindow(self, project_id)  # Create new window
            self.report_window.grab_set()  # Make other pages unclickable
        else:
            self.report_window.focus()  # If already open, bring it to front


# ProjectDetailsWindow configuration
class ProjectDetailsWindow(BasePage):
    def __init__(self, parent, project_id):
        super().__init__(parent, "Project Details")

        self.project_id = project_id

        # Label to show project details
        self.label_project_details = ctk.CTkLabel(self.frame_top, text=self.get_project_details())
        self.label_project_details.grid(row=1, column=1, padx=5, pady=5)

        self.create_project_profile_grid()

    # Puts project details into a printable statement
    def get_project_details(self):
        details = database.get_project_details(self.project_id)
        details_report = f"Project: {details[0]} | Status: {details[1]} | Creation Date: {details[2]} | Sample Count: {details[3]}"
        return details_report

    def close_window(self):
        ProjectDetailsWindow.destroy(self)

    def create_project_profile_grid(self):
        sample_numbers = database.get_sample_numbers_for_project(self.project_id)
        test_list = database.get_test_profile_tests_only(self.project_id)
        indexed_test_list = list(enumerate(test_list))

        header_span = len(sample_numbers)

        label_sample_header = ctk.CTkLabel(self.frame_middle, text="Sample")
        label_sample_header.grid(row=0, column=1, columnspan=header_span, padx=5, pady=5)

        for index, test in indexed_test_list:
            label_test = ctk.CTkLabel(self.frame_middle, text=test)
            label_test.grid(row=index+2, column=0, padx=5, pady=5)

        column = 1
        for sample in sample_numbers:
            profile = database.sample_profile_information(self.project_id, sample)

            label_sample_number = ctk.CTkLabel(self.frame_middle, text=sample)
            label_sample_number.grid(row=1, column=column, padx=5, pady=5)

            for item in profile[1]:
                if item in test_list:
                    row = test_list.index(item) + 2
                    label_x = ctk.CTkLabel(self.frame_middle, text='X')
                    label_x.grid(row=row, column=column, padx=5, pady=5)
                else:
                    return
            column += 1

        button_close = ctk.CTkButton(self.frame_bottom, text="Close", command=self.close_window)
        button_close.grid(row=row, column=0, padx=5, pady=5)


# ResultEntryWindow configuration
class ResultEntryWindow(BasePage):
    def __init__(self, parent, project_id):
        super().__init__(parent, "Result Entry")

        self.project_id = project_id
        self.selected_option = ctk.StringVar(value=database.check_entry_complete_for_test(self.project_id)[0])        # Variable for selected options menu
        self.pathogen_selected_value = ctk.StringVar(value=config.pathogen_results[0])
        self.result_counts = []     # List to store overall project results for the test type
        self.sample_index = 0
        self.sample_id_list = []        # List for sample_id
        self.sample_number_list = []        # List for sample_numbers

        # Label for tests selection
        self.label_test_selection = ctk.CTkLabel(self.frame_middle, text="Select a test type for entry")
        self.label_test_selection.grid(row=0, column=0, padx=5, pady=5)

        # Option menu of tests to be entered
        self.menu_tests = ctk.CTkOptionMenu(self.frame_middle, values=database.check_entry_complete_for_test(self.project_id), variable=self.selected_option)
        self.menu_tests.grid(row=0, column=1, padx=5, pady=5)

        # Submit button for selected test
        self.button_test_selection = ctk.CTkButton(self.frame_middle, text="Submit", command=self.entry_grid_setup)
        self.button_test_selection.grid(row=0, column=2, padx=5, pady=5)

    # Gets the selected option from the dropdown menu
    def get_selected_option(self):
        selected_option = self.selected_option.get()        # Gets the selection from option menu
        sql_test_value = functions.convert_to_sql_single_test(selected_option)      # Converts the selection to sql code
        return sql_test_value

    # Sets up the entry grid prompts
    def entry_grid_setup(self):
        sql_test_id = self.get_selected_option()

        for widget in self.frame_bottom.winfo_children():       # Clears frame of previous entries
            widget.destroy()

        # Gets the samples to enter for the given project and test type selected
        self.sample_id_list, self.sample_number_list = database.get_samples_to_enter(self.project_id, sql_test_id)

        # If no samples to enter, return
        if not self.sample_number_list:
            label_error = ctk.CTkLabel(self.frame_bottom, text="No samples found.")
            label_error.grid(row=0, column=0, padx=5, pady=5)
            return
        if sql_test_id in config.petrifilm_tests:
            self.prompt_dilutions()
        elif sql_test_id in config.pathogen_tests:
            self.prompt_pathogen_entry()
        elif sql_test_id in config.chemistry_tests:
            self.prompt_chemistry_entry()

    def close_window(self):
        ResultEntryWindow.destroy(self)

    # Displays the results of the entered tests
    def display_final_results(self):
        results_list = self.result_counts
        test_name = self.selected_option.get()
        row = 1
        if test_name in config.result_units:
            unit = config.result_units[test_name]
        else:
            unit = ""
        for sample in results_list:
            sample_number = sample[0]
            result = sample[1]

            label_results = ctk.CTkLabel(self.frame_bottom, text=f"Sample {sample_number} result: {result} {unit}", font=("TkDefaultFont", 16))
            label_results.grid(row=row, column=0, padx=5, pady=5)
            row += 1
        database.submit_results_for_test(results_list, self.get_selected_option(), self.project_id)

        button_close = ctk.CTkButton(self.frame_bottom, text="Close", command=self.close_window)
        button_close.grid(row=row, column=0, padx=5, pady=5)

    # Gets the chemistry result entry
    def get_pathogen_result_entry(self):
        path_result = self.pathogen_selected_value.get()

        # Store sample number and final result into result_counts list
        sample_number = self.sample_number_list[self.sample_index]
        self.result_counts.append([sample_number, path_result])

        self.sample_index += 1

        for widget in self.frame_bottom.winfo_children():
            widget.destroy()

        label_previous_sample = ctk.CTkLabel(self.frame_bottom, text=f"Result for sample {sample_number} stored")
        label_previous_sample.grid(row=0, column=0, padx=5, pady=5)

        self.prompt_pathogen_entry()

    # Prompts user for chemistry result entry
    def prompt_pathogen_entry(self):
        # If all samples have been entered, displays results
        if self.sample_index >= len(self.sample_number_list):
            label_completed = ctk.CTkLabel(self.frame_bottom, text=f'All samples completed for {self.selected_option.get()}')
            label_completed.grid(row=0, column=0, padx=5, pady=5)
            print("All samples completed!", self.result_counts)
            self.display_final_results()
            return

        sample_number = self.sample_number_list[self.sample_index]

        # Label for result prompt
        label_dilutions = ctk.CTkLabel(self.frame_bottom, text=f"Sample {sample_number} - {self.selected_option.get()}:")
        label_dilutions.grid(row=1, column=0, padx=5, pady=5)

        # Menu of pathogen result options
        menu_pathogen_options = ctk.CTkOptionMenu(self.frame_bottom, values=config.pathogen_results, variable=self.pathogen_selected_value)
        menu_pathogen_options.grid(row=1, column=1, padx=5, pady=5)

        # Button to submit entries
        button_submit = ctk.CTkButton(self.frame_bottom, text="Submit", command=lambda: self.get_pathogen_result_entry())
        button_submit.grid(row=1, column=2, padx=5, pady=5)

    # Gets the chemistry result entry
    def get_chemistry_result_entry(self, event=None):
        # Error handling for result entry
        try:
            if self.selected_option.get() == "pH" or self.selected_option.get() == "Moisture":
                chem_result = Validator.is_valid_ph_moisture_result(self.entry_chem_result.get().strip())
            else:
                chem_result = Validator.is_valid_float(self.entry_chem_result.get().strip())
            final_result = functions.chemistry_rounding(chem_result)
        except ValueError:
            print("Invalid input: Please enter a number")
            return  # Ignore invalid input

        # Store sample number and final result into result_counts list
        sample_number = self.sample_number_list[self.sample_index]
        self.result_counts.append([sample_number, final_result])

        self.sample_index += 1

        for widget in self.frame_bottom.winfo_children():
            widget.destroy()

        self.prompt_chemistry_entry()

    # Prompts user for chemistry result entry
    def prompt_chemistry_entry(self):
        # If all samples have been entered, displace results
        if self.sample_index >= len(self.sample_number_list):
            label_completed = ctk.CTkLabel(self.frame_bottom, text=f'All samples completed for {self.selected_option.get()}')
            label_completed.grid(row=0, column=0, padx=5, pady=5)
            print("All samples completed!", self.result_counts)
            self.display_final_results()
            return

        sample_number = self.sample_number_list[self.sample_index]

        # Label for result prompt
        label_dilutions = ctk.CTkLabel(self.frame_bottom, text=f"Sample {sample_number} - {self.selected_option.get()}:")
        label_dilutions.grid(row=0, column=0, padx=5, pady=5)

        # Entry box for result prompt
        self.entry_chem_result = ctk.CTkEntry(self.frame_bottom)
        self.entry_chem_result.grid(row=0, column=1, padx=5, pady=5)
        self.entry_chem_result.focus()
        self.entry_chem_result.bind("<Return>", self.get_chemistry_result_entry)

    # Prompts user for number of dilutions for a sample
    def prompt_dilutions(self):
        # Displays if all samples have been entered
        if self.sample_index >= len(self.sample_number_list):
            label_completed = ctk.CTkLabel(self.frame_bottom, text=f'All samples completed for {self.selected_option.get()}')
            label_completed.grid(row=0, column=0, padx=5, pady=5)
            print("All samples completed!", self.result_counts)
            self.display_final_results()
            return

        sample_number = self.sample_number_list[self.sample_index]

        # Label for dilutions prompts
        label_dilutions = ctk.CTkLabel(self.frame_bottom, text=f"Sample {sample_number} - Enter number of dilutions:")
        label_dilutions.grid(row=0, column=0, padx=5, pady=5)

        # Entry box for dilutions prompt
        self.entry_dilutions = ctk.CTkEntry(self.frame_bottom)
        self.entry_dilutions.grid(row=0, column=1, padx=5, pady=5)
        self.entry_dilutions.focus()
        self.entry_dilutions.bind("<Return>", self.prompt_lowest_dilution)      # On 'Enter' press, prompts lowest dilution

    # Prompts user for lowest dilution for the sample
    def prompt_lowest_dilution(self):
        # Error handling for dilution count entry
        try:
            self.num_dilutions = Validator.is_valid_integer(self.entry_dilutions.get().strip(), min_value=1, max_value=4)
        except ValueError:
            return  # Ignore invalid input

        for widget in self.frame_bottom.winfo_children():       # Clears frame of previous entries
            widget.destroy()

        # Label for lowest dilution
        label_low_dilution = ctk.CTkLabel(self.frame_bottom, text="Enter lowest dilution:")
        label_low_dilution.grid(row=0, column=0, padx=5, pady=5)

        # Entry box for lowest dilution
        self.entry_lowest_dilution = ctk.CTkEntry(self.frame_bottom)
        self.entry_lowest_dilution.grid(row=0, column=1, padx=5, pady=5)
        self.entry_lowest_dilution.focus()
        self.entry_lowest_dilution.bind("<Return>", self.create_dilution_rows)

    # Creates the entry boxes for the number of dilutions
    def create_dilution_rows(self):
        # Error handling for lowest dilution entry
        try:
            self.lowest_dilution = Validator.is_valid_integer(self.entry_lowest_dilution.get().strip(), min_value=0, max_value=7)
        except ValueError:
            return

        for widget in self.frame_bottom.winfo_children():       # Clears frame of previous entries
            widget.destroy()

        # Label for dilution header
        label_dilution_header = ctk.CTkLabel(self.frame_bottom, text="Dilution")
        label_dilution_header.grid(row=0, column=0, padx=5, pady=5)

        # Label for count header
        label_count_header = ctk.CTkLabel(self.frame_bottom, text="Count")
        label_count_header.grid(row=0, column=1, padx=5, pady=5)

        self.dilution_entries = []
        dilution_factor = self.lowest_dilution      # Sets dilution_factor to current lowest dilution

        # Loops through for total number of dilutions entered
        for i in range(self.num_dilutions):
            # Label for dilution
            label_dilution = ctk.CTkLabel(self.frame_bottom, text=str(dilution_factor))
            label_dilution.grid(row=i + 1, column=0, padx=5, pady=5)

            # Entry box for count
            entry_count = ctk.CTkEntry(self.frame_bottom)
            entry_count.grid(row=i + 1, column=1, padx=5, pady=5)

            # Adds the dilution, and it's count to dilution_entries list
            self.dilution_entries.append([dilution_factor, entry_count])

            # Increase dilution factor by 1
            dilution_factor += 1

        # Button to submit entries
        button_submit = ctk.CTkButton(self.frame_bottom, text="Submit", command=self.store_petrifilm_results)
        button_submit.grid(row=self.num_dilutions + 1, column=1, padx=5, pady=5)

        print(f'Dilution_entries: {self.dilution_entries}')

    # Stores the submitted results in results_counts
    def store_petrifilm_results(self):
        sample_number = self.sample_number_list[self.sample_index]
        sample_results = []

        # Loops through all entries in dilution_entries to append into sample_results list
        for dilution_factor, entry in self.dilution_entries:
            try:
                count = Validator.is_valid_integer(entry.get().strip())
                sample_results.append([dilution_factor, count])
            except ValueError:
                print(f"Invalid count for dilution {dilution_factor}, skipping...")
        print(f'sample results: {sample_results}')
        sql_test = functions.convert_to_test_name_from_sql_code(self.get_selected_option())
        final_result = functions.compare_to_countable_range(sql_test, sample_results)
        self.result_counts.append([sample_number, final_result])
        print(f'Result counts: {self.result_counts}')

        self.sample_index += 1      # Move to next sample
        for widget in self.frame_bottom.winfo_children():       # Clears frame of previous entries
            widget.destroy()
        self.prompt_dilutions()     # Restart for next sample


# ResultReviewWindow configuration
class ResultReviewWindow(BasePage):
    def __init__(self, parent, project_id):
        super().__init__(parent, "Result Review")

        self.project_id = project_id
        self.final_results = functions.generate_report_results(project_id)
        self.project_profile = None

        self.frame_middle = ctk.CTkScrollableFrame(self, fg_color="transparent", width=950, height=500)
        self.frame_middle.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Search button creation and placement
        self.button_view_report = ctk.CTkButton(self.frame_top, text="View Report", command=lambda: self.display_review_report())
        self.button_view_report.grid(row=1, column=1, padx=5, pady=5)


    def display_review_report(self):
        sql_test_list = database.get_test_list()
        self.edited_results = {}
        row = 1

        for sample_num, sample_value in self.final_results.items():
            # Display sample header
            label_sample = ctk.CTkLabel(self.frame_middle, text=f"Sample Number: {sample_num}", font=("TkDefaultFont", 16))
            label_sample.grid(row=row, column=0, padx=5, pady=5, sticky="w")
            row += 1  # Move to next row for tests

            for test_id, result in sample_value:
                test_name = next((key for key, value in sql_test_list.items() if value == test_id), "Unknown Test")
                unit = config.result_units.get(test_name, "")

                # Frame to store each test's widgets
                test_frame = ctk.CTkFrame(self.frame_middle, fg_color="transparent")
                test_frame.grid(row=row, column=0, padx=5, pady=5, sticky="w")

                # Labels for result display
                label_test = ctk.CTkLabel(test_frame, text=f"\tTest: {test_name} |", font=("TkDefaultFont", 14))
                label_test.pack(side="left", padx=5)

                label_result = ctk.CTkLabel(test_frame, text=f" Result: {result} {unit}", font=("TkDefaultFont", 14))
                label_result.pack(side="left", padx=5)

                # Entry box for editing (initially hidden)
                entry_result = ctk.CTkEntry(test_frame, width=100)
                entry_result.insert(0, str(result))  # Pre-fill with the existing result
                entry_result.pack_forget()  # Hide initially

                # Accept button (initially hidden)
                button_accept = ctk.CTkButton(test_frame, text="Accept", width=7)
                button_accept.pack_forget()  # Hide initially

                # Create Edit Button FIRST before referencing it
                button_edit = ctk.CTkButton(test_frame, text="Edit", width=7)

                # Function to enable editing mode
                def enable_edit(entry=entry_result, label=label_result, edit_btn=button_edit, accept_btn=button_accept):
                    label.pack_forget()  # Hide label
                    entry.pack(side="left", padx=5)  # Show entry
                    edit_btn.pack_forget()  # Hide edit button
                    accept_btn.pack(side="left", padx=5)  # Show accept button

                # Function to save edited value and restore display mode
                def accept_edit(entry=entry_result, label=label_result, edit_btn=button_edit, accept_btn=button_accept, sample_num=sample_num, test_id=test_id):
                    new_value = ""
                    if test_id in config.petrifilm_tests:
                        new_value = Validator.is_valid_integer(entry.get().strip())                                             # EDIT THIS FOR RESULT VALIDATION BASED ON TEST TYPE
                    elif test_id in config.chemistry_tests:
                        if test_id == 9 or test_id == 10:
                            new_value = Validator.is_valid_ph_moisture_result(entry.get().strip())
                        else:
                            new_value = Validator.is_valid_float(entry.get().strip())
                    elif test_id in config.pathogen_tests:
                        new_value = Validator.is_valid_pathogen_result(entry.get().strip())

                    label.configure(text=f" Result: {new_value} {unit}")
                    entry.pack_forget()  # Hide entry box
                    accept_btn.pack_forget()  # Hide accept button
                    label.pack(side="left", padx=5)  # Show updated label
                    edit_btn.pack(side="left", padx=5)  # Show edit button again

                    self.edited_results[(sample_num, test_id)] = new_value

                # Edit and accept button configuration
                button_edit.configure(command=partial(enable_edit, entry_result, label_result, button_edit, button_accept))
                button_accept.configure(command=partial(accept_edit, entry_result, label_result, button_edit, button_accept, sample_num, test_id))

                # Pack buttons after assigning correct commands
                button_edit.pack(side="left", padx=5)

                row += 1  # Move to next row for the next test

        # Button to submit changes to the database
        button_submit_changes = ctk.CTkButton(self.frame_middle, text="Accept Results", command=self.submit_changes)
        button_submit_changes.grid(row=row + 1, column=0, padx=5, pady=5)

    def close_window(self):
        ResultReviewWindow.destroy(self)

    # Submit the changes to the database
    def submit_changes(self):

        for (sample_num, test_id), new_value in self.edited_results.items():
            # Call the database update function
            database.submit_edited_results(sample_num, test_id, new_value)

        self.edited_results.clear()  # Clear edits after saving
        database.change_project_status(self.project_id, "Closed")

        self.success_window = SubmittedWindow(self, message=f"Project {self.project_id} results reviewed")
        self.success_window.grab_set()

        self.button_close = ctk.CTkButton(self.frame_bottom, text="Close", command=self.close_window)
        self.button_close.pack(padx=5, pady=5)


# ProjectReportWindow configuration
class ProjectReportWindow(BasePage):
    def __init__(self, parent, project_id):
        super().__init__(parent, "Project Report")

        self.project_id = project_id
        self.final_results = functions.generate_report_results(project_id)
        self.project_profile = None

        # Search button creation and placement
        self.button_generate_report = ctk.CTkButton(self.frame_top, text="Generate Report", command=lambda: self.display_report_text())
        self.button_generate_report.grid(row=1, column=1, padx=5, pady=5)

    def close_window(self):
        ProjectReportWindow.destroy(self)

        # self.display_report_text()
    def display_report_text(self):
        sql_test_list = database.get_test_list()
        row = 1

        for sample_num, sample_value in self.final_results.items():
            result_strings = []  # Store test results as formatted strings

            for test_id, result in sample_value:  # Unpack test_id and result
                # Get test name from test_id
                test_name = next((key for key, value in sql_test_list.items() if value == test_id), "Unknown Test")

                # Get the unit for the test
                unit = config.result_units.get(test_name, "")

                # Store formatted result for this test
                result_strings.append(f"Test: {test_name} | Result: {result} {unit}".strip())

            # Create a multi-line string for this sample
            result_text = f"Sample Number: {sample_num}\n\t" + "\n\t".join(result_strings)

            # Create a single label per sample, displaying multiple lines
            label_results = ctk.CTkLabel(self.frame_middle, text=result_text, font=("TkDefaultFont", 16), justify="left")
            label_results.grid(row=row, column=0, padx=5, pady=5, sticky="w")
            row += 1  # Move to the next row for the next sample

        report.generate_report(self.project_id)

        self.button_close = ctk.CTkButton(self.frame_bottom, text="Close", command=self.close_window)
        self.button_close.grid(row=row, column=0, padx=5, pady=5)


# ProjectCreationWindow configuration
class ProjectCreationWindow(BasePage):
    def __init__(self, parent):
        super().__init__(parent, "Project Creation")

        self.test_window = None     # Set test_window to None

        self.sample_count = 0
        self.current_sample = 1
        self.test_profile = {}
        self.project_number = database.get_current_project_number() + 1     # Set project_number to one more than most recently used number

        # Label with the prompt to enter number of samples
        self.label_prompt = ctk.CTkLabel(self.frame_top, text="Enter number of samples:")
        self.label_prompt.grid(row=1, column=1, padx=10, pady=5)

        # Entry box to get sample amount
        self.entry_sample_count = ctk.CTkEntry(self.frame_top, placeholder_text="Ex: 4")
        self.entry_sample_count.grid(row=1, column=2, padx=10, pady=5)

        # Empty label for error message
        self.label_result = ctk.CTkLabel(self.frame_top, text="")
        self.label_result.grid(row=2, column=1, padx=10, pady=5)

        # Button to submit the entry box. Runs get_sample_count to get entry value and start test entry
        self.button_sample_count_submit = ctk.CTkButton(self.frame_top, text="Submit", command=lambda: self.get_sample_count())
        self.button_sample_count_submit.grid(row=1, column=3, padx=5, pady=5)

    # Validate the entry box input and initiate TestGrid for test entry
    def get_sample_count(self):
        count_string = self.entry_sample_count.get().strip()        # Clean entry
        try:
            self.sample_count = Validator.is_valid_integer(count_string, min_value=1, max_value=10)
            self.display_sample_row()
        except:
            self.label_result.configure(text="Invalid input. Please enter a number.", text_color="red")

    # Creates a row to select tests for a sample
    def display_sample_row(self):
        # If the current_sample is higher than the sample count, show the final submission button
        if self.current_sample > self.sample_count:
            self.show_final_submit()
            return

        # Display sample label
        label_sample_id = ctk.CTkLabel(self.frame_middle, text=f"Sample {self.current_sample}")
        label_sample_id.grid(row=self.current_sample, column=0, padx=5, pady=5)

        # "+" Button to open test selection window
        button_add_test = ctk.CTkButton(self.frame_middle, text="+", width=7, command=self.open_test_selection_window)
        button_add_test.grid(row=self.current_sample, column=1, padx=5, pady=5)

        # "Submit" Button to finalize sample
        button_submit = ctk.CTkButton(self.frame_middle, text="Submit", command=self.finalize_sample)
        button_submit.grid(row=self.current_sample, column=2, padx=5, pady=5)

    # Open the test selection window
    def open_test_selection_window(self):
        # If the window doesn't exist, open the window and focus
        if self.test_window is None or not self.test_window.winfo_exists():
            self.test_window = TestSelectionWindow(self)  # Create new window
            self.test_window.grab_set()  # Make other pages unclickable
        # If the window already exists, focus it
        else:
            self.test_window.focus()

    # Compile the selected test for the sample and move to the next sample
    def finalize_sample(self):
        if self.current_sample in self.test_profile and self.test_profile[self.current_sample]:
            print(f'Sample {self.current_sample} tests: {self.test_profile[self.current_sample]}')
            self.current_sample += 1
            self.display_sample_row()
        else:
            print("No test selected for this sample")

    # Store the selected tests
    def store_selected_tests(self, selected_tests):
        functions.store_selected_tests(self.test_profile, self.current_sample, selected_tests)

    # Create and place the "Submit All" button
    def show_final_submit(self):
        button_final_submit = ctk.CTkButton(self.frame_bottom, text="Submit All", command=self.submit_project)
        button_final_submit.grid(row=self.current_sample + 1, column=2, padx=10, pady=5)

    # Gets test lists and submits the project and samples into the database
    def submit_project(self):
        processed_results = self.test_profile
        try:
            database.submit_project_creation(self.project_number, processed_results)

            self.success_window = SubmittedWindow(self, message=f"Project {self.project_number} created successfully")
            self.success_window.grab_set()

        except Exception as e:
            print(f"Error submitting project: {e}")
            ctk.CTkLabel(self.frame_bottom, text="Error: Could not submit project.", text_color="red").grid(row=self.current_sample + 2, column=2, padx=5, pady=5)


# TestSelectionWindow configuration
class TestSelectionWindow(BasePage):
    def __init__(self, parent):
        super().__init__(parent, "Test Selection")

        self.parent = parent
        self.selected_tests = []
        self.test_list = functions.set_test_list()
        self.checkbox_selection = {}

        # Creates the grid of selectable tests
        self.generate_test_checkboxes(self.frame_middle)

    def generate_test_checkboxes(self, frame):
        current_row = 0
        current_column = 0
        # Go through each test from the test list and creates a checkbox for each
        for index, test in enumerate(self.test_list):
            var = ctk.BooleanVar()  # Boolean variable to track checkbox state
            checkbox = ctk.CTkCheckBox(frame, text=test, variable=var)
            # Sets the max tests per row to be 5
            if current_column == 5:
                current_column = 0
                current_row += 1

            checkbox.grid(row=current_row + 1, column=current_column, padx=10, pady=2)

            current_column += 1

            # Stores the selected checkbox tests into a list
            self.checkbox_selection[test] = var  # Store reference to the variable

        # Creates a submit button after the test grid is created
        button_submit = ctk.CTkButton(self, text="Submit", command=self.submit_selected_tests)
        button_submit.grid(row=current_row + 2, column=0, padx=5, pady=5)

    # Confirm selected tests and destroy the window
    def submit_selected_tests(self):
        for test, var in self.checkbox_selection.items():
            if var.get():
                self.selected_tests.append(test)
        self.parent.store_selected_tests(self.selected_tests)
        self.destroy()


class SubmittedWindow(ctk.CTkToplevel):
    def __init__(self, parent, message="Successful"):
        super().__init__(parent)

        self.title("Success")
        self.geometry("300x150")
        self.resizable(False, False)

        label_success = ctk.CTkLabel(self, text=message)
        label_success.pack(padx=5, pady=5)

        # Button to close the window
        self.close_button = ctk.CTkButton(self, text="Close", command=self.destroy)
        self.close_button.pack(padx=5, pady=5)
