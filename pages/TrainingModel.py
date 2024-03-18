import tkinter as tk
from tkinter import messagebox
from utils.face_recognition import start_capture, train_classifier
from PIL import Image, ImageTk


class TrainingModel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Carica l'immagine e ridimensiona mantenendo le proporzioni
        image_path = "../utils/images/userlog.png"
        image = Image.open(image_path)
        image_height = 200
        image_width = int(image.width * image_height / image.height)
        image = image.resize((image_width, image_height))
        self.logo = ImageTk.PhotoImage(image)

        # Aggiungi l'immagine al frame
        self.logo_label = tk.Label(self, image=self.logo)
        self.logo_label.pack(pady=(10, 10))

        # Creazione e posizionamento della label
        self.img_label = tk.Label(self, text="Model Training", fg="#263942", font='Helvetica 16 bold')
        self.img_label.pack(pady=(0, 10))  # Centrato verticalmente con padding sopra

        # Stile dei bottoni
        button_style = {"fg": "#263942", "bg": "#ffffff"}
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        # Prima riga di bottoni
        button_row1 = tk.Frame(button_frame)
        button_row1.pack(side="top", pady=5)

        # Bottone per catturare le immagini
        self.capture_button = tk.Button(button_row1, text="Save Images", command=self.capimg, **button_style)
        # Bottone per addestrare il modello
        self.train_button = tk.Button(button_row1, text="Model Train", command=self.trainmodel, **button_style)

        self.capture_button.pack(side="left", padx=20)
        self.train_button.pack(side="left", padx=20)

        # Seconda riga di bottoni
        button_row2 = tk.Frame(button_frame)
        button_row2.pack(side="top", pady=5)

        # Bottone per tornare alla StartPage
        self.buttoncanc = tk.Button(button_row2, text="Back to Home",
                                    command=lambda: controller.show_frame("StartPage"), **button_style)

        self.buttoncanc.pack(side="left", padx=20)

    # Metodo per catturare le immagini del volto
    def capimg(self):
        # Mostra un messaggio con le istruzioni per la cattura delle immagini
        messagebox.showinfo("INSTRUCTIONS", "We will capture 300 pictures of your face")

        # Avvia la cattura delle immagini e ottiene il numero di immagini catturate
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x

        # Aggiorna l'etichetta con il numero di immagini catturate
        self.img_label.config(text=str("Number of images captured = " + str(x)))

    # Metodo per addestrare il modello di riconoscimento facciale
    def trainmodel(self):
        # Controlla se sono state catturata un numero sufficiente di immagini
        if self.controller.num_of_images < 300:
            messagebox.showerror("ERROR", "Not enough data. Capture at least 300 images!")
            return

        # Addestra il modello con le immagini catturate
        train_classifier(self.controller.active_name)

        # Mostra un messaggio di successo dopo l'addestramento del modello
        messagebox.showinfo("SUCCESS", "The model has been successfully trained!")

        # Passa alla pagina per il controllo del volto
        self.controller.show_frame("CheckFace")
