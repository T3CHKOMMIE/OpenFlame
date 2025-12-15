![OpenFlame Logo](images/OpenFlame2.png)

OpenFlame is my attempt to modernize and secure the software released with the MagikFlame Appliance.

## Architecture
There are several parts of this system that I have been able to enumerate:
1. Metal "insert" and optically coated glass. Glass is coated on one side, make sure you put coated side up for best viewing expereince.
2. Insignia Fire TV - Displays the fire videos (Mp4) over HDMI from RPI (input 2).
3. Touch Screen - A 2.8 in TFT hat from Adafruit for RPI. Mine has the hardware buttons cutoff... which is weird, becuase the insert has a opening in the sheet metal for the buttons. My guess is that this was originally supposed to be used with the 4 hardware buttons on the hat.
4. Fire Brains -  A RPI 3B running Jessie from 2016.
5. Log Set - Doubles as an electric space heater.
6. Log Brains - Presumably arduino board that is tired into the physical controls of the logset and allows the RPI to control it via BT/Serial.


## How it works
1. The raspberry pi loads the antiquated Jessie OS and runs a barrage of python scripts on the EOL/EOS python 2.7.
2. It attempts to discover a BT/BLE device with the name 'MFL' and pairs with a hard coded 4 digit pin. This BT connection allows the RPI to send commands over serial (pyserial) to the log set and gives the user remote accesss to control Flame, Heat, Power and Log Animation. I assume this is an arduino board, but I havnt confirmed. It is something small, with BT that can interface with toggle buttons, LEDs and Relay on the log set.
3. RPI kicks off OMXPlayer to loop the videos with little loop disruptions. This is where the system shows it's age. OMXPlayer has been depricated in favor of VLC on newer kernels. It's VERY hard to get VLC to play 1080p flame videos on the old RPI3B and the hardware (GPU) acceloration doesnt seem to where it needs to. Newer OS will probably need VLC and RPI4/5 to play videos smoothly. This makes upgrading the current system much more challening. Video is played via HDMI out on RPI.
4. The iOS app seems to sync via BT with either the RPI or the Arduino where you have most of your control features. The iOS app has a feature for "connecting to a network". There is a bug with this feature that fails to "validate" internet connectivity with what seems like an old hard coded Google Cloud Project IP address. This IP doesnt seem to return anything so the internet check fails and the iOS app doesnt seem to think the device is connected. If you attempt to connect again via the iOS app, the RPI continues to add WPA Supplicant profiles to the configuration and then gets really broken/nasty. Dont connect MagikFlame to your home network. More about that later.
5. 

## What I wanted to do
I had the biggest problem with needing to touch the TFT screen AND push the power button on the remote to get the TV to turn on. There really is no need for that with libraries like LibCEC or PyCEC. I did not like the extra remotes and iOS app user expereince. I dont use apple products and I just started to get into Home Assistant. I wanted to make changes to the MagikFlame so that I could better control or even automate the electric fireplace. 

## What I did
After days of fumbling with VLC on newer images on the RPI3B as well as trying to get newer code to run on the orginial image, I settled for Video Looper. 

My image still uses OMXPlayer but does so with a slightly newer (but still old) OS that leverages the GPU acceloration on the RPI3B. I wrote an extremly bare bones API script that plays one video (the flame video that i prefer), creates the BT and Serial connection with the log set, and exposes those endpoints over rest_commands in Home assistant. The result is that my fireplace works well enough with video and audio and I can now control the main features of the appliance via a custom card in Home Assistant. I run the home assistant app on my android phone, so there isnt a need for me to have another android app. I couldnt get pycec to work becuase of dependancy problems with RPI Buster and the repos being depricated so I solved th TV Power On problem by simply rebooting the RPI. When the PI reboots, it reinitializes the HDMI connection and this brings the TV out of sleep and promptly starts the flame video.

## What doesnt work
Remember, I wanted my fireplace to work the way I wanted it to, so this came at some (temporary?) tradeoffs.

1. iOS app
2. TFT display... just remove it or use a different RPI like I did. the TFT screen flickers and isnt the best at picking up presses. If you use a different RPI, find a safe place to mount it where it doesnt ground/short itself out on the metal insert. You'll notice the orginal RPI has copious ammounts of electrical tape all over it.
3. Volume Control (you'll need the fire tv remote for that)
4. Aquarium video, or multiple videos (i just hard coded the one video i liked)
5. Auto Discovery of BT logs - Just use something to find the MAC of the device with MFL name and put that MAC in the server.py script.
6. Nature Sounds
7. Probably other things for now?

   
Bonus: I added a w1 Themal Sensor to the RPI and HA to monitor the heat from the space heater.


