import csv
from multiprocessing import Pool
from operator import itemgetter

def cant_mediciones_corte(file_name):
    cantidad = 0    
    file = open(f'{file_name}.csv', 'r',encoding='latin')
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        voltaje_fases = [float(row[3]),float(row[4]),float(row[5])] #sacamos las 3 fases por cada medicion(fila)
        for v in voltaje_fases:
            if v<50:
                cantidad+=1
                break #Si encuentra uno entonces sale del bucle y cantidad de mediciones aumenta en 1(encontramos al menos uno)
    return cantidad         

def cant_mediciones_sobretension(file_name):
    mes = 'junio' if 'junio' in file_name else 'mayo'
    cantidad = 0    
    file = open(f'{file_name}.csv', 'r',encoding='latin')
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        voltaje_fases = [float(row[3]),float(row[4]),float(row[5])]
        for v in voltaje_fases:
            if v>277:
                cantidad+=1
                break #Si encuentra uno entonces sale del bucle y cantidad de mediciones aumenta en 1(encontramos al menos uno)
    return cantidad,mes           

if __name__=="__main__":

    file_junio = 'bi_data_voltajes_junio_todos'
    file_mayo = 'bi_data_voltajes_mayo_todos'

    #a)¿Qué mes tiene mayor cantidad de mediciones (filas del csv) donde al menos una de las fases está en corte?
    mediciones_corte_junio = cant_mediciones_corte(file_junio)
    mediciones_corte_mayo = cant_mediciones_corte(file_mayo)
    mes = 'junio' if mediciones_corte_junio > mediciones_corte_mayo else 'mayo' #hallamos el mes con la mayor cantidad de mediciones
    print('El mes con mayor cantidad de mediciones con al menos una de las fases en corte es', mes)

    #b)¿Qué mes tiene mayor cantidad de mediciones (filas del csv) con sobretensión en al menos una de las fases?
    p = Pool(processes=2) #como se procesan 2 archivos a la vez, considero 2 procesos
    results = p.map(cant_mediciones_sobretension, [file_junio, file_mayo])
    p.close()
    p.join()
    mes = max(results,key=itemgetter(0))[1] #hallamos el mes con la mayor cantidad de mediciones
    print('El mes con mayor cantidad de mediciones con al menos una de las fases en sobretension es', mes)