import socket

SOCK_BUFFER = 1024

if __name__ == '__main__':
    intentos = 0 #Numero de intentos
    # Creamos el objeto de socket para el servidor
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 5001)
    print(f"Iniciando el servidor en la direccion {server_address[0]} y puerto {server_address[1]}")
    sock.bind(server_address)

    # Escuchamos conexiones
    sock.listen(5)

    # Empezamos bucle de servidor
    while True:
        print("Esperando conexiones...")
        conn, client_address = sock.accept()
        try:
            print(f"Conexion establecida con {client_address}")
            usuario= 'jose'
            contrasena= '20018823'
            codigo_correcto = f"{usuario}_{contrasena}" #Definimos el codigo correcto a partir de las variables indicadas
            
            while True:
                data = conn.recv(SOCK_BUFFER)
                if data:
                    data_conv = data.decode('utf-8')
                    print(f"Recibi {data} de {client_address}")

                    if (data_conv == codigo_correcto): #Validamos que la data recibida sea igual al codigo correcto
                        msg = "Datos correctos"        #con el mensaje Datos correctos
                        print(f"{msg} , intentos: {intentos}")
                        conn.sendall(msg.encode('utf-8'))
                        break
                    else:
                        intentos += 1                  #Si se recibe un codigo incorrecto entonces aumentamos el numero de intentos 
                        msg = "Datos incorrectos"
                        print(f"{msg} , intentos: {intentos}")   
                        conn.sendall(msg.encode('utf-8'))
                        if(intentos ==3):              #Si la cantidad de intentos llega a 3 salimos del bucle 
                            break
                else:
                    break
        finally:
            if(intentos == 3): #Si llegamos a 3 intentos salimos del bucle principal y terminamos el programa en el servidor                          
                conn.close() 
                break
            print("Se ha cerrado la conexion")
            conn.close()