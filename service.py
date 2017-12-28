import time
import socket
import xbmc

#-------------------------------------------------------------------------
#List of light bulbs
bulb1 = "192.168.5.110"
bulb2 = "192.168.5.111"
bulb3 = "192.168.5.112"
bulb4 = "192.168.5.113"

port=55443
#-------------------------------------------------------------------------
#Method of yeelight

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

def turn_off_all():
    turn_off(bulb1)
    turn_off(bulb2)
    turn_off(bulb3)
    turn_off(bulb4)

def setMovieScene():
    turn_off_all()
    turn_on(bulb4)
    set_rgb(bulb4,9599999)
    set_bright(bulb4,50)

def setDefaultScene():
    set_rgb(bulb4,16777215)
    set_bright(bulb4,100)

#-------------------------------------------------------------------------
#MAIN OF YEELIGHTPRO
#List of conditions: http://kodi.wiki/view/List_of_boolean_conditions
isPlaying = False
while True:
    if xbmc.getCondVisibility('Player.Playing'):
        setMovieScene()
        isPlaying=True
    elif isPlaying == True:
        setDefaultScene()
        isPlaying=False
    time.sleep(10)
