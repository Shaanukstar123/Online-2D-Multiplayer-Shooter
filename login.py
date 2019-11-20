from tkinter import *
import sqlite3
from tkinter import messagebox as ms

with sqlite3.connect("quit.db") as db:
    cursor =db.cursor()
cursor.execute ("CREATE TABLE IF NOT EXISTS player(username TEXT NOT NULL, password TEXT NOT NULL, highscores INTEGER)")
cursor.execute ("SELECT* FROM player")
db.commit()
db.close()

class Login_system():
    def __init__(self,root):
        self.root=root
        self.username=StringVar()
        self.password = StringVar()
        self.new_username=StringVar()
        self.new_pass=StringVar()
        self.widgets()

    def login(self):
        with sqlite3.connect("quit.db") as db:
            cursor =db.cursor()
        player_search=("SELECT* FROM player WHERE username=?  and password=?")
        cursor.execute(player_search,[self.username.get(),self.password.get ()])
        returned = cursor.fetchall()
        if returned:
            self.logframe.pack_forget()
            self.header["text"] = self.username.get()
            self.header["pady"] = 150
        else:
            ms.showerror("Account details not found. Please make sure the details are entered properly.")

    def create_account(self):
        with sqlite3.connect('quit.db') as db:
            cursor = db.cursor()

        player_search = ('SELECT * FROM player WHERE username = ?')
        cursor.execute(player_search,[(self.username.get())])
        if cursor.fetchall():
            ms.showerror("This username has already been taken. Please chose another one")
        else:
            ms.showinfo("Account created successfully")
            self.login()
        store = 'INSERT INTO player(username,password) VALUES(?,?)'
        cursor.execute(store,[(self.new_username.get()),(self.new_pass.get())])
        db.commit()

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
        self.createframe.pack()

    def widgets(self):


        self.header = Label(self.root,text = 'Login',font = ('',35),pady = 10)
        self.header.pack()
        self.logframe = Frame(self.root,padx =10,pady = 10)
        Label(self.logframe,text = 'username: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.logframe,textvariable = self.username,bd = 5,font = ('',15)).grid(row=0,column=1)
        Label(self.logframe,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.logframe,textvariable = self.password,bd = 5,font = ('',15),show = '*').grid(row=1,column=1)
        Button(self.logframe,text = ' Login ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.log_frame).grid()
        Button(self.logframe,text = ' Create Account ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.create_frame).grid(row=2,column=1)
        self.logframe.pack()

        self.createframe = Frame(self.root,padx =10,pady = 10)
        Label(self.createframe,text = 'username: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.createframe,textvariable = self.new_username,bd = 5,font = ('',15)).grid(row=0,column=1)
        Label(self.createframe,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.createframe,textvariable = self.new_pass,bd = 5,font = ('',15),show = '*').grid(row=1,column=1)
        Button(self.createframe,text = 'Create Account',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.create_account).grid()
        Button(self.createframe,text = 'Go to Login',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.log_frame).grid(row=2,column=1)



root=Tk()
Login_system(root)
root.mainloop()
