from gpiozero import MotionSensor
from picamera2 import Picamera2
import time

# Temps en secondes après lequel la caméra sera éteinte en l'absence de mouvement
TEMPS_INACTIVITE_MAX = 10

def main():
    pir = MotionSensor(4)
    camera = Picamera2() 

    print("Démarrage du script")

    time_since_motion = 0  # Initialiser la variable à l'extérieur de la boucle
    camera_active = True
    camera.start_preview()

    while True:
        if pir.motion_detected:
            print("Mouvement détecté!")
            time_since_motion = 0 # Réinitialiser le compteur de temps d'inactivité
            if not camera_active:
                camera = Picamera2()
                camera.start_preview()
                camera_active = True
                print("la caméra est réactiver")
        else:
            time.sleep(1)  # Attendre une seconde
            time_since_motion += 1

            print(time_since_motion)
            if camera_active and time_since_motion >= TEMPS_INACTIVITE_MAX:
                print(f"Aucun mouvement depuis {TEMPS_INACTIVITE_MAX} secondes. Désactivation de la caméra.")
                camera.close()
                camera_active = False


if __name__ == "__main__":
    main()

