from typing import Tuple

import customtkinter as CTk


class App(CTk.CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.withdraw()
        self.window = Window(master=self)

    def new_window(self):
        self.window.destroy()
        self.window = Window(master=self)


class Window(CTk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master=master)
        self.geometry("200x80")

        button = CTk.CTkButton(
            master=self,
            text="destroy",
            command=lambda: self.master.new_window(),
        )
        button.pack(padx=25, pady=25)

        self.protocol("WM_DELETE_WINDOW", self.master.destroy)


if __name__ == "__main__":
    app = App()
    app.mainloop()