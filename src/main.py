import time
import network

time.sleep(2)

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('La Casita', 'elcuchitril')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig()[0])



do_connect()

import server

server.run()

