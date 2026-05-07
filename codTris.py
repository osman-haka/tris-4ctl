scacchiera = ["_"] * 9


# Funzione per stampare la scacchiera
def stampa_scacchiera(scacchiera):
    print(f"\n {scacchiera[0]} | {scacchiera[1]} | {scacchiera[2]}")
    print(f" {scacchiera[3]} | {scacchiera[4]} | {scacchiera[5]}")
    print(f" {scacchiera[6]} | {scacchiera[7]} | {scacchiera[8]}\n")


# Test
stampa_scacchiera(scacchiera)
def fai_mossa(scacchiera, posizione, giocatore):
    # Controlla se la posizione è libera
    if scacchiera[posizione] == "_":
        scacchiera[posizione] = giocatore
        return True
    else:
        return False
def ha_vinto(scacchiera, giocatore):
    combinazioni_vincenti = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Righe
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Colonne
        [0, 4, 8], [2, 4, 6]             # Diagonali
    ]
   
    for combo in combinazioni_vincenti:
     
        if scacchiera[combo[0]] == scacchiera[combo[1]] == scacchiera[combo[2]] == giocatore:
            return True
    return False
def gioca():
    nome_X = input("Nome del gicatore che usa X: ")
    nome_O = input("Nome del gicatore che usa O: ")

    scacchiera = ["_"] * 9
    giocatore_corrente = "X"
    mosse_fatte = 0


    print("Benvenuto a Tris! Inserisci un numero da 0 a 8 per muovere.")


    while True:
        stampa_scacchiera(scacchiera)
        nome_turno = nome_X if giocatore_corrente == "X" else nome_O
        try:
            mossa = int(input(f"Turno di {giocatore_corrente}. Inserisci posizione (0-8): "))
           
            if mossa < 0 or mossa > 8:
                print("Errore: il numero deve essere tra 0 e 8!")
                continue
               
            if fai_mossa(scacchiera, mossa, giocatore_corrente):
                mosse_fatte += 1
               
                # Controllo vittoria
                if ha_vinto(scacchiera, giocatore_corrente):
                    stampa_scacchiera(scacchiera)
                    print(f"Complimenti! Il giocatore {giocatore_corrente} ha vinto!")
                    break
               
                # Controllo pareggio (scacchiera piena)
                if mosse_fatte == 9:
                    stampa_scacchiera(scacchiera)
                    print("Pareggio!")
                    break
               
                # Cambio turno
                giocatore_corrente = "O" if giocatore_corrente == "X" else "X"
            else:
                print("Cella già occupata! Riprova.")
               
        except ValueError:
            print("Input non valido! Inserisci un numero intero.")


# Avvia la partita
gioca()
