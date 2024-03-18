import numpy as np
from PIL import Image
import os
import cv2


# Metodo per addestrare un classificatore personalizzato per riconoscere il volto
def train_classifier(name):
    # Leggi tutte le immagini nel dataset personalizzato
    path = f"../data/{name}/"
    faces = []
    ids = []

    # Memorizza le immagini in formato numpy e gli ID dell'utente nella stessa posizione in imageNp e nella lista id
    for root, dirs, files in os.walk(path):
        for pic in files:
            imgpath = os.path.join(root, pic)
            img = Image.open(imgpath).convert('L')  # Converti l'immagine in scala di grigi
            imageNp = np.array(img, 'uint8')  # Converti l'immagine in un array numpy di interi senza segno a 8 bit
            id = int(pic.split(name)[0])  # Estrai l'ID dell'utente dall'immagine
            faces.append(imageNp)  # Aggiungi l'immagine all'elenco delle facce
            ids.append(id)  # Aggiungi l'ID dell'utente all'elenco degli ID

    ids = np.array(ids)  # Converti la lista degli ID in un array numpy

    # Addestra e salva il classificatore
    classifier_path = "../data/classifiers/"
    # Crea la directory dei classificatori se non esiste già
    os.makedirs(classifier_path, exist_ok=True)
    classifier_file = os.path.join(classifier_path, f"{name}_classifier.xml")

    # Create an instance of the LBPH face recognizer
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.save(classifier_file)
