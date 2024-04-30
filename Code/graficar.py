import pandas as pd
import subprocess
from sqlalchemy import create_engine
from datetime import datetime
import matplotlib as plt
import matplotlib.pyplot as plt

def graficarDatos(id_inicial, id_final):
    # Crea motor de SQLAlchemy
    engine = create_engine('mysql+mysqlconnector://root:Pa$$w0rd@localhost/Sensores')

    # Construye la consulta SQL con el rango de IDs
    consulta_sql = f"SELECT * FROM lecturas WHERE id BETWEEN {id_inicial} AND {id_final}"

    # Crea un Dataframe de pandas
    df = pd.read_sql_query(consulta_sql, engine)
    
    # Convert 'tiempo' column to datetime format if it's not already in datetime format
    df['tiempo'] = pd.to_datetime(df['tiempo'])

    # Create a figure with a specified size
    plt.figure(figsize=(12, 8))

    print(df)
    # Plotting the first subplot
    plt.subplot(2, 2, 1)
    plt.scatter(df['tiempo'], df['temperatura'])
    plt.xlabel("Tiempo")
    plt.ylabel("Temperatura")
    plt.title("Temperatura")
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d-%m %H:%M'))
    plt.xticks(rotation='vertical')

    # Plotting the second subplot
    plt.subplot(2, 2, 2)
    plt.scatter(df['tiempo'], df['pH'])
    plt.xlabel("Tiempo")
    plt.ylabel("pH")
    plt.title("pH")
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d-%m %H:%M'))
    plt.xticks(rotation='vertical')

    # Plotting the third subplot
    plt.subplot(2, 2, 3)
    plt.scatter(df['tiempo'], df['conductividad'])
    plt.xlabel("Tiempo")
    plt.ylabel("Conductividad")
    plt.title("Conductividad")
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d-%m %H:%M'))
    plt.xticks(rotation='vertical')

    # Plotting the fourth subplot
    plt.subplot(2, 2, 4)
    plt.scatter(df['tiempo'], df['indice'])
    plt.xlabel("Tiempo")
    plt.ylabel("Indice")
    plt.title("Indice")
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d-%m %H:%M'))
    plt.xticks(rotation='vertical')

    # Adjusting the layout to prevent overlapping
    plt.tight_layout()

    # Display the plot
    plt.show()

# Ejemplo de uso de la funcion
if __name__ == "__main__":
    graficar(7,11)
