import cv2
from djitellopy import Tello
from time import sleep
from threading import Thread

tello = Tello()
tello.connect()


keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()

def videoRecorder():
    # create a VideoWrite object, recoring to ./video.avi
    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter('mission4.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        sleep(1 / 30)



# we need to run the recorder in a seperate thread, otherwise blocking options
#  would prevent frames from getting added to the video

recorder = Thread(target=videoRecorder)
recorder.start()

tello.takeoff()
print(tello.get_height())
tello.move_up(20)
tello.move_down(30)
print(tello.get_height())
tello.move_left(20)
tello.move_right(20)
tello.flip("l")
tello.flip("r")
tello.flip("b")
tello.move_forward(20)
cv2.imwrite("mission4.png", frame_read.frame)

tello.rotate_counter_clockwise(180)
#tello.flip("f")

tello.land()
print(tello.get_battery())

keepRecording = False
tello.streamoff()
recorder.join()
