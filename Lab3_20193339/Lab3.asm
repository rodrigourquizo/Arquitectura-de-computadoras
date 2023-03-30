section .data
    arrin db 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24 ;declaramos el arreglo de entrada
    arrout db 0,0,0,0,0,0,0,0,0 ;declaramos el arreglo de salida

section .bss
	valor resb 1

section .text
    global _start
    
_start:
;introducimos el arreglo de entrada en el registro r9
mov  r9, arrin
mov rcx, [r9] 
;introducimos el arreglo de salida en el registro rdi
mov rdi, arrout
mov al, cl ;colocamos el valor del arreglo de entrada en el de salida
mov [rdi], al

add r9, 1
add r9, 1
add rdi, 1

mov rcx, [r9] 
mov al, cl 
mov [rdi], al

add r9, 1
add r9, 1
add rdi, 1

mov rcx, [r9] 
mov al, cl 
mov [rdi], al

;Al momento de llegar a las filas impares recorro 6 espacios de memoria
;ya que dichas filas se eliminan
;y cuando estamos en las filas que si utilizamos recorro solo un espacio de memoria de forma
;intercalada para asignar los numeros de las columnas impares en la matriz de salida 

add r9, 1
add r9, 1
add r9, 1
add r9, 1
add r9, 1
add r9, 1
add rdi, 1
mov rcx, [r9] 
mov al, cl 
mov [rdi], al

add r9, 1
add r9, 1
add rdi, 1

mov rcx, [r9] 
mov al, cl 
mov [rdi], al

add r9, 1
add r9, 1
add rdi, 1

mov rcx, [r9] 
mov al, cl 
mov [rdi], al

add r9, 1
add r9, 1
add r9, 1
add r9, 1
add r9, 1
add r9, 1
add rdi, 1
mov rcx, [r9] 
mov al, cl 
mov [rdi], al

add r9, 1
add r9, 1
add rdi, 1

mov rcx, [r9] 
mov al, cl 
mov [rdi], al

add r9, 1
add r9, 1
add rdi, 1

mov rcx, [r9] 
mov al, cl 
mov [rdi], al


fin:
mov rax,60
mov rdi,0
syscall

