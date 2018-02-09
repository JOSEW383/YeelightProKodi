import re
import socket
from time import sleep
from time import strftime
from ast import literal_eval
import xbmc
#-------------------------------------------------------------------------
#List of light bulbs
bulb1 = "192.168.5.110"
bulb2 = "192.168.5.111"
bulb3 = "192.168.5.112"
bulb4 = "192.168.5.113"

port=55443

#List of colors
white=16777215
blue=255
green=65280
red=16711680
pink=16711935
yellow=16776960
turquoise=65535
film=9599999
#-------------------------------------------------------------------------
#Methods of yeelight

#TO DO
def get_param_value(data, info):
    dictionary = literal_eval(data[0])
    value = dictionary["result"]
    if info == "power":
        return value[0]
    elif info == "bright":
        return value[1]
    elif info == "rgb":
        return value[2]
    else:
        return "error"

#info= power / bright / rgb
def get_info(ip,info):
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.settimeout(2)
        tcp_socket.connect((ip, int(port)))
        tcp_socket.send("{\"id\":" + ip + ", \"method\":\"get_prop\", \"params\":[\"power\", \"bright\", \"rgb\"]}\r\n")
        data = tcp_socket.recvfrom(2048)
        tcp_socket.close()
        return get_param_value(data,info)
    except Exception as e:
        return "empty"

def operate_on_bulb(ip, method, params):
	try:
		tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tcp_socket.settimeout(2)
		print "Send to ",ip, port ,"..."
		tcp_socket.connect((ip, int(port)))

		#msg2="{\"id\": 192.168.4.234, \"method\": \"set_rgb\", \"params\":[\"65280\", \"sudden\", 500]}\r\n"

		msg="{\"id\":" + str(ip) + ",\"method\":\""
		msg += method + "\",\"params\":[" + params + "]}\r\n"

		tcp_socket.send(msg)
		tcp_socket.close()
	except Exception as e:
		print "An error has ocurred:", e

def set_rgb(ip, color):
    #white 16777215 blue 255 green 65280 red 16711680 pink 16711935 yellow 16776960 turquoise 65535
    params=",\"smooth\",500"
    operate_on_bulb(ip, "set_rgb", str(color)+params)

def set_bright(ip, bright):
    params=",\"smooth\",500"
    operate_on_bulb(ip, "set_bright", str(bright)+params)
    #effect (str)  The type of effect. Can be "smooth" or "sudden".
    #Minimun of bright is 1!!

def set_color_temp(ip):
    operate_on_bulb(ip,"set_color_temp","")
    #Parameters:	degrees (int)  The degrees to set the color temperature to (1700 _ 6500).

def toggle(ip):
    operate_on_bulb(ip,"toggle","")

def turn_on(ip):
    params="\"on\",\"smooth\",500"
    operate_on_bulb(ip,"set_power",params)

def turn_off(ip):
    params="\"off\",\"smooth\",500"
    operate_on_bulb(ip,"set_power",params)

#-------------------------------------------------------------------------
#Voids witch all light bulbs

def turn_on_all():
    turn_on(bulb1)
    turn_on(bulb2)
    turn_on(bulb3)
    turn_on(bulb4)

def turn_off_all():
    turn_off(bulb1)
    turn_off(bulb2)
    turn_off(bulb3)
    turn_off(bulb4)

#-------------------------------------------------------------------------
#Scenes
def setMovieScene3():
    turn_off_all()
    turn_on(bulb3)
    set_rgb(bulb3,film)
    set_bright(bulb3,20)

def setDefaultScene3():
    set_rgb(bulb3,white)
    set_bright(bulb3,50)

def setMovieScene4():
    turn_off_all()
    turn_on(bulb4)
    set_rgb(bulb4,film)
    set_bright(bulb4,50)

def setDefaultScene4():
    set_rgb(bulb4,white)
    set_bright(bulb4,100)

#-------------------------------------------------------------------------
#MAIN OF YEELIGHTPRO
#List of conditions: http://kodi.wiki/view/List_of_boolean_conditions
isPlaying = False
while True:
    #Bulbs turn on wich time it is between 17:30 - 8:00
    hour = int(strftime("%H%M"))
    if hour<800 or hour>1730:
        #VIDEO PLAYING
        if xbmc.getCondVisibility('Player.Playing') and not isPlaying:
            state_bulb4 = get_info(bulb4,"power")
            if state_bulb4 == "empty":
                setMovieScene3()
            else:
                setMovieScene4()
            isPlaying=True
        #NOT VIDEO PLAYING
        elif not xbmc.getCondVisibility('Player.Playing') and  isPlaying == True:
            if state_bulb4 == "empty":
                setDefaultScene3()
            else:
                setDefaultScene4()
            isPlaying=False
    sleep(10)
