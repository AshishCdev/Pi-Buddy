# Pi-Buddy
Simple Raspberry pi controlled IOT based home automation project that will allow you to communicate with your home appliances with the Twitter at front end.

# Required Python modules
1. Sixohsix module for twitter https://github.com/sixohsix/twitter
2. spi-dev module for accessing temperature via SPI interface https://github.com/doceme/py-spidev .
    In this project I used this SPI-analog-expander https://github.com/AshishCdev/SPI-Analog-expander
3. RPi.GPIO module for accessing GPIO https://pypi.python.org/pypi/RPi.GPIO

# Twitter API Keys
1. Make one more twitter account for raspberry pi and visit to this page https://apps.twitter.com/ 
2. Create new app and set the permission to Read, Write and Access direct messages.
3. Generate all your API keys. This will provide four API keys- Consumer Key, Consumer Secret, 	Access Token and Access Token Secret.

#Setting up the hardwares
Since connecting all the electronics may lead to misconnections resuilts damadge to GPIO.The relay board(module) is recommended. GPIO 02 - FAN, GPIO 03 - LIGHT, GPIO 04 - A.C.
Prefer this diagram for GPIO allocation https://www.element14.com/community/servlet/JiveServlet/previewBody/73950-102-9-339300/pi3_gpio.png

#Setting up the Software
1. login to your Raspberry Pi and enable SPI module by entering raspi-config in the terminal.
2. Install the mentioned Required Python modules
3. Enter in the terminal 
    1. git clone https://github.com/AshishCdev/Pi-Buddy
    2. cd Pi-Buddy
    3. sudo nano Pi\ Buddy.py 
    Hit enter and that will open the nano editor for editing the Pi Buddy.py file.
4. Enter your API keys, you just have got from the twitter and save this file. Also enter the twitter handle accounts of        your's and your Pi buddy app's. Now save this file.
5. Now set this script at the startup so that the program will run automatically at startup without logging in. In order to do that open the terminal and type-
   1.sudo nano /etc/rc.local
   2.This will open the file to edit. Add this line just above the exit0 "python /home/pi/Pi-Buddy/Pi\ Buddy.py &"
 Save and restart. As the Application will start, it will send "Hey,How Can I help you?" and you can control your home appliances at configured GPIO.
   


