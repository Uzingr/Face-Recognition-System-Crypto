import tkinter as tk
from tkinter import messagebox, ttk
from utils.password_utils import load_passwords, save_passwords, hash_password
from PIL import Image, ImageTk


class SignUp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Impostiamo un margine superiore per la prima riga del frame
        self.grid_rowconfigure(0, pad=20)

        # Carica l'immagine e ridimensiona mantenendo le proporzioni
        image_path = "../utils/images/login.png"
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

        # Bottoni per tornare alla StartPage, procedere e cancellare l'input
        self.buttoncanc = tk.Button(button_frame, text="Back to Home", command=lambda: controller.show_frame("StartPage"), **button_style)
        self.buttonext = tk.Button(button_frame, text="Next", command=self.start_training, **button_style)
        self.buttonclear = tk.Button(button_frame, text="Clear", command=self.clear, **button_style)

        self.buttoncanc.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.buttonext.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        self.buttonclear.grid(row=0, column=2, padx=20, pady=10, sticky="ew")

    def start_training(self):
        # Ottieni il nome utente e la password inseriti
        name = self.user_name.get()
        password = self.password.get()

        # Controlla se il nome utente e la password sono stati inseriti
        if not name:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        if not password:
            messagebox.showerror("Error", "Password cannot be empty!")
            return

        # Controlla se il nome utente è disponibile
        if name in load_passwords():
            messagebox.showerror("Error", "Username not available")
            return

        # Salvataggio del nome utente e della password dopo l'hashing
        passwords = load_passwords()
        hashed_password = hash_password(password)
        passwords[name] = hashed_password
        save_passwords(passwords)

        # Mostra un messaggio di successo e passa alla pagina di training del modello
        messagebox.showinfo("Success", "User registered successfully!")
        self.controller.active_name = name
        self.controller.show_frame("TrainingModel")

    def clear(self):
        # Cancella il contenuto dell'entry relative a username e password
        self.user_name.delete(0, 'end')
        self.password.delete(0, 'end')

    def toggle_password_visibility(self):
        # Mostra o nasconde la password quando il pulsante viene premuto
        current_show_state = self.password.cget("show")
        if current_show_state == "*":
            self.password.config(show="")
            self.show_password_btn.config(text="Hide Pw")
        else:
            self.password.config(show="*")
            self.show_password_btn.config(text="Show Pw")
