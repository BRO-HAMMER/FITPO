# ----- DEFINICIÓN DE FUNCIONES ----- #


def suma(lista):
    # devuelve la sumatoria de los valores contenidos en una lista.
    resultado = 0
    for i in lista:
        resultado += i

    return resultado


def calc_ci(valor1, valor2):
    # devuelve el valor correspondiente al centro del intervalo a partir de sus extremos.
    return (valor1 + valor2) / 2


def calc_media_n(tabla):
    # calcula la media de la tabla de datos como la sumatoria de los centros de intervalo multiplicados
    # por la frecuencia relativa respectiva a cada uno de ellos.

    medias_parciales = []  # inicializa lista de medias parciales
    n = 0  # inicializa contador de observaciones en la tabla
    for num_intervalo in range(1, len(tabla)):
        # corresponde a una fila de datos (ignora índice 0), ya que la función 'range'
        # tomará valores desde 1 hasta la cantidad de elementos en la lista

        # con los primeros 2 elementos (max y min del intervalo), calcula el centro
        ci = calc_ci(tabla[num_intervalo][0], tabla[num_intervalo][1])
        # 2 es el índice correspondiente a las frecuencias absolutas
        fai = tabla[num_intervalo][2]
        # agrega a la lista las medias parciales de cada intervalo (CI * fai)
        medias_parciales.append(ci * fai)
        # agrega al contador las observaciones correspondientes al intervalo
        n += fai

    # calcula la media correspondiente a la tabla
    media = suma(medias_parciales) / n

    # devuelve la media y el número de observaciones
    return media, n


def calc_var_s(tabla, media, n_muestras):

    # calcula la varianza de la tabla como:  suma[ fai . ( X - CI )**2 ] / n

    var_parciales = []  # inicializa lista de medias parciales
    for num_intervalo in range(1, len(tabla)):
        # corresponde a una fila de datos (ignora índice 0), ya que la función 'range'
        # tomará valores desde 1 hasta la cantidad de elementos en la lista

        # con los primeros 2 elementos (max y min del intervalo), calcula el centro
        ci = calc_ci(tabla[num_intervalo][0], tabla[num_intervalo][1])
        # 2 es el índice correspondiente a las frecuencias absolutas
        fai = tabla[num_intervalo][2]
        # agrega a la lista las varianzas parciales de cada intervalo
        var_intervalo = fai * (media - ci)**2
        var_parciales.append(var_intervalo)

    # calcula la media correspondiente a la tabla
    var = suma(var_parciales) / n_muestras

    # calcula el desvío estándar como la raíz cuadrada de la varianza
    s = var**0.5

    return var, s


def calc_cv(media, s):
    # calcula el coeficiente de variación
    cv = s/media
    # decide si el conjunto es homogéneo o heterogéneo
    if cv < 0.25:
        tipo_de_conjunto = "Homogéneo"
    else:
        tipo_de_conjunto = "Heterogéneo"

    return cv, tipo_de_conjunto


def obtener_estadisticos(datos):
    # genera un array con los resultados del análisis estadístico

    estadisticos = []
    # recorrer cada tabla en el array de datos
    for num_tabla in range(len(datos)):
        # creará un array con una columna por cada tabla con la forma
        # ["nombre_tabla", X, s, CV, tipo_de_conjunto]
        estadisticos.append([])

        # añade el título de la tabla
        titulo = datos[num_tabla][0]
        estadisticos[num_tabla].append(titulo)

        # calcula la media y la añade
        # en la posición correspondiente del array
        media, n = calc_media_n(datos[num_tabla])
        estadisticos[num_tabla].append(media)

        # calcula el desvío estándar y lo añade
        # en la posición correspondiente del array
        var, s = calc_var_s(datos[num_tabla], media, n)
        estadisticos[num_tabla].append(s)

        # calcula el coeficiente de variación y lo añade
        # en la posición correspondiente del array
        cv, tipo_de_conjunto = calc_cv(media, s)
        estadisticos[num_tabla].append(cv)
        estadisticos[num_tabla].append(tipo_de_conjunto)

    # devuelve el array con los estadísticos de interés
    return estadisticos

# ----- FUNCIONES UTILITARIAS PARA LA INTERFAZ ----- #


def desplegar_menu(lista, mensaje="Seleccione una opción.", salircon0=False):

    # despliega una lista como un menú indexado, la opción 0 es salir del menú
    for idx in range(len(lista)):
        print(idx + 1, ")", lista[idx])
    if salircon0:
        print("0 ) Salir")

    opcion = -1
    print(mensaje)
    # se pide ingresar un dato hasta que el usuario ingrese una opción válida
    while opcion < 0 or opcion > len(lista):

        opcion = int(input("Opción: "))

    return opcion  # devuelve la opción elegida por el usuario


def imprimir_tabla(tabla):
    # se imprime el título de la tabla y de cada columna
    print(tabla[0])
    print("#", "[min", "max", "obs]")

    for fila in range(1, len(tabla)):  # se ignora la primer línea que corresponde al nombre
        # se imprime cada fila
        print(str(fila), tabla[fila])
    # deja una línea en blanco debajo de la tabla
    print("\n")


def actualizar_opciones(datos):
    # se definen algunos datos necesarios para el menú de usuario
    # se obtienen los nombres de las tablas que ya se encuentran cargadas
    tablas = []
    for t in datos:
        # se recorre cada tabla en el array de datos, agregando a la lista sus nombres
        tablas.append(t[0][0])

    n_tablas = str(len(tablas))
    # se agrega la opción de ingresar una nueva tabla
    tablas.append("Ingresar nueva tabla")
    return tablas, n_tablas


def cargar_datos():
    nombre = input("\nIngrese título de la tabla: ")
    # inicializar una nueva tabla
    nueva_tabla = [[nombre]]
    n = 0
    continuar = True  # variable tomará valor False al finalizar
    while continuar:
        n += 1
        print("Ingresando fila", n)
        minimo = float(input("Ingrese valor mínimo del intervalo: "))
        maximo = float(input("Ingrese valor máximo del intervalo: "))
        obs = int(input("Ingrese número de observaciones: "))
        # validación de datos: mínimo debe ser menor al máximo
        # y no se aceptan números negativos
        if minimo >= maximo or minimo < 0 or maximo < 0 or obs < 0:
            print("LOS DATOS INGRESADOS NO SON VÁLIDOS.\n")
            n -= 1  # retorna a las condiciones previas al ingreso de datos
        else:
            # agregar los datos a la nueva tabla
            nueva_tabla.append([minimo, maximo, obs])
            # consultar si continuará ingresando datos
            while True:
                check = input("¿Desea ingresar otra fila? (S / N) ")
                if check == "n" or check == "N":
                    continuar = False  # no vuelve a ingresar al bucle principal
                    break  # sale de este bucle
                elif check == "s" or check == "S":
                    break  # sale de este bucle pero no del principal
                else:
                    print("LA OPCIÓN INGRESADA NO ES VÁLIDA.\n")

    # si la tabla tiene al menos una fila de valores, añadirla al array de datos
    if len(nueva_tabla) > 1:
        array_datos.append(nueva_tabla)
        # proveer información de diagnóstico
        print("tabla", nueva_tabla[0][0], "con", len(nueva_tabla), "filas agregadas.")
    else:
        print("La tabla ingresada no contiene datos.")


# ----- INICIA EL PROGRAMA ----- #
# se inicializa el array de datos
array_datos = [

              [["Sin tratamiento"], [7.6, 8.2, 4], [8.2, 8.8, 22], [8.8, 9.4, 95],
               [9.4, 10.0, 251], [10.0, 10.6, 177], [10.6, 11.2, 43], [11.2, 11.8, 6]],

              [["Con tratamiento"], [6.2, 7.1, 1], [7.1, 8.0, 1], [8.0, 8.9, 32],
               [8.9, 9.8, 189], [9.8, 10.7, 369], [10.7, 11.6, 60], [11.6, 12.5, 2]]

              ]

# se inicializa la lista de opciones
opciones = ["Imprimir Tabla", "Media - X", "Desvío estándar - s", "Coeficiente de Variación - CV"]

# ------- MENÚ DE USUARIO ------- #

print("| BIENVENIDO |")

# bucle principal
while True:
    # se actualiza la información que se encuentra cargada en el sistema
    menu_tablas, cantidad_tablas = actualizar_opciones(array_datos)

    # presentación de la información disponible y opción de agregar nuevas tablas
    print("\nSe encontraron " + cantidad_tablas + " tablas de datos:")

    # despliegue de menú y selección de tabla sobre la cuál se desde trabajar
    num_tabla = desplegar_menu(menu_tablas, "\n¿Con cuál desea trabajar?", salircon0=True)

    # carga de datos (siempre será la última opción)
    if num_tabla == len(menu_tablas):
        cargar_datos()

    # opción de salida
    if num_tabla == 0:
        break

    # bucle anidado
    while num_tabla != len(menu_tablas): # los datos ya fueron validados por desplegar_menu
        # utilizando las funciones definidas se obtiene un array con los estadísticos de interés
        resultados = obtener_estadisticos(array_datos)  # ["nombre_tabla", X, s, CV, tipo_de_conjunto]

        # despliegue del menú de trabajo sobre la tabla elegida
        print("\nTabla: " + menu_tablas[num_tabla-1])
        dar_dato = desplegar_menu(opciones, "\nIndique qué dato desea obtener", salircon0=True)
        if dar_dato == 0:
            break
        elif dar_dato == 1:
            imprimir_tabla(array_datos[num_tabla-1])
        else:  # los datos ya fueron validados por desplegar_menu
            print("\n"+opciones[dar_dato-1], "=", resultados[num_tabla-1][dar_dato-1])

        # en caso de que solicite el coeficiente de variación, agregar dato de homogeneidad
        if dar_dato == 4:
            print("El conjunto de datos es "+resultados[num_tabla-1][4])

        input("\nPresione ENTER para continuar.")

# ----- FINALIZA EL PROGRAMA ----- #
print("\nProgramado por Nicolás Aldecoa Rodrigo")
