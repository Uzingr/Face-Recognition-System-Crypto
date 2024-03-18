import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Frame per contenere l'immagine, la label e i bottoni
        content_frame = tk.Frame(self)
        content_frame.pack(expand=True, fill="both", padx=80, pady=10)

        # Caricamento e ridimensionamento dell'immagine
        image = Image.open("../utils/images/logo.png")
        resized_image = image.resize((150, 150))
        self.render = ImageTk.PhotoImage(resized_image)

        # Creazione e posizionamento dell'immagine
        img = tk.Label(content_frame, image=self.render)
        img.grid(row=0, column=0, columnspan=2, pady=(20, 10))  # Centrato verticalmente con padding sopra e sotto

        # Creazione e posizionamento della label
        label = tk.Label(content_frame, text="Home Page", font=self.controller.title_font, fg="#263942")
        label.grid(row=1, column=0, columnspan=2, pady=(0, 5))  # Centrato verticalmente con padding sopra

        # Stile dei bottoni
        button_style = {"fg": "#263942", "bg": "#ffffff"}

        # Frame per i bottoni
        button_frame = tk.Frame(content_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=0)  # Centrato verticalmente

        # Creazione e posizionamento dei bottoni
        button1 = tk.Button(button_frame, text="Sign up", command=lambda: self.controller.show_frame("SignUp"), **button_style)
        button2 = tk.Button(button_frame, text="Check a User", command=lambda: self.controller.show_frame("CheckCredential"), **button_style)
        button3 = tk.Button(button_frame, text="Quit", command=self.controller.on_closing, **button_style)
        button4 = tk.Button(button_frame, text="View Logged Users", command=self.admin_login, **button_style)
        button5 = tk.Button(button_frame, text="Encryption", command=lambda: self.controller.show_frame("EncryptionPage"), **button_style)

        button1.grid(row=0, column=0, padx=20, pady=5, sticky="ew")
        button2.grid(row=0, column=1, padx=20, pady=5, sticky="ew")
        button3.grid(row=2, column=0, columnspan=2, padx=20, pady=5, sticky="ew")
        button4.grid(row=1, column=1, padx=20, pady=5, sticky="ew")
        button5.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

    def admin_login(self):
        # Crea una finestra di dialogo per l'inserimento delle credenziali di amministratore
        admin_window = tk.Toplevel(self)
        admin_window.title("Admin Login")

        # Creazione dei widget per l'inserimento delle credenziali
        username_label = tk.Label(admin_window, text="Username:")
        password_label = tk.Label(admin_window, text="Password:")
        username_entry = tk.Entry(admin_window)
        password_entry = tk.Entry(admin_window, show="*")

        username_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        username_entry.grid(row=0, column=1, padx=10, pady=5)
        password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Funzione per verificare le credenziali di amministratore
        def check_admin_credentials():
            if username_entry.get() == "admin" and password_entry.get() == "admin":
                admin_window.destroy()
                self.controller.show_frame("LoggedUsersPage")
            else:
                messagebox.showerror("Error", "Invalid credentials")

        # Bottone per confermare le credenziali
        confirm_button = tk.Button(admin_window, text="Confirm", command=check_admin_credentials)
        confirm_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Centra la finestra di dialogo rispetto alla finestra principale
        admin_window.geometry("+{}+{}".format(
            int(self.winfo_rootx() + self.winfo_width() / 2 - admin_window.winfo_reqwidth() / 2),
            int(self.winfo_rooty() + self.winfo_height() / 2 - admin_window.winfo_reqheight() / 2)
        ))
        admin_window.transient(self)
        admin_window.grab_set()

