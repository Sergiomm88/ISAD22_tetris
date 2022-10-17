import tkinter as tk
from tkinter import ttk

import view
from view.JokatuLehioa import JokatuLehioa

#Koloreak
botoi_kolor = "#ffffff"
atzeko_kolor = "plum1"

class Ezarpenak(object):


    def __init__(self, erabiltzaile):
        super(Ezarpenak, self).__init__()
        self.erabiltzaile=erabiltzaile
        self.window = tk.Tk()
        self.window.geometry('400x400')
        self.window.title("Tetris Jokoa")
        self.window['bg']=atzeko_kolor
        self.window.resizable(False, False)

        espacio = tk.Label(self.window, bg=atzeko_kolor, text="")
        titulo = tk.Label(self.window, bg=atzeko_kolor, text="Partidaren ezarpenak", font=("Times New Roman",25))
        titulo.pack()
        espacio.pack()

        mensaje = tk.Label(self.window, bg=atzeko_kolor, text="Partidaren ezaugarriak aukera itzazu ", font=("Calibri"))
        mensaje.pack()

        mensaje2 = tk.Label(self.window, bg=atzeko_kolor, text="(bana aukeratu arte ezingo da partida hasi) ", font=("Calibri"))
        mensaje2.pack()

        espacio.pack()

        titulo_abiadura = tk.Label(self.window, bg=atzeko_kolor, text="Abiadura:", font=("Calibri", 14))
        titulo_abiadura.place(x=60, y= 110)

        self.opcion = tk.IntVar()
        self.opcion.set(value=1)



        self.a1 = tk.Radiobutton(self.window, bg=atzeko_kolor, text="Erraza", variable=self.opcion,value=1).place(x=50, y=150)
        self.a2 = tk.Radiobutton(self.window, bg=atzeko_kolor, text="Ertaina", variable=self.opcion,value=2).place(x=130, y=150)
        self.a3 = tk.Radiobutton(self.window, bg=atzeko_kolor, text="Zaila", variable=self.opcion,value=3).place(x=210, y=150)
        self.a4 = tk.Radiobutton(self.window, bg=atzeko_kolor, text="Oso zaila", variable=self.opcion,value=4).place(x=280, y=150)



        titulo_tamaina = tk.Label(self.window, bg=atzeko_kolor, text="Tamaina:", font=("Calibri", 14))
        titulo_tamaina.place(x=60, y=190)

        self.opcion2 = tk.IntVar()
        self.opcion2.set(value=1)


        self.t1 = tk.Radiobutton(self.window, bg=atzeko_kolor, text="Erraza", variable=self.opcion2, value=1).place(x=50, y=230)
        self.t2 = tk.Radiobutton(self.window, bg=atzeko_kolor, text="Ertaina", variable=self.opcion2, value=2).place(x=130, y=230)
        self.t3 = tk.Radiobutton(self.window,  bg=atzeko_kolor,text="Zaila", variable=self.opcion2, value=3).place(x=210, y=230)
        self.t4 = tk.Radiobutton(self.window, bg=atzeko_kolor, text="Oso zaila", variable=self.opcion2, value=4).place(x=280, y=230)

        buttonirten = tk.Button(self.window, bg=botoi_kolor, text="Irten", width=8, font=("Calibri"), command=self.irten)
        buttonirten.place(x=60, y=300)
        buttonj = tk.Button(self.window, bg=botoi_kolor, text="Jolastu", width=8, font=("Calibri"), command=self.jolastenHasi)
        buttonj.place(x=220, y=300)


        self.window.mainloop()

    # PANTAILETAN MUGITZEKO
    def irten(self):
        self.window.destroy()
        if(self.erabiltzaile is None):
            view.HasierakoMenua.HasierakoMenua().__init__()
        else:
            view.Profila.Profila(self.erabiltzaile).__init__()


    def jolastenHasi(self):
        self.window.destroy()
        JokatuLehioa().__init__()

