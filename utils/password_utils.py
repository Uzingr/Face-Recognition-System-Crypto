import json
import bcrypt


# Funzione per caricare le password dal file JSON
def load_passwords():
    try:
        with open("../database/passwords.json", "rb") as file:
            passwords = json.load(file)  # Carica il contenuto del file JSON in un dizionario
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        passwords = {}  # Se il file non esiste o è vuoto, restituisce un dizionario vuoto
    return passwords


# Funzione per verificare se un utente esiste già nel database delle password
def check_user_exists(username):
    passwords = load_passwords()  # Carica le password dal file
    return username in passwords  # Restituisce True se l'utente esiste nel database delle password, altrimenti False


# Funzione per salvare le password nel file JSON
def save_passwords(passwords):
    with open("../database/passwords.json", "w") as file:
        json.dump(passwords, file)  # Salva il dizionario delle password nel file JSON


# Funzione per generare l'hash di una password
def hash_password(password):
    salt = bcrypt.gensalt()  # Genera un salt casuale
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)  # Genera l'hash della password
    return hashed_password.decode('utf-8')  # Restituisce l'hash come stringa UTF-8


# Funzione per verificare se una password inserita corrisponde all'hash della password memorizzata
def check_password(input_password, hashed_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))  # True: password coincidono
