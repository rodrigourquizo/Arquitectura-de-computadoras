import socket

SOCK_BUFFER = 1024

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 5001)
    print(f"Conectando al servidor en {server_address[0]} y puerto {server_address[1]}")
    sock.connect(server_address)

    try:
        while True:
            #Aca enviamos el mensaje con lo que solicitamos, ingresando las palabras clave:
            # hora: ítem c
            # combustible: ítem d
            # marcas: ítem e
            # kilómetros: ítem f
            #cerrar sesion: item h
            
            #msg = input("Palabra clave: ") #En los casos de prueba emplee la funcion input
            msg = "hora" #Se solicito que el mensaje sea en codigo, por eso implemente el mensaje como variable                                    
            msg = msg.encode('utf-8')
            print(f"logitud del mensaje: {len(msg)} bytes")
            sock.sendall(msg)
            data = sock.recv(SOCK_BUFFER)
            if(data.decode('utf-8') == 'Cerrando sesion'): #Recibimos la confirmacion del servidor para cerrar sesion
                break
            print(f"Informacion solicitada:\n {data.decode('utf-8')}")

    finally:
        print("Cerrando socket")
        sock.close()