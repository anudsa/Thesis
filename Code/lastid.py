import config
import mysql.connector
#Database connection
mysql_db = mysql.connector.connect(
    host = config.DB_HOST,
    user = config.DB_USER,
    password = config.DB_PASSWORD,
    database = config.DB_NAME
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
