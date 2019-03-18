from time import sleep
import serial

PORT = '/dev/ttyUSB0'
BAUD_RATE= 9600

ser = serial.Serial(PORT, BAUD_RATE)


def toarduino(command):

    cmd = command.split()
    if 'left' in cmd:

        print "Left Command"
        ser.write("<lnh>")

        return

    elif 'right' in cmd:

        print "Right Command"
        ser.write("<rnh>")

        return

    elif 'Bye' in cmd:

        print "Conversation end"
        ser.write("<ce>")

        return


def greet():

    ser.write('<gr>')
    print "Greet command"


def showleft():

    ser.write('<lnh>')
    print "Show left command"



def showright():

    ser.write('<rnh>')
    print "Show right command"


def endConv():

    print "Conversation end"
    ser.write("<ce>")


def middle():
    print "go to middle"
    ser.write("<mid>")

def introd():
    print "introduction"
    ser.write("<in>")









