#!/usr/bin/env python
#coding: utf-8
#Developed by Álvaro Justen and his students at Curso de Arduino/UFRJ
#2011-08-05
#License: GPLv2

import urllib2 #[Twitter] Used to get Twitter timeline page
import json    #[Twitter] Used to unpack JSON (returned from Twitter) as a Python dictionary
import glob    #[Arduino-communication] Used to search for available serial connections (on GNU/Linux)
import serial  #[Arduino-communication] Used to communicate with Arduino
import time    #[Arduino-communication] Used to sleep!
import sys     #[CLI] Used to refresh (flush) stdout
import socks
import socket
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1025)
socket.socket = socks.socksocket


twitter_username = 'EuArduino'

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
    search_url = 'http://search.twitter.com/search.json?q=@' + user

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


serial_ports = glob.glob('/dev/ttyUSB*')
if len(serial_ports) == 0:
        print 'No serial ports available'
        exit(1)

serial_port = serial_ports[0]
arduino = serial.Serial(serial_port, 9600, timeout=0.1)
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
