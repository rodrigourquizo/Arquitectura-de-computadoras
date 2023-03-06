from threading import Thread
import socket

SOCK_BUFFER = 1024

class Threading(Thread):    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def recibir_data(sock):
    return sock.recv(SOCK_BUFFER)

cant_costo_elevado = 0
cant_peso_mayor100_costo_elevado = 0
cant_costo_bajo = 0

def calcular(lista_datos):
    global cant_costo_elevado
    global cant_peso_mayor100_costo_elevado
    global cant_costo_bajo

    precio_unit = float(lista_datos[5])
    try:
        cant = int(lista_datos[3])
    except:
        cant = 0
    ct = precio_unit*cant
    costo = ''
    if (ct<25):
        costo = 'bajo'
        cant_costo_bajo += 1
    if(ct>=25 and ct<=49.9):
        costo = 'regular'
    if(ct>=50 and ct<=74.9):
        costo = 'alto'
    if(ct>=75):
        costo = 'elevado'
        cant_costo_elevado += 1
        peso = float(lista_datos[4])
        if(peso>100):
            cant_peso_mayor100_costo_elevado += 1
    
    print("Costo_total: ", ct )
    print("Clasificacion por costo: ", costo)
    print("Numero de componentes con costo elevado: ", cant_costo_elevado)
    print("Numero de componentes con costo elevado y peso>100g: ", cant_peso_mayor100_costo_elevado)
    print("Numero de componentes con costo bajo: ", cant_costo_bajo)

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 5000)
    print(f"Conectando al servidor en {server_address[0]} y puerto {server_address[1]}")
    sock.connect(server_address)
    try:
        while True:                                    
            t1 = Threading(target = recibir_data, args = (sock,))
            t1.start()
            data = t1.join()
            if data:
                data_decoded = data.decode('utf-8')
                lista_datos = (data_decoded.split(";"))[0:6]
                #print(lista_datos)
                #print(f"Informacion solicitada:\n {data_decoded}\n")
                t2 = Threading(target = calcular, args = (lista_datos,))
                t2.start()
                t2.join()
                

    finally:
        print("Cerrando socket")
        sock.close()
