import pandas as pd
import subprocess
from sqlalchemy import create_engine
from datetime import datetime

def exportarExcel(id_inicial, id_final):
    # Crea motor de SQLAlchemy
    engine = create_engine('mysql+mysqlconnector://root:Pa$$w0rd@localhost/Sensores')

    # Construye la consulta SQL con el rango de IDs
    consulta_sql = f"SELECT * FROM lecturas WHERE id BETWEEN {id_inicial} AND {id_final}"

    # Crea un Dataframe de pandas
    df = pd.read_sql_query(consulta_sql, engine)

    # Obtener la fecha y hora actual
    timestampFormat = datetime.now().strftime("%d-%m-%Y %H-%M-%S")

    # Definir el nombre del archivo con el formato deseado
    nombre_archivo = f"Lecturas {timestampFormat}.xlsx"

    # Definir la ruta de la carpeta
    #ruta_carpeta = "/Users/anu/Documents/IPN/Tesis/Github Repo/Thesis/export"
    ruta_carpeta = "/home/pi/Desktop/ArchivosExportados/"
    # Guardar el DataFrame en un archivo Excel en la carpeta especificada
    df.to_excel(ruta_carpeta + nombre_archivo, index=False)

    # Abre la carpeta en el explorador de archivos por defecto en Linux
    subprocess.run(["xdg-open", ruta_carpeta])

    return True
    # Abre la carpeta en el Finder en macOS
    #subprocess.run(["open", ruta_carpeta])

# Ejemplo de uso de la funcion
if __name__ == "__main__":
    exportarExcel(2, 4)
