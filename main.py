import customtkinter as ctk
from ui import MainPage

class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LabNotebook")
        self.geometry("1000x750")

        self.main_page = MainPage(self)
        self.main_page.pack(fill="both", expand=True)

if __name__ == "__main__":

    app = MyApp()
    app.mainloop()
