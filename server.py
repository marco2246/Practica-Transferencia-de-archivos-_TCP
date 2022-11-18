#   1    iMPOrtar libreria del sistema operativo, sockets y threading 
import os
import socket
import threading

# 2  asignaremos el nombre del host dinamicamente  
#la ventaja es que si se usa este codigo en otro programa no es necesario cambiar el host, esto se hará automaticamente
IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
# 7 vamos a crear la carpeta donde se almacenarán los archivos creados  
SERVER_DATA_PATH = "server_data" 

  #  8  hacer funcion del cliente para conectarlo al server 
def handle_client(conn, addr):
    print(f"[NUEVA CONEXION] {addr} Conectado.")

    #  9  utilizaremos este formato para comunicarnos con el servidor CMD@Msg 
    conn.send("OK@Bienvenido al servidor de archivos.".encode(FORMAT))

 # 10 abrimos el ciclo while esperando que el cliente mande el comando que desea ejecutar

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]
 # 11 si el comando es Listar vamos a listar los archivos que esten en la carpeta del servidor 
        if cmd == "LISTAR":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
 # 12 si no hay archivos mandar mensaje al usuario 

            if len(files) == 0:
               send_data += "El servidor está vacío"
            else:
 # 13 si todo está bien imprimir archivos uno por uno dando un salto de linea en cada uno 
                send_data += "\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))

 # 14 si el comando es CARGAR vamos a cargar el archivos que se seleccione 
        elif cmd == "CARGAR":
            name, text = data[1], data[2]
            filepath = os.path.join(SERVER_DATA_PATH, name)
            with open(filepath, "w") as f:
                f.write(text)

 # 15 si Avisamos al  cliente que su archivo fue cargado exitosamente 
            send_data = "OK@Archivo cargado exitosamente."
            conn.send(send_data.encode(FORMAT))
 # 15 si elige BORRAR  vamos a buscar en la lista el archivo que desea borrar
        elif cmd == "BORRAR":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            filename = data[1]
# 16 si está vacio  entonces que le avise al cliente 
            if len(files) == 0:
                send_data += "El servidor está vacío"
            else:   

                # si el archivo existe entonces lo va remover por medio de la libreria os
                if filename in files:
                    os.remove(f"{SERVER_DATA_PATH}/{filename}")
                    send_data += "Archivo borrado exitosamente."
                else:
                    send_data += "Archivo no encontrado."

            conn.send(send_data.encode(FORMAT))
#17  si manda el comando salir entonces vamos a terminar la sesion 
        elif cmd == "SALIR":
            break

        # 18 si elige el comando de ayuda entonces listamos las posibles opciones que tiene en la lista de  comandos 
        elif cmd == "AYUDA":
            data = "OK@"
            data += "LISTAR: Listar todos los archivos del servidor.\n"
            data += "CARGAR <path>: Cargar un archivo al servidor.\n"
            data += "BORRAR <filename>: Borrar archivo del servidor.\n"
            data += "SALIR: Disconnect from the server.\n"
            data += "AYUDA: Listar los comandos."

            conn.send(data.encode(FORMAT))
  # 19 al cerrar la sesión debemos avisarle al cliente y cerrar la conexion de el mismo.
    print(f"[DESCONECTADO] {addr} se a desconectado")
    conn.close()



# 3  hacemos la funcion principal  donde iniciamos el servidor 
def main():
    print("[INICIANDO] el servidor está iniciando")
  # 4  hacemos el servidor mediante sockets indicando af INET para ipv4 y SOCK_STREAM para tcp 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[ESCUCHANDO] Servidor escuchando en  {IP}:{PORT}.")
 # 5 Ciclo infinito de comunicación entre servidor y cliente
    while True:
        conn, addr = server.accept()
#  6 asignamos un hilo a cada cliente para que sea concurrente 
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[CONEXIONES ACTIVAS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()
