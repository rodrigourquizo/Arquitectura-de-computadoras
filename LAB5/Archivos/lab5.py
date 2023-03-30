import numpy as np
import time
from statistics import mean, median
import ctypes
import matplotlib.pyplot as plt


def filtro_mediana(sign, w):
    signc = []
    lc = sign+sign+sign
    ii = len(sign)
    for i in range(len(sign)):
        izq = i + ii - w//2
        der = i + ii + w//2
        signc.append(median(lc[izq:der+1]))
    return signc

#Funciones en Python-lab viernes
def matvecCMRV_python(A, x, b, N):
    tmp = 0.0
    for i in range(N):
        tmp = 0.0
        for j in range(N):
            tmp += A[i + j*N]*x[j]
        b[i] = tmp
    return b

def matvecCMCV_python(A, x, b, N):
    for j in range(N):
        for i in range(N):
            b[i] += A[i + j*N]*x[j]
    return b

def ctypes_matvecCMRVc():
    # ruta de la shared library
    lib = ctypes.CDLL('./matvecCMRV.so')
    
    # tipo de los argumentos
    lib.matvecCMRV.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.float64),
        np.ctypeslib.ndpointer(dtype=np.float64),
        np.ctypeslib.ndpointer(dtype=np.float64),
        ctypes.c_int
    ]
    
    # se devuelve la función configurada
    return lib.matvecCMRV

def ctypes_matvecCMRVasm():
    # ruta de la shared library
    lib = ctypes.CDLL('./matvecCMRV_asm.so')
    
    # tipo de los argumentos
    lib.matvecCMRV_asm.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.float64),
        np.ctypeslib.ndpointer(dtype=np.float64),
        np.ctypeslib.ndpointer(dtype=np.float64),
        ctypes.c_int
    ]
    
    # se devuelve la función configurada
    return lib.matvecCMRV_asm


def ctypes_matvecCMCV():
    # ruta de la shared library
    lib = ctypes.CDLL('./matvecCMCV.so')
    
    # tipo de los argumentos
    lib.matvecCMCV.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.float64),
        np.ctypeslib.ndpointer(dtype=np.float64),
        np.ctypeslib.ndpointer(dtype=np.float64),
        ctypes.c_int
    ]
    
    # se devuelve la función configurada
    return lib.matvecCMCV


def ctypes_matvecCMCVasm():
    # ruta de la shared library
    lib = ctypes.CDLL('./matvecCMCV_asm.so')
    
    # tipo de los argumentos
    lib.matvecCMCV_asm.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.float64),
        np.ctypeslib.ndpointer(dtype=np.float64),
        np.ctypeslib.ndpointer(dtype=np.float64),
        ctypes.c_int
    ]
    
    # se devuelve la función configurada
    return lib.matvecCMCV_asm

matvecCMRV_c = ctypes_matvecCMRVc()
matvecCMRV_asm = ctypes_matvecCMRVasm()
matvecCMCV_c = ctypes_matvecCMCV()
matvecCMCV_asm = ctypes_matvecCMCVasm()

#ns= [ 256, 512, 1024, 2048, 4096]
#Uso valores de N pequeños ya que con los casos solicitados demora demasiado en ejecutar
#en colab y en aws se detiene la ejecucion con el mensaje 'killed' 
#esto me paso incluso disminuyendo el numero de iteraciones a 5
ns = [2,4,8,16,32]
veces = 10
tcmcv_c = np.zeros((len(ns),1),dtype=np.float32)
tcmcv_python = np.zeros((len(ns),1),dtype=np.float32)
tcmcv_asm = np.zeros((len(ns),1),dtype=np.float32)

for i, n in enumerate(ns):
    tcmcvi_c = []
    tcmcvi_python = []
    tcmcvi_asm = []
    for j in range(veces):
        # datos
        A = np.random.rand(n,n)
        x = np.random.rand(n,1)  
        # entradas RM
        Arm = A.flatten()
        # entradas CM
        Acm = np.transpose(A).flatten()
        # referencia
        bref = np.dot(A,x)
        # salidas
        bCMCV = np.zeros_like(bref)
        
        # tiempo Python
        t = time.time()
        matvecCMRV_python(Acm,x,bCMCV,n)
        tcmcvi_python.append(time.time() - t)
        
        # tiempo C
        t = time.time()
        matvecCMRV_c(Acm,x,bCMCV,n)
        tcmcvi_c.append(time.time() - t)
        
        # tiempo ASM
        t = time.time()
        matvecCMRV_asm(Acm,x,bCMCV,n)
        tcmcvi_asm.append(time.time() - t)

    tcmcv_python[i]=(mean(filtro_mediana(tcmcvi_python,9)))
    tcmcv_c[i]=(mean(filtro_mediana(tcmcvi_c,9)))
    tcmcv_asm[i]=(mean(filtro_mediana(tcmcvi_asm,9)))


#Grafico N vs tiempo
plt.plot(ns, tcmcv_c, 'b-o', label='tiempos C')
plt.plot(ns, tcmcv_python, 'c-o', label='tiempos Python')
plt.plot(ns, tcmcv_asm, 'r-o', label='tiempos ASM')
plt.title('Efectos de la localidad-CMRV')
plt.xlabel('tamagno')
plt.ylabel('tiempo promedio')
plt.legend()
plt.savefig('CMRV_tiempos.jpg')

#Grafico N vs speedup
#En que proporcion ASM es mas rapido que Python y ASM
plt.figure(figsize=(10,5))
plt.plot(ns, tcmcv_c/tcmcv_asm, 'g-o', label='C-ASM')
plt.plot(ns, tcmcv_python/tcmcv_asm, 'r-o', label='Python-ASM')
plt.title('speedup por tamagno-CMRV')
plt.xlabel('tamagno')
plt.ylabel('speedup')
plt.legend()
plt.savefig('CMRV_speedup.jpg')

