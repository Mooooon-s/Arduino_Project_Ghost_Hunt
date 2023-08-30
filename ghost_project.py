from Arduino import Arduino
from Arduino.arduino import build_cmd_str
import time

class Ultrasonic(object):
   def __init__(self,board,trigPin=6,echoPin=5):
       self.board=board
       self.sr=board.sr
       self.trigPin=trigPin
       self.echoPin=echoPin
   
   def distanceMeasure(self):
       # return values are in centimeters
       cmd_str = build_cmd_str("us", (self.trigPin, self.echoPin))
       self.sr.write(cmd_str)
       self.sr.flush()
       rd = self.sr.readline().replace("\r\n", "")

       if rd.isdigit():
           return int(rd)
        

RLED=11
GLED=10
BLED=9
TMP=0

piezo =3
Button =8
echoPin = 5 #5
trigPin = 6


board=Arduino('9600')

board.pinMode(RLED,"OUTPUT")
board.pinMode(GLED,"OUTPUT")
board.pinMode(BLED,"OUTPUT")

board.pinMode(TMP,"INPUT")

board.pinMode(echoPin,"INPUT")
board.pinMode(trigPin,"OUTPUT")

board.pinMode(piezo,"OUTPUT")
board.pinMode(Button,"INPUT")

lastButton=0
currentButton=1

changeMode=False

temperature=0
startTmp=0
changeTmp=0

def debounse(last):
    current=board.digitalRead(Button)
    if last!=current:
        time.sleep(0.005)
        current=board.digitalRead(Button)
    return current

startTmp=board.analogRead(TMP)
temperature = (startTmp)/2

while True:
    duration=0
    distance=0

    currentButton = debounse(lastButton)

    if lastButton==0 and currentButton==1:
        if changeMode==False:
            changeMode=True
            board.analogWrite(GLED,255)
            board.analogWrite(BLED,255)
            board.analogWrite(RLED,255)
        else:
            changeMode=False
        print("-----------------CHANGE MODE-----------------")
    lastButton=currentButton

    if changeMode==False:       #check temperature
        time.sleep(0.02)
        startTmp=board.analogRead(TMP);
        changeTMP=(startTmp)/2
        print "start temperature",temperature, "\tchange temperature",changeTMP

        if changeTMP<=temperature-1.0 and changeTMP>temperature-3.0:
            board.analogWrite(GLED,0) #GLED ON
            board.analogWrite(BLED,255)
            board.analogWrite(RLED,255)
            print("level 1")
        elif changeTMP<=temperature-3.0 and changeTMP>temperature-5.0:
            board.analogWrite(BLED,0) #BLED ON
            board.analogWrite(GLED,255)
            board.analogWrite(RLED,255)
            print("level 2")
        elif changeTMP<=temperature-5.0:
            board.analogWrite(RLED,0) #RLED ON
            board.analogWrite(GLED,255)
            board.analogWrite(BLED,255)
            print("level 3")
        else:
            board.analogWrite(RLED,255) #LED OFF
            board.analogWrite(GLED,255)
            board.analogWrite(BLED,255)

    elif changeMode==True:      #check wave

        us1=Ultrasonic(board,6,5)    #6, trigPin; 5, echoPin

        dis=us1.distanceMeasure()
        print "물체의 거리",dis, 'cm'

        if dis<10:
            board.digitalWrite(piezo,"HIGH")#piezo ON
            print "warning GHOST"
            time.sleep(0.02)
            board.digitalWrite(piezo,"LOW")#piezo OFF
        time.sleep(0.5)




        #echo를 받아오지 못함
        #board.digitalWrite(trigPin,"HIGH")  #wave ON
        
        
        #pulse_start = time.time()
        #print("pulse_start", pulse_start)
        
        #time.sleep(0.01)
        # board.digitalWrite(trigPin,"LOW")   #wave OFF

        #pulse_end = time.time()

        #a = board.digitalRead(echoPin)
        #b = board.digitalRead(trigPin)
        #print('a:', a,"echo:",b)
        #while board.digitalRead(echoPin)==0: #start time
        #    pulse_end=time.time()
        #    print("in while")
        #print("out")

        #board.digitalWrite(trigPin,"LOW")   #wave OFF
        #print("pulse_end", pulse_end)
        
        # while board.digitalRead(echoPin)==1:#end time
        #     pulse_end=time.time()

        #duration = pulse_end-pulse_start #duration time
        #distance = duration*17000
        #distance = round(distance,2)

        #print(distance,"cm")

        #if distance<100:    #in 100cm
        #    board.digitalWrite(piezo,"HIGH")#piezo ON
        #    time.sleep(0.5)
        #    board.digitalWrite(piezo,"LOW")#piezo OFF









    
        
