#!/bin/bash
if [[ $# == 0 ]] #Si no hay argumentos se muestra un mensaje
then
    echo "[*] Debe ingresar un argumento"
else
    cantidad=$1
    mkdir Laboratorio1 #Creamos la carpeta Laboratorio1
    cd Laboratorio1 #Nos movemos a dicha carpeta 
    for ((i=1;i<=$cantidad; i++)) #Se creara la cantidad de carpetas igual al argumento de entrada
    do
        mkdir "Carpeta$i" #Creacion de carpetas
        chmod u=rwx "Carpeta$i" #Asignacion de permisos de las carpetas al propietario
    done
    for ((i=1;i<=$cantidad; i++))#Se creara un archivo para cada carpeta
    do
        touch "Archivo$i.txt" #Creacion de archivos
        echo " Hola Carpeta$i ">"Archivo$i.txt" #Escribir cadena de caracteres en el archivo
        mv  "Archivo$i.txt" "Carpeta$i" #Mover cada archivo a su carpeta
    done
fi