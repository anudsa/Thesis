"""
ICA = (Σᵢ₌₁ⁿ Pᵢ×Wᵢ)
      _____________
     (Σᵢ₌₁ⁿ Pᵢ)
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
    if CE > 0:
        subindice_CE = 0.1
    elif 400 <= CE <= 600:
        subindice_CE = 1.0
    else:
        subindice_CE = 0.5

    return subindice_CE

def calcular_indice( CE,T, pH,):
    # Cálculo de los subíndices
    subindice_CE = calcular_subindice_conductividad(CE)
    subindice_T = calcular_subindice_temperatura(T)
    subindice_pH = calcular_subindice_ph(pH)
    # Cálculo del ICA global
    indice = (0.2 * subindice_T + 0.5 * subindice_pH + 0.3 * subindice_CE) / (0.2 + 0.5 + 0.3)
    return indice

def interpretacion(indice):
    if indice < 0.3:
        return "Baja"
    elif 0.3 <= indice <= 0.7:
        return "Aceptable"
    else:
        return "Excelente"

# Escenarios de prueba
escenarios = [
    {'CE': 120,'T': 30, 'pH': 5, },    # Baja
    { 'CE': 800,'T': 15, 'pH': 8,},      # Aceptable
    { 'CE': 500,'T': 23, 'pH': 7.6,},   # Excelente
]
if __name__ == "__main__":
    for i, escenario in enumerate(escenarios, start=1):
        ica = calcular_indice(escenario['T'], escenario['pH'], escenario['CE'])
        interpretacionICA = interpretacion(ica)
        print(f"Prueba {i}: Índice de Calidad del Agua (ICA) para el escenario {escenario}: {ica:.2f} ({interpretacionICA})")
