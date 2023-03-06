from threading import Thread

rutas_posibles = [
	"LIM_PIU_CAJ",
	"LIM_PIU_CHI_HUA_CAJ",
	"LIM_PIU_CHI_OXA_HUA_CAJ",
	"LIM_OXA_CHI_PIU_CAJ",
	"LIM_OXA_CHI_HUA_CAJ",
	"LIM_OXA_HUA_CAJ",
	"LIM_OXA_HUA_CHI_PIU_CAJ",
	"LIM_CHI_PIU_CAJ",
	"LIM_CHI_OXA_HUA_CAJ",
	"LIM_CHI_HUA_CAJ"
]

distancias = {
	"LIM_PIU": 14,
	"LIM_CHI": 10,
	"LIM_OXA": 8,
	"PIU_CAJ": 18,
	"PIU_CHI": 3,
	"OXA_CHI": 25,
	"OXA_HUA": 5,
	"CHI_PIU": 3,
	"CHI_OXA": 25,
	"CHI_HUA": 2,
	"HUA_CHI": 2,
	"HUA_CAJ": 10
}

if __name__ == "__main__":
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

    def calcular_tiempo_recorrido(ruta):
      tiempo_total = 0
      ciudades_separadas = ruta.split('_')
      anterior = ciudades_separadas[0]
      for i in range(1,len(ciudades_separadas)): 
         actual = ciudades_separadas[i]                         
         partida_destino = anterior + '_' + actual              #separo las ciudades para obtener todas las conexiones                  
         print(partida_destino, distancias[partida_destino])    #imprimo la conexion con el tiempo que toma
         tiempo_total += distancias[partida_destino]            #sumo ese tiempo al tiempo total del recorrido
         anterior = actual                                      #actualizo la nueva ciudad para luego obtener la nueva conexion            
      return tiempo_total

    for ruta in rutas_posibles:
      thread = Threading(target = calcular_tiempo_recorrido, args = (ruta,)) #creo un thread por cada combinacion posible
      thread.start()                                
      t_total = thread.join()                                                #obtengo el tiempo total que toma cada ruta           
      print(ruta, t_total, '\n')                                    
      if ruta == "LIM_PIU_CAJ" or t_total<menor_tiempo:                      #tomo la ruta inicial como referencia, si el tiempo total es menor al tiempo menor actualizo los valores   
        ruta_mas_corta = ruta
        menor_tiempo = t_total

    print(f'La ruta mas corta es {ruta_mas_corta} con un tiempo de {t_total} horas')