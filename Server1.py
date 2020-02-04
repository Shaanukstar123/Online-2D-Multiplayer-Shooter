import socket
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

def run(name):
    start_new_thread(multicast,(name,))

    global all_data,timer, totalConnections, timerHasStarted, timer

    totalConnections = 0
    #server = "192.168.1.224"
    port = 5555
    host=socket.gethostname()
    IP = socket.gethostbyname(host)
    server = ""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)

    s.listen(2)
    print("Waiting for a connection, Server Started")
    timer = Timer()
    collectable_data = []
    #item=Collectable()
    #spawn_chance = 20
    #itemlist=Collectable_list()
    #collectables = CollectableList()
    #players=[Player(0,0,"sprite1.png"),Player(100,100,"sprite2.png")]
    all_data = [{
        'player':Player(0,0,["sprite1.png","right.png","left.png"],1,1,0,100),
        "timer": timer,
        "collectable": collectable_data
    }, {
        'player': Player(100,100,["sprite2.png","player2right.png","player2left.png"],2,2,0,100),
        "timer": timer,
        "collectable": collectable_data
    }]
    '''talk about why parallel data sets not sent due to synch issues and buffer needed'''
    #all_data[0]

    timerHasStarted = False

    walls=[pygame.Rect(900,500,228,44),pygame.Rect(600, 250, 44, 228),pygame.Rect(200,350,228,44)]


    for i in range(random.randint(10,20)):
        item = Collectable()
        if item.generate(walls):
            collectable_data.append([item.x,item.y,item.time,item.life,item.type])

    currentPlayer = 0
    while True:

        conn, addr = s.accept()
        print("Connected to:", addr)
        totalConnections += 1

        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1


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
                all_data[0]['timer'] = timer
                all_data[1]['timer'] = timer

                if totalConnections == 2:
                    if not timerHasStarted:
                        print("STARTING")
                        timer.start()
                        timerHasStarted = True
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

def multicast(name):

    message = name
    multicast_group = ('224.3.29.71', 10000)

    # Create the datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout so the socket does not block indefinitely when trying
    # to receive data.
    sock.settimeout(0.2)

    # Set the time-to-live for messages to 1 so they do not go past the
    # local network segment.
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    try:
        while True:
            # Send data to the multicast group
            #print (sys.stderr, 'sending "%s"' % message)
            sent = sock.sendto(message.encode("utf-8"), multicast_group)

            # Look for responses from all recipients
            while True:
                #print (sys.stderr, 'waiting to receive')
                try:
                    data, server = sock.recvfrom(16)
                except socket.timeout:
                    #print (sys.stderr, 'timed out, no more responses')
                    break
                else:
                    pass
                    #print (sys.stderr, 'received "%s" from %s' % (data, server))
            if totalConnections == 2:
                break

    finally:
        print (sys.stderr, 'closing socket')
        sock.close()

def error():
    print("You can't do that")


#run("server1")
