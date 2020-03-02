import sqlite3
from tkinter import *

class Highscores():

    def __init__(self,master,run):
        self.run = run
        self.root=master
        self.height = 250
        self.root.geometry('650x'+(str(self.height))+'+100+200')
        self.root.title('Highscore')
        self.connection = sqlite3.connect('playerdata.db')
        self.cursor = self.connection.cursor()
        self.username_label = Label(self.root, text="Username",font = ("fixedsys",22), width=20, background = "black", foreground = "white")
        self.username_label.grid(row=0, column=0)
        self.score_label = Label(self.root, text="Highscores",font = ("fixedsys",22), width=20, background = "black", foreground = "white")
        self.score_label.grid(row=0, column=2)
        self.sorted_scores= []
        self.player_dict ={}
        self.root.configure(background='black')

        self.showallrecords()

    def showallrecords(self):
        index=0
        data = self.readfromdatabase()
        print("This is data: ",data)
        for array in data:
            print("This is array: ", array)
            self.sorted_scores.append(array[1])
            self.player_dict[array[0]] = array[1]
        for score in self.sorted_scores:
            if score is None:
                pointer = self.sorted_scores.index(score)
                self.sorted_scores[pointer]=0
        self.sorted_scores=self.merge_sort(self.sorted_scores)

        no_score = []
        no_score_count=-1
        for key in self.player_dict:
            if self.player_dict[key] == 0:
                no_score.append(key)

        for score in self.sorted_scores:
            index+=2
            if score == 0:
                no_score_count+=1
                print(self.player_dict)
                Label(self.root, text=no_score[no_score_count-1],font = ("fixedsys",17), background = "black", foreground = "white").grid(row=index, column=0)
                Label(self.root, text=0,font = ("fixedsys",17), background = "black", foreground = "white").grid(row=index, column=2)
            else:
                player_name = (list(self.player_dict.keys())[list(self.player_dict.values()).index(score)])
                Label(self.root, text=player_name,font = ("fixedsys",17), background = "black", foreground = "white").grid(row=index, column=0)
                Label(self.root, text=score,font = ("fixedsys",17), background = "black", foreground = "white").grid(row=index, column=2)

    def readfromdatabase(self):
        self.cursor.execute("SELECT username, highscore FROM player")
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


def run_table():
    root=Tk()
    instance = Highscores(root,True)
    root.mainloop()
