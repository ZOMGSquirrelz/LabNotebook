import customtkinter as ctk
from PIL import Image
import database
import functions

# Logo images
main_logo = ctk.CTkImage(light_image=Image.open('images/NotebookLogo.JPG'),
                          dark_image=Image.open('images/NotebookLogo.JPG'),
                          size=(150, 200))

secondary_logo = ctk.CTkImage(light_image=Image.open('images/NotebookLogo.JPG'),
                              dark_image=Image.open('images/NotebookLogo.JPG'),
                              size=(60, 80))

#MainPage configuration
class MainPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        #Logo creation and placement
        self.label_logo = ctk.CTkLabel(self, image=main_logo, text="")
        self.label_logo.pack(pady=10)

        #Currently a test button
        self.test_button = ctk.CTkButton(self, text="Search for Project", command=self.open_project_search_window)
        self.test_button.pack(pady=5)

        #Button to open the new project creation window - ProjectCreationWindow
        self.create_project_button = ctk.CTkButton(self, text="New Project", command=self.open_project_creation_window)
        self.create_project_button.pack(pady=5)

        #TEST BUTTON
        self.create_project_button = ctk.CTkButton(self, text="TEST", command=lambda: self.show_tests())
        self.create_project_button.pack(pady=5)

        #Labal for the test button output
        self.label_test_list = ctk.CTkLabel(self, text="")
        self.label_test_list.pack(pady=5)

        #Store reference to the project window
        self.project_creation_window = None
        self.project_search_window = None

    #TEST STUFF
    def show_tests(self):
        tests = database.get_samples_to_enter(10, 1)
        self.label_test_list.configure(text=tests)

    #Open ProjectSearchWindow if it isn't already open
    def open_project_search_window(self):
        if self.project_search_window is None or not self.project_search_window.winfo_exists():
            self.project_search_window = ProjectSearchWindow(self)  #Create new window
            self.project_search_window.grab_set()  #Make other pages unclickable
        else:
            self.project_search_window.focus()  #If already open, bring it to front

    #Open ProjectCreationWindow if it isn't already open
    def open_project_creation_window(self):
        if self.project_creation_window is None or not self.project_creation_window.winfo_exists():
            self.project_creation_window = ProjectCreationWindow(self)  #Create new window
            self.project_creation_window.grab_set()  #Make other pages unclickable
        else:
            self.project_creation_window.focus()  #If already open, bring it to front

#ProjectSearchWindow configuration
class ProjectSearchWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.project_window = None
        self.results_window = None
        self.review_window = None
        self.report_window = None
        self.selected_search_status = []
        self.list_of_status = database.get_status_list()
        self.status_vars = {}

        #Page title creation and window size
        self.title("Project Search")
        self.geometry("1000x750")

        #Set up the top frame of the page
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Set up the bottom frame of the page
        self.frame_middle = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_middle.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        #Set up the bottom frame of the page
        self.frame_bottom = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_bottom.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        #Logo creation and placement
        self.label_logo = ctk.CTkLabel(self.frame_top, text="", image=secondary_logo)
        self.label_logo.grid(row=0, column=0, padx=10, pady=10)

        #Title for the top of the ProjectCreationWindow
        self.title_label = ctk.CTkLabel(self.frame_top, text="Project Search", font=("", 20))
        self.title_label.grid(row=0, column=1, padx=10, pady=5)

        #Search button creation and placement
        self.button_search_all = ctk.CTkButton(self.frame_top, text="Search", command=lambda: self.search_projects())
        self.button_search_all.grid(row=1, column=1, padx=5, pady=5)

        #Set up status filter checkboxes
        filter_start_column =  2
        for status in self.list_of_status:
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(self.frame_top, text=status, variable=var)
            checkbox.grid(row=1, column=filter_start_column, padx=5, pady=5)
            self.status_vars[status] = var
            filter_start_column += 1

        #Label to dispaly the resulting projects
        self.label_project_results = ctk.CTkLabel(self.frame_middle, text="")
        self.label_project_results.grid(row=0, column=0, padx=5, pady=5)

    def search_projects(self):
        self.selected_search_status = [status for status, var in self.status_vars.items() if var.get()]
        if not self.selected_search_status:
            projects = database.get_all_projects_list()
        else:
            projects = database.get_filtered_projects_list(self.selected_search_status)

        #Clears frame when new search is conducted
        for widget in self.frame_middle.winfo_children():
            widget.destroy()

        if projects:
            for index, project in enumerate(projects):
                project_id, status = project
                label = ctk.CTkLabel(self.frame_middle, text=f'Project: {project_id} | Status: {status}', font=("TkDefaultFont", 16))
                label.grid(row=index, column=0, padx=5, pady=5)

                #Buttons to open various project windows
                button_view = ctk.CTkButton(self.frame_middle, text="View Project", command=lambda p_id=project_id: self.open_project_window(p_id))
                button_view.grid(row=index, column=1, padx=5, pady=5)

                button_enter = ctk.CTkButton(self.frame_middle, text="Enter Results", command=lambda p_id=project_id: self.open_results_window(p_id))
                button_enter.grid(row=index, column=2, padx=5, pady=5)

                button_review = ctk.CTkButton(self.frame_middle, text="Review Project", command=lambda p_id=project_id: self.open_review_window(p_id))
                button_review.grid(row=index, column=3, padx=5, pady=5)

                button_report = ctk.CTkButton(self.frame_middle, text="View Report", command=lambda p_id=project_id: self.open_report_window(p_id))
                button_report.grid(row=index, column=4, padx=5, pady=5)

                #Button state changes based on project status
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
            self.label_project_results.configure(text="No projects found.")


            
    #Open ProjectDetailsWindow if it isn't already open
    def open_project_window(self, project_id):
        if self.project_window is None or not self.project_window.winfo_exists():
            self.project_window = ProjectDetailsWindow(self, project_id)  #Create new window
            self.project_window.grab_set()  #Make other pages unclickable
        else:
            self.project_window.focus()  #If already open, bring it to front

    #Open ResultsEntryWindow if it isn't already open
    def open_results_window(self, project_id):
        if self.results_window is None or not self.results_window.winfo_exists():
            self.results_window = ResultEntryWindow(self, project_id)  #Create new window
            self.results_window.grab_set()  #Make other pages unclickable
        else:
            self.results_window.focus()  #If already open, bring it to front

    #Open ResultReviewWindow if it isn't already open
    def open_review_window(self, project_id):
        if self.review_window is None or not self.review_window.winfo_exists():
            self.review_window = ResultReviewWindow(self, project_id)  #Create new window
            self.review_window.grab_set()  #Make other pages unclickable
        else:
            self.review_window.focus()  #If already open, bring it to front

    #Open ProjectReportWindow if it isn't already open
    def open_report_window(self, project_id):
        if self.report_window is None or not self.report_window.winfo_exists():
            self.report_window = ProjectReportWindow(self, project_id)  #Create new window
            self.report_window.grab_set()  #Make other pages unclickable
        else:
            self.report_window.focus()  #If already open, bring it to front

#ProjectDetailsWindow configuration
class ProjectDetailsWindow(ctk.CTkToplevel):
    def __init__(self, parent, project_id):
        super().__init__(parent)

        self.project_id = project_id

        #Page title creation and window size
        self.title("Project Details")
        self.geometry("1000x750")

        #Set up the top frame of the page
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Set up the bottom frame of the page
        self.frame_middle = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_middle.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        #Set up the bottom frame of the page
        self.frame_bottom = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_bottom.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        #Logo creation and placement
        self.label_logo = ctk.CTkLabel(self.frame_top, text="", image=secondary_logo)
        self.label_logo.grid(row=0, column=0, padx=10, pady=10)

        #Title for the top of the ProjectCreationWindow
        self.title_label = ctk.CTkLabel(self.frame_top, text="Project Details", font=("", 20))
        self.title_label.grid(row=0, column=1, padx=10, pady=5)

        #Label to show project details
        self.label_project_details = ctk.CTkLabel(self.frame_top, text=self.get_project_details())
        self.label_project_details.grid(row=1, column=1, padx=5, pady=5)

    #Puts project details into a printable statement
    def get_project_details(self):
        details = database.get_project_details((self.project_id))
        details_report = "Project: {} | Status: {} | Creation Date: {} | Sample Count: {}".format(details[0], details[1], details[2], details[3])
        print(type(details[0]))         #Debugging
        print(type(details[1]))
        print(type(details[2]))
        print(type(details[3]))
        return details_report

#ProjectDetailsWindow configuration
class ResultEntryWindow(ctk.CTkToplevel):
    def __init__(self, parent, project_id):
        super().__init__(parent)

        self.project_id = project_id
        self.selected_option = ctk.StringVar(value=database.get_test_profile_tests_only(self.project_id)[0])

        #Page title creation and window size
        self.title("Result Entry")
        self.geometry("1000x750")

        #Set up the top frame of the page
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Set up the bottom frame of the page
        self.frame_middle = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_middle.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        #Set up the bottom frame of the page
        self.frame_bottom = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_bottom.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        #Logo creation and placement
        self.label_logo = ctk.CTkLabel(self.frame_top, text="", image=secondary_logo)
        self.label_logo.grid(row=0, column=0, padx=10, pady=10)

        #Title for the top of the ProjectCreationWindow
        self.title_label = ctk.CTkLabel(self.frame_top, text="Result Entry", font=("", 20))
        self.title_label.grid(row=0, column=1, padx=10, pady=5)

        #Label for test entry selection
        self.label_test_selection = ctk.CTkLabel(self.frame_middle, text="Select a test type for entry")
        self.label_test_selection.grid(row=0, column=0, padx=5, pady=5)

        #Dropdown for tests selection
        self.menu_tests = ctk.CTkOptionMenu(self.frame_middle, values=database.get_test_profile_tests_only(self.project_id), variable=self.selected_option)
        self.menu_tests.grid(row=0, column=1, padx=5, pady=5)

        #Button to submit selected test
        self.button_test_selection = ctk.CTkButton(self.frame_middle, text="Submit", command=lambda: entry_grid_setup(get_selected_option()))
        self.button_test_selection.grid(row=0, column=2, padx=5, pady=5)



        #Gets selected option from dropdown for test selection
        def get_selected_option():
            selected_option = self.selected_option.get()
            sql_test_value = functions.convert_to_sql_single_test(selected_option)
            return sql_test_value

        def entry_grid_setup(sql_test_value):
            #Clears frame when new test is selected for entry
            for widget in self.frame_bottom.winfo_children():
                widget.destroy()

            #Gets samples id and sample numbers from database and puts them into lists
            sample_id_list, sample_number_list = database.get_samples_to_enter(self.project_id, sql_test_value)
            current_row = 2

            #Label for the test type to be entered
            label_test_title = ctk.CTkLabel(self.frame_bottom, text=f"Test Entry For {self.selected_option.get()}")
            label_test_title.grid(row=0, column=0, padx=5, pady=5)

            #Label for the sample number header
            label_sample_number_header = ctk.CTkLabel(self.frame_bottom, text="Sample Number")
            label_sample_number_header.grid(row=1, column=0, padx=5, pady=5)

            #Label for the Test Result header
            label_test_header = ctk.CTkLabel(self.frame_bottom, text="Test Result")
            label_test_header.grid(row=1, column=1, padx=5, pady=5)

            #Creates a row with label and entry box for each sample
            for sample in sample_number_list:
                #Label for sample number
                label_sample_number = ctk.CTkLabel(self.frame_bottom, text=sample)
                label_sample_number.grid(row=current_row, column=0, padx=5, pady=5)

                #Entry box for test result
                entry_result = ctk.CTkEntry(self.frame_bottom)
                entry_result.grid(row=current_row, column=1, padx=5, pady=5)

                current_row += 1

#ProjectDetailsWindow configuration
class ResultReviewWindow(ctk.CTkToplevel):
    def __init__(self, parent, project_id):
        super().__init__(parent)

        self.project_id = project_id

        #Page title creation and window size
        self.title("Result Review")
        self.geometry("1000x750")

        #Set up the top frame of the page
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Set up the bottom frame of the page
        self.frame_middle = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_middle.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        #Set up the bottom frame of the page
        self.frame_bottom = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_bottom.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        #Logo creation and placement
        self.label_logo = ctk.CTkLabel(self.frame_top, text="", image=secondary_logo)
        self.label_logo.grid(row=0, column=0, padx=10, pady=10)

        #Title for the top of the ProjectCreationWindow
        self.title_label = ctk.CTkLabel(self.frame_top, text="Result Review", font=("", 20))
        self.title_label.grid(row=0, column=1, padx=10, pady=5)

#ProjectDetailsWindow configuration
class ProjectReportWindow(ctk.CTkToplevel):
    def __init__(self, parent, project_id):
        super().__init__(parent)

        self.project_id = project_id

        #Page title creation and window size
        self.title("Project Report")
        self.geometry("1000x750")

        #Set up the top frame of the page
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Set up the bottom frame of the page
        self.frame_middle = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_middle.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        #Set up the bottom frame of the page
        self.frame_bottom = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_bottom.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        #Logo creation and placement
        self.label_logo = ctk.CTkLabel(self.frame_top, text="", image=secondary_logo)
        self.label_logo.grid(row=0, column=0, padx=10, pady=10)

        #Title for the top of the ProjectCreationWindow
        self.title_label = ctk.CTkLabel(self.frame_top, text="Project Report", font=("", 20))
        self.title_label.grid(row=0, column=1, padx=10, pady=5)

#ProjectCreationWindow configuration
class ProjectCreationWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.test_window = None     #Set test_window to None

        self.sample_count = 0
        self.current_sample = 1
        self.test_results = {}
        self.project_number = database.get_current_project_number() + 1     #Set project_number to one more than most recently used number

        #Page title creation and window size
        self.title("Project Creation")
        self.geometry("1000x750")

        #Set up the top frame of the page
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        #Set up the bottom frame of the page
        self.frame_bottom = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_bottom.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        #Logo creation and placement
        self.label_logo = ctk.CTkLabel(self.frame_top, text="", image=secondary_logo)
        self.label_logo.grid(row=0, column=0, padx=10, pady=10)

        #Title for the top of the ProjectCreationWindow
        self.title_label = ctk.CTkLabel(self.frame_top, text="Project Creation", font=("", 20))
        self.title_label.grid(row=0, column=1, padx=10, pady=5)

        #Label with the prompt to enter number of samples
        self.label_prompt = ctk.CTkLabel(self.frame_top, text="Enter number of samples:")
        self.label_prompt.grid(row=1, column=1, padx=10, pady=5)

        #Entry box to get sample amount
        self.entry_sample_count = ctk.CTkEntry(self.frame_top, placeholder_text="Ex: 4")
        self.entry_sample_count.grid(row=1, column=2, padx=10, pady=5)

        #Empty label for error message
        self.label_result = ctk.CTkLabel(self.frame_top, text="")
        self.label_result.grid(row=2, column=1, padx=10, pady=5)

        #Button to submit the entry box. Runs get_sample_count to get entry value and start test entry
        self.button_sample_count_submit = ctk.CTkButton(self.frame_top, text="Submit", command=lambda: self.get_sample_count())
        self.button_sample_count_submit.grid(row=1, column=3, padx=5, pady=5)

        #Button to close the window
        # self.close_button = ctk.CTkButton(self, text="Close", command=self.destroy)
        # self.close_button.grid(row=3, column=1, padx=10, pady=5)

    #Validate the entry box input and initiate TestGrid for test entry
    def get_sample_count(self):
        count_string = self.entry_sample_count.get().strip()        #Clean entry
        # #If entry is a digit
        if count_string.isdigit():
            self.sample_count = int(count_string)       #Set sample_count to an int
            self.display_sample_row()       #Make a new row for he sample
        #Error if entry isn't an int
        else:
            self.label_result.configure(text="Invalid input. Please enter a number.", text_color="red")

    #Creates a row to select tests for a sample
    def display_sample_row(self):
        #If the current_sample is higher than the sample count, show the final submission button
        if self.current_sample > self.sample_count:
            self.show_final_submit()
            return

        # Display sample label
        label_sample_id = ctk.CTkLabel(self.frame_bottom, text=f"Sample {self.current_sample}")
        label_sample_id.grid(row=self.current_sample, column=0, padx=5, pady=5)

        # "+" Button to open test selection window
        button_add_test = ctk.CTkButton(self.frame_bottom, text="+",width=7, command=self.open_test_selection_window)
        button_add_test.grid(row=self.current_sample, column=1, padx=5, pady=5)

        # "Submit" Button to finalize sample
        button_submit = ctk.CTkButton(self.frame_bottom, text="Submit", command=self.finalize_sample)
        button_submit.grid(row=self.current_sample, column=2, padx=5, pady=5)

    #Open the test selection window
    def open_test_selection_window(self):
        #If the window doesn't exist, open the window and focus
        if self.test_window is None or not self.test_window.winfo_exists():
            self.test_window = TestSelectionWindow(self)  #Create new window
            self.test_window.grab_set()  #Make other pages unclickable
        #If the window already exists, focus it
        else:
            self.test_window.focus()

    #Compile the selected test for the sample and move to the next sample
    def finalize_sample(self):
        if self.current_sample in self.test_results and self.test_results[self.current_sample]:
            print(f'Sample {self.current_sample} tests: {self.test_results[self.current_sample]}')
            self.current_sample += 1
            self.display_sample_row()
        else:
            print("No test selected for this sample")

    #Store the selected tests
    def store_selected_tests(self, selected_tests):
        functions.store_selected_tests(self.test_results, self.current_sample, selected_tests)

    #Create and place the "Submit All" button
    def show_final_submit(self):
        button_final_submit = ctk.CTkButton(self.frame_bottom, text="Submit All", command=self.submit_project)
        button_final_submit.grid(row=self.current_sample + 1, column=2, padx=10, pady=5)

    #Gets test lists and submits the project and samples into the database
    def submit_project(self):
        processed_results = self.test_results
        #Debuggin statements
        print("Submission complete")
        print(f'Project: {self.project_number}, Tests selected: {processed_results}')
        print("Calling database method")
        #database.submit_project_creation(self.project_number, processed_results)               #COMMENTED TO AVOID COMMITS DURING TESTING
        print("Database method ran")
        #self.destroy()

#TestSelectionWindow configuration
class TestSelectionWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.selected_tests = []
        self.test_list = functions.set_test_list()
        self.checkbox_selection = {}

        #Title creation and window size
        self.title("Test Selection")
        self.geometry("1000x750")

        #Set up top frame of window
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        #Set up bottom frame of window
        self.frame_bottom = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_bottom.grid(row=1, column=0, padx=5, pady=5)

        #Logo creation and placement
        self.label_logo = ctk.CTkLabel(self.frame_top, text="", image=secondary_logo)
        self.label_logo.grid(row=0, column=0, padx=10, pady=10)

        #Title for top of TestSelectionWindow
        self.title_label = ctk.CTkLabel(self.frame_top, text="Test Selection", font=("", 20))
        self.title_label.grid(row=0, column=1, padx=10, pady=5)

        #Creates the grid of selectable tests
        self.generate_test_checkboxes(self.frame_bottom)

    def generate_test_checkboxes(self, frame):
        current_row = 0
        current_column = 0
        #Go through each test from the test list and creates a check box for each
        for index, test in enumerate(self.test_list):
            var = ctk.BooleanVar()  # Boolean variable to track checkbox state
            checkbox = ctk.CTkCheckBox(frame, text=test, variable=var)
            #Sets the max tests per row to be 5
            if current_column == 5:
                current_column = 0
                current_row += 1

            checkbox.grid(row=current_row + 1, column=current_column, padx=10, pady=2)

            current_column += 1

            #Stores the selected checkbox tests into a list
            self.checkbox_selection[test] = var  # Store reference to the variable

        #Creates a submit button after the test grid is created
        button_submit = ctk.CTkButton(self, text="Submit", command=self.submit_selected_tests)
        button_submit.grid(row=current_row + 1, column=0, padx=10, pady=5)

    #Confirm selected tests and destory the window
    def submit_selected_tests(self):
        for test, var in self.checkbox_selection.items():
            if var.get() == True:
                self.selected_tests.append(test)
        self.parent.store_selected_tests(self.selected_tests)
        self.destroy()
