import time
import tkinter as tk
from tkinter import simpledialog, ttk
import serial
import threading
import pymeshlab as ml

class ScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicatie Scanner 3D")
        self.root.geometry("1024x720")
        self.current_menu = None

        self.com_port = 'COM13'
        self.baud_rate = 115200

        self.arduino_ser = None
        self.is_scanning = False

        self.home_screen()

    def clear(self):
        if self.current_menu is not None:
            self.current_menu.destroy()

        self.current_menu = None

    def create_frame(self, title):
        self.clear()

        # create frame and config to show information
        self.current_menu = ttk.Frame(self.root, padding=20)
        self.current_menu.pack(fill="both", expand=True)
        ttk.Label(self.current_menu, text=title).pack(pady=10)

    def home_screen(self):
        self.create_frame("Bine ati venit!")

        self.root.after(2000, self.main_menu)

    def main_menu(self):
        self.create_frame("Meniul Principal")

        menu_options = [
            {
                "name": "Incepe scanarea",
                "action": self.scan_ui
            },
            {
                "name": "Optiuni",
                "action": self.scanning_options
            },
            {
                "name": "Inchide aplicatia",
                "action": self.close_app
            }
        ]

        btns = []
        for option in menu_options:
            btn = tk.Button(self.current_menu, text=option["name"], command=option["action"])
            btn.pack(pady=10)
            btn.bind("<Return>", lambda event, b = btn: b.invoke())
            btns.append(btn)

        for i, btn in enumerate(btns):
            prev = i - 1 if i > 0 else len(btns) - 1
            next = i + 1 if i < len(btns) - 1 else 0
            btn.bind("<Down>", lambda event, n=next: btns[n].focus())
            btn.bind("<Up>", lambda event, p=prev: btns[p].focus())

        btns[0].focus()

    def scan_ui(self):
        def cancel_scan(event=None):
            """Close scan if user pressed <q>"""
            self.is_scanning = False

            if self.arduino_ser and self.arduino_ser.is_open:
                try:
                    self.arduino_ser.write(b"STOP\n")
                    print("Comanda STOP trimisa catre Arduino")
                except:
                    self.__show_msg("Eroare la transmiterea comenzii de oprire catre Arduino", text)

            self.__show_msg("Scanare anulata!", text)
            self.root.unbind("<q>")
            self.main_menu()

        self.create_frame("Scanare")

        # Footer
        footer = tk.Label(self.current_menu, text="q - Anuleaza Scanarea. Inapoi la Meniul Principal" )
        footer.pack(side="bottom", fill="x")

        self.root.bind("<q>", cancel_scan)

        # Scanned Points Area
        text_area_frame = tk.Frame(self.current_menu)
        text_area_frame.pack(fill="both", expand=True)

        # Scroll bar for Scanned Points Area
        scroll = tk.Scrollbar(text_area_frame, orient="vertical")
        scroll.pack(side="right", fill="y")

        text = tk.Text(text_area_frame, yscrollcommand=scroll.set)
        text.pack(side="left", fill="both", expand=True)

        scroll.config(command=text.yview)

        # Start second thread
        self.is_scanning = True
        threading.Thread(target=self.__scanning, args=(text,), daemon=True).start()

    def __show_msg(self, text_msg, text_area):
        def update_ui():
            if text_area.winfo_exists():
                text_area.insert(tk.END, text_msg)
                if not text_msg.endswith("\n"):
                    text_area.insert(tk.END, "\n")
                text_area.see(tk.END)

        self.root.after(0, update_ui)

    def __scanning(self, text_area):
        coords_list = []
        try:

            self.__show_msg(f"Conectare la {self.com_port}", text_area)
            self.arduino_ser = serial.Serial(self.com_port, self.baud_rate, timeout=1)
            time.sleep(2)  # wait 2 sec to let arduino reset

            self.__show_msg("Conectat", text_area)

            self.arduino_ser.write(b"START\n")
            while self.is_scanning:
                # read line, decode from bytes to text and strip white spaces/ end line
                data = self.arduino_ser.readline().decode('utf-8').strip()

                if data == 'end':
                    self.__show_msg("Scanare termninata", text_area)
                    break

                if ',' in data:
                    coords_list.append(data)

                if data:
                    self.__show_msg(data, text_area)

        except serial.SerialException:
            self.__show_msg(f"Nu s-a putut deschide portul {self.com_port}", text_area)
        except Exception as e:
            self.__show_msg(f"Eroare necunoscuta: {e}", text_area)

        finally:
            self.is_scanning = False
            # clean-ul fter scanning
            if self.arduino_ser is not None and self.arduino_ser.is_open:
                self.arduino_ser.close()
                self.__show_msg("Port serial inchis", text_area)

            # enough points for an object
            if len(coords_list) > 50:
                self.root.after(0, self.__save_data_ui, coords_list, text_area)
            else:
                self.__show_msg("Au fost obtinute prea putine.", text_area)

    def __save_data_ui(self, coords_list, text_area):
        """UI for saving data"""
        # text file name input
        prompt = self.__prompt().split(".")[0]
        if prompt:
            text_file_name = f"./{prompt}.xyz"
        else:
            text_file_name = "../dist/coords.xyz"

        self.__show_msg(f"Numele fisierului este: {text_file_name}", text_area)

        text_file = open(text_file_name, "w")
        text_file.write("\n".join(coords_list))
        text_file.flush()
        text_file.close()
        self.__show_msg("Scanare finalizata. Apasati butonul de mai jos pentru a reveni la meniul principal sau a vizualiza obiectul.", text_area)

        btn_back = tk.Button(self.current_menu, text="Inapoi la meniul principal", command=self.main_menu)
        btn_back.pack(pady=10)

        btn_mashlab = tk.Button(self.current_menu, text="Vizualizare obiect", command=lambda event=None, text_file_name=text_file_name: self.show_object(text_file_name), bg="lightgreen")
        btn_mashlab.pack(pady=10)



    def show_object(self, text_file_name):
        output_mesh = '.\\' + text_file_name[2:].split(".")[0] + '.obj'

        try:
            # create a MeshSet
            ms = ml.MeshSet()

            # load points
            ms.load_new_mesh(text_file_name)

            # calculate norm
            ms.apply_filter('compute_normal_for_point_clouds', k=16)

            # create object with Poisson algorithm
            ms.apply_filter('generate_surface_reconstruction_screened_poisson', depth=8)

            # save object
            ms.save_current_mesh(output_mesh)

            # open MeshLab to see the object
            import os
            os.startfile(output_mesh)

        except Exception as e:
            print(e)


    def __prompt(self):
        user_response = simpledialog.askstring("Nume fisier", "Cum se va numi fisierul?")

        return user_response

    def close_app(self):
        self.root.destroy()

    def scanning_options(self):
        pass