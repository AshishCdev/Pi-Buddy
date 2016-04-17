#!/usr/bin/python
from twitter import *
from time import sleep
import twitter
import spidev
import RPi.GPIO as GPIO


me = "Your twitter handle"
my_device = 'Your device twitter handle'

Cns_key = "Consumer Key"
Cns_sec = "Consumer Secret"
A_token = "Application token"
A_secrt = "Application Secret"

_FAN = 2           # GPIO no for FAN output
_LIGHT = 3	   # GPIO no for LIGHT output
_AC = 4            # GPIO no for A.C. output
 
def get_temp():                            # Function that returns the value of current room temperature           
        spi = spidev.SpiDev()
        spi.open(0,0)                      
        raw=(spi.xfer([1]))
        tmpC=((raw[0]*256*4)/1000)
        return(tmpC-5)

def slice_rsponc(main_string):         # If the response from the user contains two tasks, this function divides and returns them as individual
    main_string=main_string.lower()
    sl_indx = 0
    if ' and ' in main_string:
        sl_indx = main_string.find('and')
    elif ' & ' in main_string:
        sl_indx = main_string.find('&')
    return(main_string[0:sl_indx],main_string[sl_indx:len(main_string)])

def take_action(i,Pi_buddy):       # This function desides what action has to be taken and responses to the user
    if (len(i)==0):
        return
    elif 'status' in i:
        status = { 0:'OFF' , 1:'ON'}
        FAN = GPIO.input(_FAN)
        LIGHT = GPIO.input(_LIGHT)
        AC = GPIO.input(_AC)
        Pi_buddy.direct_messages.new(user=me,text= ("FAN = " + status[FAN]+"\nLight = "+
                                             status[LIGHT]+"\nAC = "+status[AC]+"\nTemperature = "+str(get_temp())+unichr(176)+'C'))
        return
    elif 'temp' in i or 'temperature' in i:
        Pi_buddy.direct_messages.new(user=me,text='It is '+str(get_temp())+unichr(176)+'C')
        return
    elif 'on' in i:
        seg0 = 'ON'
        if 'fan'in i:
            GPIO.output(_FAN,True)                    # ON the fan
            seg1 = 'FAN'
        elif 'light'in i:
            GPIO.output(_LIGHT,True)                  # ON the bulb
            seg1 = 'Light'
        elif ('a.c.'in i) or ('ac ' in i) or ('air conditionar' in i):
            GPIO.output(_AC,True)                     # ON the ac
            seg1 = 'air conditionar'
        else:
            Pi_buddy.direct_messages.new(user=me,text="Incomplete??")
            return
    elif 'off' in i:
        seg0 = 'OFF'
        if 'fan'in i:
            GPIO.output(_FAN,False)                  # OFF the fan
            seg1 = 'FAN'
        elif 'light'in i:
            GPIO.output(_LIGHT,False)                # OFF the bulb
            seg1 = 'Light'
        elif ('a.c.'in i):
            GPIO.output(_AC,False)                   # OFF the ac
            seg1 = 'air conditionar'
        elif('all' in i):
            GPIO.output(_FAN,False)
            GPIO.output(_LIGHT,False)
            GPIO.output(_AC,False)
            Pi_buddy.direct_messages.new(user=me,text= "All is OFF now")
            return
        else:
            Pi_buddy.direct_messages.new(user=me,text= "Incomplete??")
            return
    else :
        Pi_buddy.direct_messages.new(user=me,text="Can't understand!!!\nafterall I am machine :(")
        return
    Pi_buddy.direct_messages.new(user=me,text='Now your '+seg1+' is '+seg0+' :)')

def main():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(_LIGHT,GPIO.OUT)
    GPIO.setup(_FAN,GPIO.OUT) 
    GPIO.setup(_AC,GPIO.OUT)
    
    GPIO.output(_FAN,False)
    GPIO.output(_LIGHT,False)
    GPIO.output(_AC,False)

    Pi_buddy = Twitter(auth=OAuth(A_token,A_secrt,Cns_key,Cns_sec))
    Pi_Buddy_rec = twitter.OAuth(consumer_key=Cns_key,
                                 consumer_secret=Cns_sec,
                                 token=A_token,token_secret=A_secrt)
    
    stream = twitter.stream.TwitterStream(auth=Pi_Buddy_rec, domain='userstream.twitter.com')
    temp = get_temp()
    sen_msg="Hey,\nHow Can I help you?"
    Pi_buddy.direct_messages.new(user=me,text=sen_msg)
    for msg in stream.user():
        if 'direct_message' in msg:
            new_msg = msg ['direct_message']['text']
            if(msg['direct_message']['sender_screen_name']!=my_device):
                for i in slice_rsponc(new_msg):
                    take_action(i, Pi_buddy)
                
if __name__ == '__main__':main()
    
