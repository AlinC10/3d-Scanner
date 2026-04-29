# 3D Scanner Project

## Software

The logic of the system was implemented using C++ code (in Arduino IDE) and Python with multiple libraries.

*Note:* The GUI is currently in Romanian.

### Arduino

Arduino is responsible for how the scanner moves, scans the object and calculates the coordinates. The logic was created using OOP principles, creating different classes for different hardware components and handling their behavior inside the methods.

The classes created are:

* IR_Sensor:
  * getDistance(): was created using `SharpIR` library (by Giuseppe Masino) as a reference point. The problem with the already implemented one was that it only calculated the distance as an `int`, which was not useful for a system that tries to catch as many details as it can from an object. My implementation returns a `float` number, which represents the distance from the sensor to the object in millimeters. For a better value for the distance, the method makes multiple readings (10 by default) and returns the average distance.

* Endstop: checks if sensor reached bottom/upper part of the threaded rod
* Switch: checks if the power supply\switch is on
* Motor:
  * halfStepForward/Backwards(), fullStepForward/Backwards(): methods used to rotate motors forward/backwards in 2048 (with full step for threaded rod) or 4906 (with half step for turntable) depending on the needed precision.

Arduino code *only executes* if it receives a command from Python script, so it can't scan without Python script opened.

Variables used in the scanning process can be changed via Python script, in the `Opțiuni` menu from `Meniul Principal` without re-uploading the code (the settings changed will return to their values from Arduino code on the next launch) or via Arduino IDE (which means that the code needs to be re-uploaded).

### Python

The Python script acts as the "brain" of the operation on the PC side. It provides a Graphical User Interface (GUI), handles real-time communication with the microcontroller, and performs the complex 3D surface reconstruction. The entire logic is encapsulated in the ScannerApp class.

#### Features:
* **Serial Communication:** Utilizing the `pyserial` library (operating at a baud rate of `115200`), the script reads the incoming coordinates line by line and displays them in real-time. It also sends commands (START, STOP) and can dynamically update Arduino variables (like the number of measurements or sensor readings) without requiring the Arduino code to be recompiled or re-uploaded.
* **Data Management:** The raw coordinates are kept in memory and safely exported as an .xyz Point Cloud file. The script uses the pathlib library to automatically manage directories and save scans in dedicated folders based on user input.
* **Automated 3D Surface Reconstruction:** Once the scan is complete, the pymeshlab library is used to transform the raw .xyz points into a solid, 3D-printable .obj mesh

### How to run it

1. Setup Arduino

    1. Open `.\app_code\main\main.ino` in Arduino IDE.
    2. Check pins mapping for all hardware components.
    3. Upload code to Arduino.

2. Setup Python (3.11)
    1. Open terminal in `.\app_code\python`.
    2. Run `python -m venv .venv`
    3. Activate environment `.venv\Scripts\activate`
    4. Install libraries: `pip install -r requirements.txt`.
  
3. Install `MeshLab` to view the scanned object (optional, you can upload the `.xyz` in another app)

4. Connect Arduino, plug in the power supply and turn on the switch.

5. Run `3dScanner.exe` from `.\` or from terminal `python .\app_code\python\main.py`.

6. Press `Incepe scanarea` to start scanning.

7. After the scanning process, complete the name of the file in the pop-up window. For example, you can name the file `duck`, `my_favorite_duck`.

8. Click `Vizualizare obiect` to see the scanned object or choose `Meniu Principal` to go to the Main Menu. The file with scanned coordinates can be found in `.\scanari\your_object_name\your_object_name.xyz`.

### Future software updates

* create issues to better manage updates
* auto-search for arduino COM and baud-rate
* implement a ML algorithm to correct object coordinates
* migrate UI from Python Tkinter to a web based interface
* create a backend with python for sending information to the javascript frontend
