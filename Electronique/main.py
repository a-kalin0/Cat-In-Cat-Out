from gpiozero import MotionSensor
from picamera import PiCamera

#fonction pour prendre une photo
#def capture_photo():

def main():
    pir = MotionSensor(4)
    #camera = PiCamera()
    print("Demarrage du script")

    while True:
        pir.wait_for_motion()
        print("Mouvement détecté !")

        # Ici appelle de la fonction pour prendre une photo quand le capteur detecte un mouvement
        # capture_photo()

        pir.wait_for_no_motion()
        print("Aucun mouvement détecté.")

if __name__ == "__main__":
    main()
