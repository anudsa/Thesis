#WQI calculation
#(Σᵢ₌₁⁴ Pᵢ × Wᵢ) 
#_______________
#  (Σᵢ₌₁⁴ Pᵢ)
#Creamos una lista de valores para P y una para W
P=[1,1,2,2]
W=[1,2,3,4]
print("WQI = ")
Numerador =  sum([(P[i]*W[i]) for i in range(4)]) #suma los productos de p(i) por w(i)
Denominador = sum(P) #Suma los elementos de la lista P
WQI=Numerador/Denominador
print(WQI)