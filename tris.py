import pymysql
from datetime import date

# Configurazione della connessione al database
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "4CTL_haka.o.050508",
    "password": "tpsit0508",
    "database": "4CTL_haka.o.050508",
    "port": 3307,
    "cursorclass": pymysql.cursors.DictCursor,
    "connect_timeout": 5,
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

def initialize_database():
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS giocatori (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL,
                    partite_giocate INT DEFAULT 0,
                    vittorie INT DEFAULT 0
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS partita (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    giocatore_x_id INT,
                    giocatore_o_id INT,
                    vincitore_id INT,
                    data DATE,
                    FOREIGN KEY (giocatore_x_id) REFERENCES giocatori(id),
                    FOREIGN KEY (giocatore_o_id) REFERENCES giocatori(id),
                    FOREIGN KEY (vincitore_id) REFERENCES giocatori(id)
                )
            """)
        connection.commit()

def get_or_create_giocatore(nome):
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM giocatori WHERE nome = %s", (nome,))
            row = cursor.fetchone()
            if row:
                return row["id"]
            cursor.execute("INSERT INTO giocatori (nome, partite_giocate, vittorie) VALUES (%s, 0, 0)", (nome,))
            connection.commit()
            return cursor.lastrowid

def salva_partita(giocatore_x_id, giocatore_o_id, vincitore_id):
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO partita (giocatore_x_id, giocatore_o_id, vincitore_id, data) VALUES (%s, %s, %s, %s)",
                (giocatore_x_id, giocatore_o_id, vincitore_id, date.today())
            )
            # Aggiorna partite giocate per entrambi
            cursor.execute(
                "UPDATE giocatori SET partite_giocate = partite_giocate + 1 WHERE id IN (%s, %s)",
                (giocatore_x_id, giocatore_o_id)
            )
            # Se c'è un vincitore, aggiorna vittorie
            if vincitore_id is not None:
                cursor.execute("UPDATE giocatori SET vittorie = vittorie + 1 WHERE id = %s", (vincitore_id,))
        connection.commit()

def aggiorna_statistiche(giocatore_id, vittoria=False):
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE giocatori SET partite_giocate = partite_giocate + 1 WHERE id = %s", (giocatore_id,))
            if vittoria:
                cursor.execute("UPDATE giocatori SET vittorie = vittorie + 1 WHERE id = %s", (giocatore_id,))
        connection.commit()

def aggiungi_giocatore(nome):
    return get_or_create_giocatore(nome)

def ottieni_statistiche(giocatore_id):
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nome, partite_giocate, vittorie FROM giocatori WHERE id = %s", (giocatore_id,))
            row = cursor.fetchone()
            if not row:
                return None
            partite = row.get("partite_giocate", 0) or 0
            vittorie = row.get("vittorie", 0) or 0
            win_rate = (vittorie / partite * 100) if partite > 0 else 0.0
            return {
                "id": row["id"],
                "nome": row["nome"],
                "partite_giocate": partite,
                "vittorie": vittorie,
                "win_rate_percentuale": round(win_rate, 2)
            }

def ottieni_leaderboard(limit=10):
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, nome, vittorie, partite_giocate FROM giocatori ORDER BY vittorie DESC, partite_giocate ASC LIMIT %s",
                (limit,)
            )
            return cursor.fetchall()
