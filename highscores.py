import sqlite3
from tkinter import *

class Records():

     #class created to see records that have been previously inputted#
    def __init__(self,master,run):
        self.run = run
        self.master=master
        self.master.geometry('450x200+100+200')
        self.master.title('Highscore')
        self.connection = sqlite3.connect('playerdata.db')
        self.cursor = self.connection.cursor()
        self.username_label = Label(self.master, text="Username", width=20)
        self.username_label.grid(row=0, column=0)
        #self.password_label = Label(self.master, text="Password", width=10)
        #self.password_label.grid(row=0, column=1)
        self.score_label = Label(self.master, text="Highscores", width=20)
        self.score_label.grid(row=0, column=2)
        self.sorted_scores= []
        self.player_dict ={}
        self.showallrecords()

    def showallrecords(self):
        index=0
        data = self.readfromdatabase()
        for array in data:
            self.sorted_scores.append(array[2])
            self.player_dict[array[2]] = array[0]
        for score in self.sorted_scores:
            if score is None:
                pointer = self.sorted_scores.index(score)
                self.sorted_scores[pointer]=0
        print(self.sorted_scores)
        self.sorted_scores=self.merge_sort(self.sorted_scores)


        for score in self.sorted_scores:
            index+=1
            if score == 0:
                Label(self.master, text=self.player_dict[None]).grid(row=index, column=0)
                Label(self.master, text=0).grid(row=index, column=2)
            else:
                Label(self.master, text=self.player_dict[score]).grid(row=index, column=0)
                Label(self.master, text=score).grid(row=index, column=2)

        '''for index, dat in enumerate(data):
            Label(self.master, text=dat[0]).grid(row=index+1, column=0)
            #Label(self.master, text=dat[1]).grid(row=index+1, column=1)
            Label(self.master, text=dat[2]).grid(row=index+1, column=2)'''

    def readfromdatabase(self):
        self.cursor.execute("SELECT* FROM player")
        #print(self.cursor.fetchall)
        return self.cursor.fetchall()


    def merge_sort(self,score_list):
      if len(score_list)<=1:
        return score_list
      mid = int((len(score_list))/2)
      left = self.merge_sort(score_list[:mid])
      right = self.merge_sort(score_list[mid:])
      return self.merge(left,right)

    def merge(self,left,right):
      final_list = []
      left_pointer = 0
      right_pointer = 0

      while left_pointer<len(left) and right_pointer < len(right):
        if left[left_pointer]> right[right_pointer]:
          final_list.append(left[left_pointer])
          left_pointer +=1
        else:
          final_list.append(right[right_pointer])
          right_pointer +=1

      final_list.extend(left[left_pointer:])
      final_list.extend(right[right_pointer:])
      return final_list

    #final = merge_sort(score_list)



def run_table():
    root=Tk()
    instance = Records(root,True)
    root.mainloop()

#instance = Records(root,True)
