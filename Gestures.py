#!/user/bin/python

#Team Activated Almonds

import os #https://docs.python.org/3/library/os.html - This module provides a portable way of using operating system dependent functionality.
import glob #https://docs.python.org/2/library/glob.html - The glob module finds all the pathnames matching a specified pattern according to the rules used by the Unix shell, although results are returned in arbitrary order.
import subprocess #https://docs.python.org/2/library/subprocess.html - Spawn new processes to connect to their input/output/error pipe and obtain their return codes.
import RPi.GPIO as GPIO #https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/ - By doing it this way, you can refer to it as just GPIO through the rest of your script.
import time #https://docs.python.org/3/library/time.html - This module provides various time-related functions. For related functionality, see also the datetime and calendar modules.
from time import sleep #https://www.journaldev.com/15797/python-time-sleep - Python time sleep function is used to add delay in the execution of a program. We can use python sleep function to halt the execution of the program for given time in seconds. Notice that python time sleep function actually stops the execution of current thread only, not the whole program.

TRIGGER = 4
ECHO = 22
LED1 = 14
LED2 = 15
LED3 = 18
LED4 = 23
LED5 = 24
LED6 = 25
LED7 = 8
LED8 = 7
LED9 = 12
LED10 = 16
LEFT_SENSOR=27
RIGHT_SENSOR=17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_SENSOR,GPIO.IN)
GPIO.setup(RIGHT_SENSOR,GPIO.IN)

GPIO.setup(TRIGGER,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.setup(LED1,GPIO.OUT)
GPIO.setup(LED2,GPIO.OUT)
GPIO.setup(LED3,GPIO.OUT)
GPIO.setup(LED4,GPIO.OUT)
GPIO.setup(LED5,GPIO.OUT)
GPIO.setup(LED6,GPIO.OUT)
GPIO.setup(LED7,GPIO.OUT)
GPIO.setup(LED8,GPIO.OUT)
GPIO.setup(LED9,GPIO.OUT)
GPIO.setup(LED10,GPIO.OUT)

os.chdir('/home/pi/Music')
f = glob.glob('*mp3')
h = len(f)
status = 1
pointer = 0
start = 0
volume = 8

def distance():
    GPIO.output(TRIGGER,True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER,False)
    StartTime = time.time()
    StopTime = time.time()
    while GPIO.input(ECHO) == 0:
        StartTime = time.time()
    while GPIO.input(ECHO) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime-StartTime
    distance=(TimeElapsed*34300)/2
    return distance



if __name__=='__main__':

    try:
    
        for counter in range(1,10):
            volume = counter
            led()
            sleep(0.1)
            
        for counter in range(1,9):
            volume = 10-counter
            led()
            sleep(0.1)
            
        for counter in range(1,8):
            volume = counter
            led()
            sleep(0.1)
            
        while True:
            led()
            dist = int(distance())
            
            if(status==1):
                player = subprocess.Popen(["omxplayer",f[pointer]],stdin=subprocess.PIPE)
                fi = player.poll()
                status = 0
                start = 0
                volume = 8
                
            if(dist>=0 and dist<=35):
                vol = dist/3
                
                if(vol>volume):
                
                    for counter in range(1,vol-volume):
                        player.stdin.write("+")
                        volume = volume + 1
                        led()
                        sleep(0.1)
                        
                elif(vol<volume):
                
                    for counter in range(1,volume-vol):
                        player.stdin.write("-")
                        volume = volume - 1
                        led()
                        sleep(0.1)
                        
            if(GPIO.input(LEFT_SENSOR)==True and GPIO.input(RIGHT_SENSOR)==True):
                sleep(0.5)
                fi = player.poll()
                
                if fi!=0:
                    player.stdin.write("p")
                    
            elif(GPIO.input(LEFT_SENSOR)==True):
            
                for counter in range(0,10000):
                
                    if(GPIO.input(RIGHT_SENSOR)==True):
                    
                        if start==0:
                            player.stdin.write("q")
                            status = 1
                            pointer = pointer +1
                            
                            if(pointer>h-1):
                                pointer = 0
                                
                            break 
                    sleep(0.0001)
                    
            elif(GPIO.input(RIGHT_SENSOR)==True):
            
                for counter in range(0,10000):
                
                    if(GPIO.input(LEFT_SENSOR)==True):
                    
                        if(start==0):
                            player.stdin.write("q")
                        status = 1
                        pointer = pointer - 1
                        
                        if(pointer<0):
                            pointer = h-1
                            
                        break
                    sleep(0.0001)
                    
            else:
                fi = player.poll()
                if(fi==0 and start==0):
                    status = 1
                    pointer = pointer +1
                    if(pointer>h-1):
                        pointer = 0
                sleep(0.1)
                
    except KeyboardInterrupt:
            print("Stopped by user")
            GPIO.cleanup()
        
        
