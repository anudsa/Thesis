import pandas as pd
from sqlalchemy import create_engine

def exportarExcel(id_inicial, id_final):
    # Create SQLAlchemy engine with MariaDB dialect
    engine = create_engine("mysql+pymysql://user:pass@localhost/dbname?charset=utf8mb4")

    # Construct the SQL query with the range of IDs
    consulta_sql = f"SELECT * FROM lecturas WHERE id BETWEEN {id_inicial} AND {id_final}"

    # Create a DataFrame using pandas
    df = pd.read_sql_query(consulta_sql, engine)

    # Define the folder path
    ruta_carpeta = "/home/pi/Desktop/ArchivosExportados/"

    # Get the current date and time
    timestampFormat = datetime.now().strftime("%d-%m-%Y %H-%M-%S")

    # Define the file name with the desired format
    nombre_archivo = f"Lecturas {timestampFormat}.xlsx"

    # Save the DataFrame to an Excel file in the specified folder
    df.to_excel(ruta_carpeta + nombre_archivo, index=False)

    # Open the folder in the default file manager on Linux
    subprocess.run(["xdg-open", ruta_carpeta])

# Call the function with the desired range of IDs
if __name__ == "__main__":
    exportarExcel(2, 4)
