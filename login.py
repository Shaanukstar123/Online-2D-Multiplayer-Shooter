'''from tkinter import *
import sqlite3
from tkinter import messagebox as ms
from MainMenu import *'''
import pygame
from Network import Network
from classes import *
from MainMenu import menu
import time
import socket
from _thread import *
import sqlite3
from tkinter import*
from tkinter import messagebox as ms
from MainGame import *

with sqlite3.connect("playerdata.db") as db:
    cursor =db.cursor()
cursor.execute ("CREATE TABLE IF NOT EXISTS player(username TEXT NOT NULL, password TEXT NOT NULL, highscore INTEGER NOT NULL)")
db.commit()
db.close()

class Login_system():
    def __init__(self,root):
        self.root=root
        self.root.title('Login')
        self.username=StringVar()
        self.password = StringVar()
        self.new_username=StringVar()
        self.new_pass=StringVar()
        self.widgets()
        self.start_game=False
        self.hash = {}

    def login(self):
        #self.widgets()
        with sqlite3.connect("playerdata.db") as db:
            cursor =db.cursor()
        player_search=("SELECT * FROM player WHERE username=?  and password=?")
        cursor.execute(player_search,[self.username.get(),self.encrypt(self.password.get ())])
        returned = cursor.fetchall()
        if returned:
            self.logframe.pack_forget()
            self.header['text'] = self.username.get() + '\n Logged In'
            self.header["pady"] = 150
            self.start_game=True
            self.root.quit()
            start_check(self.username.get())

        else:
            if self.username.get() == "" or self.password.get() == "" :
                 ms.showerror("Error","Please do not leave username or password fields blank.")
            else:
                print("not found")
                ms.showerror("Error","Account details not found. Please make sure the details are entered properly.")

    def create_account(self):
        with sqlite3.connect('playerdata.db') as db:
            cursor = db.cursor()

        player_search = ('SELECT * FROM player WHERE username = ?')
        cursor.execute(player_search,[(self.new_username.get())])

        if cursor.fetchall() or self.new_username.get() == "" or self.new_pass.get()== "":
            print(self.new_username.get())
            if self.new_username.get() == "" or self.new_pass.get()== "":
                ms.showerror("Error","Fields cannot be blank")
            else:
                ms.showerror("Error","This username has already been taken. Please chose another one")
        else:
            ms.showinfo("Success","Account created successfully")
            self.log_frame()
            store = 'INSERT INTO player(username,password,highscore) VALUES(?,?,0)'
            cursor.execute(store,[(self.new_username.get()),self.encrypt((self.new_pass.get()))])
        db.commit()

    def encrypt(self,password):
        password_list  = [ord(i) for i in password]
        new_password_list=[]
        for char in password_list:
            new_password_list.append(char+2)
        new_pass=''.join(chr(i) for i in new_password_list)
        return new_pass


    def log_frame(self):
        self.username.set('')
        self.password.set('')
        self.header['text'] = 'Login'
        self.createframe.pack_forget()
        self.logframe.pack()
    def create_frame(self):
        self.new_username.set('')
        self.new_pass.set('')
        self.header['text'] = 'Create Account'
        self.logframe.pack_forget()
        self.createframe.pack(fill="both", expand=True)

    def widgets(self):
        self.header = Label(self.root,text = 'Login',font = ("fixedsys",35),pady = 10)
        self.header.pack()
        self.logframe = Frame(self.root,padx =10,pady = 10)
        Label(self.logframe,text = 'username: ',font = ("fixedsys",20),pady=20,padx=55).grid(sticky = W)
        Entry(self.logframe,textvariable = self.username,bd = 5,font = ("fixedsys",15)).grid(row=0,column=1)
        Label(self.logframe,text = 'Password: ',font = ("fixedsys",20),pady=20,padx=55).grid(sticky = W)
        Entry(self.logframe,textvariable = self.password,bd = 5,font = ("fixedsys",15),show = '*').grid(row=1,column=1)
        Button(self.logframe,text = ' Login ',bd = 3 ,font = ("fixedsys",15),padx=5,pady=5,command=self.login).grid()
        Button(self.logframe,text = ' Create Account ',bd = 3 ,font = ("fixedsys",15),padx=5,pady=5,command=self.create_frame).grid(row=2,column=1)
        self.logframe.pack(fill="both", expand=True)

        self.createframe = Frame(self.root,padx =10,pady = 10)
        Label(self.createframe,text = 'username: ',font = ("fixedsys",20),pady=5,padx=5).grid(sticky = W)
        Entry(self.createframe,textvariable = self.new_username,bd = 5,font = ("fixedsys",15)).grid(row=0,column=1)
        Label(self.createframe,text = 'Password: ',font = ("fixedsys",20),pady=5,padx=5).grid(sticky = W)
        Entry(self.createframe,textvariable = self.new_pass,bd = 5,font = ("fixedsys",15),show = '*').grid(row=1,column=1)
        Button(self.createframe,text = 'Create Account',bd = 3 ,font = ("fixedsys",15),padx=5,pady=5,command=self.create_account).grid()
        Button(self.createframe,text = 'Go to Login',bd = 3 ,font = ("fixedsys",15),padx=5,pady=5,command=self.log_frame).grid(row=2,column=1)

root=Tk()
root.geometry("600x350")
login=Login_system(root)

root.mainloop()
