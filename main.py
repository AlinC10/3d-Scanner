from ScannerApp import ScannerApp
import tkinter as tk


root = tk.Tk()
app = ScannerApp(root)
app.show_object("./coords.xyz")
# root.mainloop()