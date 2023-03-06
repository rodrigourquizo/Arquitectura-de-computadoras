from threading import Thread
import csv 
import socket
import time

def leer():
    file = open('PartesDeElectrónica.csv', 'r',encoding='latin')
    reader = csv.reader(file)
    next(reader)
    return reader

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

t1 = Threading(target = leer, args = ())
t1.start()
reader = t1.join()

filas = [] #aca tengo todas las filas en listas
for i in reader:
    string = ''.join(i) 
    #lista = string.split(';')
    filas.append(str(string)) 

def enviar_datos(conn):
    for msg in filas:
        print(msg)
        time.sleep(1)
        conn.sendall(msg.encode('utf-8'))


if __name__ == '__main__':
    SOCK_BUFFER = 1024
    # Creamos el objeto de socket para el servidor
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 5000)
    print(f"Iniciando el servidor en la direccion {server_address[0]} y puerto {server_address[1]}")
    sock.bind(server_address)
    sock.listen(5)

    while True:
        print("Esperando conexiones...")
        conn, client_address = sock.accept()
        try:
            print(f"Conexion establecida con {client_address}")
            i = 0    
            t2 = Threading(target = enviar_datos, args = (conn,))
            t2.start()
            t2.join()
            
        except ConnectionResetError:
            print("Conexion cerrada por el cliente abruptamente")
        finally:
            print("El cliente ha cerrado la conexion")
            conn.close()

