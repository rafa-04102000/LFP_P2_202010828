from tkinter import Tk, SOLID, Frame,Label,Button,Toplevel,Text,Scrollbar,ttk,filedialog,messagebox,END,INSERT,Entry

class ModuloATDP(Frame):
    def __init__(self, gestor, master, padre) -> None:
        super().__init__(master)
        self.gestor = gestor
        self.master = master
        self.padre = padre
        self.config(width="600", height="500" )
        self.master.title("Modulo Automata De Pila")
        self.master.resizable(0,0)
        self.master.protocol("WM_DELETE_WINDOW", self.regresar)

        self.btn_mostrar_informacion = Button(self, text="Mostrar Informacion General",cursor='hand2',relief=SOLID,state="disabled",command=self.info_adpl)
        self.btn_validar_cadena= Button(self, text="Validar Cadena",cursor='hand2',relief=SOLID,state="disabled",command=self.validar_cadena)
        self.btn_ruta_validacion= Button(self, text="Ruta De Validacion",cursor='hand2',relief=SOLID,state="disabled",command=self.validar_ruta)
        self.btn_recorrido_paso_a_paso = Button(self, text="Recorrido Paso A Paso",cursor='hand2',relief=SOLID,state="disabled",command=self.pasoApaso)
        self.btn_validar_cadena_unaPasada = Button(self, text="Validar Cadena En Una Pasada",cursor='hand2',relief=SOLID,state="disabled",command=self.validar_cadena_en_una_pasada)


        self.text_area_info = Text()

        self.nombres_atp = []
        self.combobox_mostrar_atps = ttk.Combobox(self,state="readonly")
        self.llenar_lista_atms()

        self.ingreso_cadena = Entry(self)

        self.pack()
        self.crear_contenido()

    def crear_contenido(self):

        btn_cargar_archivo = Button(self, text="Cargar Archivo",cursor='hand2',relief=SOLID,command=self.cargar_archivo)
        btn_cargar_archivo.place(relx=0.11,rely=0.10,width=130,height=50)

        self.btn_mostrar_informacion.place(relx=0.06,rely=0.27,width=190,height=50)
        self.btn_validar_cadena.place(relx=0.06,rely=0.40,width=190,height=50)
        self.btn_ruta_validacion.place(relx=0.06,rely=0.52,width=190,height=50)
        self.btn_recorrido_paso_a_paso.place(relx=0.06,rely=0.65,width=190,height=50)
        self.btn_validar_cadena_unaPasada.place(relx=0.06,rely=0.77,width=190,height=50)

                
        
        self.combobox_mostrar_atps.place(relx=0.47,rely=0.07)
        self.combobox_mostrar_atps['values'] = self.nombres_atp

        btn_seleccionar = Button(self, text="Seleccionar",cursor='hand2',relief=SOLID,command=self.seleccionar)
        btn_seleccionar.place(relx=0.72,rely=0.04,width=100,height=40)

                
        label1 = Label(self, text="Ingreso de cadena",relief=SOLID)
        label1.place(relx=0.58,rely=0.20,width=120,height=35)

        self.ingreso_cadena.place(relx=0.47,rely=0.30,width=250,height=35)

        label2 = Label(self, text="Resultado ruta de validacion",relief=SOLID)
        label2.place(relx=0.52,rely=0.44,width=200,height=35)


        frame1 = Frame(self)
        frame1.place(relx=0.45,rely=0.55) 

        self.text_area_info = Text(frame1,width=30,height=11,font='Arial',state='disabled')
        self.text_area_info.grid(row=0,column=0)

        SC_archivo1 = Scrollbar(frame1, command=self.text_area_info.yview)
        self.text_area_info['yscroll'] = SC_archivo1.set
        SC_archivo1.grid(row=0,column=2)

        self.padre.withdraw()


    def cargar_archivo(self):
        rutaArchivo = filedialog.askopenfilename(initialdir="/", title="Seleccione un archivo para automas de pila", filetypes=(("ap files", "*.ap"),("all files", "*.*")))
        if rutaArchivo != '':
            self.gestor.leer_automatasdp(rutaArchivo)
            self.llenar_lista_atms()
            self.combobox_mostrar_atps.set("")
            self.combobox_mostrar_atps.config(values=self.nombres_atp)


    def llenar_lista_atms(self):
        self.nombres_atp = []
        lista = self.gestor.lista_atms()
        for at in lista:
            self.nombres_atp.append(at.nombre)

    def seleccionar(self):
        if self.combobox_mostrar_atps.get() == "":
            messagebox.showwarning("Advertencia","Debe seleccionar un Automata de Pila existente")
        else:
            self.btn_mostrar_informacion["state"] = "normal"
            self.btn_validar_cadena["state"] = "normal"
            self.btn_ruta_validacion["state"] = "normal"
            self.btn_recorrido_paso_a_paso["state"] = "normal"
            self.btn_validar_cadena_unaPasada["state"] = "normal"

    
    def info_adpl(self):
        self.gestor.informacion_automatadpl(self.combobox_mostrar_atps.get())
            

    def validar_cadena(self):
        if self.ingreso_cadena.get() == "":
            messagebox.showwarning("Advertencia","Debe escribir una cadena")
        else:
            self.gestor.validar_ruta(self.combobox_mostrar_atps.get(),self.ingreso_cadena.get(),1)


    def validar_ruta(self):
        if self.ingreso_cadena.get() == "":
            messagebox.showwarning("Advertencia","Debe escribir una cadena")
        else:
            self.text_area_info.config(state='normal')
            self.text_area_info.delete('1.0',END)
            self.text_area_info.config(state='disabled')
            try:
                caminos = self.gestor.validar_ruta(self.combobox_mostrar_atps.get(),self.ingreso_cadena.get(),2)
                cadenaCaminos = f'La cadena: {self.ingreso_cadena.get()}\r\nfue reconocida exitosamente:\r\nRuta:\r\n'

                for camino in caminos:
                    entrada = ''
                    salida = ''
                    inserto = ''
                    if camino.entrada == '$':
                        entrada = 'λ'
                    else:
                        entrada = camino.entrada

                    if camino.salida == '$':
                        salida = 'λ'
                    else:
                        salida = camino.salida

                    if camino.inserto == '$':
                        inserto = 'λ'
                    else:
                        inserto = camino.inserto
                    cadenaCaminos += f'{camino.origen},{entrada},{salida};{camino.destino},{inserto}\n'

                self.text_area_info.config(state='normal')
                self.text_area_info.delete('1.0',END)
                self.text_area_info.insert(INSERT,cadenaCaminos)  
                self.text_area_info.config(state='disabled')
            except:
                pass

    def pasoApaso(self):
        if self.ingreso_cadena.get() == "":
            messagebox.showwarning("Advertencia","Debe escribir una cadena")
        else:
            self.gestor.validar_ruta(self.combobox_mostrar_atps.get(),self.ingreso_cadena.get(),3)

    def validar_cadena_en_una_pasada(self):
        if self.ingreso_cadena.get() == "":
            messagebox.showwarning("Advertencia","Debe escribir una cadena")
        else:
            self.gestor.validar_ruta(self.combobox_mostrar_atps.get(),self.ingreso_cadena.get(),4)

    def regresar(self):
        self.padre.deiconify()
        self.master.destroy()