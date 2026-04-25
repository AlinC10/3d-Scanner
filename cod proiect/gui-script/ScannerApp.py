import time
import tkinter as tk
from tkinter import simpledialog, ttk
import serial
import threading
import pymeshlab as ml
from pathlib import Path


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

    def open_serial(self):
        self.arduino_ser = serial.Serial(self.com_port, self.baud_rate, timeout=1)
        time.sleep(2)  # wait 2 sec to let arduino reset

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

        try:
            self.open_serial()
        except serial.SerialException:
            print(serial.SerialException)

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
            btn.bind("<Return>", lambda event, b=btn: b.invoke())
            btns.append(btn)

        for i, btn in enumerate(btns):
            prev = i - 1 if i > 0 else len(btns) - 1
            next = i + 1 if i < len(btns) - 1 else 0
            btn.bind("<Down>", lambda event, n=next: btns[n].focus())
            btn.bind("<Up>", lambda event, p=prev: btns[p].focus())

        btns[0].focus()

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

            # self.__show_msg(f"Conectare la {self.com_port}", text_area)
            # self.arduino_ser = serial.Serial(self.com_port, self.baud_rate, timeout=1)
            # time.sleep(2)  # wait 2 sec to let arduino reset
            #
            # self.__show_msg("Conectat", text_area)

            self.arduino_ser.write(b"START\n")
            while self.is_scanning:
                # read line, decode from bytes to text and strip white spaces/ end line
                data = self.arduino_ser.readline().decode('utf-8').strip()

                if data:
                    if data == 'end':
                        self.__show_msg("Scanare termninata", text_area)
                        break

                    if data[0].isdigit() or data[1].isdigit():
                        coords_list.append(data)

                    self.__show_msg(data, text_area)

        except serial.SerialException:
            self.__show_msg(f"Nu s-a putut deschide portul {self.com_port}", text_area)
        except Exception as e:
            self.__show_msg(f"Eroare necunoscuta: {e}", text_area)

        finally:
            self.is_scanning = False
            # clean up after scanning
            if self.arduino_ser is not None and self.arduino_ser.is_open:
                self.arduino_ser.close()
                self.__show_msg("Port serial inchis", text_area)

            # enough points for an object
            if len(coords_list) > 50:
                self.root.after(0, lambda: self.__save_data_ui(coords_list, text_area))
            else:
                self.__show_msg("Au fost obtinute prea putine.", text_area)

    def __save_data_ui(self, coords_list, text_area):
        """UI for saving data"""
        # text file name input
        prompt = self.__prompt()

        if prompt:
            if '.' in prompt:
                prompt = prompt.split('.')[0]

        else:
            prompt = "coords"

        text_file_name = prompt + ".xyz"

        # create a new directory and add coords file to it
        folder_path = Path(prompt)
        folder_path.mkdir(parents=True, exist_ok=True)
        file_path = folder_path / text_file_name

        self.__show_msg(f"Numele fisierului este: {text_file_name}", text_area)

        with open(file_path, "w") as file:
            file.write("\n".join(coords_list))

        self.__show_msg(
            "Scanare finalizata. Apasati butonul de mai jos pentru a reveni la meniul principal sau a vizualiza obiectul.",
            text_area)

        btn_back = tk.Button(self.current_menu, text="Inapoi la meniul principal", command=self.main_menu)
        btn_back.pack(pady=10)

        btn_meshlab = tk.Button(self.current_menu, text="Vizualizare obiect",
                                command=lambda event=None, text_file_name=text_file_name: self.show_object(
                                    text_file_name), bg="lightgreen")
        btn_meshlab.pack(pady=10)

    def show_object(self, text_file_name):
        text_file_name = text_file_name.split(".")
        output_mesh = f".\\{text_file_name}\\{text_file_name}.obj"

        try:
            # create a MeshSet
            ms = ml.MeshSet()

            # load points
            ms.load_new_mesh(text_file_name)

            # calculate object norms
            ms.apply_filter('compute_normal_for_point_clouds', k=16, flipflag=False)

            # create object with Poisson algorithm
            ms.apply_filter('generate_surface_reconstruction_screened_poisson', depth=8, samplespernode=1.5,
                            pointweight=4)

            # delete points at z < 0 to clean meshlab object
            ms.apply_filter('compute_selection_by_condition_per_vertex', condselect="z < 0")
            ms.apply_filter('meshing_remove_selected_vertices')

            # close object base
            ms.apply_filter('meshing_close_holes', maxholesize=100000)

            # save object
            ms.save_current_mesh(output_mesh)

            # open MeshLab to see the object
            import os
            os.startfile(output_mesh)

        except Exception as e:
            print(e)

    def __prompt(self, title="Nume fisier", description="Cum se va numi fisierul?"):
        user_response = simpledialog.askstring(title, description)

        return user_response

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
        footer = tk.Label(self.current_menu, text="q - Anuleaza Scanarea. Inapoi la Meniul Principal")
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

    def close_app(self):
        self.root.destroy()

    def send_variable_to_arduino(self, info, var_name):
        value = self.__prompt(title=info["title"], description=info["description"])

        if self.arduino_ser and self.arduino_ser.is_open:
            if value and value.isdecimal():
                command = f"{var_name}:{value}"

                self.arduino_ser.write(command.encode("utf-8"))


    def scanning_options(self):
        self.create_frame("Setari scanner")

        menu_options = [
            {
                "var_name": "MEASSUREMENTS",
                "info": {
                    "title": "Numarul de masuratori pe o rotatie completa",
                    "description": "Cate masuratori se vor executa intr-o rotatie completa? (ex: 32, 64, 128, 256)"
                },
            },
            {
                "var_name": "ROTATIONS",
                "info": {
                    "title": "Numarul de scanari ale senzorului",
                    "description": "Cate scanari va realiza senzorul pentru a calcula un punct? (ex: 5, 8, 10 etc) "
                }
            },
        ]

        btns = []

        for option in menu_options[:2]:
            btn = tk.Button(self.current_menu, text=option["info"]["title"], command=lambda var_name=option["var_name"], info=option["info"]: self.send_variable_to_arduino(info, var_name))
            btn.pack(pady=10)
            btn.bind("<Return>", lambda event, b=btn: b.invoke())
            btns.append(btn)

        btns[0].focus()

        btn_back = tk.Button(self.current_menu, text="Inapoi la meniul principal", command=self.main_menu)
        btn_back.bind("<Return>", lambda event, b=btn_back: b.invoke())
        btn_back.pack(pady=10)
        btns.append(btn_back)

        for i, btn in enumerate(btns):
            prev = i - 1 if i > 0 else len(btns) - 1
            next = i + 1 if i < len(btns) - 1 else 0
            btn.bind("<Down>", lambda event, n=next: btns[n].focus())
            btn.bind("<Up>", lambda event, p=prev: btns[p].focus())