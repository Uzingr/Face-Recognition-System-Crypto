import cv2
from time import time
from tkinter import messagebox


def main(name, timeout=5):
    """
    Funzione principale dell'applicazione per il riconoscimento facciale.

    Args:
        name (str): Nome dell'utente.
        timeout (int, optional): Tempo massimo di esecuzione in secondi. Default a 5 secondi.
    """

    # Percorso del classificatore per il riconoscimento facciale dell'utente
    file_path = f"../data/classifiers/{name}_classifier.xml"

    # Caricamento del classificatore e del cascade per il riconoscimento dei volti
    face_cascade = cv2.CascadeClassifier('../data/haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(file_path)

    # Apertura della fotocamera
    cap = cv2.VideoCapture(0)

    # Flag per indicare se il volto è stato riconosciuto
    pred = False
    start_time = time()

    while True:
        ret, frame = cap.read()

        # Conversione dell'immagine in scala di grigi
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Rilevamento dei volti nell'immagine
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            # Ritaglio dell'area del volto
            roi_gray = gray[y:y + h, x:x + w]
            # Predizione del volto utilizzando il classificatore
            id, confidence = recognizer.predict(roi_gray)
            confidence = 100 - int(confidence)
            if confidence > 50:
                pred = True
                text = 'Recognized: ' + name.upper()
                color = (0, 255, 0)
            else:
                pred = False
                text = "Unknown Face"
                color = (0, 0, 255)

            # Disegno del rettangolo intorno al volto e scrittura del testo
            font = cv2.FONT_HERSHEY_PLAIN
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            frame = cv2.putText(frame, text, (x, y - 4), font, 1, color, 1, cv2.LINE_AA)

        # Visualizzazione dell'immagine con i rettangoli e i testi
        cv2.imshow("images", frame)

        # Tempo trascorso dall'inizio
        elapsed_time = time() - start_time
        if elapsed_time >= timeout:
            if pred:
                messagebox.showinfo('Verified User', 'You have already checked in')
                cap.release()  # Chiusura della fotocamera e di tutte le finestre di OpenCV
                cv2.destroyAllWindows()
                return name     # Restituisce il nome dell'utente riconosciuto
            else:
                messagebox.showerror('Alert', 'Please check in again')
                cap.release()  # Chiusura della fotocamera e di tutte le finestre di OpenCV
                cv2.destroyAllWindows()
                return None    # Restituisce None se il riconoscimento non ha avuto successo
            break

        # Interrompi il loop se viene premuto il tasto "q"
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    # Chiusura della fotocamera e di tutte le finestre di OpenCV
    cap.release()
    cv2.destroyAllWindows()
