from picamera2 import Picamera2
from time import sleep
#from gpiozero import MotionSensor

#pir = MotionSensor(4)
picam2 = Picamera2()

picam2.start_and_capture_file("test.jpg")

sleep(5)

picam2.start_and_record_video("test.mp4", duration=5)


#while True:
#        pir.wait_for_motion()
#        print("Il y a une détection")
#        pir.wait_for_no_motion()
#        print("Il n'y a pas de détection")
