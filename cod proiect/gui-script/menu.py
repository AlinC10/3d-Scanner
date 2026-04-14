import time
import tkinter as tk
from tkinter import ttk

class ScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicatie Scanner 3D")
        self.root.geometry("500x500")
        self.current_menu = None

        self.home_screen()

    def clear(self):
        if self.current_menu is not None:
            self.current_menu.destroy()

        self.current_menu = None

    def home_screen(self):
        self.current_menu = ttk.Frame(self.root, padding=20)
        self.current_menu.pack(fill="both", expand=True)
        ttk.Label(self.current_menu, text="Bine ati venit!").pack(pady=10)
        time.sleep(2)
        self.clear()
        self.main_menu()

    def main_menu(self):
        self.clear()

        # create frame and config to show information
        self.current_menu = ttk.Frame(self.root, padding=20)
        self.current_menu.pack(fill="both", expand=True)

        ttk.Label(self.current_menu, text="MENIU PRINCIPAL").pack(pady=20)

        menu_options = [
            {
                "name": "Incepe scanarea",
                "action": start_scanning
            },
            {
                "name": "Optiuni",
                "action": scanning_options
            },
            {
                "name": "Inchide aplicatia",
                "action": close_app
            }
        ]

        btns = []
        for option in menu_options:
            btn = tk.Button(self.current_menu, text=option["name"], command=option["action"])
            btn.pack(pady=10)
            btn.bind("<Return>", lambda event: option["action"])
            btns.append(btn)

        for i, btn in enumerate(btns):
            prev = i - 1 if i > 0 else len(btns) - 1
            next = i + 1 if i < len(btns) - 1 else 0
            btn.bind("<Down>", lambda event, n=next: btns[n].focus())
            btn.bind("<Up>", lambda event, p=prev: btns[p].focus())

        btns[0].focus()


def start_scanning():
    pass

def scanning_options():
    pass

def close_app():
    pass


root = tk.Tk()
app = ScannerApp(root)
root.mainloop()