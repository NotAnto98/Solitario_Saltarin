import PySimpleGUI as sg
import numpy as np
import random as rd
import time

class Nodo:
    def __init__(self, estado, padre=None, accion=None):
        self.estado = estado
        self.padre = padre
        self.accion = accion

def es_fin(tablero):
    
    cont = np.count_nonzero(tablero == 1)
    if cont == 1:
        return True
    else:
        return False

def r_movimientos(tablero,i,j):
    res = []
    #arr
    if i-2 >= 0 and tablero[i-2,j] == 0 and tablero[i-1,j] == 1:
        res.append(((i,j),(i-2,j)))
    #aba
    if i+2 <= 6 and tablero[i+2,j] == 0 and tablero[i+1,j] == 1:
        res.append(((i,j),(i+2,j))) 
    #izq
    if j-2 >= 0 and tablero[i,j-2] == 0 and tablero[i,j-1] == 1:
        res.append(((i,j),(i,j-2)))
    #der
    if j+2 <= 6 and tablero[i,j+2] == 0 and tablero[i,j+1] == 1:
        res.append(((i,j),(i,j+2)))

    return res

def devuelve_movimientos(tablero):
    res = []
    for i in range(tablero.shape[0]):
        for j in range(tablero.shape[1]):
            if tablero[i,j] == 1:
                movimientos_legales = r_movimientos(tablero,i,j)
                if bool(movimientos_legales):
                    res = res + movimientos_legales
    return res

def mueve(tablero, movimiento):
    tablero_modificado = np.copy(tablero)  # crea una copia del tablero original
    x,y = movimiento
    a,b = x
    c,d = y
    
    if a != c:
        tablero_modificado[a,b] = 0
        tablero_modificado[max(a,c)-1,b] = 0
        tablero_modificado[c,d] = 1
    else:
        tablero_modificado[a,b] = 0
        tablero_modificado[c,max(b,d)-1] = 0
        tablero_modificado[c,d] = 1

    return tablero_modificado

def mueve_inversa(tablero, movimiento):
    tablero_modificado = np.copy(tablero)  # crea una copia del tablero original
    x,y = movimiento
    a,b = x
    c,d = y
    
    if a != c:
        tablero_modificado[a,b] = 0
        tablero_modificado[max(a,c)-1,b] = 1
        tablero_modificado[c,d] = 1
    else:
        tablero_modificado[a,b] = 0
        tablero_modificado[c,max(b,d)-1] = 1
        tablero_modificado[c,d] = 1

    return tablero_modificado

def dfs(estado):
    estado0 = Nodo(estado)
    frontera = []
    frontera.append(estado0)

    visitados = set()

    while frontera:
        nodo_actual = frontera.pop(0)
        estado_actual = nodo_actual.estado

        if es_fin(estado_actual):
            camino = []
            while nodo_actual.padre:
                camino.append(nodo_actual.accion)
                nodo_actual = nodo_actual.padre
            camino.reverse()
            return camino
        
        visitados.add(tuple(estado_actual.flatten()))

        movimientos = devuelve_movimientos(estado_actual)
        for movimiento in movimientos:
            estado_nuevo = mueve(estado_actual, movimiento)

            nuevo_nodo = Nodo(estado_nuevo, nodo_actual, movimiento)

            if tuple(estado_nuevo.flatten()) not in visitados:
                frontera.insert(0, nuevo_nodo)

    return None

# dado un tablero, devuelve un indice aleatorio de aquellos 1 que haya 
def indice_random(tablero):
    lista_indices = np.array(np.where(tablero == 1))
    ls = [x for x in zip(lista_indices[0],lista_indices[1])]
    x = ls[rd.randint(0,len(ls)-1)]
    return x

def inversa(n):
    n-=1
    tablero = np.zeros((7,7),dtype=int)

    tablero[:2, :2] = -1
    tablero[:2, -2:] = -1
    tablero[-2:, :2] = -1
    tablero[-2:, -2:] = -1

    i = rd.randint(0,6)
    j = 0

    if i < 2 or i > 4:
        j = rd.randint(2,4)
    else:
        j = rd.randint(0,6)

    tablero[i,j] = 1
    intentos = []
    while n != 0:
        i,j = indice_random(tablero)
        if (i,j) not in intentos:
            opciones = []
            #arr
            if i-2 >= 0 and tablero[i-2,j] == 0 and tablero[i-1,j] == 0:
                opciones.append(((i,j),(i-2,j)))
            #aba
            if i+2 <= 6 and tablero[i+2,j] == 0 and tablero[i+1,j] == 0:
                opciones.append(((i,j),(i+2,j))) 
            #izq
            if j-2 >= 0 and tablero[i,j-2] == 0 and tablero[i,j-1] == 0:
                opciones.append(((i,j),(i,j-2)))
            #der
            if j+2 <= 6 and tablero[i,j+2] == 0 and tablero[i,j+1] == 0:
                opciones.append(((i,j),(i,j+2)))

            if opciones == []:
                intentos.append((i,j))
            else:
                n-=1
                intentos = []
                opcion_aleatoria = rd.choice(opciones)
                tablero = mueve_inversa(tablero,opcion_aleatoria)
    return tablero

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # SEPARACION APLICACION # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def inicio():

    layout = [
        [sg.Image('images/inicio.png')],
        [sg.Button('Jugar', key='Jugar', size=(9,2), button_color=('dark blue'), pad=(140,50))]
    ]

    window = sg.Window('Inicio', layout, finalize=True)

    # bucle de la ventana
    while True:

        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Jugar':
            window.close()
            juego()

def guardar_tablero(tablero):
    carpeta = 'save files'
    layout = [
        [sg.Text('Inserte el nombre que desee para el archivo de guardado: ')],
        [sg.Input(key='Archivo')],
        [sg.Button('Guardar')]
    ]

    window = sg.Window('Guardado', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Guardar':
            nombre_archivo = values['Archivo']
            if nombre_archivo:
                np.savetxt(f'save files/{nombre_archivo}.txt', tablero, fmt='%d')
                sg.Popup('Se ha guardado correctamente')
                window.close()
            else:
                sg.Popup('Inserta un nombre valido para el archivo')

    window.close()

def cargar_tablero():
    carpeta = 'save files'
    layout = [
        [sg.Text('Seleccione el archivo a cargar: ')],
        [sg.Input(key='Archivo'), sg.FileBrowse(initial_folder=carpeta, file_types=(('Archivos de texto', '*.txt'),))],
        [sg.Button('Cargar')]
    ]

    window = sg.Window('Explorador de archivos', layout)

    tablero = None

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Cargar':
            nombre_archivo = values['Archivo']
            if nombre_archivo.endswith('.txt'):
                tablero = np.loadtxt(nombre_archivo, dtype=int)
                window.close()
            else:
                sg.Popup('No se ha especificado ningun archivo')
                window.close()
        
        return tablero

def instrucciones():
    archivo = open('Instrucciones.txt', 'r', encoding='utf-8')
    texto = archivo.read()
    archivo.close()
    layout = [
        [sg.Multiline(texto, size=(100,40), justification='justify', disabled=True)]
    ]

    window = sg.Window('Instrucciones', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

def popup_game_over():
    
    layout = [
        [sg.Text('GAME OVER', font=('Impact', 50))],
        [sg.Button('OK')]
    ]

    window = sg.Window('Fin del juego', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'OK':
            break
    window.close()

def popup_victoria():

    layout = [
        [sg.Text('¡Victoria!', font=('Impact', 50))],
        [sg.Button('OK')]
    ]

    window = sg.Window('Fin del juego', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'OK':
            break
    window.close()


# rutas de las imagenes para que pueda generarse adecuadamente un ejecutable

img_pieza = 'images/pieza.png'
img_pieza_sel = 'images/pieza_sel.png'
img_madera = 'images/madera.PNG'
img_madera_sel = 'images/madera_sel.png'
img_madera_inhab = 'images/madera_inhab.png'



def crear_tablero():
    tablero_inicial = np.ones((7,7),dtype=int)

    tablero_inicial[3,3] = 0

    tablero_inicial[:2, :2] = -1
    tablero_inicial[:2, -2:] = -1
    tablero_inicial[-2:, :2] = -1
    tablero_inicial[-2:, -2:] = -1

    return tablero_inicial

def calcula_pieza_medio(movimiento):
    x,y = movimiento
    a,b = x
    c,d = y
    
    if a != c:
        i = str(max(a,c)-1)
        j = str(b)
        return np.str_(i+','+j)
    else:
        i = str(c)
        j = str(max(b,d)-1)
        return np.str_(i+','+j)


# convierte el boton pulsado en dos numeros (fila y columna) para tratar con el tablero
def indice(x):
    cadena = x.item()
    ls = cadena.split(',')
    return int(ls[0]),int(ls[1])

def juego():
    tablero = crear_tablero()

    # matriz de claves para los botones, han de ser strings
    matriz_keys = np.array([[f'{i},{j}' for j in range(7)] for i in range(7)])
    
    
    # Creacion y disenho de los botones
    boton_cargar = sg.Button('Cargar', key='Cargar', size=(9,2), button_color=('dark blue'))
    boton_guardar = sg.Button('Guardar', key='Guardar', size=(9,2), button_color=('dark blue'))
    boton_volver = sg.Button('Volver', key='Volver', size=(9,2), button_color=('dark blue'))
    boton_crear_tablero = sg.Button('Crear Tablero', key='Crear Tablero', size=(9,2), button_color=('dark blue'))
    boton_pista = sg.Button('Pista', key='Pista', size=(9,2), button_color=('dark blue'))
    boton_movimientos = sg.Button('Movimientos', key='Movimientos', size=(9,2), button_color=('dark blue'))
    boton_reiniciar = sg.Button('Reiniciar', key='Reiniciar', size=(9,2), button_color=('dark blue'))
    boton_deshacer = sg.Button('Deshacer', key='Deshacer', size=(9,2), button_color=('dark blue'))
    boton_verificacion = sg.Button('Verificacion', key='Verificacion', size=(9,2), button_color=('dark blue'))
    boton_instrucciones = sg.Button('Instrucciones', key='Instrucciones', size=(9,2), button_color=('dark blue'))

    layout = [
        [sg.Column(
            [[boton_crear_tablero, boton_reiniciar, boton_pista, boton_movimientos, boton_guardar]], pad=(5,0)
            )
        ],
        [sg.Column(
            [[boton_volver, boton_deshacer, boton_verificacion, boton_instrucciones, boton_cargar]], pad=(5,0)
            )
        ],
        [sg.Column(
            [[sg.Text('Modo entrenamiento, inserte el numero de piezas: ')]]
            )
        ],
        [sg.Column(
            [[sg.Input(key='num_piezas'),
            sg.Button('Crear', size=(13,1), key='Crear', button_color=('dark blue'))]]
            )
        ]
    ] + [
        [sg.Button(' ', image_filename=img_madera_inhab if tablero[i,j] == -1 else img_pieza if tablero[i,j] == 1 else img_madera, size=(8,4),
                    key=matriz_keys[i,j], pad=(0,0), button_color=('white', 'green')) 
                        for j in range(7)
        ]
        for i in range(7)
    ]

    window = sg.Window('Solitario', layout, finalize=True)

    # variables auxiliares para el tratamiento de pulsaciones
    boton_pulsado = None
    boton_ya_pulsado = None
    botones_pulsados = None
    creando_tablero = False

    historial = []

    # bucle de la ventana
    while True:
        
        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED:
            break
               
        # se pulsa por primera vez el modo crear tablero, cambiamos la variable y la descripcion del boton
        elif event == 'Crear Tablero' and creando_tablero == False:
            window['Crear Tablero'].update(button_color=('red'))
            creando_tablero = True
            historial = []
            if botones_pulsados is not None:
                for x in botones_pulsados:
                    window[x].update(button_color=('white', 'green'), image_filename=img_pieza)
                botones_pulsados = None
            elif boton_ya_pulsado is not None:
                window[boton_ya_pulsado].update(button_color=('white', 'green'), image_filename=img_pieza)
                boton_ya_pulsado = None
            window['Crear Tablero'].update('Creando tablero')
        
        # se pulsa por segunda vez el modo creando tablero, cambiamos la variable y la descripcion del objeto
        elif event == 'Crear Tablero' and creando_tablero:
            window['Crear Tablero'].update(button_color=('dark blue'))
            creando_tablero = False
            window['Crear Tablero'].update('Crear tablero')
        
        # si estamos en modo creando tablero, al pulsar una pieza se cambia a hueco y viceversa
        elif creando_tablero:
            historial = []
            if event == 'Creando Tablero':
                creando_tablero = False
                window['Crear Tablero'].update('Crear tablero', window['Pista'].ButtonColor)
            # si se pulsa un boton que no es del tablero, se avisa de que se esta en el modo creando tablero
            elif event == 'Movimientos' or event == 'Reiniciar' or event == 'Pista' or event == 'Deshacer' or event == 'Verificacion' or event == 'Crear' or event == 'Cargar' or event == 'Guardar' or event == 'Instrucciones' or event == 'Volver':
                sg.Popup('Estas en modo creacion de tablero. \nSal del modo creacion para interactuar con otros botones')
            else:
                boton_pulsado = event
                i,j = indice(boton_pulsado)

                if tablero[i,j] == 0:
                    tablero[i,j] = 1
                    window[boton_pulsado].update(image_filename=img_pieza)
                elif tablero[i,j] == 1:
                    tablero[i,j] = 0
                    window[boton_pulsado].update(image_filename=img_madera)
        
        # mostrar instrucciones
        elif event == 'Instrucciones':
            instrucciones()
        
        # guardar tablero
        elif event == 'Guardar':
            guardar_tablero(tablero)
            

        # cargar tablero
        elif event == 'Cargar':
            tablero = cargar_tablero()
            if tablero is not None:
                for ls in matriz_keys:
                    for key in ls:
                        i,j = indice(key)
                        if tablero[i,j] == 1:
                            window[key].update(button_color=('white', 'green'), image_filename=img_pieza)
                        elif tablero[i,j] == -1:
                            window[key].update(button_color=('white', 'green'), image_filename=img_madera_inhab)
                        else:
                            window[key].update(button_color=('white', 'green'), image_filename=img_madera)
            boton_pulsado = None
            boton_ya_pulsado = None
            botones_pulsados = None

        # volver a inicio
        elif event == 'Volver':
            window.close()
            inicio()

        # modo entrenamiento
        elif event == 'Crear':
            historial = []
            num_piezas = values['num_piezas']
            if not num_piezas.isdigit():
                sg.Popup('Tienes que insertar un numero natural.')
            elif int(num_piezas) > 32:
                sg.Popup('El numero tiene que estar comprendido entre 1 y 32.')
            else:
                num_piezas = int(num_piezas)
                tablero = inversa(num_piezas)
                for ls in matriz_keys:
                    for key in ls:
                        i,j = indice(key)
                        if tablero[i,j] == 1:
                            window[key].update(button_color=('white', 'green'), image_filename=img_pieza)
                        elif tablero[i,j] == -1:
                            window[key].update(button_color=('white', 'green'), image_filename=img_madera_inhab)
                        else:
                            window[key].update(button_color=('white', 'green'), image_filename=img_madera)

        # deshace el ultimo movimiento cogiendo el tablero anterior del historial
        elif event == 'Deshacer':
            if historial:
                tablero = historial.pop()
                for ls in matriz_keys:
                    for key in ls:
                        i,j = indice(key)
                        if tablero[i,j] == 1:
                            window[key].update(button_color=('white', 'green'), image_filename=img_pieza)
                        elif tablero[i,j] == -1:
                            window[key].update(button_color=('white', 'green'), image_filename=img_madera_inhab)
                        else:
                            window[key].update(button_color=('white', 'green'), image_filename=img_madera)
            else:
                sg.Popup('No hay movimientos que deshacer.')
            boton_pulsado = None
            boton_ya_pulsado = None
            botones_pulsados = None
        
        # verifica si el tablero actual tiene solucion
        elif event == 'Verificacion':
            
            sol = dfs(tablero)
            
            if sol is not None:
                sg.Popup('Existe solucion para el tablero actual')
            else:
                sg.Popup('NO hay solucion para el tablero actual')

        # reiniciamos el tablero y todas las variables
        elif event == 'Reiniciar':
            tablero = crear_tablero()
            for ls in matriz_keys:
                for key in ls:
                    i,j = indice(key)
                    if tablero[i,j] == 1:
                        window[key].update(button_color=('white', 'green'), image_filename=img_pieza)
                    elif tablero[i,j] == -1:
                        window[key].update(button_color=('white', 'green'), image_filename=img_madera_inhab)
                    else:
                        window[key].update(button_color=('white', 'green'), image_filename=img_madera)
            boton_pulsado = None
            boton_ya_pulsado = None
            botones_pulsados = None
            
        elif event == 'Movimientos':                
            # si pido movimientos, diferenciamos si hay pieza pulsada o no
            # si lo hay selecciona los movimientos disponibles
            if boton_ya_pulsado is not None:
                i,j = indice(boton_ya_pulsado)
                movimientos = r_movimientos(tablero, i, j)
                # si hay movimientos disponibles se seleccionan los huecos
                if movimientos is not None and movimientos != []:
                    botones_pulsados = [(np.str_(x[1][0])+','+np.str_(x[1][1])) for x in movimientos]
                    for n in botones_pulsados:
                        window[n].update(button_color=('white', 'red'), image_filename=img_madera_sel)
                # si no hay movimientos disponibles no hacemos nada
                

            # si no hay boton pulsado seleccionamos las piezas que tienen movimiento disponible
            else:
                movimientos = devuelve_movimientos(tablero)
                botones_pulsados = [(np.str_(x[0][0])+','+np.str_(x[0][1])) for x in movimientos]
                for n in botones_pulsados:
                    window[n].update(button_color=('white', 'red'), image_filename=img_pieza_sel)

        elif event == 'Pista':
            if botones_pulsados is not None:
                for x in botones_pulsados:
                    window[x].update(button_color=('white', 'green'), image_filename=img_pieza)
            if boton_ya_pulsado is not None:
                window[boton_ya_pulsado].update(button_color=('white', 'green'), image_filename=img_pieza)
            
            inicio_timer = time.time()
            sol = dfs(tablero)
            fin_timer = time.time()
            print('tiempo', fin_timer-inicio_timer)
            
            # si pido una pista, diferenciamos si hay solucion o no
            if sol is not None:
                pista = sol.pop(0)
                pieza = np.str_(pista[0])
                hueco = np.str_(pista[1])
                pieza = pieza.replace('(','').replace(')', '').replace(' ', '')
                hueco = hueco.replace('(','').replace(')','').replace(' ','')
                window[pieza].update(button_color=('white', 'red'), image_filename=img_pieza_sel)
                window[hueco].update(button_color=('white', 'red'), image_filename=img_madera_sel)
                botones_pulsados = [hueco]
                    
                # si hay solucion y boton ya pulsado, deseleccionamos el boton pulsado y seleccionamos la pieza de la pista
                if boton_ya_pulsado is not None and boton_ya_pulsado != pieza:
                    window[boton_ya_pulsado].update(button_color=('white', 'green'), image_filename=img_pieza)
                    boton_ya_pulsado = pieza

                # si hay solucion y no habia boton pulsado, guardamos como ya pulsada la pieza de la pista
                else:
                    boton_ya_pulsado = pieza
            # si no hay solucion, avisamos de que no la hay y pregntamos si el usuario quiere retrocecder hasta que la haya
            else:
                sg.Popup('NO existe solucion. ')
            
        else:

            boton_pulsado = event
            if boton_pulsado != 'Movimientos' or boton_pulsado != 'Reiniciar' or boton_pulsado != 'Pista' or boton_pulsado != 'Deshacer' or boton_pulsado != 'Verificacion' or boton_pulsado != 'Crear' or boton_pulsado != 'Cargar' or boton_pulsado != 'Guardar' or boton_pulsado != 'Instrucciones' or boton_pulsado != 'Volver':
                i,j = indice(boton_pulsado)

            # si hay botones pulsados resultado de movimientos y se pulsa una pieza, el resto se deseleccionan
            if botones_pulsados is not None and boton_ya_pulsado is not None:
                # si habiendo movimientos destacados pulso otra pieza, se deselecciona todo y se selecciona la nueva pieza
                # caso en el que el boton de movimientos se pulso con una pieza
                if tablero[i,j] == 1:
                    for x in botones_pulsados:
                        window[x].update(button_color=('white', 'green'), image_filename=img_madera)
                    window[boton_ya_pulsado].update(button_color=('white', 'green'), image_filename=img_pieza)
                    window[boton_pulsado].update(button_color=('white', 'red'), image_filename=img_pieza_sel)
                    boton_ya_pulsado = boton_pulsado
                    botones_pulsados = None


                # si habiendo movimientos destacados con una pieza seleccionada pulso un hueco que no es valido, deselecciono todo 
                elif tablero[i,j] == 0 and boton_pulsado not in botones_pulsados:
                    for x in botones_pulsados:
                        window[x].update(button_color=('white', 'green'), image_filename=img_madera)
                    window[boton_ya_pulsado].update(button_color=('white', 'green'), image_filename=img_pieza)
                    boton_ya_pulsado = None
                    botones_pulsados = None
                
                # si habiendo movimientos destacados pulso un hueco valido, deselecciono el resto de huecos y muevo 
                elif tablero[i,j] == 0 and boton_pulsado in botones_pulsados:
                    for x in botones_pulsados:
                        if x != boton_pulsado:
                            window[x].update(button_color=('white', 'green'), image_filename=img_madera)
                    
                    x,y = indice(np.str_(boton_ya_pulsado))
                    
                    historial.append(tablero.copy())
                    tablero = mueve(tablero,((x,y),(i,j)))

                    window[boton_pulsado].update(button_color=('white', 'green'), image_filename=img_pieza)

                    window[boton_ya_pulsado].update(button_color=('white', 'green'), image_filename=img_madera)
                    boton_ya_pulsado = None

                    boton_medio = calcula_pieza_medio(((x,y),(i,j)))
                    window[boton_medio].update(button_color=('white', 'green'), image_filename=img_madera)

                    botones_pulsados = None

                    if es_fin(tablero):
                        popup_victoria()
                    elif devuelve_movimientos(tablero) == []:
                        popup_game_over()


            # caso en el que al pulsar movimientos no habia ninguna pieza seleccionada y ahora pulso una pieza
            elif botones_pulsados is not None and boton_ya_pulsado is None:
                i,j = indice(boton_pulsado)
                if tablero[i,j] == 1:
                    # si se ha pulsado un boton que no estaba seleccionado, se selecciona
                    if boton_pulsado not in botones_pulsados:
                        window[boton_pulsado].update(button_color=('white', 'red'), image_filename=img_pieza_sel)
                    # se deselecciona el resto
                    for x in botones_pulsados:
                        if x != boton_pulsado:
                            window[x].update(button_color=('white', 'green'), image_filename=img_pieza)
                boton_ya_pulsado = boton_pulsado
                botones_pulsados = None



            # hay boton ya pulsado y lo vuelvo a pulsar, lo deseleccionamos
            elif boton_ya_pulsado is not None and event == boton_ya_pulsado:
                window[boton_ya_pulsado].update(button_color=('white', 'green'), image_filename=img_pieza)

                boton_ya_pulsado = None

            # hay boton ya pulsado y pulso otro, diferenciamos entre haber pulsado pieza o no
            elif boton_ya_pulsado is not None and boton_pulsado != boton_ya_pulsado:
                # si he pulsado una pieza, deseleccionamos y pulsamos la nueva
                if tablero[i,j] == 1:
                    window[boton_ya_pulsado].update(button_color=('white', 'green'), image_filename=img_pieza)

                    window[boton_pulsado].update(button_color=('white', 'red'), image_filename=img_pieza_sel)

                    boton_ya_pulsado = boton_pulsado
                
                # si se ha pulsado un hueco, comprobamos si es movimiento legal, si lo es se hace el movimiento
                elif tablero[i,j] == 0:
                    x,y = indice(boton_ya_pulsado)
                    ls_movimientos = r_movimientos(tablero,x,y)
                    if ((x,y),(i,j)) in ls_movimientos:
                        historial.append(tablero.copy())
                        tablero = mueve(tablero,((x,y),(i,j)))

                        window[boton_pulsado].update(button_color=('white', 'green'), image_filename=img_pieza)

                        window[boton_ya_pulsado].update(button_color=('white', 'green'), image_filename=img_madera)
                        boton_ya_pulsado = None

                        boton_medio = calcula_pieza_medio(((x,y),(i,j)))
                        window[boton_medio].update(button_color=('white', 'green'), image_filename=img_madera)

                        if es_fin(tablero):
                            popup_victoria()
                        elif devuelve_movimientos(tablero) == []:
                            popup_game_over()
                    if botones_pulsados is not None:
                        for x in botones_pulsados:
                            window[x].update(image_filename=img_madera)
            
            # no hay boton ya pulsado, compruebo si se ha pulsado una pieza para seleccionarla
            elif boton_ya_pulsado is None and tablero[i,j] == 1: 
                window[boton_pulsado].update(button_color=('white', 'red'), image_filename=img_pieza_sel)

                boton_ya_pulsado = boton_pulsado


    window.close()

if __name__ == '__main__':
    inicio()

