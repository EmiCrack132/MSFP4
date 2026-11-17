"""
Práctica 4: Modelado y control del sistema endócrino

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Emiliano Gómez Quiroa
Número de control: 23212196
Correo institucional: l23212196@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0,t0,tend,dt,w,h=0,0,10,1E-3,7,3.5
N=round(tend/dt)+1 #numero de iteraciones para la funcion de tranferencia
t=np.linspace(t0,tend,N) #arreglo del tiempo

u1=np.ones(N) #Step
u2=np.zeros(N); u2[round(1/dt):round(2/dt)]=1
u3=t/tend #rampa
u4=np.sin(m.pi/2*t)
u=np.column_stack((u1,u2,u3,u4))

signals=["Step","Impulse","Ramp","Sinusoidal"]

# Componentes del circuito RLC y función de transferencia
#Control
R1,R2,L,C=1E3,100E3,47E-6,1E-6
num=[L,R2]
den=[R1*C*L,R1*R2*C+L,R1+R2]
sys=ctrl.tf(num,den)
print(f"Función de tranferencia: {sys}\n")

# Polos del sistema
L=np.roots(den)
print(f"Polos del sistema: L1={L[0]:.3e}, L2={L[1]:.3e}\n")

#Caso
R1_C,R2_C,L_C,C_C=1E3,1E3,47E-6,1000E-6
numC=[L_C,R2_C]
denC=[R1_C*C_C*L_C,R1_C*R2_C*C_C+L_C,R1_C+R2_C]
sysC=ctrl.tf(numC,denC)
print(f"Función de tranferencia: {sysC}\n")

# Polos del sistema
LC=np.roots(denC)
print(f"Polos del sistema: L1={LC[0]:.3e}, L2={LC[1]:.3e}\n")

# Componentes del controlador
kP,kI,kD=529.0879,51836.0493,.17756
Cr=1E-6
Re=1/(Cr*kI)
Rr=kP*Re
#Ce=kD/Rr

numPID=[Rr*Cr,1]
denPID=[Re*Cr,0]
#numPID=[Re*Rr*Ce*Cr,Re*Ce+Rr*Cr,1]
#denPID=[Re*Cr,0]
PID=ctrl.tf(numPID,denPID)
print(f"El valor de la capacitancia Cr es de {Cr} Faradios.\n")
print(f"El valor de la capacitancia Re es de {Re} Ohms.\n")
print(f"El valor de la capacitancia Rr es de {Rr} Ohms.\n")
#print(f"El valor de la capacitancia Ce es de {Ce} Faradios.\n")
print(f"Funcion de transferencia del controlador PID: {PID}.\n")

# Sistema de control en lazo cerrado
sysPID=ctrl.feedback(ctrl.series(PID,sys),1,sign=-1)
print(f"Función de transferencia del sistema de control de lazo cerrado: {sysPID}")

# Colores
clr1=np.array([255,0,0])/255
clr2=np.array([0,255,0])/255
clr3=np.array([0,0,255])/255
clr4=np.array([0, 0, 0])/255


# Funciones del sistema en lazo abierto y lazo cerrado
def openloop(t,sys,u):
    _,PAu=ctrl.forced_response(sys,t,u,x0)
    return PAu

def closedloop(t,sysPID,u):
    _,PIDu=ctrl.forced_response(sysPID,t,u,x0)
    return PIDu


# Respuesta del sistema en lazo abierto y en lazo cerrado
for i in range(0,1):
    control=openloop(t,sys,u[:,i])
    caso=openloop(t,sysC,control)

    PID=closedloop(t,sysPID,control)

    fg=plt.figure(i+1)
    fg.set_size_inches(w,h)
    plt.rcParams['font.size']=11
    plt.rcParams['font.family']='serif'
    plt.rcParams['font.serif']=['Times New Roman']

    plt.plot(t,u[:,i],'-',color=clr1,label='Ve(t)')
    plt.plot(t,control,'--',color=clr2,label='Vs(t): Control')
    plt.plot(t,caso,'--',color=clr3,label='Vs(t): Caso')
    
    plt.plot(t,PID,':',linewidth=2.5,color=clr4,label='PID(t): Tratamiento')
    plt.xlim(0,10);plt.xticks(np.arange(0,11,1))
    plt.ylim(0,1.1); plt.yticks(np.arange(0,1.2,0.1))
   

    plt.xlabel('t [S]')
    plt.ylabel('V(t) [V]')
    plt.legend(bbox_to_anchor=(0.5,-0.25),loc='center',ncol=4,frameon=False)
    plt.show()
    fg.savefig(signals[i]+'_python.pdf',bbox_inches='tight')