#!/usr/bin/env python
#coding: utf-8
#Developed by Álvaro Justen and his students at Curso de Arduino/UFRJ
#2011-08-05
#License: GPLv2

import urllib2 #[Twitter] Used to get Twitter timeline page
import json    #[Twitter] Used to unpack JSON (returned from Twitter) as a Python dictionary
import time    #[Twitter] Used to change the URL you get every time (to avoid proxy/caches)
import glob    #[Arduino-communication] Used to search for available serial connections (on GNU/Linux)
import serial  #[Arduino-communication] Used to communicate with Arduino
import time    #[Arduino-communication] Used to sleep!
import sys     #[CLI] Used to refresh (flush) stdout


twitter_username = 'CursoDeArduino'
arduino_version = 'Uno'
baud_rate = 9600


def turn_light_on():
    arduino.write('H')
    arduino.flush()


def turn_light_off():
    arduino.write('L')
    arduino.flush()

def get_last_tweet(user):
    #timeline_as_json_url = 'http://twitter.com/statuses/user_timeline/%s.json' % user
    #Use the URL above if do you want to obey tweets of only one owner
    # (need to change 'results' code below)
    search_url = 'http://search.twitter.com/search.json?q=@%s&timestamp=%f' % (user, time.time())

    try:
        fp = urllib2.urlopen(search_url)
    except IOError: #Cannot get JSON with user timeline
        return u''

    try:
        info = json.loads(fp.read())
    except ValueError: #Cannot unpack json
        return u''

    fp.close()
    if not len(info['results']):
        return u''
    tweets = info['results']
    if not len(tweets):
        return u''
    try:
        if 'text' not in tweets[0]:
            return u''

        return tweets[0]['text'], tweets[0]['from_user']
    except KeyError:
        return u''

if arduino_version.lower() == 'uno':
    usb_wildcard = '/dev/ttyACM*'
else:
    usb_wildcard = '/dev/ttyUSB*'
    
serial_ports = glob.glob(usb_wildcard)
if len(serial_ports) == 0:
        print 'No serial ports available'
        exit(1)

serial_port = serial_ports[0]
arduino = serial.Serial(serial_port, baud_rate, timeout=0.1)
arduino.write('   ')

while True:
    try:
        print 'Updating... ',
        sys.stdout.flush()
        last_tweet = get_last_tweet(twitter_username)
        if not last_tweet:
            print 'Got nothing!'
        elif u'lâmpada on' in last_tweet[0]:
            turn_light_on()
            print 'Light -> ON (by @%s)' % last_tweet[1]
        elif u'lâmpada off' in last_tweet[0]:
            turn_light_off()
            print 'Light -> OFF (by @%s)' % last_tweet[1]
        else:
            print 'nothing to do' 
        time.sleep(5)
    except KeyboardInterrupt:
        break

arduino.close()
