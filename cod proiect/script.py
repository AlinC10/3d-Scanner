import serial, time
import numpy as np
import open3d as o3d

def read_serial(comport, baudrate):
    coords_list = []

    print(f"Conectare la {comport}")
    arduino_ser = serial.Serial(comport, baudrate, timeout=1)
    time.sleep(2) # wait 2 sec to let arduino reset

    print("Conectat")
    try:
        while True:
            # read line, decode from bytes to text and strip white spaces/ end line
            data = arduino_ser.readline().decode('utf-8').strip()

            if data == 'end':
                print("Scanare termninata")

                if 'arduino_ser' in locals() and arduino_ser.is_open:
                    arduino_ser.close()
                    print("Port serial inchis")

                break

            if data:
                coords = [float(x) for x in data.split(',')]
                coords_list.append(coords)
                print(data)
                # text_file.write(data + '\n')
                # text_file.flush()

    except Exception:
        print("Eroare")

    finally:
        if 'arduino_ser' in locals() and arduino_ser.is_open:
            arduino_ser.close()
            print("Port serial inchis")

    return coords_list

def scan():
    coords_list = read_serial(port_serial, baud_rate)

    if len(coords_list) < 10:
        print("Prea putine puncte")
        return

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(np.array(coords_list))

    print("Salvare coordonate")
    o3d.io.write_point_cloud("./coords.xyz", pcd)

    # clear noise
    print("Curatare zgomot puncte")
    pcd, ind = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)

    # surface calculation
    print("Generare obiect")
    pcd.estimate_normals()
    pcd.orient_normals_consistent_tangent_plane(100)
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)

    # export in .stl
    o3d.io.write_triangle_mesh('object.stl', mesh)
    print("Fisier .stl generat.")

    print("Deschidere vizualizare obiect")
    o3d.visualization.draw_geometries([mesh], window_name="Vizualizare obiect", width=800, height=600)


port_serial = 'COM13'
baud_rate = 115200
scan()