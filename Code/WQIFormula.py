#Cálculo del índice de calidad de agua
#(Σᵢ₌₁³ Pᵢ × Wᵢ) 
#_______________
#  (Σᵢ₌₁³ Pᵢ)

#Datos de prueba
conductividad=550
temp=23
pH=7


def parametrizacion(conductividad,temp,pH):
    #Creamos una lista vacía de 3 elementos para P y los pesos fijos para W.
    P=[None]*3

    if conductividad < 250 or conductividad > 500:
        P[0]=2
    else:
        P[0]=1

    if temp < 20 or temp > 25:
        P[1]=2
    else:
        P[1]=1

    if pH < 6.5 or pH > 8.5:
        P[2]=2
    else:
        P[2]=1

    return P

def calculo(P,W):
    Numerador =  sum([(P[i]*W[i]) for i in range(3)]) #suma los productos de p(i) por w(i)
    Denominador = sum(P) #Suma los elementos de la lista P
    WQI=Numerador/Denominador
    return WQI
# The calculated WQIs were then classified according to
# the following range: >2.5 were excellent quality water;
# 2.0 to 2.5 good quality water; and <2.0 poor quality water. 
def interpretacion(WQI):
    if WQI < 2:
        return "Baja"
    elif WQI <2.5:
        return "Aceptable"
    elif WQI <=3:
        return "Excelente"
""""
if __name__ == "__main__":
    W=[1,2,3]
    P=parametrizacion(330,2,2)
    WQI = calculo(P,W)
    print(WQI)
    print(f"WQI = {WQI}")
    print(interpretacion(WQI))
"""
if __name__ == "__main__":
    W = [1, 2, 3]
    
    # "Baja" (Poor quality water) scenario
    P_baja = parametrizacion(600, 23, 7)
    WQI_baja = calculo(P_baja, W)
    print(f"WQI for 'Baja' scenario: {WQI_baja}")
    print(f"Classification: {interpretacion(WQI_baja)}")

    # "Aceptable" (Acceptable quality water) scenario
    P_aceptable = parametrizacion(300, 24, 8.4)
    WQI_aceptable = calculo(P_aceptable, W)
    print(f"WQI for 'Aceptable' scenario: {WQI_aceptable}")
    print(f"Classification: {interpretacion(WQI_aceptable)}")

    # "Excelente" (Excellent quality water) scenario
    P_excelente = parametrizacion(300, 22, 7.5)
    WQI_excelente = calculo(P_excelente, W)
    print(f"WQI for 'Excelente' scenario: {WQI_excelente}")
    print(f"Classification: {interpretacion(WQI_excelente)}")
