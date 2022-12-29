from tkinter import messagebox
from Clase_GramaticaLC import Gramatica
from Clase_Produccion import Produccion
from Clase_AutomataDP import Automata
from Clase_Transicion import Transicion
import os
from PIL import Image
from webbrowser import open_new_tab
# import webbrowser as wb


class Gestor:
    def __init__(self) -> None:
        self.GramaticasLC = []
        self.AutomatasDPL = []
        self.nodo = 0
        self.transiciones_que_concluyen = []


    def leer_gramaticaslc(self,rutaArchivo):
        Archivo = open(rutaArchivo,'r+',encoding='utf8') 
        
        nombre = ''
        no_terminales = []
        terminales = []
        no_terminal_inicial = ''
        producciones = []
        ng = None
        for linea in Archivo.readlines(): 
            lineaNueva = (linea.replace('\n',''))#.replace(" ",'')
            # print(lineaNueva)
            if lineaNueva != '':
                if nombre == '':
                    nombre = lineaNueva
                elif no_terminales == []:
                    lista_no_t = (lineaNueva.replace(" ",'')).split(',')
                    for nt in lista_no_t:
                        if nt !='':
                            if nt not in no_terminales:
                                no_terminales.append(nt)
                elif terminales == []:    
                    lista_t = (lineaNueva.replace(" ",'')).split(',')
                    for t in lista_t:
                        if t !='':
                            if t not in terminales:
                                terminales.append(t)   
                elif no_terminal_inicial == '':
                    no_terminal_inicial = lineaNueva.replace(" ",'')
                    ng = Gramatica(nombre,lista_no_t,lista_t,no_terminal_inicial)
                elif lineaNueva != '%':
                    try:
                        separacion_por_signo_mayor = lineaNueva.split('>')
                        nuevaP = Produccion(separacion_por_signo_mayor[0].replace(" ",''))
                        cont = 0
                        separacion_por_espacios = separacion_por_signo_mayor[1].split(' ')
                        while cont < len(separacion_por_espacios):
                            if separacion_por_espacios[cont] != '':
                                nuevaP.expresion.append(separacion_por_espacios[cont].replace(" ",''))
                            cont+=1
                        # while cont < len(separacion_por_signo_mayor[1]):
                        #     nuevaP.expresion.append(separacion_por_signo_mayor[1][cont])
                        #     cont+=1
                        if nuevaP not in producciones:
                            producciones.append(nuevaP)
                    except:
                        pass
                elif lineaNueva == '%':
                    ng.producciones = producciones
                    if nombre == '' or no_terminales == [] or terminales == [] or no_terminal_inicial == '' or producciones == []:
                        print('no se introdujo algo para esta gramatica')
                    else:
                        self.validar_gramatica(ng)
                    nombre = ''
                    no_terminales = []
                    terminales = []
                    no_terminal_inicial = ''
                    producciones = []
                    ng = None

    def validar_gramatica(self,nuevaGR):
        nombre = nuevaGR.nombre
        no_terminales = nuevaGR.no_terminales
        terminales = nuevaGR.terminales
        no_terminal_inicial = nuevaGR.no_terminal_inicial
        producciones = nuevaGR.producciones
        error = False

        # busco si hay produccion con el inicial
        for x in producciones:
            if x.no_terminal == no_terminal_inicial:
                error = False
                break
            else:
                error = True
        
        if error:
            return False

        #ordeno las producciones, las A contas luegos las B... y asi
        a_pasar = producciones
        producciones_ordenadas = []
        buscar = no_terminal_inicial
        eliminar = ''
        while True:
            encontro_otro = False
            if eliminar != '':
                a_pasar.remove(eliminar)

            if a_pasar == []:
                break

            for tt in a_pasar:
                if tt.no_terminal == buscar:
                    producciones_ordenadas.append(tt)
                    eliminar = tt
                    encontro_otro = True
                    break

            if not encontro_otro and a_pasar != []:
                buscar = a_pasar[0].no_terminal
                eliminar = ''

        producciones = producciones_ordenadas
        nuevaGR.producciones = producciones
        #-----------------------veo si estan bien los datos----------------------------

        for terminal in terminales:
            if terminal in no_terminales:
                error = True
        
        if no_terminal_inicial not in no_terminales:
            error = True
        
        if error:
            return False


        #-------------veo si es una gramatica libre de contexto---------------
        nt_usados = []
        t_usados = []
        glctxt = False
        nt_usados.append(no_terminal_inicial)

        for produccion in producciones:
            cadena = '' #la uso para ver que patron se formo t = terminal, n = no terminal
            if produccion.no_terminal not in no_terminales:
                error = True
                break
            else:
                if len(produccion.expresion) >=3:
                    glctxt = True
                    for ex0 in produccion.expresion:
                        if ex0 in no_terminales or ex0 in terminales:

                            if ex0 in no_terminales:
                                if ex0 not in nt_usados:
                                    nt_usados.append(ex0)
                    
                            if ex0 in terminales:
                                if ex0 not in t_usados:
                                    t_usados.append(ex0)
                        else:
                            error = True
                            break
                else:
                    cont_ex = 0
                    for ex in produccion.expresion:
                        if ex in no_terminales or ex in terminales:
                            if ex in no_terminales and cont_ex < 2:
                                cadena += 'n'
                            elif ex in terminales and cont_ex < 2:
                                cadena += 't'

                            if ex in no_terminales:
                                if ex not in nt_usados:
                                    nt_usados.append(ex)

                            
                            if ex in terminales:
                                # print(ex,'este es el terminal')
                                if ex not in t_usados:
                                    t_usados.append(ex)
                        else:
                            error = True
                            break
                        cont_ex +=1
                
                    if cadena == 'n' or cadena == 'nn' or cadena == 'tt' and error == False:
                        glctxt = True

        if error:
            return False
        for nusado in no_terminales:
            if nusado not in nt_usados:
                error = True
                break

        for tusado in terminales:
            if tusado not in t_usados:
                error = True
                break

        if not glctxt:
            error = True

        if error:
            return False

        self.GramaticasLC.append(nuevaGR)

        # print(nt_usados,'no terminalees usados')
        # print(no_terminales,'lista no terminales')

        # print(t_usados,'terminalees usados')
        # print(terminales,'lista terminales')

        # print(nombre,'nombre')
        # print(no_terminales,'no terminales')
        # print(terminales,'terminales')
        # print(no_terminal_inicial,'no terminal inicial')
        # for p in producciones:
        #     c = ''
        #     for car in p.expresion:
        #         c += f'-{car}'

        #     print(c)

    def lista_grs(self):
        return self.GramaticasLC

    def mostrar_info_general(self,nombre):
        grBuscada = None
        for gr in self.GramaticasLC:
            if gr.nombre == nombre:
                grBuscada = gr

        cadena = ''
        cadena += f'Nombre: {grBuscada.nombre}\n'

        nterminales = ''
        for i in range(0,len(grBuscada.no_terminales)):
            if i+1 == len(grBuscada.no_terminales):
                nterminales += f'{grBuscada.no_terminales[i]}'
            else:
                nterminales += f'{grBuscada.no_terminales[i]},'
        cadena += f'No Terminales {nterminales}\n'


        terminales = ''
        for t in range(0,len(grBuscada.terminales)):
            if t+1 == len(grBuscada.terminales):
                terminales += f'{grBuscada.terminales[t]}'
            else:
                terminales += f'{grBuscada.terminales[t]},'
        cadena += f'Terminales: {terminales}\n'
        cadena += f'No terminal inicial: {grBuscada.no_terminal_inicial}\n'
        
        cadena += f'Producciones:\n'

        anterior = ''
        for produccion in grBuscada.producciones:
            cadenaP = ''
            if anterior != produccion.no_terminal:
                cadenaP += f'{produccion.no_terminal}>'
                for ex in produccion.expresion:
                    cadenaP += f'{ex} '
                cadena += f'{cadenaP}\n'
                anterior = produccion.no_terminal
            elif anterior == produccion.no_terminal:
                cadenaP += f'   |'
                for ex in produccion.expresion:
                    cadenaP += f'{ex} '
                cadena += f'{cadenaP}\n'

        return cadena

    def arbol_derivacion(self,nombre):
        self.nodo = 0
        grBuscada = None
        for gr in self.GramaticasLC:
            if gr.nombre == nombre:
                grBuscada = gr

        nterminales = grBuscada.no_terminales
        terminales = grBuscada.terminales
        inicial = grBuscada.no_terminal_inicial
        producciones = grBuscada.producciones
        copia = []
        for p in producciones:
            copia.append(p)            
        grBuscada.producciones = copia


        cadenaE = 'graph GramaticaLC {\r'
        cadenaE += 'layout=dot rankdir=TB \r'

        borrar = ''
        buscar = inicial
        tiene_no_ternimal = False
        siguientes = []
        for produccion in producciones:
            if produccion.no_terminal == buscar:
                for ex in produccion.expresion:
                    if ex in nterminales:
                        tiene_no_ternimal = True
                if tiene_no_ternimal:
                    cadenaE += f'nodo{self.nodo} [label={produccion.no_terminal} shape=circle]\r'
                    raiz = self.nodo
                    self.nodo +=1
                    for ex in produccion.expresion:
                        if ex in nterminales:
                            cadenaE += f'nodo{self.nodo} [label={ex} shape=circle]\r'
                            hoja = self.nodo
                            siguientes.append([ex,hoja])
                            self.nodo +=1
                            cadenaE += f'nodo{raiz} -- nodo{hoja}\r'
                        else:
                            cadenaE += f'nodo{self.nodo} [label={ex} shape=plain]\r'
                            hoja = self.nodo
                            self.nodo +=1
                            cadenaE += f'nodo{raiz} -- nodo{hoja}\r'
                    borrar = produccion
                    break
        
        producciones.remove(borrar)

        for sig in siguientes:
            cadenaE += self.arbol_recursivo(sig[0],sig[1],producciones,nterminales) #lo primero es el no terminal a buscar y lo segundo el nodo padre

        cadenaE += '}'


        nombre_sin_espacio = (grBuscada.nombre).strip()
        file = open(f"ArbolDeDerivacion/arbol_{nombre_sin_espacio}.dot", "w+")
        file.write(cadenaE)
        file.close()
        os.system(f'dot -Tpng ArbolDeDerivacion/arbol_{nombre_sin_espacio}.dot -o ArbolDeDerivacion/arbol_{nombre_sin_espacio}.png')

        messagebox.showinfo('SE CREO LA IMAGEN','LA IMAGEN SE GUARDO EN LA CARPETA ArbolDeDerivacion')
        img = Image.open(f'ArbolDeDerivacion/arbol_{nombre_sin_espacio}.png')
        img.show()


    def arbol_recursivo(self,buscar,nodoPadre,producciones,nterminales):
        producciones1 = producciones
        siguientes = []

        cadena = ''
        tiene_no_ternimal = False
        borrar = ''

        for produccion in producciones1:
            if produccion.no_terminal == buscar:
                for ex in produccion.expresion:
                    if ex in nterminales:
                        tiene_no_ternimal = True
                if tiene_no_ternimal:
                    for ex in produccion.expresion:
                        if ex in nterminales:
                            cadena += f'nodo{self.nodo} [label={ex} shape=circle]\r'
                            hoja = self.nodo
                            siguientes.append([ex,hoja])
                            self.nodo +=1
                            cadena += f'nodo{nodoPadre} -- nodo{hoja}\r'
                        else:
                            cadena += f'nodo{self.nodo} [label={ex} shape=plain]\r'
                            hoja = self.nodo
                            self.nodo +=1
                            cadena += f'nodo{nodoPadre} -- nodo{hoja}\r'
                    borrar = produccion
                    break

        if tiene_no_ternimal:
            producciones1.remove(borrar)
            for sig in siguientes:
                cadena += self.arbol_recursivo(sig[0],sig[1],producciones1,nterminales) #lo primero es el no terminal a buscar y lo segundo el nodo padre
            
            return cadena
        else:
            for produccion in producciones1:
                if produccion.no_terminal == buscar:
                    for ex in produccion.expresion:
                        cadena += f'nodo{self.nodo} [label={ex} shape=plain]\r'
                        hoja = self.nodo
                        self.nodo +=1
                        cadena += f'nodo{nodoPadre} -- nodo{hoja}\r'
                    break

            return cadena


    def leer_automatasdp(self,rutaArchivo):
        Archivo = open(rutaArchivo,'r+',encoding='utf8') 
        
        nombre = ''
        alfabeto = []
        simbolosP = []
        estados = []
        estado_inicial = ''
        estado_aceptacion = []
        transiciones = []
        na = None
        for linea in Archivo.readlines(): 
            lineaNueva = (linea.replace('\n',''))#.replace(" ",'')
            if lineaNueva != '':
                if nombre == '':
                    nombre = lineaNueva
                elif alfabeto == []:
                    lista_alfabeto = (lineaNueva.replace(" ",'')).split(',')
                    for alf in lista_alfabeto:
                        if alf !='':
                            if alf not in alfabeto:
                                alfabeto.append(alf)
                elif simbolosP == []:    
                    lista_simbolos = (lineaNueva.replace(" ",'')).split(',')
                    for simbolo in lista_simbolos:
                        if simbolo !='':
                            if simbolo not in simbolosP:
                                simbolosP.append(simbolo)   
                elif estados == []:
                    lista_estados = (lineaNueva.replace(" ",'')).split(',')
                    for estado in lista_estados:
                        if estado !='':
                            if estado not in estados:
                                estados.append(estado)   
                elif estado_inicial == '':
                    estado_inicial = lineaNueva.replace(" ",'')
                elif estado_aceptacion == []:
                    lista_estadosA = (lineaNueva.replace(" ",'')).split(',')
                    for eAceptacion in lista_estadosA:
                        if eAceptacion !='':
                            if eAceptacion not in estado_aceptacion:
                                estado_aceptacion.append(eAceptacion)  
                    na = Automata(nombre,alfabeto,simbolosP,estados,estado_inicial,estado_aceptacion)
                elif lineaNueva != '%':
                    try:
                        separacion_por_punto_y_coma = (lineaNueva.replace(" ",'')).split(';')

                        separacion_por_coma_p1 = (separacion_por_punto_y_coma[0].replace(" ",'')).split(',')
                        separacion_por_coma_p2 = (separacion_por_punto_y_coma[1].replace(" ",'')).split(',')

                        
                        if separacion_por_coma_p1[0] != '':
                            origen = separacion_por_coma_p1[0]
                        
                        if separacion_por_coma_p1[1] != '':
                            entrada = separacion_por_coma_p1[1]
                        
                        if separacion_por_coma_p1[2] != '':
                            salida = separacion_por_coma_p1[2]
                        
                        if separacion_por_coma_p2[0] != '':
                            destino = separacion_por_coma_p2[0]
                        
                        if separacion_por_coma_p2[1] != '':
                            inserto = separacion_por_coma_p2[1]                    

                        nuevaP = Transicion(origen,entrada,salida,destino,inserto)

                        if nuevaP not in transiciones:
                            transiciones.append(nuevaP)
                    except:
                        print('hubo error')
                        pass
                elif lineaNueva == '%':
                    na.transiciones = transiciones
                    if nombre == '' or alfabeto == [] or simbolosP == [] or estados == [] or estado_inicial == '' or estado_aceptacion == [] or transiciones == []:
                        print('no se introdujo algo para este automata')
                    else:
                        self.validar_automata(na)
                    nombre = ''
                    alfabeto = []
                    simbolosP = []
                    estados = []
                    estado_inicial = ''
                    estado_aceptacion = []
                    transiciones = []
                    na = None

    def validar_automata(self,nuevoAT):
        self.transiciones_que_concluyen = []

        nombre = nuevoAT.nombre
        alfabeto = nuevoAT.alfabeto
        simbolosP = nuevoAT.simbolosP
        estados = nuevoAT.estados
        estado_inicial = nuevoAT.estado_inicial
        estado_aceptacion = nuevoAT.estado_aceptacion
        transiciones = nuevoAT.transiciones
        copia = []
        error = False

        # busco si hay transicion con el inicial

        for x in transiciones:
            if x.origen == estado_inicial:
                error = False
                break
            else:
                error = True

        if error:
            return False

        #ordeno las transiciones, las A contas luegos las B... y asi
        a_pasar = transiciones
        transiciones_ordenadas = []
        buscar = estado_inicial
        eliminar = ''
        while True:
            encontro_otro = False
            if eliminar != '':
                a_pasar.remove(eliminar)

            if a_pasar == []:
                break

            for tt in a_pasar:
                if tt.origen == buscar:
                    transiciones_ordenadas.append(tt)
                    eliminar = tt
                    encontro_otro = True
                    break

            if not encontro_otro and a_pasar != []:
                buscar = a_pasar[0].origen
                eliminar = ''

        transiciones = transiciones_ordenadas
        for tt in transiciones:
            copia.append(tt)
        nuevoAT.transiciones = copia

        #-----------------------veo si estan bien los datos----------------------------

        for simbolo in simbolosP:
            if simbolo != '#' and simbolo not in alfabeto:
                error = True
        
        for estado in estados:
            if estado in alfabeto:
                error = True

        if estado_inicial not in estados:
            error = True

        for eAceptado in estado_aceptacion:
            if eAceptado not in estados:
                error = True
        
        if error:
            return False

        #-------------veo si es un automata de pila---------------
        estados_usados = []
        alfabeto_usado = []
        simbolos_pila_usados = []
       
        estados_usados.append(estado_inicial)

        busco = estado_inicial
        borrar = ''
    


        for transicion in transiciones:
            if transicion.origen not in estados:
                error = True
                break
            
            if transicion.origen == busco:

                if busco not in estados_usados:
                    estados_usados.append(busco)

                if transicion.entrada != '$' and transicion.entrada not in alfabeto:
                    error = True
                    break
                elif transicion.entrada != '$':
                    if transicion.entrada not in alfabeto_usado:
                        alfabeto_usado.append(transicion.entrada)
                        simbolos_pila_usados.append(transicion.entrada)

                if transicion.salida != '$' and transicion.salida not in simbolosP:
                    error = True
                    break
                elif transicion.salida != '$':
                    if transicion.salida not in simbolos_pila_usados:
                        simbolos_pila_usados.append(transicion.salida)
                
                if transicion.destino not in estados:
                    error = True
                    break
                else:
                    busco = transicion.destino


                if transicion.inserto != '$' and transicion.inserto not in simbolosP:
                    error = True
                    break
                self.transiciones_que_concluyen.append(transicion)
                borrar = transicion
                break
        
        if error:
            return False
        
        transiciones.remove(borrar)

        if transiciones == []:
            return False

        if self.verificador_de_transicones(busco,transiciones,nuevoAT,estados_usados,alfabeto_usado,simbolos_pila_usados):
            
            # print(estados,'estados')
            # print(estados_usados)
            # print(alfabeto,'alfabeto')
            # print(alfabeto_usado)
            # print(simbolosP,'simbolos pila')
            # print(simbolos_pila_usados)

            for e in estados:
                if e not in estados_usados:
                    error = True

            for a in alfabeto:
                if a not in alfabeto_usado:
                    error = True

            for s in simbolosP:
                if s not in simbolos_pila_usados:
                    error = True

            if error:
                return False

            self.AutomatasDPL.append(nuevoAT)

            # print(nombre,'nombre')
            # print(alfabeto,'alfabeto')
            # print(simbolosP,'simbolos de la pila')
            # print(estados,'estados')
            # print(estado_inicial,'estado inicial')
            # print(estado_aceptacion,'estado aceptacon')
            # for p in nuevoAT.transiciones:
            #     c = ''
            #     c += f'{p.origen},{p.entrada},{p.salida},{p.destino},{p.inserto}'

            #     print(c)

        else:
            return False

    def verificador_de_transicones(self,busco,transiciones,nuevoAT,estados_usados,alfabeto_usado,simbolos_pila_usados):
        alfabeto = nuevoAT.alfabeto
        simbolosP = nuevoAT.simbolosP
        estados = nuevoAT.estados
        estado_inicial = nuevoAT.estado_inicial
        estado_aceptacion = nuevoAT.estado_aceptacion
        error = False
        encontro = False

        for transicion in transiciones:
            if transicion.origen not in estados:
                error = True
                break
            
            if transicion.origen == busco:

                if busco not in estados_usados:
                    estados_usados.append(busco)

                if transicion.entrada != '$' and transicion.entrada not in alfabeto:
                    error = True
                    break
                elif transicion.entrada != '$':
                    if transicion.entrada not in alfabeto_usado:
                        alfabeto_usado.append(transicion.entrada)
                        simbolos_pila_usados.append(transicion.entrada)

                if transicion.salida != '$' and transicion.salida not in simbolosP:
                    error = True
                    break
                elif transicion.salida != '$':
                    if transicion.salida not in simbolos_pila_usados:
                        simbolos_pila_usados.append(transicion.salida)
                
                if transicion.destino not in estados:
                    print(transicion.destino)
                    error = True
                    break
                else:
                    busco = transicion.destino


                if transicion.inserto != '$' and transicion.inserto not in simbolosP:
                    error = True
                    break
                self.transiciones_que_concluyen.append(transicion)
                borrar = transicion
                encontro = True
                break
            else:
                encontro = False
        

        if error:
            return False

        if encontro:
            transiciones.remove(borrar)
        else:
            if busco in estado_aceptacion:
                if busco not in estados_usados:
                    estados_usados.append(busco)

                if transiciones != []:
                    busco = transiciones[0].origen
            else:
                si = False

                for x in self.transiciones_que_concluyen:
                    if x.destino == busco:
                        if busco not in estados_usados:
                            estados_usados.append(busco)                       
                        si = True
                        break
                
                if si:
                    if transiciones != []:
                        busco = transiciones[0].origen
                else:
                    return False
            

        if transiciones == []:
            if busco in estado_aceptacion:
                if busco not in estados_usados:
                    estados_usados.append(busco)
                return True
            else:
                si = False
                for x in self.transiciones_que_concluyen:
                    if x.destino == busco:
                        if busco not in estados_usados:
                            estados_usados.append(busco)                       
                        si = True
                        break
                
                if si:
                    return True
                else:
                    return False

        else:
            if self.verificador_de_transicones(busco,transiciones,nuevoAT,estados_usados,alfabeto_usado,simbolos_pila_usados):
                return True
            else:
                return False
            


    def lista_atms(self):
        return self.AutomatasDPL


    def informacion_automatadpl(self,nombreADPL):
        adp_buscado = None
        for ap in self.AutomatasDPL:
            if ap.nombre == nombreADPL:
                adp_buscado = ap

        nombre = adp_buscado.nombre
        alfabeto = adp_buscado.alfabeto
        simbolosP = adp_buscado.simbolosP
        estados = adp_buscado.estados
        estado_inicial = adp_buscado.estado_inicial
        estado_aceptacion = adp_buscado.estado_aceptacion
        transiciones = adp_buscado.transiciones

        cadena_alfabeto = ''
        for q in range(0,len(alfabeto)):
            if q+1 == len(alfabeto):
                cadena_alfabeto += f'{alfabeto[q]}'
            else:
                cadena_alfabeto += f'{alfabeto[q]},'

        cadena_simbolosP = ''
        for w in range(0,len(simbolosP)):
            if w+1 == len(simbolosP):
                cadena_simbolosP += f'{simbolosP[w]}'
            else:
                cadena_simbolosP += f'{simbolosP[w]},'

        cadena_estados = ''
        for e in range(0,len(estados)):
            if e+1 == len(estados):
                cadena_estados += f'{estados[e]}'
            else:
                cadena_estados += f'{estados[e]},'

        cadena_estados_aceptacion = ''
        for r in range(0,len(estado_aceptacion)):
            if r+1 == len(estado_aceptacion):
                cadena_estados_aceptacion += f'{estado_aceptacion[r]}'
            else:
                cadena_estados_aceptacion += f'{estado_aceptacion[r]},'


        cadena = 'digraph grafo_afd { \r'
        cadena += '     fontname="Helvetica,Arial,sans-serif"\r'
        cadena += '     edge [fontname="Helvetica,Arial,sans-serif"]\r'
        cadena += '	    rankdir=LR;\r'
        for e_aceptacion in adp_buscado.estado_aceptacion:
            cadena += f'	    {e_aceptacion} [shape=doublecircle]\r'

        
        cadena += '     	node [shape = circle];\r'
        for transicion in transiciones:
            entrada = ''
            salida = ''
            inserto = ''
            if transicion.entrada == '$':
                entrada = 'λ'
            else:
                entrada = transicion.entrada

            if transicion.salida == '$':
                salida = 'λ'
            else:
                salida = transicion.salida

            if transicion.inserto == '$':
                inserto = 'λ'
            else:
                inserto = transicion.inserto

            cadena += f'     {transicion.origen} -> {transicion.destino} [label = "{entrada},{salida};{inserto}"];\r'

        # espacio para el cuadro
        nombre_sin_espacio = (adp_buscado.nombre).strip()
        cadena += f'     {nombre_sin_espacio} [\r'
        cadena += f'            fillcolor="#ff880022"\r'
        cadena += f'            label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="18"> \r'
        cadena += f'            <tr> <td> <b>Nombre: {adp_buscado.nombre}</b> </td> </tr> \r'
        cadena += f'            <tr> <td> Alfabeto: {cadena_alfabeto}</td> </tr>\r'
        cadena += f'            <tr> <td> Alfabeto de pila: {cadena_simbolosP}</td> </tr>\r'
        cadena += f'            <tr> <td> Estados: {cadena_estados}</td> </tr> \r'
        cadena += f'            <tr> <td> Estado inicial: {estado_inicial}</td> </tr> \r'
        cadena += f'            <tr> <td> Estado aceptacion: {cadena_estados_aceptacion}</td> </tr> \r'
        cadena += f'            <tr> <td align="left"> \r'
        cadena += f'            <br align="left"/>\r'
        cadena += f'     Transiciones:<br align="left"/>\r'
        for t in transiciones:
            entrada = ''
            salida = ''
            inserto = ''
            if t.entrada == '$':
                entrada = 'λ'
            else:
                entrada = t.entrada

            if t.salida == '$':
                salida = 'λ'
            else:
                salida = t.salida

            if t.inserto == '$':
                inserto = 'λ'
            else:
                inserto = t.inserto
            cadena += f'     {t.origen},{entrada},{salida};{t.destino},{inserto} <br align="left"/>\r'

        cadena += f'            <br align="left"/>\r'
        cadena += f'            </td> </tr>\r'

        cadena += f'            </table>> \r'
        cadena += f'            shape=plain \r'
        cadena += f']\r'

        cadena += "}"

        file = open(f"InfoAutomatasDePila/grafo_{nombre_sin_espacio}.dot", "w+", encoding="utf-8")
        file.write(cadena)
        file.close()
        os.system(f'dot -Tpdf InfoAutomatasDePila/grafo_{nombre_sin_espacio}.dot -o InfoAutomatasDePila/grafo_{nombre_sin_espacio}.pdf')

        messagebox.showinfo('GENERACION CORRECTA','EL DOCUMENTO SE CREO',detail='SE CREO UN PDF CON EL AFD SELECCIONADO, ESTA EN LA CARPETA InfoAutomatasDePila')
        open_new_tab(f"InfoAutomatasDePila\grafo_{nombre_sin_espacio}.pdf")    


    def validar_ruta(self,nombreADPL:str,cadena:str,tipo):
        # print(nombreADPL)
        # print(cadena)
        adp_buscado = None
        for ap in self.AutomatasDPL:
            if ap.nombre == nombreADPL:
                adp_buscado = ap

        alfabeto = adp_buscado.alfabeto
        simbolosP = adp_buscado.simbolosP
        estados = adp_buscado.estados
        estado_inicial = adp_buscado.estado_inicial
        estado_aceptacion = adp_buscado.estado_aceptacion
        transiciones = adp_buscado.transiciones


        error = False
        pila = []
        caminos = []
        buscar = []
        for t in transiciones:
            if t.origen == estado_inicial:
                buscar.append(t)
                if t not in pila:
                    pila.append(t.inserto)
                break
        
        actual = ''
        contador_caracteres = 0
        for w in buscar:
            for tt in transiciones:
                if cadena[0] not in simbolosP:
                    error= True
                    break
                elif tt.origen == w.destino and tt.entrada == cadena[0]:
                    caminos.append(w)
                    actual = tt.origen
                    break
            if error:
                break

            if actual != '':
                break

        if error or actual == '':
            messagebox.showwarning('Error','CADENA INCORRECTA, NO SE CUMPLE CON LA ESTRUCTURA QUE DEBERIA TENER aaa')
            return False

        

        while contador_caracteres < len(cadena):
            encontro_caminio = False

            if cadena[contador_caracteres] not in simbolosP:
                messagebox.showwarning('Error','CARACTER INVALIDO, CADENA INCORRECTA',detail='UN CARACTER NO ESTA EN EL ALFABETO PERMITIDO')
                return False
            else:
                for transicion in transiciones:
                    if actual == transicion.origen and cadena[contador_caracteres] == transicion.entrada:
                        if transicion.salida != '$':

                            if transicion.salida == pila[-1]:
                                pila.pop()
                            else:
                                error = True
                                break

                        if transicion.inserto != '$':
                            pila.append(transicion.inserto)
                 
                        actual = transicion.destino
                        encontro_caminio = True
                        caminos.append(transicion)
                        break

                if error:
                    messagebox.showwarning('Error','CADENA INCORRECTA, NO SE CUMPLE CON LA ESTRUCTURA QUE DEBERIA TENER bbb')
                    return False

            if not encontro_caminio:   
                messagebox.showwarning('Error','CADENA INCORRECTA, NO SE CUMPLE CON LA ESTRUCTURA QUE DEBERIA TENER ccc')
                return False

            contador_caracteres +=1

        encontro = False

        for ww in transiciones:
            if actual == ww.origen and ww.destino in estado_aceptacion:
                if ww.salida == pila[-1]:
                    encontro = True
                    caminos.append(ww)
                    pila.remove(ww.salida)
                    break
                else:
                    messagebox.showwarning('Error','CADENA INCORRECTA, NO SE CUMPLE CON LA ESTRUCTURA QUE DEBERIA TENER ddd')
                    break
        

        if encontro and pila == []:
            if tipo == 1:
                messagebox.showinfo('CADENA CORRECTA','LA CADENA INTRODUCIDA ES CORRECTA')
            elif tipo == 2:
                return caminos

        else:
            messagebox.showwarning('Error','CADENA INCORRECTA, NO SE CUMPLE CON LA ESTRUCTURA QUE DEBERIA TENER eee')

