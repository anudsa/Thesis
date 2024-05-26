"""
ICA = (Σᵢ₌₁ⁿ Pᵢ×Wᵢ)
      _____________
     (Σᵢ₌₁ⁿ Wᵢ)
"""
def calcular_subindice_temperatura(T):
    # Subíndice de Temperatura (ICA_T)
    if T > 25:
        subindice_T = 0.1
    elif 20 <= T <= 25:
        subindice_T = 1.0
    else:
        subindice_T = 0.5

    return subindice_T

def calcular_subindice_ph(pH):
    # Subíndice de pH (ICA_pH)
    if pH < 6:
        subindice_pH = 0.1
    elif 6 <= pH <= 7.5:
        subindice_pH = 0.5
    else:
        subindice_pH = 1.0

    return subindice_pH

def calcular_subindice_conductividad(CE):
    # Subíndice de Conductividad Eléctrica (ICA_CE)
    if CE > 0 and CE < 300:
        subindice_CE = 0.1
    elif 300 <= CE <= 700:
        subindice_CE = 1.0
    else:
        subindice_CE = 0.5

    return subindice_CE

def calcular_indice( CE,T, pH,):
    # Cálculo de los subíndices
    subindice_CE = calcular_subindice_conductividad(CE)
    print(subindice_CE)
    subindice_T = calcular_subindice_temperatura(T)
    subindice_pH = calcular_subindice_ph(pH)
    # Cálculo del ICA global
    indice = (0.2 * subindice_T + 0.5 * subindice_pH + 0.3 * subindice_CE) / (0.2 + 0.5 + 0.3)
    return indice

def interpretacion(indice):
    if indice <= 0.25:
        return "Baja"
    elif 0.25 < indice <= 0.75:
        return "Regular"
    else:
        return "Excelente"
    
#For the English version    
def interpretation(indice):
    if indice <= 0.25:
        return "Low"
    elif 0.25 < indice <= 0.75:
        return "Regular"
    else:
        return "Excellent"
    

if __name__ == "__main__":
    # Escenarios de prueba
    escenarios = [
        {'CE': 120, 'T': 30, 'pH': 5},    # Baja
        {'CE': 800, 'T': 15, 'pH': 8},     # Aceptable
        {'CE': 500, 'T': 23, 'pH': 7.6},   # Excelente
    ]

    # Ejecutar escenarios de prueba
    for escenario in escenarios:
        CE = escenario['CE']
        T = escenario['T']
        pH = escenario['pH']
        
        indice = calcular_indice(CE, T, pH)
        interpretVariable = interpretacion(indice)
        
        print(f"Para CE: {CE}, T: {T}, pH: {pH}, el índice es: {indice} ({interpretVariable})")

