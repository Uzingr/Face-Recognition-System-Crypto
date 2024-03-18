import tkinter as tk
from tkinter import ttk


class LoggedUsersPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Creazione e posizionamento dei widget nella finestra
        tk.Label(self, text="Logged Users", font=self.controller.title_font, fg="#263942").grid(row=0, column=0, pady=10, padx=5)
        self.user_label = tk.Label(self, text="", font='Helvetica 10')
        self.user_label.grid(row=1, column=0, padx=10, pady=5)

        # Stile dei bottoni
        button_style = {"fg": "#263942", "bg": "#ffffff"}

        # Frame per i bottoni
        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        # Bottone per tornare alla StartPage
        button_back = tk.Button(button_frame, text="Back to Home", command=lambda: controller.show_frame("StartPage"),
                                **button_style)
        button_back.grid(row=0, column=0, padx=20, pady=30, sticky="ew")

        # Creazione della tabella per visualizzare gli utenti loggati
        self.tree = ttk.Treeview(self, columns=("Time", "Result"))
        self.tree.heading("#0", text="Username")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Result", text="Result")
        self.tree.column("#0", width=150)
        self.tree.column("Time", width=150)
        self.tree.column("Result", width=150)
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Aggiungi uno scrollbar per la tabella
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Ridimensiona la tabella per espanderla a tutto schermo nella finestra
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Carica gli utenti loggati e aggiungili alla tabella
        self.load_logged_users()

    def load_logged_users(self):
        # Apri il file dei log e leggi le informazioni
        with open("../database/login_log.txt", "r") as file:
            lines = file.readlines()

        # Per ogni riga nel file, aggiungi le informazioni alla tabella
        for line in lines:
            username, timestamp, result = line.strip().split(",")
            self.tree.insert("", "end", text=username, values=(timestamp, result))

        # Ridimensiona le colonne in base al contenuto
        self.tree.column("#0", width=self.tree.column("#0", option="minwidth"))
        self.tree.column("Time", width=self.tree.column("Time", option="minwidth"))
        self.tree.column("Result", width=self.tree.column("Result", option="minwidth"))


