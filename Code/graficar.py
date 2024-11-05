
import config
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import matplotlib as plt
import matplotlib.pyplot as plt

def graficarDatos(id_inicial, id_final):
    #Crea el motor de SQLAlchemy
    engine = create_engine(f"mysql+mysqlconnector://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}")

    #Construye la consulta SQL con el rango de IDs
    consulta_sql = f"SELECT * FROM lecturas WHERE id BETWEEN {id_inicial} AND {id_final}"

    #Crea un Dataframe de pandas
    df = pd.read_sql_query(consulta_sql, engine)
    
    #Convierte la columna 'tiempo' al formato datetime si aún no está en ese formato
    df['tiempo'] = pd.to_datetime(df['tiempo'])

    #Imprime el Dataframe en la terminal
    print(df.to_string(index=False))

   #Crea la figura con el tamaño específico
    plt.figure(figsize=(12, 8))

    #Grafica la primera subgráfica
    plt.subplot(2, 2, 1)
    plt.scatter(df['tiempo'], df['temperatura'])
    plt.xlabel("Tiempo")
    plt.ylabel("Temperatura (ºC)")
    plt.title("Temperatura")
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d-%m %H:%M'))
    plt.xticks(rotation='vertical')

    #Grafica la segunda subgráfica
    plt.subplot(2, 2, 2)
    plt.scatter(df['tiempo'], df['pH'])
    plt.xlabel("Tiempo")
    plt.ylabel("pH")
    plt.title("pH")
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d-%m %H:%M'))
    plt.xticks(rotation='vertical')

    #Grafica la tercera subgráfica
    plt.subplot(2, 2, 3)
    plt.scatter(df['tiempo'], df['conductividad'])
    plt.xlabel("Tiempo")
    plt.ylabel("Conductividad (\u00b5S/cm)")
    plt.title("Conductividad Eléctrica")
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d-%m %H:%M'))
    plt.xticks(rotation='vertical')

    #Grafica la cuarta subgráfica
    plt.subplot(2, 2, 4)
    plt.scatter(df['tiempo'], df['indice'])
    plt.xlabel("Tiempo")
    plt.ylabel("Índice")
    plt.title("Índice de Calidad de Agua")
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d-%m %H:%M'))
    plt.xticks(rotation='vertical')

    #Ajusta el diseño para evitar superposiciones
    plt.tight_layout()

    #Muestra la gráfica
    plt.show()

#Ejemplo de uso de la funcion
if __name__ == "__main__":
    #Se llama a la función con los id a graficar
    graficarDatos(2,10)
