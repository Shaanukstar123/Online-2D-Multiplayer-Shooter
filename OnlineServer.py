import socket
from _thread import *
import sys
import pickle
import random
import time
width=1300
height=700

class Player():
    def __init__(self, x, y,sprite,player,direction,score):
        self.x = x
        self.y = y
        self.player=player
        self.projectiles = []
        self.speed = 10
        self.gravity=10
        self.sprite=sprite
        self.direction = direction #1=right, 2=left
        self.health=100
        self.display=sprite[direction]
        self.bullet_count=2 #limits number of bullets per shot
        self.dead=False
        self.collision_left=False
        self.collision_right=False
        self.collision_up=False
        self.collision_down=False
        self.username=None
        self.score=score
        self.jump=False
        self.jump_position=10
        self.jump_speed=10
        self.jump_direction=None
        self.free_fall = False
        self.counter=0
        self.visible = True
        self.items=[]
        self.speed_power_timer = 0
        self.invisibility_timer = 0

class Collectable_list:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def get(self, id):
        pass
    def remove(self, item):
        self.items.remove(item)

class Collectable():
    def __init__(self):
        self.type=random.randint(1,3) # health, super-speed and invulnerability
        self.sprite=None
        self.x=random.randint(0,width-50)
        self.y=random.randint(0,height-50)
        self.type=None
        self.life = random.randint(300,2000)
        #self.hitbox=pygame.Rect(self.x,self.y,25,25)
        self.correct_position=False
        self.status=None
        self.collected=False
        self.counter=0
        self.vanish=False
        self.id = random.randint(0,10)
        self.time = random.randint(0,100) #Indicates at what time from timer the item will spawn
        self.active=None

    def generate(self):
        self.type = random.randint(1,3)
        self.x=random.randint(0,width-50)
        self.y=random.randint(0,height-50)
        '''self.hitbox=pygame.Rect(self.x,self.y,25,25)

        for wall in walls:
            if self.hitbox.colliderect(wall):
                self.correct_position=False
                return False
                #self.generate(walls)
            else:
                self.correct_position=True'''
        return True
    def recreate(self,x,y,time,life,type):
        self.x = x
        self.y = y
        self.time = time
        self.life = life
        self.type = type

    def levitate(self):
        self.counter+=1
        if self.counter<40:
            self.y+=0.2
        else:
            self.y-=0.2
            if self.counter>80:
                self.counter=0

    def collect(self,player):
        pass
        '''if self.hitbox.colliderect(player.hitbox):
            self.collected=True
            print("Item Collected")
            return True'''

    def display(self,gameDisplay,image):
        gameDisplay.blit(image,(self.x,self.y))


    def display_anime(self,gameDisplay,images,index):
        for image in images:
            gameDisplay.blit(images[index],(self.x,self.y))
            #pygame.draw.rect(gameDisplay,(99,99,99), self.hitbox)


class Timer(object):
    def __init__(self):
        self.start_time = None
        self.stop_time = None
        self.started = False

    def start(self):
        self.start_time = time.time()
        self.started=True

    def stop(self):
        self.stop_time = time.time()

    @property
    def time_elapsed(self):
        if not self.has_started:
            return 0
        return int(time.time() - self.start_time)

    @property
    def has_started(self):
        return self.start_time != None

    @property
    def total_run_time(self):
        print("HAS IT STARTED: " + str(self.has_started))

        return self.stop_time - self.start_time

    def __enter__(self):
        self.start()
        return self


totalConnections = 0
port = 5555
server = "192.168.1.225"
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
    'player':Player(0,0,["sprite1.png","right.png","left.png"],1,1,0),
    "timer": timer,
    "collectable": collectable_data
}, {
    'player': Player(100,100,["sprite2.png","player2right.png","player2left.png"],2,2,0),
    "timer": timer,
    "collectable": collectable_data
}]
'''talk about why parallel data sets not sent due to synch issues and buffer needed'''
#all_data[0]

timerHasStarted = False

#walls=[pygame.Rect(900,500,228,44),pygame.Rect(600, 250, 44, 228),pygame.Rect(200,350,228,44)]


for i in range(random.randint(10,20)):
    item = Collectable()
    if item.generate():
        collectable_data.append([item.x,item.y,item.time,item.life,item.type])


def threaded_client(conn, player):
    global totalConnections, timerHasStarted, timer

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

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    totalConnections += 1

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1


def error():
    print("You can't do that")
