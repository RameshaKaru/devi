import multiprocessing
from threading import Thread

import displayapp2
import fspeechtotext
import ftexttospeech
import ftoarduino
import autodetect
import live_run
import fnlp

from time import sleep
import serial
import signal
import cv2 as cv2

ser = serial.Serial('/dev/ttyUSB0', 9600)  # Establish the connection on a specific port

sleep(2)


def autodet():
    while(True):
        if displayapp2.flag1 ==1:
            print "auto detect"
            pathlist= autodetect.auto_run()
            if pathlist == None:
                displayapp2.flag1 = 0
            else:
                print pathlist[1]

                text_out = fspeechtotext.speechtotext(pathlist[1],pathlist[0])
                if text_out != '':
                    nlp_out = fnlp.nlpcall(text_out)
                    convo= nlp_out.split()
                    print "to arduino"
                    ftoarduino.toarduino(nlp_out)
                    #sleep(5)
                    ftexttospeech.texttospeech(nlp_out)
                    print "end"
                    if "Bye" in convo:
                        break
                else:
                    print "Audio is not properly captured"


def showapp():
    app = displayapp2.receptionistApp()
    app.geometry("800x480")
    app.title("ENTC Robot Receptionist")

    noise = Thread(target=autodet)
    noise.start()
    app.mainloop()
    noise.join()


def proxface():

    ftoarduino.endConv()

    while (1):

        while ser.in_waiting:
            list1 = []
            comd = ''
            a = ser.read()
            if (a != '<'):
                continue
            elif (a == '<'):
                while (1):
                    if ser.in_waiting:
                        cha = ser.read()
                        if cha == '>':
                            break
                        else:
                            list1.append(cha)
            print list1
            for i in range(len(list1)):
                comd = comd + list1[i]
            print comd

            if comd== "det":

                signal.signal(signal.SIGALRM, handler)
                signal.alarm(25)
                nofaceflag=0
                try:
                    video_capture = cv2.VideoCapture(0)
                    person = live_run.runface(video_capture)
                except Exception, exc:
                    print exc
                    video_capture.release()
                    cv2.destroyAllWindows()
                    nofaceflag=1
                    ftoarduino.endConv()
                    print "face not detected1"
                signal.alarm(0)

                if nofaceflag==0:
                    if person == "unknown":
                        print "unknown"
                        ftoarduino.greet()
                        text_out = "Welcome to the department of E N T C."
                        print text_out
                        ftexttospeech.texttospeech(text_out)
                        ftoarduino.middle()
                        sleep(8)
                        ftexttospeech.texttospeech("Can you please enter your name?")
                    elif person == "0":

                        print "exit face"
                        ftoarduino.endConv()

                    else:

                        print "name done"
                        ftoarduino.greet()
                        text_out = "Welcome to the department of E N T C " + person
                        print text_out
                        ftexttospeech.texttospeech(text_out)
                        ftoarduino.middle()
                        sleep(8)
                        ftexttospeech.texttospeech("What can I do for you")

        def handler(signum, frame):
            print "Face not detected"
            raise Exception("end of time")



if __name__ == '__main__':

    person = ""

    app = multiprocessing.Process(target=showapp)
    prox = multiprocessing.Process(target=proxface)


    app.start()

    prox.start()








