from gpiozero import MotionSensor
from picamera2 import Picamera2
import time

# Temps en secondes après lequel la caméra sera éteinte en l'absence de mouvement
TEMPS_INACTIVITE_MAX = 10

def main():
    pir = MotionSensor(4)
    pir2 = MotionSensor(27)
    camera = Picamera2() 

    print("Démarrage du script")

    time_since_motion = 0  # Initialiser la variable à l'extérieur de la boucle
    camera_active = True

    while True:
        if pir.motion_detected or pir2.motion_detected :
            camera.start()
            print("Mouvement détecté!")
            time_since_motion = 0 # Réinitialiser le compteur de temps d'inactivité
            camera_active = True
            
            if camera.start is not None:
                camera.capture_file("test.jpg") # Vérifier si la caméra s'est bien réactiver
                print("la caméra est réactiver")
            else:
                print("La caméra n'est pas réactiver")
        else:
            time.sleep(1)  # Attendre une seconde
            time_since_motion += 1

            print(f"{time_since_motion} secondes")
            if camera_active and time_since_motion >= TEMPS_INACTIVITE_MAX:
                print(f"Aucun mouvement depuis {TEMPS_INACTIVITE_MAX} secondes. Désactivation de la caméra.")
                camera.stop()
                camera_active = False
                
                if camera.stop is not None:
                    print("La caméra est bien eteinte.")
                else:
                    camera.capture_file("test.jpg")
                    print("La caméra n'est pas éteinte car ça a pris une photo.")
    
if __name__ == "__main__":
    main()

