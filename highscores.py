import sqlite3
from tkinter import *

class Records():

     #class created to see records that have been previously inputted#
    def __init__(self,master,run):
        self.run = run
        self.master=master
        self.master.geometry('450x200+100+200')
        self.master.title('Highscores')
        self.connection = sqlite3.connect('playerdata.db')
        self.cursor = self.connection.cursor()
        self.username_label = Label(self.master, text="Username", width=20)
        self.username_label.grid(row=0, column=0)
        #self.password_label = Label(self.master, text="Password", width=10)
        #self.password_label.grid(row=0, column=1)
        self.score_label = Label(self.master, text="Highscores", width=20)
        self.score_label.grid(row=0, column=2)
        self.showallrecords()

    def showallrecords(self):
        data = self.readfromdatabase()
        for index, dat in enumerate(data):
            Label(self.master, text=dat[0]).grid(row=index+1, column=0)
            #Label(self.master, text=dat[1]).grid(row=index+1, column=1)
            Label(self.master, text=dat[2]).grid(row=index+1, column=2)

    def readfromdatabase(self):
        self.cursor.execute("SELECT * FROM player")
        return self.cursor.fetchall()

def run_table():
    root=Tk()
    instance = Records(root,True)
    root.mainloop()

#instance = Records(root,True)
