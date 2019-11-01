import socket
from _thread import *
import sys
from player import Player
import pickle
import pygame
from bullet import Projectile

server = "192.168.1.224"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

players=[Player(0,450,"sprite1.png",1),Player(100,450,"sprite2.png",2)]
bullets=[Projectile(1),Projectile(2)]

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    conn.send(pickle.dumps(bullets[player]))
    reply = ""
    while True:
        try:
            received = pickle.loads(conn.recv(2048))
            for i in received:
                if i.vel:
                    data=i
                else:
                    bulletdata=i

            #bulletdata=pickle.loads(conn.rev(2048))
            #data2 = pickle.loads(conn.recv(2048))
            players[player] = data
            bullets[player]=bulletdata

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                    reply2=bullets[0]
                else:
                    reply = players[1]
                    reply2=bullets[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
            conn.sendall(pickle.dumps(reply2))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
