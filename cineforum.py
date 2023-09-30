import mysql.connector
from mysql.connector import errorcode
import random
import datetime

# Configurazione della connessione al database
config = {
    'user': 'cineforum_user',
    'password': 'XXXXXXXXX',
    'host': 'XXXXXXXXX',
    'database': 'cineforum',
}

def connetti_al_database():
    try:
        connessione = mysql.connector.connect(**config)
        if connessione.is_connected():
            return connessione
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Accesso al database negato")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database non esistente")
        else:
            print(err)
    return None

def inserisci_film(connessione, titolo):
    try:
        cursor = connessione.cursor()
        inserimento_film = ("INSERT INTO film (TITLE) VALUES (%s)")
        cursor.execute(inserimento_film, (titolo,))
        connessione.commit()
        cursor.close()
        print(f"Film '{titolo}' inserito nel database.")
    except mysql.connector.Error as err:
        print(f"Errore durante l'inserimento del film: {err}")

def estrai_film(connessione):
    try:
        cursor = connessione.cursor()
        selezione_film_non_estratti = ("SELECT TITLE FROM film WHERE EXTRACTION_TIME IS NULL")
        cursor.execute(selezione_film_non_estratti)
        film_non_estratti = cursor.fetchall()

        if not film_non_estratti:
            print("Nessun film disponibile per l'estrazione.")
            return

        film_da_estrarre = random.choice(film_non_estratti)[0]
        aggiorna_timestamp = ("UPDATE film SET EXTRACTION_TIME = %s WHERE TITLE = %s")
        cursor.execute(aggiorna_timestamp, (datetime.datetime.now(), film_da_estrarre))
        connessione.commit()
        cursor.close()
        print(f"Film estratto: '{film_da_estrarre}'")
    except mysql.connector.Error as err:
        print(f"Errore durante l'estrazione del film: {err}")

def main():
    connessione = connetti_al_database()
    if connessione:
        while True:
            print("\nMenu:")
            print("1. Inserisci un film")
            print("2. Estrai un film")
            print("3. Esci")
            scelta = input("Seleziona un'opzione: ")

            if scelta == '1':
                    titolo = ""
                    while titolo.lower() != "exit":
                        titolo = input("Inserisci il titolo del film, \"exit\" per uscire: ")
                        if(titolo!="exit" and titolo !=""):
                            inserisci_film(connessione, titolo)
            elif scelta == '2':
                estrai_film(connessione)
            elif scelta == '3':
                break
            else:
                print("Opzione non valida. Riprova.")

        connessione.close()
        print("Programma terminato.")

if __name__ == "__main__":
    main()
