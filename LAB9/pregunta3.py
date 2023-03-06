from socket import AF_INET, SOCK_DGRAM
import datetime
import socket
import struct
from threading import Thread
import time
from datetime import timedelta

servidores_ntp = [
    "0.uk.pool.ntp.org",    # Londres(Reino Unido)
    "1.es.pool.ntp.org",    # Madrid (España)
    "0.us.pool.ntp.org",    # Nueva York(Estados Unidos)
    "0.hk.pool.ntp.org",    # Hong Kong
    "0.jp.pool.ntp.org"     # Tokyo(Japón)
]

"""
Función: get_ntp_time
Descripción: Imprime la  fecha-hora actual en un país determinado
Entrada: Cualquiera de las URLs definidas en la lista servidores_ntp
Salida: Retorna la fecha-hora(timestamp) en formato datetime.datetime, también la imprime
IMPORTANTE: NO modifique esta funcion 
"""
def get_ntp_time(host):
    timezone_dict = {'uk': ['UK', 0 * 3600], 'es': ['España', 1 * 3600],
                     'hk': ['Hong Kong', 8 * 3600], 'jp': ['Japón', 9 * 3600],
                     'us': ['Estados Unidos', -5*3600]}
    key = ''
    port = 123
    buf = 1024
    address = (host, port)
    msg = b'\x1b' + 47 * b'\0'

    # reference time (in seconds since 1900-01-01 00:00:00)
    TIME1970 = 2208988800  # 1970-01-01 00:00:00
    # connect to server
    client = socket.socket(AF_INET, SOCK_DGRAM)
    client.sendto(msg, address)
    msg, address = client.recvfrom(buf)
    t = struct.unpack("!12I", msg)[10]
    t -= TIME1970
    client.close()

    for each_key in timezone_dict:
        if each_key in host:
            key = each_key
            break
    print(f"Hora en {timezone_dict[key][0]}: {datetime.datetime.utcfromtimestamp(t + timezone_dict[key][1])}")
    return datetime.datetime.utcfromtimestamp(t + timezone_dict[key][1])


if __name__ == "__main__":
    #a)Funcion para hallar el pais mas proximo a abrir sin hilos
    paises = ['Reino Unido', 'Espana', 'Estados Unidos', 'China', 'Japon']
    def calcular_pais_proximo_a_abrir_sinThread():
        for server, pais in zip(servidores_ntp, paises):
            fecha = get_ntp_time(server)                                                    #Existen dos casos:         
            ocho_am_hoy = datetime.datetime(fecha.year,fecha.month,fecha.day,8,0,0)         #cuando abre a las 8 am de ese dia(todavia no son las 8 am)
            ocho_am_manana = ocho_am_hoy + timedelta(days=1)                                #cuando abre a las 8 am del sgte dia(ya nos pasamos de las 8 am)
            if fecha<=ocho_am_hoy:                                                          #si aun no son las 8m o son las 8 am, la hora de apertura es ese dia a las 8 am
                hora_apertura = ocho_am_hoy 
            else:
                hora_apertura = ocho_am_manana                                              #si son mas de las 8am, la hora de apertura es al dia siguiente a las 8 am
            diferencia = hora_apertura - fecha
            print('Falta: ', diferencia)                                                    #imprimo el tiempo que falta para abrir en cada pais
            if pais == 'Reino Unido' or diferencia<menor_diferencia:                        #uso el primer pais como referencia, cuando el tiempo que tomara en abrir es menor al tiempo menor actualizo los valores
                menor_diferencia = diferencia
                pais_proximo_a_abrir = pais
    
        return pais_proximo_a_abrir
    print("Ejecucion sin hilos")
    ti = time.perf_counter()                                                                #calculo de tiempo de ejecucion
    pais = calcular_pais_proximo_a_abrir_sinThread()
    to = time.perf_counter()
    print('El pais mas proximo a abrir es:', pais)
    print('El tiempo de ejecucion sin Thread es: ', to-ti, 's\n')

    #b)Uso hilos para cada elemento de la lista servidores_ntp
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

    def calcular_tiempo_para_abrir(server):
        fecha = get_ntp_time(server)                                                    #Existen dos casos: 
        ocho_am_hoy = datetime.datetime(fecha.year,fecha.month,fecha.day,8,0,0)         #cuando abre a las 8 am de ese dia(todavia no son las 8 am)
        ocho_am_manana = ocho_am_hoy + timedelta(days=1)                                #cuando abre a las 8 am del sgte dia(ya nos pasamos de las 8 am)
        if fecha<=ocho_am_hoy:                                                          #si aun no son las 8m o son las 8am, la hora de apertura es ese dia a las 8 am
            hora_apertura = ocho_am_hoy
        else:
            hora_apertura = ocho_am_manana                                              #si son mas de las 8am, la hora de apertura es al dia siguiente a las 8 am
        diferencia = hora_apertura - fecha
        print('Falta: ', diferencia)
        return diferencia

    def calcular_pais_proximo_a_abrir_conThread():
        hilos = []
        for server in servidores_ntp:
            hilo = Threading(target = calcular_tiempo_para_abrir, args = (server,)) #con cada hilo calculo el tiempo que tomara en abrir cada bolsa
            hilos.append(hilo)

        for hilo in hilos:
            hilo.start()                                                            #inicio los hilos

        for hilo, pais in zip(hilos, paises):
            tiempo = hilo.join()
            if pais == 'Reino Unido' or tiempo<tiempo_menor:                        #uso el primer pais como referencia, cuando el tiempo que tomara en abrir es menor al tiempo menor actualizo los valores
                tiempo_menor = tiempo
                pais_proximo_abrir = pais 
        return pais_proximo_abrir
        
    print("Ejecucion con hilos")
    ti = time.perf_counter()                                                        #calculo de tiempo de ejecucion
    pais = calcular_pais_proximo_a_abrir_conThread()
    to = time.perf_counter()
    
    print('El pais mas proximo a abrir es:', pais)
    print('El tiempo de ejecucion con Thread es: ', to-ti, 's')


    
