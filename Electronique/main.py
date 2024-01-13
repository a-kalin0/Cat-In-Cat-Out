from gpiozero import MotionSensor
from picamera2 import Picamera2
import send_data
import time
import cv2
import os

def delete_video(video_path):
    """Supprime la vidéo spécifiée si elle existe."""
    try:
        if os.path.exists(video_path):
            os.remove(video_path)
            print(f"Vidéo {video_path} supprimée.")
            return True
        else:
            print(f"Vidéo {video_path} non trouvée, pas de suppression.")
            return False
    except Exception as e:
        print(f"Erreur lors de la suppression de la vidéo : {e}")
        return False

camera = Picamera2()
camera.start()

pir_out = MotionSensor(27)  
pir_in = MotionSensor(4)

try:
    print("Attente du mouvement. Appuyez sur Ctrl+C pour quitter.")
    time.sleep(2) 

    while True:
        if pir_out.motion_detected or pir_in.motion_detected:
            print("Mouvement détecté! Enregistrement de la vidéo.")

            sensor_trigger = "in" if pir_in.motion_detected else "out"

            timestamp = time.strftime("%d-%m-%y-%H-%M-%S", time.localtime())
            filename = f"/home/cico/Pictures/{sensor_trigger}-{timestamp}.mp4"

            camera.start_and_record_video(filename, duration=20)
            print(f"Vidéo enregistrée") 
            
            video_path = filename
            cam = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
            
            frames_dict = {}
            open_files = []  

            frame_count = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
            start_frame = frame_count - 4 if sensor_trigger == "in" else 0

            cam.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

            for i in range(4):
                ret, frame = cam.read()
                if ret:
                    image_path = f"/home/cico/Pictures/{sensor_trigger}-{timestamp}_frame{i+1}.jpg"
                    cv2.imwrite(image_path, frame)
                    print(f"Image {sensor_trigger}-{timestamp}_frame{i+1}.jpg créée avec succès pour la vidéo {filename}")
                    
                    img_file = open(image_path, 'rb')
                    frames_dict[f"frame{i+1}"] = (os.path.basename(image_path), img_file, 'image/jpg')
                    open_files.append(img_file)  

            cam.release()
            
            
            send_data.send_data(frames_dict)
            print("Données envoyées", frames_dict)
            
            delete_video(video_path)

            # Ferme tous les fichiers ouverts
            for file in open_files:
                file.close()

        else:
            print("Aucun mouvement détecté.")
            time.sleep(1)

except KeyboardInterrupt:
    print("Test terminé.")
    camera.close()
