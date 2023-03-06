import socket

SOCK_BUFFER = 1024

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 5002)
    print(f"Conectando al servidor en {server_address[0]} y puerto {server_address[1]}")
    sock.connect(server_address)

    try:
        msg = input("Nombre: ") #En los casos de prueba emplee la funcion input                                    
        msg = msg.encode('utf-8')
        sock.sendall(msg)
        data = sock.recv(SOCK_BUFFER)

        if(data.decode('utf-8') == "Procesando data"): #Recibimos la confirmacion del servidor
            while True:
                msg = input("Palabra clave: ") #En los casos de prueba emplee la funcion input                                    
                msg = msg.encode('utf-8')
                sock.sendall(msg)
                data = sock.recv(SOCK_BUFFER)
                print(f"Informacion solicitada:\n {data.decode('utf-8')}")

    finally:
        print("Cerrando socket")
        sock.close()