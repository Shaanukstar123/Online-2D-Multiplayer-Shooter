import socket
from _thread import *
import sys
from player import *
import pickle

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

#players=[Player(0,0,"sprite1.png"),Player(100,100,"sprite2.png")]
all_data = [{
    'player':Player(0,0,["sprite1.png","right.png","left.png"],1,1)

}, {
    'player': Player(100,100,["sprite2.png","player2right.png","player2left.png"],2,2)

}]

#all_data[0]

def threaded_client(conn, player):
    conn.send(pickle.dumps(all_data[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            all_data[player] = data

            if not data:
                print("Client Disconnected")
                break
            else:
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

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1


def error():
    print("You can't do that :)")
