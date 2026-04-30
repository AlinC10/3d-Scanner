import time
import tkinter as tk
from tkinter import simpledialog, ttk, messagebox
import serial
import threading
import pymeshlab as ml
from pathlib import Path
from ComPort import get_com_port


class ScannerApp:
    """Class used to manage user interface (UI) and the interaction with the Arduino for the 3d scanner.
        This class contains the information about UI resolution, serial port and baud rate used.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Aplicatie Scanner 3D")
        self.root.geometry("1024x720")
        self.current_menu = None

        self.com_port = None
        self.baud_rate = 115200

        self.arduino_ser = None
        self.is_scanning = False

        self.home_screen()

    def clear(self):
        """Function for clearing current window."""
        if self.current_menu is not None:
            self.current_menu.destroy()

        self.current_menu = None

    def open_serial(self):
        """Function for opening serial port for interaction with Arduino."""
        self.arduino_ser = serial.Serial(self.com_port, self.baud_rate, timeout=1)
        time.sleep(2)  # wait 2 sec to let arduino reset

    def create_frame(self, title):
        """Function for creating a new page for the UI."""
        self.clear()

        # create frame and config to show information
        self.current_menu = ttk.Frame(self.root, padding=20)
        self.current_menu.pack(fill="both", expand=True)
        ttk.Label(self.current_menu, text=title).pack(pady=10)

    def home_screen(self):
        """App's page with a \"Welcome!\" message."""
        self.create_frame("Bine ati venit!")

        self.com_port = get_com_port()

        def retry_connection():
            self.com_port = get_com_port()
            if self.com_port is not None:
                self.root.after(0, self.home_screen)

        if self.com_port is None:
            btn = tk.Button(self.current_menu, text="Cauta portul serial din nou", command=retry_connection)
            btn.pack(pady=10)
        else:
            self.root.after(2000, self.main_menu)

    def main_menu(self):
        """Main menu page, used for navigation in the app.
            The options available in the menu are:
            - start scan
            - scanner settings
            - exit application
        """
        self.create_frame("Meniul Principal")

        try:
            self.open_serial()
        except serial.SerialException:
            messagebox.showerror("Eroare Port Serial", serial.SerialException)

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

        ScannerApp.__bind_keyboard_arrows(btns)

        btns[0].focus()

    def __show_msg(self, text_msg, text_area):
        """Function to print messages to the UI in a text box.
            Used for printing scanned coordinates, current level of the sensor and messages to let user know what is
            happening with the scanning.
        """

        def update_ui():
            if text_area.winfo_exists():
                text_area.insert(tk.END, text_msg)
                if not text_msg.endswith("\n"):
                    text_area.insert(tk.END, "\n")
                text_area.see(tk.END)

        self.root.after(0, update_ui)

    def __scanning(self, text_area):
        """Scanning function.
            It receives the coordinates from the Arduino ,and it call __show_msg() method for printing the information.
            It also closes the serial communication and saves the file with coordinates through __save_data_ui().
        """

        coords_list = []
        try:
            self.arduino_ser.write(b"START\n")
            while self.is_scanning:
                # read line, decode from bytes to text and strip white spaces/ end line
                data = self.arduino_ser.readline().decode('utf-8').strip()

                if data:
                    # check information received through serial to see if they are coordinates or an information
                    # message for the user.
                    if data == 'end':
                        self.__show_msg("Scanare terminata", text_area)
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
        """UI for saving data that gives an option to see the object model."""
        # text file name input
        prompt = self.__prompt()

        if prompt:
            if '.' in prompt:
                prompt = prompt.split('.')[0]

        else:
            prompt = "coords"

        text_file_name = prompt + ".xyz"

        # create a new directory and add coords file to it
        folder_path = Path("scanari") / Path(prompt)
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
        """Function that creates object model using PyMeshLab library.
            It uses some filters from the library to create the object from the coordinates obtain during scanning
            and opens the MeshLab app for visualization.
        """
        text_file_name = text_file_name.split(".")[0]
        path = f".\\scanari\\{text_file_name}\\{text_file_name}.xyz"
        output_mesh = f".\\scanari\\{text_file_name}\\{text_file_name}.obj"

        try:
            # create a MeshSet
            ms = ml.MeshSet()

            # load points
            ms.load_new_mesh(path)

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

            # smooth object surface
            ms.apply_filter('apply_coord_taubin_smoothing', stepsmoothnum=10)

            # save object
            ms.save_current_mesh(output_mesh)

            # save in .stl format
            ms.save_current_mesh(output_mesh[:-3] + 'stl')

            # open MeshLab to see the object
            import os
            os.startfile(output_mesh)

        except Exception as e:
            print(e)

    def __prompt(self, title="Nume fisier", description="Cum se va numi fisierul?"):
        """Prompt window for asking user different questions.
            For example: name of the file that will be saved, variables values
        """
        user_response = simpledialog.askstring(title, description)

        return user_response

    def scan_ui(self):
        """It creates the UI for the scanning process where users can see the information received from microcontroller.
            It uses 2 threads:
            - one for __scanning() method
            - one to listen to <q> bind and cancel the scan if that's the user intention
        """
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

        # Start second thread for the scanning.
        self.is_scanning = True
        threading.Thread(target=self.__scanning, args=(text,), daemon=True).start()

    def close_app(self):
        """Close the app window"""
        self.root.destroy()

    def send_variable_to_arduino(self, info, var_name):
        """Change variables values from Arduino, if the user wants it."""
        value = self.__prompt(title=info["title"], description=info["description"])

        if self.arduino_ser and self.arduino_ser.is_open:
            if value and value.isdecimal():
                command = f"{var_name}:{value}"

                self.arduino_ser.write(command.encode("utf-8"))

    def scanning_options(self):
        """Scanning options menu.
            It has 2 variables that can be changed:
            - rotation step of the turntable in a 360 degrees rotation
            - number of sensor readings for one step (it calculates an average for the coordinates)

            And an option to go back to main menu.
        """
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
            btn = tk.Button(self.current_menu, text=option["info"]["title"], command=lambda var_name=option["var_name"],
                                                                                            info=option[
                                                                                                "info"]: self.send_variable_to_arduino(
                info, var_name))
            btn.pack(pady=10)
            btn.bind("<Return>", lambda event, b=btn: b.invoke())
            btns.append(btn)

        btns[0].focus()

        btn_back = tk.Button(self.current_menu, text="Inapoi la meniul principal", command=self.main_menu)
        btn_back.bind("<Return>", lambda event, b=btn_back: b.invoke())
        btn_back.pack(pady=10)
        btns.append(btn_back)

        ScannerApp.__bind_keyboard_arrows(btns)

    @staticmethod
    def __bind_keyboard_arrows(btns):
        """Bind keyboard up and down arrows to GUI buttons."""
        for i, btn in enumerate(btns):
            prev = i - 1 if i > 0 else len(btns) - 1
            next = i + 1 if i < len(btns) - 1 else 0
            btn.bind("<Down>", lambda event, n=next: btns[n].focus())
            btn.bind("<Up>", lambda event, p=prev: btns[p].focus())
