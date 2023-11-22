from gpiozero import MotionSensor
from picamera import PiCamera
import time

# Temps en secondes après lequel la caméra sera éteinte en l'absence de mouvement
TEMPS_INACTIVITE_MAX = 300

#def capture_photo():
    # Implémentez la logique pour prendre une photo
    #pass

def main():
    pir = MotionSensor(4)
    camera = PiCamera()
    camera.start_preview()  # Démarrez la prévisualisation

    dernier_mouvement = time.time()

    print("Démarrage du script")

    try:
        while True:
            if pir.motion_detected:
                print("Mouvement détecté !")
                capture_photo()
                dernier_mouvement = time.time()

            # Vérifiez le temps écoulé depuis le dernier mouvement
            temps_inactivite = time.time() - dernier_mouvement

            if temps_inactivite > TEMPS_INACTIVITE_MAX:
                # Éteignez la caméra en cas d'inactivité
                camera.stop_preview()
                print("Mode veille activé.")
                while not pir.motion_detected:
                    time.sleep(1)
                # Redémarre la caméra lorsque le mouvement est détecté
                camera.start_preview()
                dernier_mouvement = time.time()

    except KeyboardInterrupt:
        # Gestion de l'arrêt du script avec Ctrl+C
        print("Arrêt du script")
    finally:
        camera.stop_preview()
        camera.close()

if __name__ == "__main__":
    main()
