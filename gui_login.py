import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
import re
import webbrowser

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, switch_to_main_callback):
        super().__init__(master, fg_color="#040404")
        self.master = master
        self.switch_to_main = switch_to_main_callback
        self.build_ui()

    def build_ui(self):
        self.label = ctk.CTkLabel(self, text="Welcome to Login", font=("Arial", 33, "bold"))
        self.label.pack(pady=40)

        self.entry_email = ctk.CTkEntry(self, placeholder_text="Email...", width=300, height=33)
        self.entry_email.pack(pady=10)

        self.entry_password = ctk.CTkEntry(self, placeholder_text="Password...", width=300, height=33, show="*")
        self.entry_password.pack(pady=10)

        self.button_login = ctk.CTkButton(self, text="Login", command=self.validate_login)
        self.button_login.pack(pady=20)

    def is_valid_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email)

    def validate_login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()

        if not self.is_valid_email(email):
            CTkMessagebox(title="Error", message="Not a valid Email")
        elif password == "":
            CTkMessagebox(title="Error", message="Plz put Password")
        else:
            self.switch_to_main()

class MainAppFrame(ctk.CTkFrame):
    def __init__(self, master, logout_callback):
        super().__init__(master)
        self.master = master
        self.logout_callback = logout_callback
        self.build_ui()

    def build_ui(self):
        self.label = ctk.CTkLabel(self, text="Welcome to Main App", font=("Arial", 28, "bold"))
        self.label.pack(pady=40)

        self.dashboard_btn = ctk.CTkButton(self, text="Go to Dashboard", command=self.open_dashboard)
        self.dashboard_btn.pack(pady=10)

        self.logout_btn = ctk.CTkButton(self, text="Logout", command=self.logout_callback)
        self.logout_btn.pack(pady=10)

    def open_dashboard(self):
        webbrowser.open("https://www.youtube.com")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Secure App with Frame Switch")
        self.geometry("800x600")

        self.login_frame = LoginFrame(self, self.show_main_frame)
        self.main_frame = MainAppFrame(self, self.show_login_frame)

        self.login_frame.pack(fill="both", expand=True)

    def show_main_frame(self):
        self.login_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)

    def show_login_frame(self):
        self.main_frame.pack_forget()
        self.login_frame.entry_password.delete(0, 'end')
        self.login_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()



import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk
import re

from gui_main import Appmain
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("App")
        self.resizable(False, False)
        self.after(10, self.state, 'zoomed')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        

        # เปิดภาพและใช้ CTkImage พร้อมระบุ size
        self.bkMain_sky = Image.open("gui\\bkmain1.png")
        self.show_sky_bg = ctk.CTkImage(light_image=self.bkMain_sky, size=(screen_width, screen_height))

        # ใช้ place แทน pack และขนาดภาพจะพอดีกับหน้าจอ
        self.imgbgmain = ctk.CTkLabel(self, text="", image=self.show_sky_bg)
        self.imgbgmain.place(x=0, y=0, relwidth=1, relheight=1)  # เต็มหน้าจอ
        self.imgbgmain.lower()  # ส่งภาพไปอยู่ข้างหลัง

        self.bkmain = ctk.CTkFrame(self, width=1600, height=700, fg_color="#040404")
        self.bkmain.place(relx=0.5, rely=0.5, anchor="center")

        self.bkmain22 = ctk.CTkFrame(self.bkmain, width=800, height=700, fg_color="#040404")
        self.bkmain22.place(relx=0, rely=0.5, anchor="w")

        self.bkmain_input = ctk.CTkFrame(self.bkmain, width=800, height=700, fg_color="#040404")
        self.bkmain_input.place(relx=1, rely=0.35, anchor="e")

        self.image1_Let = Image.open("gui\\img2.png")
        self.showimg = ctk.CTkImage(light_image=self.image1_Let, size=(770, 670))

        self.bkmain_img = ctk.CTkLabel(self.bkmain22, image=self.showimg, text="")
        self.bkmain_img.image1_Let = self.showimg
        self.bkmain_img.place(relx=0.5, rely=0.5, anchor="center")

        self.label1 = ctk.CTkLabel(
            master=self.bkmain_input,
            text="Welcome to Login",
            text_color="white",
            corner_radius=8,
            font=("Arial", 33, "bold")
        )
        self.label1.place(relx=0.5, rely=0.5, anchor="center")

        self.entry1 = ctk.CTkEntry(
            master=self.bkmain_input,
            placeholder_text="Email...",
            width=300,
            height=33,
            border_width=3,
            corner_radius=10,
        )
        self.entry1.place(relx=0.5, rely=0.6, anchor="n")

        self.entry2 = ctk.CTkEntry(
            master=self.bkmain_input,
            placeholder_text="Password...",
            width=300,
            height=33,
            border_width=3,
            corner_radius=10,
            show="*"
        )
        self.entry2.place(relx=0.5, rely=0.7, anchor="n")

        self.button1 = ctk.CTkButton(
            master=self.bkmain_input,
            text="Login",
            command=self.ConnfigT,
            font=("Arial", 20),
        )
        self.button1.place(relx=0.5, rely=0.8, anchor="n")

    def is_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email)

    def show_error_not_email(self):
        email = self.entry1.get()
        password = self.entry2.get()
        if self.is_email(email):
            CTkMessagebox(title="Info", message="Valid Email")
        elif password == "":
            CTkMessagebox(title="Error", message="Plz put Password")
        else:
            CTkMessagebox(title="Error", message="Not a valid Email")

    def ConnfigT(self):
        if self.show_error_not_email():
            self.after(100, self.open_appmain)

    def open_appmain(self):
        from gui_main import Appmain
        self.destroy()
        app = Appmain()
        app.mainloop()


if __name__ == "__main__":
    mainapp = App()
    mainapp.mainloop()

from asyncio import sleep
import customtkinter as ctk
from CTkMenuBar import *
import cv2
from PIL import Image , ImageTk
import webbrowser
import sys
import subprocess
import os



class Appmain(ctk.CTk):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Camala sy => pro")
        self.resizable(False,False)
        self.after(100, lambda: self.state('zoomed'))
        
        self.screen_app_width = self.winfo_screenwidth()
        x_off = self.screen_app_width // 2
        self.menu = CTkTitleMenu(master=self , x_offset=x_off)
        self.MenuMain()
        self.MenuUser()
        
    def MenuMain(self):
        self.file_menu = self.menu.add_cascade("Menu")
        self.dropdown = CustomDropdownMenu(widget=self.file_menu)
        self.dropdown.add_option(option="New" ,command=lambda :print("New clicked"))
        self.dropdown.add_option(option="Check" ,command=lambda :print("New clicked"))
        self.dropdown.add_option(option="Dashboard",command=lambda : webbrowser.open("https://www.youtube.com"))
        self.dropdown.add_separator()
        self.dropdown.add_option(option="Exit" , command=self.quit)
    
    def MenuUser(self):
        self.file_menu = self.menu.add_cascade("User")
        self.dropdown = CustomDropdownMenu(widget=self.file_menu)
        self.dropdown.add_option(option="Profile",command=lambda : webbrowser.open("https://www.youtube.com"))
        self.dropdown.add_separator()
        self.dropdown.add_option(option="Logout" , command=self.end_main_gui )
        self.dropdown.add_option(option="Exit" , command=self.quit)
        
    def end_main_gui(self):
        self.quit()
        self.destroy()
        script_path = os.path.join("gui", "gui_login.py")
        subprocess.Popen([sys.executable, script_path])
        sys.exit()
        
if __name__ == "__main__":
    mainapp = Appmain()
    mainapp.mainloop()
