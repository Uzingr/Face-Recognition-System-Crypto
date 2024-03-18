import tkinter as tk
from PIL import Image, ImageTk
from utils.Detector import main
from datetime import datetime


class CheckFace(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Frame per contenere l'immagine, la label e i bottoni
        content_frame = tk.Frame(self)
        content_frame.pack(expand=True, fill="both", padx=70, pady=20)

        # Caricamento e ridimensionamento dell'immagine
        image = Image.open("../utils/images/icon3.png")
        resized_image = image.resize((350, 180))
        self.render = ImageTk.PhotoImage(resized_image)

        # Creazione e posizionamento dell'immagine
        img = tk.Label(content_frame, image=self.render)
        img.grid(row=0, column=0, columnspan=2, pady=(20, 10))  # Centrato verticalmente con padding sopra e sotto

        # Creazione e posizionamento della label
        label = tk.Label(content_frame, text="Facial Recognition", fg="#263942", font='Helvetica 16 bold')
        label.grid(row=1, column=0, columnspan=2, pady=(0, 10))  # Centrato verticalmente con padding sopra

        # Frame per contenere i bottoni
        button_frame = tk.Frame(content_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)  # Centrato verticalmente

        # Stile dei bottoni
        button_style = {"fg": "#263942", "bg": "#ffffff"}

        # Creazione e posizionamento dei bottoni
        button1 = tk.Button(button_frame, text="Start Recognition", command=self.start_recognition, **button_style)
        button2 = tk.Button(button_frame, text="Go to Home Page",
                            command=lambda: self.controller.show_frame("StartPage"), **button_style)

        button1.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        button2.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        # Centratura della label e dei bottoni nel frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def start_recognition(self):
        # Avvia il riconoscimento facciale
        result = main(self.controller.active_name)

        # Salva il risultato nella tabella dei log
        self.log_recognition_result(self.controller.active_name, result)

    def log_recognition_result(self, username, result):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Determina il testo del log in base all'esito del riconoscimento
        if result:
            log_text = "Utente riconosciuto"
        else:
            log_text = "Utente non riconosciuto"

        # Scrive il log nella tabella degli accessi
        with open("../database/login_log.txt", "a") as log_file:
            log_file.write(f"{username},{timestamp},{log_text}\n")
        self.controller.frames["LoggedUsersPage"].tree.insert("", "end", text=username, values=(timestamp, log_text))