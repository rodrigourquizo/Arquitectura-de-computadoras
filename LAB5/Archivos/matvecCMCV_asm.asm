global matvecCMCV_asm
section .text

;RDI<-A[0]  RSI<-x[0]  RDX<-b[0] RCX<-N

matvecCMCV_asm:
xorpd xmm0,xmm0
xorpd xmm1,xmm1
xorpd xmm2,xmm2
xorpd xmm3,xmm3

mov r8, 0                   ;i=0
mov r9, 0                   ;j=0
mov r10, rcx                ;r10=N
mov r11, rdi                ;r11=A[0] 
mov r12, 8

buclei:
mov rax, r9                 ;rax<-j
mul r10b                    ;rax<-j*N
add rax, r8                 ;rax<- j*N + i
movsd xmm1, [rdi + 8*rax] 	;A[i + j*N]
movsd xmm2, [rsi + 8*r9] 	;x[j] 
mulsd xmm1, xmm2 			;xmm1<-A[i + j*N]*x[j]

movsd xmm3, [rdx]           ;xmm3<-b[i]
addsd xmm3,xmm1             ;xmm3<-b[i] + A[i + j*N]*x[j]
movsd [rdx], xmm3           ;b[i]<-xmm3           

cmp r8, rcx
je inc_j                    ;si i=N sale del bucle
inc r8                      ;i=i+1
add rdx,8                   ;paso al sgte elemento del arreglo b
jmp buclei                  

inc_j:
cmp r9, rcx                 ;si j=N sale del bucle     
je fin                      
inc r9                      ;j<-j+1    
mov r8, 0                   ;i=0

mov rax,rcx                 ;rax<-N    
mul r12b                    ;rax<-N*8
sub rdx, rax                ;rdx<-b[0]
xor rax, rax
jmp buclei

fin:
ret
