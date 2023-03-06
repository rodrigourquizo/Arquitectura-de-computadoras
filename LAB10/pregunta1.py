from multiprocessing import Pool
import time

def fx(x, inicio, limite):
    suma = 0
    for a in range(inicio,limite+1):
        suma += a*(x)**a
    return suma

if __name__=="__main__":

    x  = 2022
    #a) Calculo en serie
    ti = time.perf_counter()
    resultado_serial = fx(x,1,10_000)
    tf = time.perf_counter()
    time_serial = tf-ti
    print("Tiempo de ejecucion de f(2022) en serie:", time_serial,'s')    

    #b)calculo en paralelo
    ti = time.perf_counter()
    p = Pool(processes=4)
    results = p.starmap(fx, [(x,1,2500),(x,2501,5000),(x,5001,7500), (x, 7501,10_000)]) #la operacion la divido en 4 rangos
    p.close()
    p.join()
    tf = time.perf_counter()
    time_paralelo = tf-ti
    print("Tiempo de ejecucion de f(2022) con multiprocessing", time_paralelo,'s')
    resultado_paralelo = sum(results)
    #speed up
    speedup = time_serial/time_paralelo
    print('Speed up:', speedup)

    assert resultado_serial == resultado_paralelo #verificamos la igualdad de resultados
    print("Resultados iguales")

    