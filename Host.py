import configparser
from sense_hat import SenseHat
import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util
import json
import time
import paho.mqtt.client as mqtt
import time
import ssl
import threading
import os

b = (0,0,0)
w = (255,255,255)

play = [
    b, w, w, b, w, b, b, b,
    b, w, w, b, w, w, b, b,
    b, w, w, b, w, w, w, b,
    b, w, w, b, w, w, w, w,
    b, w, w, b, w, w, w, w,
    b, w, w, b, w, w, w, b,
    b, w, w, b, w, w, b, b,
    b, w, w, b, w, b, b, b
]

pause = [
    b, b, b, b, b, b, b, b,
    b, w, w, b, b, w, w, b,
    b, w, w, b, b, w, w, b,
    b, w, w, b, b, w, w, b,
    b, w, w, b, b, w, w, b,
    b, w, w, b, b, w, w, b,
    b, w, w, b, b, w, w, b,
    b, b, b, b, b, b, b, b
]

#MYQTTHUB Info 
host          = "node02.myqtthub.com"
port          = 1883
clean_session = True
client_id     = "TestDevice"
user_name     = "aa01"
password      = "Active1"

#Bluetooth signal of the host
bluetoothSignal = 255
sense = SenseHat()
#Initially the host is playing music
playing = True
instanceId = "TestDevice"
alreadyStarted = True
#Here is where we add devices!
clientsDict = {"TestDevice": bluetoothSignal, "TestDevice2": 255, "TestDevice3": 255, "TestDevice4": 255}
currentlyPlayingDict = {"TestDevice": playing, "TestDevice2": False, "TestDevice3": False, "TestDevice4": False}

def on_connect (client, userdata, flags, rc):
    """ Callback called when connection/reconnection is detected """
    print ("Connect %s result is: %s" % (host, rc))
    
    client.subscribe("BluetoothSignal")
    client.subscribe("SendMusicTo")
    # With Paho, always subscribe at on_connect (if you want to
    # subscribe) to ensure you resubscribe if connection is
    # lost.
    # client.subscribe("some/topic")

    if rc == 0:
        client.connected_flag = True
        print ("connected OK")
        return
    
    print ("Failed to connect to %s, error was, rc=%s" % rc)
    # handle error here
    sys.exit (-1)


def on_message(client, userdata, msg):
    """ Callback called for every PUBLISH received """
    print("received message")
    print ("%s => %s" % (msg.topic, str(msg.payload.decode("UTF-8"))))
    if msg.topic == "BluetoothSignal":
        handleBluetoothSignal(json.loads(str(msg.payload.decode("UTF-8"))))
        evaluateClients()
    else:
        print("SendMusicTo")
        clientPlaying(json.loads(str(msg.payload.decode("UTF-8"))))
    

# Define clientId, host, user and password
client = mqtt.Client (client_id = client_id, clean_session = clean_session)
client.username_pw_set (user_name, password)

client.on_connect = on_connect

def subscribing():
    client.on_message = on_message
    client.loop_forever()
    
client.connect (host, port, keepalive = 60)
client.connected_flag = False


while not client.connected_flag:
    client.loop()
    time.sleep (1)

config = configparser.ConfigParser()
config.read('config.cfg')
client_id = config.get('SPOTIFY', 'CLIENT_ID')
client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')
client_uri = config.get('SPOTIFY', 'CLIENT_URI')

auth = oauth2.SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
)

username="plpkacper"
scope = "user-read-playback-state,user-modify-playback-state"

#token = auth.get_access_token()
token = util.prompt_for_user_token(username, scope, client_id, client_secret, client_uri)
spotify = spotipy.Spotify(auth=token)
mode = 0

#device_id= spotify.devices().get("devices")[0].get("id")

playing= 1
print(playing)

def evaluateClients():
    max = 255;
    closestClient = None;
    for key in clientsDict:
        if clientsDict.get(key) < max:
            closestClient = key
            max = clientsDict.get(key)
    actualClosest = {closestClient: True}
    for key in currentlyPlayingDict:
        if key == closestClient:
            currentlyPlayingDict.update(actualClosest)
        else:
            notClosest = {key: False}
            currentlyPlayingDict.update(notClosest)

def handleBluetoothSignal(dict):
    for key in clientsDict:
        for key2 in dict:
            if key == key2:
                clientsDict.update(dict)
                
def clientPlaying(dict):
    for key in dict:
        if key == instanceId:
            if dict.get(key):
                playing = True
                if alreadyStarted:
                    print("continuing to play")
                else:
                    unmute()
                    alreadyStarted = True
            else:
                playing = False
                mute()


def mute():
    print("Muting")
    command = "amixer sset Speaker 0%"
    returnedVal = os.system(command)

def unmute():
    print("Unmuting")
    command = "amixer sset Speaker 100%"
    returnedVal = os.system(command)

def up():
    spotify.start_playback()
    print("START")

def down():
    spotify.pause_playback()
    print("PAUSE")

def left():
    spotify.previous_track()
    spotify.previous_track()
    print("PREVIOUS")
  
def right():
    spotify.next_track()
    print("NEXT")
    

def middle():
    global playing
    
    playing+=1
    print(playing)
    
    if playing%2==0:
        spotify.pause_playback()
        print("PAUSE")
        sense.clear()
        sense.set_pixels(pause)
        time.sleep(2)
        sense.clear()
    else:
        spotify.start_playback()
        print("START")
        sense.clear()
        sense.set_pixels(play)
        time.sleep(2)
        sense.clear()

def changePrintMode():
    global mode
    if mode == 2:
        mode = 0;
    else:
        mode = mode + 1
            
def printInfo():
    global mode
    currentTrack = spotify.current_user_playing_track()
    if mode == 0:
        sense.show_message("Song:", scroll_speed=0.05)
        sense.show_message(currentTrack.get("item").get("name"), scroll_speed=0.05)
    elif mode == 1:
        sense.show_message("Artist:", scroll_speed=0.05)
        sense.show_message(currentTrack.get("item").get("artists")[0].get("name"), scroll_speed=0.05)
    else:
        sense.show_message("Album:", scroll_speed=0.05)
        sense.show_message(currentTrack.get("item").get("album").get("name"), scroll_speed=0.05)

def publishing():
    bluetoothSignalDict = {instanceId: 15}
    while True:
        ret = client.publish ("SendMusicTo", json.dumps(currentlyPlayingDict))
        print ("Publish operation finished with ret=%s" % ret)
        ret2 = client.publish ("BluetoothSignal", json.dumps(bluetoothSignalDict))
        print ("Publish operation finished with ret=%s" % ret2)
        time.sleep(10)

def startCVLC():
    print("Starting CVLC")
    command = "cvlc -vvv alsa://hw:1,0 --sout '#transcode{acodec=mp3,ab=320}:rtp{mux=ts,dst=239.255.1.1,sdp=sap}'"
    returnedVal = os.system(command)
    print("Returned Value From Start")
    print(returnedVal)
    
def stopCVLC():
    print("Stopping CVLC & Stream")
    command = "killall vlc"
    returnedVal = os.system(command)
    print(returnedVal)
    
def main():
    unmute()
    cvlcProcess.start()
    while True:
        if playing:
            for event in sense.stick.get_events():
                if event.action == "pressed":
                    if event.direction == "up":
                        #up()
                        changePrintMode()
                        printInfo()
                        
                    elif event.direction == "down":
                        #down()
                        printInfo()
                        
                    elif event.direction == "left":
                        left()
                        printInfo()
                        
                    elif event.direction == "right":
                        right()
                        printInfo()
                        
                    elif event.direction == "middle":
                        middle()

cvlcProcess=threading.Thread(target=startCVLC)
sub=threading.Thread(target=subscribing)
but=threading.Thread(target=main)
pub=threading.Thread(target=publishing)

sub.start()
but.start()
pub.start()
