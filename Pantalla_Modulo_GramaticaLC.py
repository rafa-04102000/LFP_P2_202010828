from tkinter import Tk, SOLID, Frame,Label,Button,Toplevel,Text,Scrollbar,ttk,filedialog,messagebox,END,INSERT

class ModuloGLC(Frame):
    def __init__(self, gestor, master, padre) -> None:
        super().__init__(master)
        self.gestor = gestor
        self.master = master
        self.padre = padre
        self.config(width="600", height="300" )
        self.master.title("Modulo Gramatica Libre de Contexto")
        self.master.resizable(0,0)
        self.master.protocol("WM_DELETE_WINDOW", self.regresar)


        self.btn_mostrar_informacion = Button(self, text="Mostrar Informacion General",cursor='hand2',relief=SOLID,state="disabled",command=self.informacion_general)
        self.btn_arbol_derivacion = Button(self, text="Arbol de Derivacion",cursor='hand2',relief=SOLID,state="disabled",command=self.arbol_derivacion)         
        
        self.text_area_info = Text()

        self.nombres_grs = []
        self.combobox_mostrar_grs = ttk.Combobox(self,state="readonly")
        self.llenar_lista_grs()

        self.pack()
        self.crear_contenido()

    def crear_contenido(self):
        btn_cargar_archivo = Button(self, text="Cargar Archivo",cursor='hand2',relief=SOLID,command=self.cargar_archivo)
        btn_cargar_archivo.place(relx=0.12,rely=0.20,width=130,height=50)
                
        
        self.btn_mostrar_informacion.place(relx=0.07,rely=0.47,width=190,height=50)
                
        self.btn_arbol_derivacion.place(relx=0.12,rely=0.73,width=130,height=50)


        self.combobox_mostrar_grs.place(relx=0.47,rely=0.07)
        self.combobox_mostrar_grs['values'] = self.nombres_grs

        btn_seleccionar = Button(self, text="Seleccionar",cursor='hand2',relief=SOLID,command=self.seleccionar)
        btn_seleccionar.place(relx=0.72,rely=0.04,width=100,height=40)


        frame1 = Frame(self)
        frame1.place(relx=0.45,rely=0.20) 

        self.text_area_info = Text(frame1,width=30,height=12,font='Arial',state='disabled')
        self.text_area_info.grid(row=0,column=0)

        SC_archivo1 = Scrollbar(frame1, command=self.text_area_info.yview)
        self.text_area_info['yscroll'] = SC_archivo1.set
        SC_archivo1.grid(row=0,column=2)



        self.padre.withdraw()

    def cargar_archivo(self):
        rutaArchivo = filedialog.askopenfilename(initialdir="/", title="Seleccione un archivo para gramaticas LC", filetypes=(("glc files", "*.glc"),("all files", "*.*")))
        if rutaArchivo != '':
            self.gestor.leer_gramaticaslc(rutaArchivo)
            self.llenar_lista_grs()
            self.combobox_mostrar_grs.set("")
            self.combobox_mostrar_grs.config(values=self.nombres_grs)

    
    def llenar_lista_grs(self):
        self.nombres_grs = []
        lista = self.gestor.lista_grs()
        for gr in lista:
            self.nombres_grs.append(gr.nombre)

    def seleccionar(self):
        if self.combobox_mostrar_grs.get() == "":
            messagebox.showwarning("Advertencia","Debe seleccionar una GRAMATICA LC existente")
        else:
            self.btn_mostrar_informacion["state"] = "normal"
            self.btn_arbol_derivacion["state"] = "normal"


    def informacion_general(self):
        cadena = self.gestor.mostrar_info_general(self.combobox_mostrar_grs.get())
        # print(cadena)
        self.text_area_info.config(state='normal')
        self.text_area_info.delete('1.0',END)
        self.text_area_info.insert(INSERT,cadena)  
        self.text_area_info.config(state='disabled')

    def arbol_derivacion(self):
        self.gestor.arbol_derivacion(self.combobox_mostrar_grs.get())

    def regresar(self):
        self.padre.deiconify()
        self.master.destroy()