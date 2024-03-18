import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox

# Import delle classi dai file
from StartPage import StartPage
from SignUp import SignUp
from pages.CheckCredential import CheckCredential
from TrainingModel import TrainingModel
from pages.CheckFace import CheckFace
from LoggedUsersPage import LoggedUsersPage
from EncryptionPage import EncryptionPage


# Classe per la GUI principale
class MainUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.logged_users_page = None  # Attributo per memorizzare l'istanza di LoggedUsersPage

        # Impostazioni generali della finestra
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("Face Recognizer")
        self.resizable(False, False)
        self.geometry("500x350")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Creazione di un contenitore per i frame della GUI
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        # Ciclo per creare e inizializzare i frame della GUI
        for F in (StartPage, SignUp, CheckCredential, TrainingModel, CheckFace, LoggedUsersPage, EncryptionPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Visualizzazione del frame di avvio
        self.show_frame("StartPage")

    # Funzione per mostrare un frame specifico
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    # Funzione per gestire la chiusura dell'applicazione
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            self.destroy()


# Creazione dell'istanza dell'applicazione principale e avvio del loop principale
if __name__ == "__main__":
    app = MainUI()
    app.iconphoto(True, tk.PhotoImage(file='../utils/images/logo.png'))
    app.mainloop()

