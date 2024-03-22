#Cálculo del índice de calidad de agua
#(Σᵢ₌₁⁴ Pᵢ × Wᵢ) 
#_______________
#  (Σᵢ₌₁⁴ Pᵢ)

#Datos de prueba
conductividad=500
temp=27
pH=7
oxigenoDisuelto=6

#Creamos una lista vacía de 4 elementos para P y una para W.
P=[None]*4
W=[None]*4

if conductividad < 250 or conductividad > 700:
    P[1]=2
else:
    P[1]=1

if temp < 20 or temp > 25:
    P[0]=2
else:
    P[0]=1

if pH < 6 or pH > 8.5:
    P[2]=2
else:
    P[2]=1

if oxigenoDisuelto < 5 or oxigenoDisuelto > 10:
    P[3]=2
else:
    P[3]=1

W=[1,2,3,4]

Numerador =  sum([(P[i]*W[i]) for i in range(4)]) #suma los productos de p(i) por w(i)
Denominador = sum(P) #Suma los elementos de la lista P
WQI=Numerador/Denominador
print(f"WQI = {WQI}")

if WQI < 1.5:
    print("Calidad Baja")
elif WQI <2.5:
    print("Calidad Aceptable")
elif WQI <=4:
    print("Calidad Excelente")