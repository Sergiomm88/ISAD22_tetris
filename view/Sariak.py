import tkinter as tk
from tkinter import *
from tkinter import ttk
import sys
from view import Profila
from controller.db_conn import DbConn

# https://www.youtube.com/watch?v=0WafQCaok6g scrollbar

# Koloreak
botoi_kolor = "#ffffff"
atzeko_kolor = "#7ec0ee"


class Sariak(object):

    def __init__(self, erabiltzaile):
        super(Sariak, self).__init__()
        self.window = tk.Tk()
        self.window.protocol("WM_DELETE_WINDOW", sys.exit)  # "X" botoia erabiltzean programa gelditzea ahalbidetzen du
        self.window.title("Sariak")
        self.window.geometry('400x400')

        self.erabiltzaile=erabiltzaile
        global atzeko_kolor
        atzeko_kolor = DbConn.get_jokalari_fondoa(DbConn(), self.erabiltzaile)
        global  botoi_kolor
        botoi_kolor = DbConn.get_jokalari_botoi_kolor(DbConn(), self.erabiltzaile)
        self.window['bg'] = atzeko_kolor
        self.window.resizable(False, False)


        # 1 create a main frame
        nagusia = Frame(self.window, bg=atzeko_kolor)
        nagusia.pack(fill=BOTH, expand=1)

        # 2 create a canvas
        nire_canvas = Canvas(nagusia, bg=atzeko_kolor)
        nire_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # 3 add a scrollbar to the canvas
        scrollbar = ttk.Scrollbar(nagusia, orient=VERTICAL, command=nire_canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # 4 configure the canvas
        nire_canvas.configure(yscrollcommand=scrollbar.set)
        nire_canvas.bind('<Configure>', lambda e: nire_canvas.configure(scrollregion=nire_canvas.bbox("all")))

        # 5 create another frame inside canvas
        self.marko = Frame(nire_canvas, bg=atzeko_kolor)

        # 6 add that new frame to a window in the canvas
        nire_canvas.create_window((0, 0), window=self.marko, anchor="nw")


        emaitza = DbConn.sariak_lortu(DbConn(), self.erabiltzaile)
        lerroKop = len(emaitza)
        #TODO
        if lerroKop == 0:
            Label(self.marko, text="Ez dago saririk", font="Helvetica", bg=atzeko_kolor).grid(row=lerroKop, column=0, pady=10, padx=10)
        else:
            Label(self.marko, text="MAILA", bg=atzeko_kolor).grid(row=1, column=0, pady=10, padx=10)
            Label(self.marko, text="PR", bg=atzeko_kolor).grid(row=1, column=1, pady=10, padx=10)
            Label(self.marko, text="1 SARIA", bg=atzeko_kolor).grid(row=1, column=2, pady=10, padx=10)
            Label(self.marko, text="2 SARIA", bg=atzeko_kolor).grid(row=1, column=3, pady=10, padx=10)
            Label(self.marko, text="3 SARIA", bg=atzeko_kolor).grid(row=1, column=4, pady=10, padx=10)
            lerro=0
            kont=2
            for i in range(lerroKop):
                if emaitza[i][0]==0:
                    Label(self.marko, text="Orokorra", bg=atzeko_kolor).grid(row=lerro+2, column=0, pady=10, padx=10)
                else:
                    maila = emaitza[i][0]+'x'+emaitza[i][1]
                    Label(self.marko, text=maila, bg=atzeko_kolor).grid(row=lerro + 2, column=0, pady=10, padx=10)
                if kont==2:
                    Label(self.marko, text=emaitza[i][3], bg=atzeko_kolor).grid(row=lerro + 2, column=1, pady=10, padx=10)
                Label(self.marko, text=emaitza[i][2], bg=atzeko_kolor).grid(row=lerro + 2, column=kont, pady=10, padx=10)
                kont=kont+1
                if kont==5:
                    kont=2
                    lerro=lerro+1
        Button(self.marko, text="Irten", cursor="hand2", width=8, font=("Times New Roman", 16), bg=botoi_kolor, command=self.irten).grid(row=lerroKop+3, column=2, pady=10, padx=10)
        self.window.mainloop()

    def irten(self):
        self.window.destroy()
        Profila.Profila(self.erabiltzaile).__init__()
