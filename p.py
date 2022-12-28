# # Cronometro 
# # @autor: Magno Efren
# # Youtube: https://www.youtube.com/c/MagnoEfren

# from tkinter import Canvas, Button, Frame, Label,Tk

# ventana = Tk()
# ventana.config(bg='black')
# ventana.geometry('500x250')
# ventana.title('Cronometro')
# ventana.minsize(width=500, height=250)

# ventana.columnconfigure([0,1,2],weight=2)
# #ventana.columnconfigure(1, weight=2)
# #ventana.columnconfigure(2,weight=2)
# ventana.rowconfigure(0, weight=2)
# ventana.rowconfigure(1,weight=1)

# frame1 = Frame(ventana)
# frame1.grid(column=0,row=0,sticky='snew')
# frame2 = Frame(ventana)
# frame2.grid(column=1,row=0,sticky='snew')
# frame3 = Frame(ventana)
# frame3.grid(column=2,row=0,sticky='snew')
# frame4 = Frame(ventana, bg='gray10')
# frame4.grid(row=1, columnspan=3, sticky='snew')
# frame5 = Frame(ventana, bg='black')
# frame5.grid(row=2, columnspan=3, sticky='snew')
# #---
# frame1.columnconfigure(0, weight=1)
# frame1.rowconfigure(0, weight=1)
# frame2.columnconfigure(0, weight=1)
# frame2.rowconfigure(0, weight=1)
# frame3.columnconfigure(0, weight=1)
# frame3.rowconfigure(0, weight=1)
# frame4.columnconfigure(0, weight=1)
# frame4.rowconfigure(0, weight=1)
# frame5.columnconfigure(0, weight=1)
# frame5.rowconfigure(0, weight=1)


# canvas1= Canvas(frame1, bg='gray40', width=200, height =200,highlightthickness=0)
# canvas1.grid(column=0,row=0, sticky='nsew')
# canvas2= Canvas(frame2, bg='gray30', width=200, height =200,highlightthickness=0)
# canvas2.grid(column=0,row=0, sticky='nsew')
# canvas3= Canvas(frame3, bg='gray20', width=200, height =200,highlightthickness=0)
# canvas3.grid(column=0,row=0, sticky='nsew')


# texto1 = canvas1.create_text(1,1, text='0', font=('Arial',12,'bold'), fill= 'White')
# texto2 = canvas2.create_text(1,1, text='0', font=('Arial',12,'bold'), fill= 'White')
# texto3 = canvas3.create_text(1,1, text='0', font=('Arial',12,'bold'), fill= 'White')

# texto_minutos = canvas1.create_text(1,1, text='Minutos', 
# 	font=('Arial',12,'bold'), fill= 'White')
# texto_segundos = canvas2.create_text(1,1, text='Segundos', 
# 	font=('Arial',12,'bold'), fill= 'White')
# texto_milisegundos  = canvas3.create_text(1,1, text='Milisegundos', 
# 	font=('Arial',10,'bold'), fill= 'White')

# circulo1 = canvas1.create_oval(10,10,100,100, outline='red2',width=10)
# circulo2 = canvas2.create_oval(10,10,100,100, outline='medium spring green',width=10)
# circulo3 = canvas3.create_oval(10,10,100,100, outline='magenta2',width=10)

# mi = 0
# se = 0
# ml = 0
# contar = 0
# click_lectura = 0
# clik_stop = 0
# clik_inicio =0
# def coordenadas():
# 	x = canvas1.winfo_width()
# 	y = canvas1.winfo_height()
# 	x1 = int(x - 0.1*x - 0.1*y + 25)
# 	y1 = int(y - 0.1*x - 0.1*y + 20)
# 	x2 = int(x - 0.4*x - 0.4*y - 15)
# 	y2 = int(y - 0.4*x - 0.4*y - 30)
# 	tamano = int( y1*0.2 + x1*0.1 + 10 )
# 	tamano_texto = int( y1*0.02 + x1*0.02 + 3 )
# 	#print(x1, y1, x2, y2)	
# 	canvas1.coords(circulo1, x1,y1,x2,y2)
# 	canvas2.coords(circulo2, x1,y1,x2,y2)
# 	canvas3.coords(circulo3, x1,y1,x2,y2)

# 	#cordenas numeros
# 	z1 = int(x1*0.6- 10)
# 	z2 = int(y1*0.6 - 10)
# 	#coordenadas texto 
# 	w1 = int(x1*0.49 + 8)
# 	w2 = int(y1*0.8 + 10)
# 	canvas1.coords(texto1, z1, z2)
# 	canvas2.coords(texto2, z1, z2)
# 	canvas3.coords(texto3, z1, z2)	
# 	canvas1.itemconfig(texto1, font=('Arial',tamano,'bold'),text= mi)
# 	canvas2.itemconfig(texto2, font=('Arial',tamano,'bold'),text= se )
# 	canvas3.itemconfig(texto2, font=('Arial',tamano,'bold'), text= ml)
# 	canvas1.coords(texto_minutos, w1, w2)
# 	canvas2.coords(texto_segundos, w1, w2)
# 	canvas3.coords(texto_milisegundos, w1, w2)
# 	canvas1.itemconfig(texto_minutos, font=('Arial',tamano_texto,'bold'))
# 	canvas2.itemconfig(texto_segundos, font=('Arial',tamano_texto,'bold'))
# 	canvas3.itemconfig(texto_milisegundos, font=('Arial',tamano_texto,'bold'))	
	
# 	canvas1.after(1000, coordenadas)

# coordenadas()
# ventana.mainloop()
import tkinter as tk
import random
def actualizar_etiqueta():
    numero_aleatorio = random.randint(1, 100)
    etiqueta1.config(text=f"Número aleatorio: {numero_aleatorio}")
    
ventana = tk.Tk()
ventana.title("Ejemplo after() en Tk")
ventana.config(width=400, height=300)
etiqueta1 = tk.Label(text="¡Hola mundo!")
etiqueta1.place(x=100, y=70)
ventana.after(2000, actualizar_etiqueta)
ventana.mainloop()