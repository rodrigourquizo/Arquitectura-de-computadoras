global matvecCMRV_asm
section .text

;RDI<-A[0]  RSI<-x[0]  RDX<-b[0] RCX<-N

matvecCMRV_asm:
xorpd xmm0,xmm0             ;tmp
xorpd xmm1,xmm1
xorpd xmm2,xmm2
mov r8, 0                   ;i=0
mov r9, 0                   ;j=0
mov r10, rcx                ;r10=N
mov r11, rdi                ;r11=A[0] 

buclej:
mov rax, r9                 ;rax<-j
mul r10b                     ;rax<-j*N
add rax, r8                 ;rax<- j*N + i
movsd xmm1, [rdi + 8*rax] 	;A[i + j*N]
movsd xmm2, [rsi + 8*r9] 	;x[j] 
mulsd xmm1, xmm2 			;xmm1<-A[i + j*N]*x[j]
addsd xmm0, xmm1  			;tmp += xmm1
cmp r9, rcx
je inc_i                    ;si j=N sale del bucle
inc r9                      ;j=j+1
jmp buclej                  

inc_i:
movsd [rdx], xmm0           ;b[i]<-tmp

cmp r8, rcx                 ;si i=N sale del bucle     
je fin                      
inc r8                      ;i<-i+1    
add rdx, 8                  ;paso al sgte elemento del arreglo b
mov r9, 0                   ;j=0    
xorpd xmm0, xmm0            ;tmp=0.0
jmp buclej

fin:
ret