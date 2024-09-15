import pandas as pd
import numpy as np


def calificacion(dataFrame_Sorted):
    # le asigna una calificacion a cada elemento del dataframe de 10 a 0 como corresponda
    calificaciones = np.linspace(10, 0, len(dataFrame_Sorted))
    dataFrame_Sorted.loc[:, 'Calificacion'] = calificaciones

    return  dataFrame_Sorted

def promedio(trabajo, estado, ocupacionSorted, entidadSorted):
    # se observa la calificación de cada variable y se observa el promedio
    calificacion_trabajo = ocupacionSorted.loc[ocupacionSorted['Ocupacion'] == trabajo, 'Calificacion']
    calificacion_estado = entidadSorted.loc[entidadSorted['Entidad'] == estado, 'Calificacion']

    # se asigna valor
    calificacion_trabajo = calificacion_trabajo.values[0]
    calificacion_estado = calificacion_estado.values[0]
    promedio = (calificacion_trabajo + calificacion_estado) / 2

    return promedio

def verificacionClase(promedio):
    # se verifica la clase a la que pertenece la persona
    if promedio >= 7:
        return 'Alta'
    elif promedio >= 3:
        return 'Media'
    else:
        return 'Baja'

ocupacion = pd.read_excel('ocupacion.xlsx')
ocupacionSorted = ocupacion.sort_values(by='Ingresos', ascending=False).reset_index(drop=True)
ocupacionSorted = calificacion(ocupacionSorted)

entidad = pd.read_excel('entidad.xlsx')
entidadSorted = entidad.sort_values(by='Ingresos', ascending=False).reset_index(drop=True)
entidadSorted = calificacion(entidadSorted)

trabajo = 'Medicina'
estado = 'Ciudad de México'
edad = 42

promedio = promedio(trabajo,estado,ocupacionSorted,entidadSorted)
print(promedio)
clase = verificacionClase(promedio)
print(clase)

if clase == 'Alta':
    print('opciones A')
elif clase == 'Media':
    print('opciones B')
else:
    print('opciones C')