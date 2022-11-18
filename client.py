#20 cargamos la libreria de sockets para conectarnos al server
import socket
 # 21 obtener el host de manera dinamica, el host y el ip deben ser los mismos que en el server 
IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def main():
    # 22 iniciamos conexion tcp por ipv4
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

# 23 hacemos un ciclo para que el cliente eliga comandos
    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")
# 24 si elige desconectado   va a terminar sesión
        if cmd == "DESCONECTADO":
            print(f"[SERVER]: {msg}")
            break
 # 25 si la conexion está bien entonces que mande el mensaje utilizando > como indicador de escritura
        elif cmd == "OK":
            print(f"{msg}")

        data = input("> ")
        data = data.split(" ")
        cmd = data[0]
# 26 si elige ayuda el cliente que lo conecte a ayuda del server
        if cmd == "AYUDA":
            client.send(cmd.encode(FORMAT))
            # 27 si elige SALIR el cliente que lo conecte a SALIR del server
        elif cmd == "SALIR":
            client.send(cmd.encode(FORMAT))
            break
    # 28 si elige LISTAR el cliente que lo conecte a LISTAR del server

        elif cmd == "LISTAR":
            client.send(cmd.encode(FORMAT))
# 29 si elige BORRAR el cliente que lo conecte a BORRAR del server

        elif cmd == "BORRAR":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))
     # 30 si elige CARGAR el cliente que lo conecte a CARGAR del server
        elif cmd == "CARGAR":
            path = data[1]
     # 31 si elige CARGAR el cliente que lo conecte a CARGAR del server
  # cargamos el neuvo archivo 
            with open(f"{path}", "r") as f:
                text = f.read()
                # ajustamos el formato 
            filename = path.split("/")[-1]
            send_data = f"{cmd}@{filename}@{text}"
            client.send(send_data.encode(FORMAT))

# si eligio salir, cerramos la sesión del cliente 
    print("Se ah desconectado del servidor.")
    client.close()

if __name__ == "__main__":
    main()
