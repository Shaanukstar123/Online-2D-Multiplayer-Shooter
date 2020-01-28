import socket
from _thread import *
import sys
from classes import *
import pickle
from timer import *
from collectables import *
import random
import pygame

class Server():
    def __init__(self):
        self.total_connections = 0
        self.port = 5555
        self.host = socket.gethostname()
        self.IP = socket.gethostbyname(self.host)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.timer = Timer()
        self.collectable_data =[]
        self.all_data=None
        self.timerHasStarted = None
        self.totalConnections = 0
        self.currentPlayer = None
        self.connection = None

    def run(self):
        try:
            self.s.bind((self.IP, self.port))
        except socket.error as e:
            str(e)

        self.s.listen(2)
        print("Waiting for a connection, Server Started")

        self.all_data = [{
            'player':Player(0,0,["sprite1.png","right.png","left.png"],1,1,0,100),
            "timer": self.timer,
            "collectable": self.collectable_data
        }, {
            'player': Player(100,100,["sprite2.png","player2right.png","player2left.png"],2,2,0,100),
            "timer": self.timer,
            "collectable": self.collectable_data
        }]
        '''talk about why parallel data sets not sent due to synch issues and buffer needed'''
        #all_data[0]

        self.timerHasStarted = False

        walls=[pygame.Rect(900,500,228,44),pygame.Rect(600, 250, 44, 228),pygame.Rect(200,350,228,44)]


        for i in range(random.randint(10,20)):
            item = Collectable()
            if item.generate(walls):
                self.collectable_data.append([item.x,item.y,item.time,item.life,item.type])
        self.currentPlayer = 0

    def loop(self):
        #while True:
        self.connection, addr = self.s.accept()
        print("Connected to:", addr)
        self.totalConnections += 1
        currentPlayer = self.currentPlayer
        start_new_thread(self.threaded_client, ())
        self.currentPlayer += 1


        '''totalConnections = 0
        #server = "192.168.1.224"
        port = 5555
        host=socket.gethostname()
        IP = socket.gethostbyname(host)
        server = IP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)'''


    def threaded_client(self):#,currentPlayer):
        #global totalConnections, timerHasStarted, timer
        #print(currentPlayer)
        print(self.all_data)
        self.connection.send(pickle.dumps(self.all_data[self.currentPlayer-1]))
        reply = ""
        print("TIMER STARTED:" + str(self.timer.has_started))
        while True:
            try:
                data = pickle.loads(self.connection.recv(2048*3))
                self.all_data[self.currentPlayer-1] = data

                if not data:
                    print("Client Disconnected")
                    self.totalConnections -= 1
                    break
                else:
                    self.all_data[0]['timer'] = self.timer
                    self.all_data[1]['timer'] = self.timer

                    if self.totalConnections == 2:
                        if not self.timerHasStarted:
                            print("STARTING")
                            self.timer.start()
                            self.timerHasStarted = True
                    if currentPlayer == 1:
                        #print("Player:",CurrentPlayer)
                        reply = self.all_data[0]
                    else:
                        #print("Player:", currentPlayer)
                        print(self.currentPlayer)
                        reply = self.all_data[1]

                    #print("Received: ", data)
                    #print("Sending : ", reply)
                    self.connection.sendall(pickle.dumps(reply))
            except:
                break

        #print("Lost connection")
        #self.connection.close()


    def error(self):
        print("You cannot do that")

server = Server()
server.run()
while True:
    server.loop()
