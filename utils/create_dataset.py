import cv2
import os


# Funzione per acquisire immagini dalla fotocamera
def start_capture(name):

    # Percorso della cartella dove verranno salvate le immagini
    path = "../data/" + name
    num_of_images = 0  # Contatore delle immagini acquisite

    # Inizializzazione del classificatore di volti di Haar
    detector = cv2.CascadeClassifier("../data/haarcascade_frontalface_default.xml")

    try:
        os.makedirs(path)  # Crea la cartella se non esiste già
    except FileExistsError:
        print('Directory Already Created')

    vid = cv2.VideoCapture(1)  # Inizializzazione del video dalla fotocamera

    while True:

        ret, img = vid.read()  # Cattura un frame dalla fotocamera
        new_img = None  # Inizializza una variabile per l'immagine del volto rilevato
        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Conversione del frame in scala di grigi
        face = detector.detectMultiScale(image=grayimg, scaleFactor=1.1, minNeighbors=5)  # Rilevamento dei volti

        """
        image=grayimg: immagine su cui viene eseguito il rilevamento dei volti
        scaleFactor=1.1: riduzione dell'immagine ad ogni scala successiva durante il rilevamento
        minNeighbors=5: numero minimo di vicini per confermare il rilevamento di un volto
        """

        # Itera sui volti rilevati
        for x, y, w, h in face:
            # Disegna un rettangolo intorno al volto
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)
            # Aggiungi testo "Face Detected"
            cv2.putText(img, "Face Detected", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            # Aggiungi il numero di immagini catturate
            cv2.putText(img, str(str(num_of_images) + " images captured"), (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 0, 255))
            # Estrai l'immagine del volto
            new_img = img[y:y + h, x:x + w]

            # Mostra il frame con i volti rilevati
        cv2.imshow("Face Detection", img)

        key = cv2.waitKey(1) & 0xFF  # Attendi la pressione di un tasto

        try:
            # Salva l'immagine del volto nella cartella specificata
            cv2.imwrite(str(path + "/" + str(num_of_images) + name + ".jpg"), new_img)
            num_of_images += 1  # Incrementa il contatore delle immagini acquisite
        except Exception as e:
            print(f"Error saving image: {e}")

        # Esci dal ciclo se viene premuto 'q' o se il numero massimo di immagini è stato raggiunto
        if key == ord("q") or key == 27 or num_of_images > 300:
            break

    # Chiude la finestra del video e tutte le finestre OpenCV
    vid.release()
    cv2.destroyAllWindows()
    return num_of_images  # Restituisci il numero totale di immagini acquisite

