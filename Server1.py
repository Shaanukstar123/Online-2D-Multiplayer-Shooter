from socket import *
from _thread import *
import sys
from classes import *
import pickle
from timer import *
from collectables import *
import random
import pygame
import sys
import struct
import random

host=gethostname()
IP = gethostbyname(host)
timer = Timer()
timerHasStarted = False
def run(name,time_limit):
    start_new_thread(broadcast,(name,))

    global all_data,timer, totalConnections, timerHasStarted, timer

    totalConnections = 0

    port = 5555

    server = ""
    s = socket(AF_INET,SOCK_STREAM)

    try:
        s.bind((server, port))
    except error as e:
        str(e)

    s.listen(2)
    print("Waiting for a connection, Server Started")

    collectable_data = []
    walls=[pygame.Rect(900,500,228,44),pygame.Rect(600, 250, 44, 228),pygame.Rect(200,350,228,44)]
    #wall_objects = [Map(900, 500, 44, 228, "wall1.png"),Map(600, 250, 44, 228, "wall1.png"),Map(200, 375, 44, 22, "wall1.png")]

    print("Now: ", timer.time_elapsed)
    all_data = [{
        'player': Player(0,0,["sprite1.png","right.png","left.png","Images/sprites/hityellow.png","Images/sprites/hityellowleft.png"],1,1,0,100),
        "timer": [timer,time_limit],
        "collectable": collectable_data
        #"walls" : wall_objects
    }, {
        'player': Player(100,100,["sprite2.png","player2right.png","player2left.png","Images/sprites/hitgreen.png","Images/sprites/hityellowleft.png"],2,2,0,100),
        "timer": [timer,time_limit],
        "collectable": collectable_data
        #"walls": wall_objects
    }]
    '''talk about why parallel data sets not sent due to synch issues and buffer needed'''

    for i in range(random.randint(20,40)):
        item = Collectable()
        if item.generate(walls):
            collectable_data.append([item.x,item.y,item.time,item.life,item.type])

    currentPlayer = 0
    while True:

        conn, addr = s.accept()
        print("Connected to:", addr)
        if addr[1] != 10000:
            totalConnections += 1
            print("Total",totalConnections)

            start_new_thread(threaded_client, (conn, currentPlayer))
            currentPlayer += 1
            if currentPlayer>1:
                print("2 Players already connected")


def threaded_client(conn, player):
    global totalConnections, timerHasStarted, timer

    print(player)
    conn.send(pickle.dumps(all_data[player]))
    reply = ""
    print("TIMER STARTED:" + str(timer.has_started))
    while True:
        try:
            data = pickle.loads(conn.recv(2048*3))
            all_data[player] = data

            if not data:
                print("Client Disconnected")
                totalConnections -= 1
                break
            else:
                all_data[0]['timer'][0] = timer
                all_data[1]['timer'][0] = timer

                if totalConnections == 2:
                    if timer.started == False:
                        print("STARTING")
                        timer.start()
                        timerHasStarted = True

                if player == 1:
                    reply = all_data[0]
                else:
                    print("Player: ",player)
                    reply = all_data[1]

                conn.sendall(pickle.dumps(reply))
        except:
            print("Error")
            break

    print("Lost connection")
    conn.close()

def broadcast(name):
    time = 0
    broadcast_ip = IP.split(".")
    broadcast_ip[3] = "255"

    broadcast_ip = ".".join(broadcast_ip)

    message = name
    broadcast_address = (broadcast_ip, 10000)

    sock=socket(AF_INET, SOCK_DGRAM)
    sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    sock.settimeout(0.5)

    try:
        while True:


            sent = sock.sendto(message.encode("utf-8"), broadcast_address)
            #data, server = sock.recvfrom(16)
            #if data!=None:
                #print(data)

            while True:

                try:
                    data, server = sock.recvfrom(16)
                except timeout:
                    break
            if totalConnections == 2:
                break


    finally:
        print (sys.stderr, 'closing socket')
        sock.close()

def error():
    print("You can't do that")


#run("server1")
