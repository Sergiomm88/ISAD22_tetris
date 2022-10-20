import random
import tkinter as tk

import view
from model.Tableroa import Tableroa
from model.Piezak import *
import sys
import Irudiak
from tkinter import *
from decimal import *

abiadura = 1
tamaina2 = 2

class JokatuLehioa(object):
	"""docstring for JokatuLeioa"""


	def __init__(self, abiadura_param, tamaina_param, erab):
		super(JokatuLehioa, self).__init__()
		self.abiadura = abiadura_param
		self.tamaina = tamaina_param
		self.erabiltzaile=erab
		self.window = tk.Tk()
		# Irudia gehitu
		bg = PhotoImage(file="Irudiak/fondo.png", width=(self.tamaina * 27), height=(self.tamaina * 45))
		self.argazkia= Label(self.window, image=bg, padx=0, pady=0, bd=1)

		# "X" botoia erabiltzean programa gelditzea ahalbidetzen du
		self.window.protocol("WM_DELETE_WINDOW", sys.exit)
		leihoTamaina = (str(self.tamaina * 27) + "x" + str(self.tamaina * 45))
		self.window.geometry(leihoTamaina)
		self.window.title("Tetris Jokoa")
		#self.window.resizable(False,False)
		global abiadura
		global tamaina2
		abiadura = self.abiadura
		tamaina2 = self.tamaina

		button = tk.Button(self.window, cursor="hand2", text="Partida hasi", bg="#ffffff")
		button.pack()

		puntuazioa = tk.StringVar()
		puntuazioa.set("Puntuazioa: 0")

		puntuazioalabel = tk.Label(self.window, textvariable=puntuazioa, bg="#ffffff")
		puntuazioalabel.pack()

		canvas = TableroaPanela(master=self.window, tamaina=(tamaina2, 40), puntuazioalabel=puntuazioa)
		button.configure(command=canvas.jolastu)
		canvas.pack()
		Button(self.window, text="Irten", bg="#ffffff", command=self.irten).pack()
		#self.argazkia.pack_configure(expand=YES, fill=BOTH)
		self.argazkia.lower(belowThis=None)
		self.argazkia.place(x=0, y=0)
		self.window.bind("<Up>", canvas.joku_kontrola)
		self.window.bind("<Down>", canvas.joku_kontrola)
		self.window.bind("<Right>", canvas.joku_kontrola)
		self.window.bind("<Left>", canvas.joku_kontrola)

		self.window.mainloop()

	# Irtetzeko metodoa:
	def irten(self):
		self.window.destroy()
		view.Ezarpenak.Ezarpenak(self.erabiltzaile).__init__()

class TableroaPanela(tk.Frame):
	def __init__(self, tamaina, gelazka_tamaina=20,puntuazioalabel=None, master=None):
		tk.Frame.__init__(self, master)
		self.puntuazio_panela = puntuazioalabel
		self.tamaina = tamaina
		self.gelazka_tamaina = gelazka_tamaina
		global abiadura

		# Irudia gehitu
		bg = PhotoImage(file="Irudiak/fondo.png")


		# Canvas sortu eta bere ezaugarriak gehitu
		self.canvas = tk.Canvas(
			width=self.tamaina[0]  * self.gelazka_tamaina+1,
			height=self.tamaina[1] * self.gelazka_tamaina+1,
			bg='#eee', borderwidth=0, highlightthickness=0
		)
		self.canvas.pack(expand=tk.YES, fill=None)

		self.tab = Tableroa(tamaina)
		self.jokatzen = None
		self.tableroa_ezabatu()


	def marratu_gelazka(self, x,y,color):
		self.canvas.create_rectangle(x*self.gelazka_tamaina, y*self.gelazka_tamaina,
									(x+1)*self.gelazka_tamaina, (y+1)*self.gelazka_tamaina, fill=color)

	def tableroa_ezabatu(self):
		self.canvas.delete("all")
		self.canvas.create_rectangle(0, 0, self.tamaina[0] * self.gelazka_tamaina, self.tamaina[1] * self.gelazka_tamaina, fill='#eee')

	def marraztu_tableroa(self):
		self.tableroa_ezabatu()
		for i in range(self.tab.tamaina[1]):
			for j in range(self.tab.tamaina[0]):
				if self.tab.tab[i][j]:
					self.marratu_gelazka(j,i,self.tab.tab[i][j])
		if self.tab.pieza:
			for i in range(4):
				x = self.tab.posizioa[0] + self.tab.pieza.get_x(i)
				y = self.tab.posizioa[1] + self.tab.pieza.get_y(i)
				self.marratu_gelazka(y,x,self.tab.pieza.get_kolorea())
		self.puntuazioa_eguneratu()


	def pausu_bat(self):
		try:
			self.tab.betetako_lerroak_ezabatu()
			self.tab.mugitu_behera()
		except Exception as error:
			try:
				self.tab.pieza_finkotu(self.tab.posizioa)
				pieza_posibleak = [Laukia, Zutabea, Lforma, LformaAlderantzizko, Zforma, ZformaAlderantzizko, Tforma]
				self.tab.sartu_pieza(random.choice(pieza_posibleak)())
			except Exception as e:
				print("GAMEOVER")
				self.tab.hasieratu_tableroa()
				return

		self.jokatzen = self.after(abiadura, self.pausu_bat)
		self.marraztu_tableroa()

	def puntuazioa_eguneratu(self):
		if self.puntuazio_panela:
			self.puntuazio_panela.set(f"Puntuazioa: {self.tab.puntuazioa}")



	def joku_kontrola(self, event):
		try:
			if event.keysym == 'Up':
				self.tab.biratu_pieza()
			if event.keysym == 'Down':
				self.tab.pieza_kokatu_behean()
			if event.keysym == 'Right':
				self.tab.mugitu_eskumara()
			if event.keysym == 'Left':
				self.tab.mugitu_ezkerrera()
		except Exception as error:
			pass
		finally:
			self.marraztu_tableroa()

	def jolastu(self):
		if self.jokatzen:
			self.after_cancel(self.jokatzen)
		self.tab.hasieratu_tableroa()
		pieza_posibleak = [Laukia, Zutabea, Lforma, LformaAlderantzizko, Zforma, ZformaAlderantzizko, Tforma]
		self.tab.sartu_pieza(random.choice(pieza_posibleak)())
		self.marraztu_tableroa()
		self.jokatzen = self.after(abiadura, self.pausu_bat)


