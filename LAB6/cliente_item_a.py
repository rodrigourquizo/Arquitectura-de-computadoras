import socket


SOCK_BUFFER = 1024

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 5001)
    print(f"Conectando al servidor en {server_address[0]} y puerto {server_address[1]}")

    sock.connect(server_address)
    intentos = 0
    try:
        while True:   
            #msg = input("Ingresa el codigo: ")     #Se ingresa el codigo con el formato: usuario_contraseña
                                                    #Con la entrada por terminal realice la demostracion ya que se simulan mejor los intentos                            
            
            msg = 'pepe_19992929'                   #Se usa una variable como se indico en el lab  
            msg = msg.encode('utf-8')                   
            sock.sendall(msg)                       #Mandamos el codigo 
            data = sock.recv(SOCK_BUFFER)           #Recibimos la validacion del servidor
            data_conv = data.decode('utf-8')    
            print(f"Recibido : {data_conv}")
            if(data_conv == "Datos correctos"):
                break

            if(data_conv == "Datos incorrectos"):   #Si no se valida la contrasena se recibe el mensaje Datos incorrectos
                print("Rechazando comunicacion")
                intentos +=1
            if intentos == 3:
                print("Cerrando socket")            #Si llegamos a los 3 intentos cerramos el socket 
                break
    finally:
        
        sock.close()