import sys

#Funcion para saber si un numero es primo
def es_primo(numero):
    cant_div=0
    for i in range(1,numero+1): #Recorremos los valores desde 1 hasta numero
        if(numero%i==0): #Se evalua si es divisible por dicho valor a traves del operador modulo
            cant_div+=1 #Si es asi se incrementa la cantidad de divisores
    return cant_div == 2 #Retorna True si tiene dos divisores(primo) y False en caso contrario

#Funcion para obtener la cantidad de divisores primos de un numero
def div_por_kprimos(numero):
    cant_div_primos=0
    for i in range(1,numero+1):
        if(numero%i==0 and es_primo(i)): #Se evalua si es divisor y si es primo
            cant_div_primos+=1    
    return cant_div_primos #Retorna la cantidad de divisores primos
    
#Obtenemos los argumentos de entrada y los convertimos a enteros
a = int(sys.argv[1])
b = int(sys.argv[2])
c = int(sys.argv[3])
cant_primos = 0
cant_no_primos_div_por_kprimos=0

#Si el 3er argumento es 0 entonces contamos los primos en el rango [a-b]
if(c==0):
    for i in range(a,b+1):
        if(es_primo(i)):
            cant_primos+=1
    print("Hay {} numeros primo(s)".format(cant_primos))
#Caso contrario, debemos obtener los numeros no primos divisibles por la cantidad de primos igual a c  
elif(c>0):
    for i in range(a,b+1):
        if(not es_primo(i) and div_por_kprimos(i)==c): 
            cant_no_primos_div_por_kprimos+=1
    print("Hay {} numeros divisibles por {} primo(s)".format(cant_no_primos_div_por_kprimos, c))


