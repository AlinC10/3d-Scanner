from menu import ScannerApp
import tkinter as tk

port_serial = 'COM13'
baud_rate = 115200

root = tk.Tk()
app = ScannerApp(root)
root.mainloop()