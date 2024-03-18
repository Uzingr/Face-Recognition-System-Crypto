import os
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
from PIL import Image, ImageTk


class EncryptionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Frame principale per il contenuto
        content_frame = tk.Frame(self)
        content_frame.pack(expand=True)

        # Aggiungiamo colonne vuote a sinistra e a destra dell'immagine
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(3, weight=1)

        # Caricamento e ridimensionamento dell'immagine
        image_path = "../utils/images/login-3.png"
        image = Image.open(image_path)
        resized_image = image.resize((250, 170))
        self.render = ImageTk.PhotoImage(resized_image)

        # Creazione e posizionamento dell'immagine
        img = tk.Label(content_frame, image=self.render)
        img.grid(row=0, column=0, columnspan=3, sticky="nsew")

        # Aggiungiamo una label per inserire il nome della cartella
        tk.Label(content_frame, text="Username:").grid(row=1, column=0, pady=5)

        # Aggiungiamo un Entry per il nome della cartella
        self.folder_name_entry = tk.Entry(content_frame)
        self.folder_name_entry.grid(row=1, column=1, columnspan=2, pady=5, sticky="w")

        # Aggiungiamo un pulsante per avviare l'encryption
        self.encrypt_button = tk.Button(content_frame, text="Encryption", command=self.encrypt_folder)
        self.encrypt_button.grid(row=2, column=0, columnspan=1, pady=5)

        # Aggiungiamo un pulsante per avviare la decifratura
        self.decrypt_button = tk.Button(content_frame, text="Decryption", command=self.decrypt_folder)
        self.decrypt_button.grid(row=2, column=2, columnspan=1, pady=5)

        # Aggiungiamo un pulsante per tornare alla StartPage
        self.back_button = tk.Button(content_frame, text="Go to Home Page",
                                     command=lambda: self.controller.show_frame("StartPage"))
        self.back_button.grid(row=3, column=0, columnspan=3, pady=5)

        # Chiave utilizzata per la cifratura
        self.encryption_key = None

    def encrypt_folder(self):
        # Otteniamo il nome della cartella inserito dall'utente
        folder_name = self.folder_name_entry.get()

        # Verifichiamo se il nome della cartella è stato inserito
        if not folder_name:
            messagebox.showerror("Errore", "Inserire il nome della cartella!")
            return

        # Verifichiamo se la cartella esiste
        folder_path = os.path.join("../data", folder_name)
        if not os.path.exists(folder_path):
            messagebox.showerror("Errore", "La cartella specificata non esiste!")
            return

        # Generiamo la chiave di cifratura
        self.encryption_key = Fernet.generate_key()

        # Eseguiamo l'encryption dei file nella cartella
        encrypt_directory(self.encryption_key, folder_path)

        messagebox.showinfo("Successo", f"I file nella cartella '{folder_name}' sono stati cifrati con successo!")

    # Funzione per avviare la decifratura della cartella
    def decrypt_folder(self):
        # Otteniamo il nome della cartella inserito dall'utente
        folder_name = self.folder_name_entry.get()

        # Verifichiamo se il nome della cartella è stato inserito
        if not folder_name:
            messagebox.showerror("Errore", "Inserire il nome della cartella!")
            return

        # Verifichiamo se la cartella esiste
        folder_path = os.path.join("../data", folder_name)
        if not os.path.exists(folder_path):
            messagebox.showerror("Errore", "La cartella specificata non esiste!")
            return

        # Verifica se la chiave di cifratura è stata generata
        if not self.encryption_key:
            messagebox.showerror("Errore", "Nessuna chiave di cifratura disponibile!")
            return

        # Eseguiamo la decifratura dei file nella cartella
        decrypt_directory(self.encryption_key, folder_path)

        messagebox.showinfo("Successo", f"I file nella cartella '{folder_name}' sono stati decifrati con successo!")


def encrypt_directory(key, directory):
    fernet = Fernet(key)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith(".enc"):
                filename = os.path.join(root, file)
                with open(filename, "rb") as f:
                    data = f.read()
                encrypted_data = fernet.encrypt(data)
                with open(filename + ".enc", "wb") as f:
                    f.write(encrypted_data)
                os.remove(filename)


def decrypt_directory(key, directory):
    fernet = Fernet(key)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".enc"):
                filename = os.path.join(root, file)
                with open(filename, "rb") as f:
                    encrypted_data = f.read()
                decrypted_data = fernet.decrypt(encrypted_data)
                with open(filename[:-4], "wb") as f:  # Rimuovi l'estensione .enc dal nome del file
                    f.write(decrypted_data)
                os.remove(filename)
