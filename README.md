# cm2110-coursework-2-submissoin-activated-almonds
cm2110-coursework-2-submissoin-activated-almonds created by GitHub Classroom

#Spotipy
#A sonos like system that runs on Raspotify

#Downloading the OS
Raspian can be installed from this website. We must install "Raspbian Buster with desktop and recommended software". Now click on "Download ZIP", and the download should start. (this can take a couple of minutes depending on your ethernet connection)
Step 2: Writing the image to the SD card
Now you will need to download & install the software that will write the image to the SD card. A good one to use is called Etcher, and it works on all platforms (Linux, Mac, and Windows). You're able to download it from over at their website.
1. Once you have downloaded Etcher, follow the prompts to install it.
2. Insert your SD card into your computer. (Because some machines do not have an SD card reader, you may need to use a USB adapter.)
3. Open Etcher and select the Raspbian image that we just downloaded.
4. Select the SD card that you wish to install Raspbian on. Double-check to make sure it's the correct drive as this will wipe it clean.
5. Once you have confirmed the image and the drive you can then proceed to flash the SD card, select Flash.
6. Once it's finished, you can safely remove the SD card from the computer.
7. Insert the SD card into your Raspberry Pi and any other extra cords such as power, mouse, keyboard, and the HDMI cord.
8. Now you will be guided through the setup process. Make sure you don't forget to connect to the Ethernet because Spotify Connect is based on the Ethernet. The setup process is pretty straight forward, so it shouldn't be a problem.

#VLC
VLC is needed for this. To install run the following command:
sudo apt-get install vlc
The audio for this project is run via CVLC
Installing Raspotify on the Rasberry Pi
Raspotify is a Spotify Connect client for Raspbian on the Raspberry Pi that Just Works™. Raspotify is a Debian package and associated repository which thinly wraps the awesome "librespot" library by Paul Lietar and others. It works out of the box on all three revisions of the Pi, immediately after installation.
The install itself is as easy as it gets, follows the following steps, and you'll be up and running in 5 minutes.
Open the Terminal using the shortcut "CTRL + ALT + T"
Type in the Terminal the following and hit enter afterwards. This command downloads and installs the Debian package and adds its apt repository, which ensures you'll always be up to date with upstream changes.
curl -sL https://dtcooper.github.io/raspotify/install.sh | sh
After the installation, we will run a quick check. Open your Spotify and look for Available Devices. There should be a "raspotify (raspberrypi)" speaker available like shown below.
Now that everything works, we can configure Raspotify. By typing the following command in the Terminal, we can change the settings, like the name that we want to be displayed on Spotify.
sudo nano /etc/default/raspotify
What you've opened is the Raspotify config file. Within this file, you will see multiple different options that you can configure yourself. We will change only two settings: The Bitrate and the Device Name.
To change the device name, we will have to uncomment the line first. This can be done by hitting the delete key, your text of that line will now become white. Now we can pick a name that will be displayed in Spotify.


#For example:
DEVICE_NAME="LivingRoom"
After we've changed our name, we will revise the Bitrate. This will give us a little bit better audio quality.
Uncomment the line and replace 160 by 320.
BITRATE="320"

Now the code should look like this, except for the name difference:
<p># /etc/default/raspotify -- Arguments/configuration for librespot<br>
# Device name on Spotify Connect
DEVICE_NAME="David Room"</p><p># Bitrate, one of 96 (low quality), 160 (default quality), or 320 (high quality)
BITRATE="320"</p><p># Additional command-line arguments for librespot can be set below.
# See `librespot -h` for more info. Make sure whatever arguments you specify
# aren't already covered by other variables in this file. (See the daemon's
# config at `/lib/systemd/system/raspotify.service` for more technical details.)
#
# To make your device visible on Spotify Connect across the Internet add your
# username and password which can be set via "Set device password", on your
# account settings, use `--username` and `--password`.
#
# To choose a different output device (i.e. a USB audio dongle or HDMI audio out),
# use `--device` with something like `--device hw:0,1`. Your mileage may vary.
#
#OPTIONS="--username  --password (Premium account info goes here)
"</p><p># Uncomment to use a cache for downloaded audio files. The cache is disabled by
# default. It's best to leave this as-is if you want to use it since
# permissions are properly set on the directory `/var/cache/raspotify'.
#CACHE_ARGS="--cache /var/cache/raspotify"</p><p># By default, the volume normalization is enabled, add alternative volume
# arguments here if you'd like, but these should be fine.
#VOLUME_ARGS="--enable-volume-normalisation --linear-volume --initial-volume=100"</p><p># Backend could be set to pipe here, but it's for very advanced use cases of
# librespot, so you shouldn't need to change this under normal circumstances.
#BACKEND_ARGS="--backend alsa"</p>
 
 
To save the file hit "CTRL + X" followed by "y" and last but not least hit enter.
Restart Raspotify by using the following command.
sudo systemctl restart raspotify
Give it a quick check like we did in step 3 and look whether the name has changed or not.
Now everything is ready, and we can make our speakers ready!
 

#Connecting Pre-amped Speakers
If your speakers are already connected to an amplifier that has an AUX port, you should join an aux cable from the Raspberry Pi to the amp and disconnect the peripherals from the Raspberry Pi. Everything should work right now! Make sure you don't disconnect the Power Cable and Ethernet Cable (only when you are not connected via Wifi) as well as the AUX cable. You should have kind of the same connections as in the image below, and now you are finished. An aux adapter is needed for the host if you want to output the audio without headphones

#Python Scripts used in project

#Gestures.py
Gestures is a python script that allows users to interact with the HC-SR04 Ultrasonic Sensor on the breadboard. This relates to the python script “Gestures”. Users can use their hand to control the music. The script imports OS, glob, subprocess, RPi.GPIO, spotipy, spotipy.oauth2, spotiy.util and time. 
Then the user waves their hand from left to right. It will skip a track, vice versa will play the previous track. Holding a hand close to the sensor will mute it and distancing the hand upwards will increase the volume.  
The script pulls in from the local connection os.chdir('/home/etc/default/raspotify') 
(This may differ for each user) 
and streams out mp3 from the glob.glob list.
Subprocess is currently listed as "Spotipy music player"
(Currently not in use due to hardware limitations (needs resistor). Replacing this with JoyStickControl.py including to show team workings)

#JoyStickControl.py
JoyStickControl imports confiqparser from sense_hat import SenseHat. This script will run with Raspotify and will display things like artist, Album, Song title, pause and resume on the sense hat. Once the song has been changed this script will reflect this via the senseHat. The joystick on the pi will make changes to the sensehat/track. Up will change the mode (artist, album artist) down shows current mode result, right is next track left previous track press in is play / pause on toggle

#SpotipyTest.py
SpotipyTest is a python script that allows track information to be displayed on the SenseHat. It import configparser, import spotipy, import spotipy.oauth2 as oauth2 and import spotipy.util as util
 
#Bluetooth.PY
Bluetooth.py is a python script that creates a proximity-based range that connects the speaker and pi with a user’s Bluetooth Its imports fcntl, struct, array, bluetooth (which is referred to as bt), RPI.GPIO (which is referred to as GPIO), time, os and datetime.
The script opens the HCI socket and attempts to connect to a bluetooth device. Each pi will have this function and when a user is closer to a pi the pi should play from the pi’s connected speakers. Set to a max range of 255. 

#MyqtthubSubcribe.py
Gets data

#MyqtthubPublish.py
Sends data

#Client.py
Client imports Spotipy =, json, time, ssl, os and threading. It pulls in info from MyQTThub. For the demo we have given each client a different set bluetooth range for the video. It uses the sense hat to display info on the current track playing. It uses VLC.  There are multiple clients depending on how many speakers the user wants to output to. There is also Client 1 and 2

#Confiq.py
Script is simple. Gives client ID, Secret and URL for local host

#Host.py
Host imports Spotipy, Json, time, ssl, threading and os. Host is used for the main pi that will act as “host” for the other pis set up around the home

#SpotipyTest.py
This was for testing only. We have added it onto the git to show our working
