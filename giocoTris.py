from tris import get_or_create_giocatore, salva_partita, aggiorna_statistiche
from codTris import stampa_scacchiera, fai_mossa, ha_vinto

def gioca_db():
    nome_X = input("Nome del giocatore che usa X: ").strip()
    nome_O = input("Nome del giocatore che usa O: ").strip()

    id_X = get_or_create_giocatore(nome_X)
    id_O = get_or_create_giocatore(nome_O)

    scacchiera = ["_"] * 9
    giocatore_corrente = "X"
    mosse_fatte = 0

    print("Benvenuto a Tris! Inserisci un numero da 0 a 8 per muovere.")

    while True:
        stampa_scacchiera(scacchiera)
        try:
            mossa = int(input(f"Turno di {giocatore_corrente}. Inserisci posizione (0-8): "))
            if mossa < 0 or mossa > 8:
                print("Errore: il numero deve essere tra 0 e 8!")
                continue

            if fai_mossa(scacchiera, mossa, giocatore_corrente):
                mosse_fatte += 1

                if ha_vinto(scacchiera, giocatore_corrente):
                    stampa_scacchiera(scacchiera)
                    print(f"Complimenti! Il giocatore {giocatore_corrente} ha vinto!")
                    vincitore_id = id_X if giocatore_corrente == "X" else id_O
                    salva_partita(id_X, id_O, vincitore_id)
                    # aggiorna_statistiche aumenta partite giocate e vittorie per il vincitore
                    aggiorna_statistiche(id_X, vittoria=(vincitore_id == id_X))
                    aggiorna_statistiche(id_O, vittoria=(vincitore_id == id_O))
                    print("Risultato salvato nel database.")
                    break

                if mosse_fatte == 9:
                    stampa_scacchiera(scacchiera)
                    print("Pareggio!")
                    salva_partita(id_X, id_O, None)
                    aggiorna_statistiche(id_X, vittoria=False)
                    aggiorna_statistiche(id_O, vittoria=False)
                    print("Risultato salvato nel database.")
                    break

                giocatore_corrente = "O" if giocatore_corrente == "X" else "X"
            else:
                print("Cella già occupata! Riprova.")

        except ValueError:
            print("Input non valido! Inserisci un numero intero.")

if __name__ == "__main__":
    gioca_db()
