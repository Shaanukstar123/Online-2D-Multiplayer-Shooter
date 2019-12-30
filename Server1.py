import socket
from _thread import *
import sys
from classes import *
import pickle
from timer import *
from collectables import *
import random
import pygame

totalConnections = 0
#server = "192.168.1.224"
port = 5555
host=socket.gethostname()
IP = socket.gethostbyname(host)
server = IP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")
timer = Timer()
#item=Collectable()
spawn_chance = 20
itemlist=Collectable_list()
#collectables = CollectableList()
#players=[Player(0,0,"sprite1.png"),Player(100,100,"sprite2.png")]
all_data = [{
    'player':Player(0,0,["sprite1.png","right.png","left.png"],1,1,0),
    "timer": timer,
    "collectable": itemlist.items
}, {
    'player': Player(100,100,["sprite2.png","player2right.png","player2left.png"],2,2,0),
    "timer": timer,
    "collectable": itemlist.items
}]
'''talk about why parallel data sets not sent due to synch issues and buffer needed'''
#all_data[0]

timerHasStarted = False

walls=[pygame.Rect(900,500,228,44),pygame.Rect(600, 250, 44, 228),pygame.Rect(200,350,228,44)]

def threaded_client(conn, player):
    global totalConnections, timerHasStarted, timer

    conn.send(pickle.dumps(all_data[player]))
    reply = ""
    print("TIMER STARTED:" + str(timer.has_started))
    while True:
        try:
            data = pickle.loads(conn.recv(2048*2))
            all_data[player] = data

            if not data:
                print("Client Disconnected")
                totalConnections -= 1
                break
            else:
                all_data[0]['timer'] = timer
                all_data[1]['timer'] = timer
                #print("TIMERS =============")
                #print(timer.time_elapsed)
                #print(all_data[0]['timer'].time_elapsed)
                #print("=========================")

                if totalConnections == 2:
                    if not timerHasStarted:
                        print("STARTING")
                        timer.start()
                        timerHasStarted = True
                    shouldSpawn = random.randint(0,5000)
                    if shouldSpawn < spawn_chance:
                        item=Collectable()
                        if item.generate(walls):
                            itemlist.items.append(item)
                    for item in itemlist.items:
                        item.levitate()
                        print(item.collected)
                        #print(item.collected)
                        item.life-=1
                        if item.life<=0 or item.collected==True:
                            itemlist.items.remove(item)


                    all_data[0]['collectable'] = itemlist.items
                    all_data[1]['collectable'] = itemlist.items
                        #if item.collected == True:
                            #itemlist.remove(item)
                #print(itemlist.items)
                if player == 1:
                    reply = all_data[0]
                else:
                    reply = all_data[1]

                #print("Received: ", data)
                #print("Sending : ", reply)
                conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    totalConnections += 1

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1


def error():
    print("You can't do that")
