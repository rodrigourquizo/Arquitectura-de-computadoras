import csv 
import pprint
import random
import asyncio
import time
import socket

#a)lectura del archivo
file = open('players_viernes.csv', 'r',encoding='utf-8')
reader = csv.reader(file)
next(reader)

jugadores = {}

#b)Listas de 5 jugadores con el valor mas alto de minutos jugados
for x in reader:
    equipo = x[4]
    if equipo not in jugadores: #si el equipo no esta entonces genera una lista vacia para llenar
        jugadores[equipo] = []
    try:
        jugador_min = ( x[3], float(x[6]) )
        jugadores[equipo].append(jugador_min) #agregamos la tupla (jugador, minutos jugados) por equipo
    except:
        pass

cinco_primeros = {}

for pais, players in jugadores.items():
    lista_ordenada = sorted(players, key=lambda x: x[1],reverse=True)[0:5] #ordenamos la lista de tuplas por la cantidad de minutos jugados y obtenemos los 5 primeros
    cinco_primeros[pais] = [x for x,y in lista_ordenada] 

#c)Hallo la funcion que me da el ganador de cada encuentro

pts_prom = {} #diccionario donde almacenare los puntajes promedios

file_ = open('players_viernes.csv', 'r',encoding='utf-8')
reader = csv.reader(file_)
next(reader) #saltamos el header

for x in reader:
    pts = int(x[21]) #columna PTS
    if x[4] not in pts_prom:
        pts_prom[x[4]] = [0,0]   
    pts_prom[x[4]][0] += pts #suma de puntajes
    pts_prom[x[4]][1] += 1 #contador

for x,y in pts_prom.items(): #Con esto obtengo los promedios de puntajes por equipo
    pts_prom[x] = y[0] / y[1] #prom = suma/numero de elementos

async def partido(tipo_de_partido,lista_equipos):
    equipo1 = lista_equipos[0]
    equipo2 = lista_equipos[1]

    if tipo_de_partido == 'grupos': #Si el tipo de partido corresponde a una fase de grupos, el ganador se determina por el mayor puntaje promedio
        pts1_avg = pts_prom[equipo1] #obtengo los promedios
        pts2_avg = pts_prom[equipo2]
        
        if(pts1_avg>pts2_avg): #comparo los promedios y saco el ganador
            ganador = equipo1 
        else:
            ganador = equipo2
    else: #Si no, corresponde a una eliminatoria y el ganador se determina de forma aleatoria
        ganador = random.choice([equipo1, equipo2])
    await asyncio.sleep(0.15) #sleep de 0.15 s
    return ganador 


def partido_sinc(tipo_de_partido,lista_equipos):
    equipo1 = lista_equipos[0]
    equipo2 = lista_equipos[1]

    if tipo_de_partido == 'grupos': #Si el tipo de partido corresponde a una fase de grupos, el ganador se determina por el mayor puntaje promedio
        pts1_avg = pts_prom[equipo1] #obtengo los promedios
        pts2_avg = pts_prom[equipo2]
        
        if(pts1_avg>pts2_avg): #comparo los promedios y saco el ganador
            ganador = equipo1 
        else:
            ganador = equipo2
    else: #Si no, corresponde a una eliminatoria y el ganador se determina de forma aleatoria
        ganador = random.choice([equipo1, equipo2])
    time.sleep(0.15) #sleep de 0.15 s
    return ganador 

#d) Fase de grupos (asincrono)
grupo_A = ['ATL', 'BOS', 'BRK', 'CHA']
grupo_B = ['DAL', 'DEN', 'DET', 'GSW']
grupo_C = ['LAC', 'LAL', 'MEM', 'MIA']
grupo_D = ['NOP', 'NYK', 'OKC', 'ORL']
grupo_E = ['POR', 'SAC', 'SAS', 'SEA']
grupo_F = ['WAS', 'CHI', 'CLE', 'UTA']
grupo_G = ['HOU', 'IND', 'MIL', 'MIN']
grupo_H = ['PHI', 'PHX', 'TOR', 'BOL']


async def ganadores(grupo, fase):
    l = await asyncio.gather(partido(fase, [grupo[0], grupo[1]]),partido(fase, [grupo[0], grupo[2]]),partido(fase, [grupo[0], grupo[3]]), partido(fase, [grupo[1], grupo[2]]),partido(fase, [grupo[1], grupo[3]]), partido(fase, [grupo[2], grupo[3]]) )
    puntajes = [(l.count(x),x) for x in set(l)]
    ptjs_ordenados = sorted(puntajes, key=lambda x: x[0],reverse=True)
    ganadores = [y for x,y in ptjs_ordenados][0:2] #Agregamos los 2 con puntaje mas alto en la lista
    return ganadores

async def grupos_async():
    equipos  = await asyncio.gather(ganadores(grupo_A, 'grupos'),ganadores(grupo_B,'grupos' ), ganadores(grupo_C,'grupos' ), ganadores(grupo_D,'grupos' ),
    ganadores(grupo_E,'grupos' ), ganadores(grupo_F,'grupos' ), ganadores(grupo_G,'grupos' ),ganadores(grupo_H,'grupos' ))
    #Segunda ronda                                                      Se enfrentan los 2 primeros lugares de los grupos:
    grupoI = [equipos[0][0], equipos[0][1],equipos[1][0],equipos[1][1]] #A B
    grupoJ = [equipos[2][0], equipos[2][1],equipos[3][0],equipos[3][1]] #C D
    grupoK = [equipos[4][0], equipos[4][1],equipos[5][0],equipos[5][1]] #E F
    grupoL = [equipos[6][0], equipos[6][1],equipos[7][0],equipos[7][1]] #G H
    return await asyncio.gather(ganadores(grupoI, 'grupos'),ganadores(grupoJ, 'grupos'), ganadores(grupoK, 'grupos'), ganadores(grupoL, 'grupos') ) 


#e)fase de grupos(sincrono)
def ganadores_sinc(grupo,fase):
    l = [partido_sinc(fase, [grupo[0], grupo[1]]),partido_sinc(fase, [grupo[0], grupo[2]]),partido_sinc(fase, [grupo[0], grupo[3]]), partido_sinc(fase, [grupo[1], grupo[2]]),partido_sinc(fase, [grupo[1], grupo[3]]), partido_sinc(fase, [grupo[2], grupo[3]])]     
    puntajes = [(l.count(x),x) for x in set(l)]
    ptjs_ordenados = sorted(puntajes, key=lambda x: x[0],reverse=True) #ordeno los equipos por partidos ganados
    ganadores = [y for x,y in ptjs_ordenados][0:2] #Agregamos los 2 con puntaje mas alto en la lista
    return ganadores

def grupos_sync():
    #primera ronda
    ga = ganadores_sinc(grupo_A,'grupos')
    gb = ganadores_sinc(grupo_B,'grupos')
    gc = ganadores_sinc(grupo_C,'grupos')
    gd = ganadores_sinc(grupo_D,'grupos')
    ge = ganadores_sinc(grupo_E,'grupos')
    gf = ganadores_sinc(grupo_F,'grupos')
    gg = ganadores_sinc(grupo_G,'grupos')
    gh = ganadores_sinc(grupo_H,'grupos')
    equipos = [ga,gb,gc,gd,ge,gf,gg,gh]
    #segunda ronda
    grupoI = [equipos[0][0], equipos[0][1],equipos[1][0],equipos[1][1]]
    grupoJ = [equipos[2][0], equipos[2][1],equipos[3][0],equipos[3][1]]
    grupoK = [equipos[4][0], equipos[4][1],equipos[5][0],equipos[5][1]]
    grupoL = [equipos[6][0], equipos[6][1],equipos[7][0],equipos[7][1]]
    gi = ganadores_sinc(grupoI, 'grupos')
    gj = ganadores_sinc(grupoJ, 'grupos')
    gk = ganadores_sinc(grupoK, 'grupos')
    gl = ganadores_sinc(grupoL, 'grupos')
    return [gi,gj,gk,gl]


#f)Eliminatorias (asincrono)
clasificados_async = asyncio.run(grupos_async()) #clasificados
async def eliminatorias_async():  
    gi = clasificados_async[0]
    gj = clasificados_async[1]
    gk = clasificados_async[2]
    gl = clasificados_async[3]

    print(gi,gj,gk,gl)
    
    #cuartos de final
    gcf = await asyncio.gather(partido('e', [gi[0], gj[1]]), partido('e', [gk[0], gl[1]]), partido('e', [gj[0], gi[1]]), partido('e', [gl[0], gk[1]]) )
    g1c = gcf[0]
    g2c = gcf[1]
    g3c = gcf[2]
    g4c = gcf[3]

    print(g1c,g2c,g3c,g4c)

    #semis
    gs = await asyncio.gather(partido('e', [g1c, g2c]), partido('e', [g3c, g4c]))
    g1s = gs[0]
    perd1 = [x for x in [g1c, g2c] if x != g1s][0]
    g2s = gs[1]
    perd2 = [x for x in [g3c, g4c] if x != g2s][0]

    print(g1s,g2s)
    
    #final
    ganador = (await asyncio.gather(partido('e', [g1s, g2s])))[0]
    segundo_lugar = [x for x in [g1s, g2s] if x!=ganador][0]

    #tercer lugar
    tercer_lugar = (await asyncio.gather(partido('e', [perd1, perd2])))[0]

    podio_async = [ganador, segundo_lugar, tercer_lugar]
    print(podio_async)
    return podio_async

#g) Eliminatorias (sincrono)
clasificados_sync = grupos_sync()
def eliminatorias_sync():
    #ganadores segunda ronda
    gi = clasificados_sync[0]
    gj = clasificados_sync[1]
    gk = clasificados_sync[2]
    gl = clasificados_sync[3]

    print(gi,gj,gk,gl)
    
    #cuartos de final
    g1c = partido_sinc('e', [gi[0], gj[1]])
    g2c = partido_sinc('e', [gk[0], gl[1]])
    g3c = partido_sinc('e', [gj[0], gi[1]])
    g4c = partido_sinc('e', [gl[0], gk[1]])
    
    print(g1c,g2c,g3c,g4c)

    #semis
    g1s = partido_sinc('e', [g1c, g2c])
    perd1 = [x for x in [g1c, g2c] if x != g1s][0]

    g2s = partido_sinc('e', [g3c, g4c])
    perd2 = [x for x in [g3c, g4c] if x != g2s][0]

    print(g1s,g2s)
    
    #final
    ganador = partido_sinc('e', [g1s, g2s])
    segundo_lugar = [x for x in [g1s, g2s] if x!=ganador][0]
    tercer_lugar = partido_sinc('e', [perd1, perd2])

    podio_sync = [ganador, segundo_lugar, tercer_lugar]
    print(podio_sync)
    return podio_sync

if __name__ == '__main__':
    SOCK_BUFFER = 1024
    # Creamos el objeto de socket para el servidor
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 5002)
    print(f"Iniciando el servidor en la direccion {server_address[0]} y puerto {server_address[1]}")
    sock.bind(server_address)
    sock.listen(5)

    while True:
        print("Esperando conexiones...")
        conn, client_address = sock.accept()
        try:
            print(f"Conexion establecida con {client_address}")
            data = conn.recv(SOCK_BUFFER)
            data_conv = data.decode('utf-8')
            if data:
                msg = "Procesando data" #Mensaje de confirmacion
                print(msg)
                conn.sendall(msg.encode('utf-8'))    
                while True:
                    data = conn.recv(SOCK_BUFFER)
                    data_conv = data.decode('utf-8')    

                    if data_conv =="equipos":
                        listas_b  = cinco_primeros
                        pprint.pprint(listas_b)

                    if data_conv =="fase de grupos asincrono":
                        clasificados_async = asyncio.run(grupos_async())
                        msg  = ' '.join([' '.join(x) for x in clasificados_async])
                        conn.sendall(msg.encode('utf-8'))

                    if data_conv == "fase de grupos sincrono":
                        clasificados_sync = grupos_sync()
                        msg  = ' '.join([' '.join(x) for x in clasificados_sync])
                        conn.sendall(msg.encode('utf-8'))
    
                    if data_conv == 'eliminatorias asincrono':
                        podio_async = asyncio.run(eliminatorias_async())
                        msg  = ' '.join(podio_async)
                        conn.sendall(msg.encode('utf-8'))

                    if data_conv == 'eliminatorias sincrono':
                        podio_sync = eliminatorias_sync()
                        msg  = ' '.join(podio_sync)
                        conn.sendall(msg.encode('utf-8'))

                    if data_conv == 'reporte':
                        texto = "Items d) y e) - Fase de grupos: \n"
                        ti = time.perf_counter()
                        clasificados_async = asyncio.run(grupos_async())
                        to = time.perf_counter()
                        t1 = to-ti
                        texto += "Lista de clasificados(async)\n" + ' '.join([' '.join(x) for x in clasificados_async]) + '\n' + 'Tiempo de ejecucion: ' + str(t1) + ' s\n\n' 

                        ti = time.perf_counter()
                        clasificados_sync = grupos_sync()
                        to = time.perf_counter()
                        texto += "Lista de clasificados(sync)\n" + ' '.join([' '.join(x) for x in clasificados_sync]) + '\n' + 'Tiempo de ejecucion: ' + str(to-ti) + ' s\n\n'
                        t2= to-ti
                        #Comparo los tiempos de ejecucion
                        if t1<t2:
                            texto += "En la funcion grupos el tiempo de ejecucion asincrono es menor que el tiempo de ejecucion sincrono\n\n" 
                        else:
                            texto += "En la funcion grupos el tiempo de ejecucion asincrono es mayor que el tiempo de ejecucion sincrono\n\n" 

                        texto += "Items f) y g) - Eliminatorias:\n"
                        ti = time.perf_counter()
                        podio_async = asyncio.run(eliminatorias_async())
                        to = time.perf_counter()
                        t1 = to-ti
                        texto += "Podio(async): 1er lugar, 2do lugar, 3er lugar\n" + ' '.join(podio_async) + '\n' + 'Tiempo de ejecucion: ' + str(t1) + ' s' + "\n\n"
                        
                        ti = time.perf_counter()
                        podio_sync = eliminatorias_sync()
                        to = time.perf_counter()
                        t2=to-ti
                        texto += "Podio(sync): 1er lugar, 2do lugar, 3er lugar\n" + ' '.join(podio_sync) + '\n' + 'Tiempo de ejecucion: ' + str(t2) + ' s' + "\n\n"
                        #Comparo los tiempos de ejecucion
                        if t1<t2:
                            texto += "En la funcion eliminatorias el tiempo de ejecucion asincrono es menor que el tiempo de ejecucion sincrono\n\n" 
                        else:
                            texto += "En la funcion eliminatorias el tiempo de ejecucion asincrono es mayor que el tiempo de ejecucion sincrono\n\n" 

                        f= open("reporte.txt","w")
                        f.write(texto)
                        conn.sendall('Generando reporte'.encode('utf-8'))
                    
        except ConnectionResetError:
            print("Conexion cerrada por el cliente abruptamente")
        finally:
            print("El cliente ha cerrado la conexion")
            conn.close()


