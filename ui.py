import customtkinter as ctk
from PIL import Image

import functions

# Logo images
main_logo = ctk.CTkImage(light_image=Image.open('images/NotebookLogo.JPG'),
                          dark_image=Image.open('images/NotebookLogo.JPG'),
                          size=(150, 200))

secondary_logo = ctk.CTkImage(light_image=Image.open('images/NotebookLogo.JPG'),
                              dark_image=Image.open('images/NotebookLogo.JPG'),
                              size=(60, 80))

class MainPage(ctk.CTkFrame):
    """Main page with navigation options."""
    def __init__(self, parent):
        super().__init__(parent)

        self.label_logo = ctk.CTkLabel(self, image=main_logo, text="")
        self.label_logo.pack(pady=10)

        self.test_button = ctk.CTkButton(self, text="Show Test List", command=self.show_tests)
        self.test_button.pack(pady=5)

        self.create_project_button = ctk.CTkButton(self, text="New Project",
                                                   command=self.open_project_window)
        self.create_project_button.pack(pady=5)

        self.label_test_list = ctk.CTkLabel(self, text="")
        self.label_test_list.pack(pady=5)

        self.project_window = None  # Store reference to the project window

    def show_tests(self):
        """Displays test list fetched from the database."""
        test_list = functions.set_test_list()
        #test_list = get_test_list()
        self.label_test_list.configure(text=test_list)

    def open_project_window(self):
        """Opens the Project Creation Window if not already open."""
        if self.project_window is None or not self.project_window.winfo_exists():
            self.project_window = ProjectCreationWindow(self)  # Create new window
            self.project_window.grab_set()  # Makes it modal (prevents clicking main window)
        else:
            self.project_window.focus()  # If already open, bring it to front

class ProjectCreationWindow(ctk.CTkToplevel):
    """Project creation in a separate window."""
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Project Creation")
        self.geometry("1000x750")

        self.grid_columnconfigure(0, weight=1)

        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.frame_bottom = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_bottom.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.label_logo = ctk.CTkLabel(self.frame_top, text="", image=secondary_logo)
        self.label_logo.grid(row=0, column=0, padx=10, pady=10)

        self.title_label = ctk.CTkLabel(self.frame_top, text="Project Creation", font=("", 20))
        self.title_label.grid(row=0, column=1, padx=10, pady=5)

        self.prompt_label = ctk.CTkLabel(self.frame_top, text="Enter number of samples:")
        self.prompt_label.grid(row=1, column=1, padx=10, pady=5)

        self.entry_sample_count = ctk.CTkEntry(self.frame_top, placeholder_text="Ex: 4")
        self.entry_sample_count.grid(row=1, column=2, padx=10, pady=5)

        self.result_label = ctk.CTkLabel(self.frame_top, text="")
        self.result_label.grid(row=2, column=1, padx=10, pady=5)

        self.button_sample_count_submit = ctk.CTkButton(self.frame_top, text="Submit", command=lambda: self.get_sample_count())
        self.button_sample_count_submit.grid(row=1, column=3, padx=5, pady=5)



        # self.close_button = ctk.CTkButton(self, text="Close", command=self.destroy)
        # self.close_button.grid(row=3, column=1, padx=10, pady=5)

    def get_sample_count(self, event=None):
        """Validates sample input and updates UI."""
        count_string = self.entry_sample_count.get().strip()
        if count_string.isdigit():
            sample_count = int(count_string)
            functions.TestGrid(self.frame_bottom, sample_count)
        else:
            self.result_label.configure(text="Invalid input. Please enter a number.", text_color="red")
