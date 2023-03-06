import time
import csv

#A)Lectura del archivo
tiempo_inicial = time.perf_counter()*1000
file = open('data_encoders.txt', 'r')
reader = csv.reader(file)
file.close()
tiempo_final = time.perf_counter()*1000

print(f'El tiempo para leer el archivo es de: {tiempo_final-tiempo_inicial} msec')
print('--------------------------------------------------------')

#B)Obtengo cuantos reinicios hay por cada encoder
file = open('data_encoders.txt', 'r')
reader = csv.reader(file)
next(reader) #Saltamos el header
list_encoder1 = []
list_encoder2 = []
list_encoder3 = []
list_encoder4 = []
list_encoder5 = []
list_encoder6 = []

for row in reader:
  list_encoder1.append(int(row[0]))
  list_encoder2.append(int(row[1]))
  list_encoder3.append(int(row[2]))
  list_encoder4.append(int(row[3]))
  list_encoder5.append(int(row[4]))
  list_encoder6.append(int(row[5]))

#Funcion para calcular la cantidad de reinicios, establezco que sea una diferencia mayor a 60 000 
#entre datos consecutivos para considerarlo como reinicio
def cantidad_reinicios(list_encoder):
  reinicios = 0
  anterior = list_encoder[0]
  for i in range(1,len(list_encoder)):
    actual = list_encoder[i]
    if abs(actual-anterior)>60000:
      reinicios += 1
    anterior = actual
  return reinicios

print(f'El encoder de la rueda 1 ha presentado: {cantidad_reinicios(list_encoder1)} reinicios')
print(f'El encoder de la rueda 2 ha presentado: {cantidad_reinicios(list_encoder2)} reinicios')
print(f'El encoder de la rueda 3 ha presentado: {cantidad_reinicios(list_encoder3)} reinicios')
print(f'El encoder de la rueda 4 ha presentado: {cantidad_reinicios(list_encoder4)} reinicios')
print(f'El encoder de la rueda 5 ha presentado: {cantidad_reinicios(list_encoder5)} reinicios')
print(f'El encoder de la rueda 6 ha presentado: {cantidad_reinicios(list_encoder6)} reinicios')

print('------------------------------------------------------------')

#C)Escritura del contenido del archivo .txt en el nuevo archivo .csv
new_file= open("PulsesEncodersRobot6Wheels.csv","w", newline='')
file = open('data_encoders.txt', 'r')
reader = csv.reader(file)
tiempo_inicial = time.perf_counter()*1000
for row in reader:
  writer = csv.writer(new_file)
  writer.writerow(row)
tiempo_final = time.perf_counter()*1000

print(f'El tiempo para escribir el archivo es de: {tiempo_final-tiempo_inicial} msec')

