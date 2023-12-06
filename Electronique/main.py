from gpiozero import MotionSensor
from picamera2 import Picamera2
import send_data
import time
import cv2
import os

# Configuration de la caméra
camera = Picamera2()

# Configuration des capteurs de mouvement
pir_out = MotionSensor(4)  # Capteur OUT
pir_in = MotionSensor(27)  # Capteur IN

try:
    print("Attente du mouvement. Appuyez sur Ctrl+C pour quitter.")
    time.sleep(2)  # Attend que le capteur s'initialise

    while True:
        if pir_out.motion_detected or pir_in.motion_detected:
            print("Mouvement détecté! Enregistrement de la vidéo.")

            # Détermine quel capteur a détecté le mouvement en premier
            sensor_trigger = "in" if pir_in.motion_detected else "out"

            # Récupère la date et l'heure pour le nom de fichier
            timestamp = time.strftime("%d-%m-%y-%H-%M-%S", time.localtime())
            filename = f"/home/cico/Pictures/{sensor_trigger}-{timestamp}.mp4"

            # Enregistre la vidéo pendant 10 secondes
            camera.start_and_record_video(filename, duration=10)
            print(f"Vidéo enregistrée")
            
            # Ouvre la vidéo
            video_path = filename
            cam = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
            
            # Construit le dictionnaire pour les frames
            frames_dict = {}
            open_files = []  # Liste pour stocker les références aux fichiers ouverts

            frame_count = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
            start_frame = frame_count - 4 if sensor_trigger == "in" else 0

            # Positionne la vidéo sur le bon début de frame
            cam.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

            # Enregistre les 4 frames pertinentes
            for i in range(4):
                ret, frame = cam.read()
                if ret:
                    image_path = f"/home/cico/Pictures/{sensor_trigger}-{timestamp}_frame{i+1}.jpg"
                    cv2.imwrite(image_path, frame)
                    print(f"Image {sensor_trigger}-{timestamp}_frame{i+1}.jpg créée avec succès pour la vidéo {filename}")
                    
                    # Ouvre le fichier image et l'ajoute au dictionnaire
                    img_file = open(image_path, 'rb')
                    frames_dict[f"frame{i+1}"] = (os.path.basename(image_path), img_file, 'image/jpg')
                    open_files.append(img_file)  # Ajoute le fichier ouvert à la liste

            cam.release()
            
            # Appel de la fonction send_data
            send_data.send_data(frames_dict)
            print("Données envoyées", frames_dict)

            # Ferme tous les fichiers ouverts
            for file in open_files:
                file.close()

        else:
            print("Aucun mouvement détecté.")
            time.sleep(1)

except KeyboardInterrupt:
    print("Test terminé.")
    camera.close()
