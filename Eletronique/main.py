from picamera2 import Picamera2
from gpiozero import MotionSensor
import time
import cv2
import os
import send_data

# Configuration de la caméra
camera = Picamera2()

# Configuration du capteur de mouvement
pir = MotionSensor(4)  

try:
    print("Attente du mouvement. Appuyez sur Ctrl+C pour quitter.")
    time.sleep(2)  # Attendez que le capteur s'initialise

    while True:
        if pir.motion_detected:
            print("Mouvement détecté! Enregistrement de la vidéo.")

            # Récupère l'heure actuelle pour le nom du fichier
            current_time = time.localtime()
            filename = f"{current_time.tm_hour}-{current_time.tm_min}-{current_time.tm_sec}.mp4"

            # Enregistre la vidéo pendant 10 secondes
            camera.start_and_record_video(filename, duration=10)
            print(f"Vidéo enregistrée : {filename}")
            
            # Ouvre la vidéo
            video_path = filename
            cam = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
            
            # Construit le dictionnaire pour les frames
            frames_dict = {}
    
            # Enregistre les 4 premières frames
            for i in range(4):
                ret, frame = cam.read()

                if ret:
                    # Obtient le nom de la vidéo sans l'extension
                    video_name_without_extension = os.path.splitext(os.path.basename(video_path))[0]

                    # Construit le chemin du fichier image
                    image_path = f"/home/cico/Pictures/{video_name_without_extension}_frame{i+1}.jpg"

                    # Enregistre l'image
                    cv2.imwrite(image_path, frame)
                    print(f"Image {video_name_without_extension}_frame{i+1}.jpg créée avec succès pour la vidéo {filename}")
                    
                    # Ajoute le chemin de l'image au dictionnaire
                    frames_dict[f"frame{i+1}"] = open(image_path, 'rb')

            # Ferme la vidéo
            cam.release()
            # appel de la fonction tati
            send_data(frames_dict)
           # print(frames_dict)

        else:
            print("Aucun mouvement détecté.")
            time.sleep(1)  # Délai entre les lectures

except KeyboardInterrupt:
    print("Test terminé.")
    # Ferme la caméra à la fin
    camera.close()
