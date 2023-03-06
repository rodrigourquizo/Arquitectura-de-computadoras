import numpy as np
import math
from multiprocessing import Process,cpu_count,current_process,Pool
import time

"""
Código que permite obtener un arreglo aleatorio de puntos XYZ de forma (N,3).

@param N: Indica la cantidad de puntos del arreglo. Es decir, la cantidad de filas N
@return arrayPoints: Arreglo aleatorio XYZ
"""
def getArray(N=3):
    numPoints=N
    arrayPoints = np.random.rand(numPoints,3)
    return arrayPoints

def pto_medio(v1,v2):
    return [(v1[0] + v2[0])/2,(v1[1] + v2[1])/2,(v1[2] + v2[2])/2 ]
    
def punto_medio_total(arreglo):
    while(len(arreglo)>1):
        i=0
        new = []
        while i<len(arreglo):
            try:
                punto_medio = pto_medio(arreglo[i], arreglo[i+1])
            except:
                punto_medio = arreglo[i]
            new.append(punto_medio)
            i+=2
        arreglo = new
    
    print("Proceso ",current_process().pid)
    return new[0]


if __name__=="__main__":
    ## Input for the pseudo-random number generator in Python
    #np.random.seed(17)
    ## Desarrolle en las siguientes líneas del main
    print(cpu_count())

    ti = time.perf_counter()
    p = Pool(processes=7)
    p.map(punto_medio_total, [getArray(800000),getArray(800000),getArray(800000),getArray(800000),getArray(800000),getArray(800000),getArray(800000)])
    #print(current_process().pid)
    p.close()
    p.join()
    tf = time.perf_counter()
    print(f"Tiempo de ejecucion: {tf-ti} segundos")
