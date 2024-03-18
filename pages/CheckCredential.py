import tkinter as tk
from tkinter import messagebox, ttk
from utils.password_utils import load_passwords, check_password, check_user_exists
from PIL import Image, ImageTk
from datetime import datetime


class CheckCredential(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Impostiamo un margine superiore per la prima riga del frame
        self.grid_rowconfigure(0, pad=20)

        # Carica l'immagine e ridimensiona mantenendo le proporzioni
        image_path = "../utils/images/check_user.png"
        image = Image.open(image_path)
        image_height = 150
        image_width = int(image.width * image_height / image.height)
        image = image.resize((image_width, image_height))
        self.logo = ImageTk.PhotoImage(image)

        # Aggiungi l'immagine al frame
        self.logo_label = tk.Label(self, image=self.logo)
        self.logo_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        # Label ed entry per l'inserimento dell'username
        tk.Label(self, text="Username", fg="#263942", font='Helvetica 12 bold').grid(row=1, column=0, pady=10, padx=5)
        self.user_name = ttk.Entry(self, style='Custom.TEntry')
        self.user_name.grid(row=1, column=1, pady=10, padx=10)

        # Label ed entry per l'inserimento della password
        tk.Label(self, text="Password", fg="#263942", font='Helvetica 12 bold').grid(row=2, column=0, pady=10, padx=5)
        self.password = ttk.Entry(self, show="*", style='Custom.TEntry')
        self.password.grid(row=2, column=1, pady=10, padx=10)

        # Stile dei bottoni
        button_style = {"fg": "#263942", "bg": "#ffffff"}

        # Bottone per mostrare/nascondere la password
        self.show_password_btn = tk.Button(self, text="Show pw", command=self.toggle_password_visibility,
                                           **button_style)
        self.show_password_btn.grid(row=2, column=2, padx=(0, 10), pady=10)

        # Frame per i bottoni
        button_frame = tk.Frame(self)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        # Bottoni per tornare alla Home, procedere e cancellare l'input
        self.buttoncanc = tk.Button(button_frame, text="Back to Home",
                                    command=lambda: controller.show_frame("StartPage"), **button_style)
        self.buttonext = tk.Button(button_frame, text="Next", command=self.next_foo, **button_style)
        self.buttonclear = tk.Button(button_frame, text="Clear", command=self.clear, **button_style)

        self.buttoncanc.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.buttonext.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        self.buttonclear.grid(row=0, column=2, padx=20, pady=10, sticky="ew")

    def next_foo(self):
        # Ottieni username e password inseriti
        username = self.user_name.get()
        password = self.password.get()

        # Controlla se l'username è vuoto
        if not username:
            messagebox.showerror("ERROR", "Username cannot be empty!")
            return

        # Controlla se la password è vuota
        if not password:
            messagebox.showerror("ERROR", "Password cannot be empty!")
            return

        # Verifica se l'utente esiste nel file delle password
        if not check_user_exists(username):
            messagebox.showerror("ERROR", "Username not in database")
            self.log_attempt(username, "Username not in database")
            self.controller.frames["LoggedUsersPage"].tree.insert("", "end", text=username, values=(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Username not in database"))
            return

        # Caricamento delle password e controllo
        passwords = load_passwords()
        hashed_password = passwords.get(username, b'')

        # Verifica il successo del login
        success = check_password(password, hashed_password)

        if not success:
            messagebox.showerror("ERROR", "Credenziali errate")
            # Funzione per registrare il tentativo di login nel file di log
            self.log_attempt(username, "Credenziali errate")
            self.controller.frames["LoggedUsersPage"].tree.insert("", "end", text=username, values=(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Credenziali errate"))
            return

        # Assume che il riconoscimento facciale sia stato superato
        messagebox.showinfo("Success", "Credenziali corrette")
        # Funzione per registrare il tentativo di login nel file di log
        self.log_attempt(username, "Credenziali corrette")
        self.controller.frames["LoggedUsersPage"].tree.insert("", "end", text=username, values=(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Credenziali corrette"))

        self.controller.active_name = username
        self.controller.show_frame("CheckFace")

    # Funzione che registra il tentativo di login nel file di log
    def log_attempt(self, username, result):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("../database/login_log.txt", "a") as log_file:
            log_file.write(f"{username},{timestamp},{result}\n")

    # Funzione per cancellare il contenuto dell'entry
    def clear(self):
        self.user_name.delete(0, 'end')
        self.password.delete(0, 'end')

    # Funzione che mostra o nasconde la password
    def toggle_password_visibility(self):
        current_show_state = self.password.cget("show")
        if current_show_state == "*":
            self.password.config(show="")
            self.show_password_btn.config(text="Hide pw")
        else:
            self.password.config(show="*")
            self.show_password_btn.config(text="Show pw")
