from utils.create_dataset import start_capture
from utils.create_classifier import train_classifier
from utils.Detector import main


def perform_face_recognition():
    """
    Funzione che esegue il riconoscimento facciale utilizzando le funzionalità
    fornite dai moduli create_dataset, create_classifier e Detector.
    """
    # Avvio dell'acquisizione del dataset
    num_images_captured = start_capture()

    # Verifica se è stato catturato un numero sufficiente di immagini
    if num_images_captured < 300:
        print("Errore: non sono state catturate abbastanza immagini.")
        return

    # Addestramento del classificatore utilizzando le immagini acquisite
    train_classifier()

    # Avvio dell'applicazione di riconoscimento facciale
    main()
