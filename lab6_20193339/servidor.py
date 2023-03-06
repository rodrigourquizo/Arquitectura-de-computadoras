from statistics import mode, median, mean, stdev  
import socket

SOCK_BUFFER = 1024
#ITEM B
file = open('Lab6_viernes.csv', 'r') #Lectura del csv
horas_list = []
fuel_types = []
brands = []
kilometers = []

#Obtengo las horas, los tipos de combustible, las marcas y los km recorridos en listas
#Para luego poder hallar los datos requeridos en los demas items
for id,line in enumerate(file): 
    fechas = line.split(',')[0]
    fechas = fechas.split(' ')

    fuel = line.split(',')[13]
    if fuel != 'fuelType':
      fuel_types.append(fuel)

    brand = line.split(',')[14]
    if brand != 'brand':  
      brands.append(brand)

    km = line.split(',')[11]
    try: 
      kilometers.append(int(km))
    except:
      pass

    if(fechas[0] != 'dateCrawled'):    
        try:
            hora = (fechas[1].split(':'))[0] #Uso el bloque try except para que ignore la linea del archivo donde esta el error
            horas_list.append(hora)
        except:
            continue
#ITEM C    
hora_moda = mode(horas_list) #Moda de la hora
item_c = 'Hora del día en la que se recolecta más datos: ' + str(hora_moda) + '\n'

#ITEM D
fuel_stats = {} #Numero de autos por tipo de combustible
for item in fuel_types:
   if(item != 'fuelType' and item!=''):
    if item in fuel_stats:
       fuel_stats[item] += 1
    else:
       fuel_stats[item] = 1

fuel_cant = len(fuel_stats) #Numero de tipos de combustible
fuel_mode = mode(fuel_types) #Combustible mas popular
item_d ='Tipos de combustible: '+ str(fuel_cant) +  '\n' +"Cuántos autos consumen cada tipo: " + str(fuel_stats) + '\n' + 'Combustible mas popular: '+ str(fuel_mode) + '\n'

#ITEM E
brand_stats = {} #Numero de autos por marca 
for item in brands:
   if(item != 'brand' and item!=''):
    if item in brand_stats:
      brand_stats[item] += 1
    else:
      brand_stats[item] = 1

brands_cant = len(brand_stats) #Numero de marcas
item_e = 'Número de marcas: '+ str(brands_cant) + '\n'+ 'Numero de autos por marca: ' + str(brand_stats) + '\n'

#ITEM F
#Kilometros recorridos
mean_km = mean(kilometers) #media
media_km = median(kilometers) #mediana
mode_km = mode(kilometers) #moda
stdev_km = stdev(kilometers) #desviacion estandar
item_f = f"Kilometros recorridos:\nMedia: {mean_km}'\nMediana: {media_km}\nModa: {mode_km}\nDesviacion estandar: {stdev_km}\n" 

#print(item_c)
#print(item_d)
#print(item_e)
#print(item_f)

if __name__ == '__main__':
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

            while True:
                data = conn.recv(SOCK_BUFFER)
                data_conv = data.decode('utf-8')
                #Recibimos las palabras clave: hora, combustible, marcas, kilometros y mandamos la informacion requerida
                if data_conv == 'hora': 
                    print(f"Solicita item c ")
                    conn.sendall(item_c.encode('utf-8'))
                elif data_conv == 'combustible':
                    print(f"Solicita item d ")
                    conn.sendall(item_d.encode('utf-8'))
                elif data_conv == 'marcas':
                    print(f"Solicita item e ")
                    conn.sendall(item_e.encode('utf-8'))
                elif data_conv == 'kilometros':
                    print(f"Solicita item f ")
                    conn.sendall(item_f.encode('utf-8'))
                elif data_conv == 'cerrar sesion': #Si recibimos el mensaje cerrar sesion:
                    msj = "Cerrando sesion"
                    print(msj)
                    f= open("lab_06_reporte.txt","w") #Generamos el archivo con el reporte 
                    f.write('Resumen items c,d,e,f:\n')
                    f.write("Item_c:\n")
                    f.write(item_c)
                    f.write("Item_d:\n")
                    f.write(item_d)
                    f.write("Item_e:\n")
                    f.write(item_e)
                    f.write("Item_f:\n")
                    f.write(item_f)
                    conn.sendall(msj.encode('utf-8'))
                else:
                    break
        except ConnectionResetError:
            print("Conexion cerrada por el cliente abruptamente")
        finally:
            print("El cliente ha cerrado la conexion")
            conn.close()