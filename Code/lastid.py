import mysql.connector
#Database connection
mysql_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pa$$w0rd",
    database="Sensores"
)
# Create a cursor object to execute SQL queries
cursor = mysql_db.cursor()
def leeUltimoid():
    # Consulta para encontrar el ID de la última fila de las lecturas
    cursor.execute("SELECT MAX(id) FROM lecturas")
    # Obtener el resultado
    resultado = cursor.fetchone()
    # Extraer el ID del resultado
    ultimo_id = int(resultado[0])
    return ultimo_id
print(type(leeUltimoid()))