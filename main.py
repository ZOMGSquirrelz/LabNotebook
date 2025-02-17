import tkinter as tk
import customtkinter as ctk
import creation
import pyodbc
from PIL import Image


#Set theme and colors
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

#Logo image size for the main page
main_logo = ctk.CTkImage(light_image=Image.open('images/NotebookLogo.JPG'),
                    dark_image=Image.open('images/NotebookLogo.JPG'),
                    size=(150,200))

#Logo image sized for secondary pages to go in upper left corners
secondary_logo = ctk.CTkImage(light_image=Image.open('images/NotebookLogo.JPG'),
                    dark_image=Image.open('images/NotebookLogo.JPG'),
                    size=(60,80))

#Information needed to connect to SQL database
connection_string = """DRIVER={ODBC Driver 18 for SQL Server};
                    SERVER=127.0.0.1,1433;
                    DATABASE=LabNotebook;
                    UID=econard;
                    PWD=Freeze*6;
                    TrustServerCertificate=yes"""

#Class for creating a project creation window
class ProjectCreationWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()          #Inherit from ctk
        self.geometry("1000x750")   #Set window size
        self.label_logo = ctk.CTkLabel(self,                    #Create label for logo
                                       text="",                 #Empty text in label
                                       image=secondary_logo)    #Put image into label
        self.label_project_prompt = ctk.CTkLabel(self,
                                                 text="Create new project?")
        self.button_yes = ctk.CTkButton(self,
                                        text="Yes",
                                        command= self.display_project_number)
        self.button_no = ctk.CTkButton(self,
                                        text="No",
                                        command=self.close_page)
        # self.label_logo.pack(anchor='nw',           #Anchor label to top left of window
        #                      padx=5,                #X padding
        #                      pady=5)                #Y padding
        self.label_logo.grid(row=0, column=0, padx=10, pady=10)
        self.label_project_prompt.grid(row=0, column=1, padx=10, pady=10)
        self.button_yes.grid(row=0, column=2, padx=10, pady=10)
        self.button_no.grid(row=0, column=3, padx=10, pady=10)

    def display_project_number(self):
        self.label_test = ctk.CTkLabel(self, text="Project X has been created")
        self.label_test.grid(row=1, column=1, padx=10, pady=10)

    def close_page(self):
        ProjectCreationWindow.destroy(self)

with pyodbc.connect(connection_string) as conn:     #With statement for connection being open
    class App(ctk.CTk):         #Main app window
        def __init__(self):
            super().__init__()              #Inherit from ctk
            self.title("LabNotebook")       #Set window title
            self.geometry("1000x750")       #Set window size

            self.label_logo = ctk.CTkLabel(self,                #Create label for logo
                                           text="",             #Empty text in label
                                           image=main_logo)     #Put image in label
            self.label_logo.pack(pady=(0,10))       #Pack logo label
            #Testing abilities
            self.button_show_tests = ctk.CTkButton(self,                            #Create button to show tests
                                                   text="Show Test List",           #Button label
                                                   command=self.test_button_click)  #Command to display label of tests when clicked
            self.button_show_tests.pack(pady=20)        #Pack button

            self.button_open_proj_create = ctk.CTkButton(self,                          #Create button for project creation
                                                         text="New Project",            #Button label
                                                         command=self.open_proj_window) #Command to open project creation window when clicked
            self.button_open_proj_create.pack(pady=20)      #Pack button

            self.label_test_list = ctk.CTkLabel(self,           #Create empty label to display test list text
                                                text="")
            self.label_test_list.pack(pady=10)      #Pack label

            self.project_window = None      #Set project_window to None

        #Function to display test list
        def test_button_click(self):
            test_list = creation.display_test_list()        #Calls display_test_list function from creation.py
            self.label_test_list.configure(text=test_list)  #Updates label to display test list

        #Function to open a new window for project creation
        def open_proj_window(self):
            if self.project_window is None or not self.project_window.winfo_exists():   #If project_window doesn't exist
                self.project_window = ProjectCreationWindow()       #Creates a new window of class ProjectCreationWindow
                self.project_window.grab_set()                      #Make new window only clickable window
            else:           #If project_window exists
                self.project_window.focus()         #Focus on the project_window

    app = App()         #Creates app of class App
    app.mainloop()      #Loops the app