import random
import tkinter as tk
from model.Tableroa import Tableroa
from model.Piezak import *

class JokatuLeioa(object):
	"""docstring for JokatuLeioa"""
	
	def __init__(self):
		super(JokatuLeioa, self).__init__()
		self.window = tk.Tk()
		self.window.geometry('220x450')
		self.window.title("Tetris jokoa")

		

		button = tk.Button(self.window, text="Partida hasi")
		button.pack()

		canvas = TableroaPanela(master=self.window)
		button.configure(command=canvas.jolastu)
		canvas.pack()
		self.window.bind("<Up>", canvas.joku_kontrola)
		self.window.bind("<Down>", canvas.joku_kontrola)
		self.window.bind("<Right>", canvas.joku_kontrola)
		self.window.bind("<Left>", canvas.joku_kontrola)

		self.window.mainloop()

class TableroaPanela(tk.Frame):
	def __init__(self, tamaina=(10,20), gelazka_tamaina=20, master=None):
		tk.Frame.__init__(self, master)
		self.tamaina = tamaina
		self.gelazka_tamaina = gelazka_tamaina

		self.canvas = tk.Canvas(
			width=self.tamaina[0]  * self.gelazka_tamaina,
			height=self.tamaina[1] * self.gelazka_tamaina,
			bg='#eee'
		)
		self.canvas.pack(expand=tk.YES, fill=None)

	def marratu_gelazka(self, x,y,color):
		self.canvas.create_rectangle(x*self.gelazka_tamaina, y*self.gelazka_tamaina,
									(x+1)*self.gelazka_tamaina, (y+1)*self.gelazka_tamaina, fill=color)

	def marraztu_tableroa(self):
		self.canvas.delete("all")
		for i in range(self.tab.tamaina[1]):
			for j in range(self.tab.tamaina[0]):
				if self.tab.tab[i][j]:
					self.marratu_gelazka(j,i,self.tab.tab[i][j])
		if self.tab.pieza:
			for i in range(4):
				x = self.tab.posizioa[0] + self.tab.pieza.get_x(i)
				y = self.tab.posizioa[1] + self.tab.pieza.get_y(i)
				self.marratu_gelazka(y,x,self.tab.pieza.get_kolorea())


	def pausu_bat(self):
		try:
			self.tab.betetako_lerroak_ezabatu()
			self.tab.mugitu_behera()
		except Exception as error:
			self.tab.pieza_finkotu(self.tab.posizioa)
			pieza_posibleak = [Laukia, Zutabea, Lforma, LformaAlderantzizko, Zforma, ZformaAlderantzizko, Tforma]
			try:
				self.tab.sartu_pieza(random.choice(pieza_posibleak)())
			except Exception as e:
				print("GAMEOVER")
				self.tab.hasieratu_tableroa()
				return
		finally:
			self.after(400, self.pausu_bat)
			self.marraztu_tableroa()
		

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
		self.tab = Tableroa()
		self.tab.hasieratu_tableroa()
		pieza_posibleak = [Laukia, Zutabea, Lforma, LformaAlderantzizko, Zforma, ZformaAlderantzizko, Tforma]
		self.tab.sartu_pieza(random.choice(pieza_posibleak)())
		self.marraztu_tableroa()
		self.after(400, self.pausu_bat)
		
