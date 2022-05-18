import numpy as np
import scipy.io

global file
global row_counter

def open_file(name):
    global file
    file = open(name, 'r')

def close_file():
    global file
    file.close()

def get_row():
    global file
    row_content = file.readline()
    
    array_string_values = row_content.split(', ')
    array_string = np.array(array_string_values)
    #Solo se convierte a float cuando el arreglo No esta vacío
    if len(array_string) > 1:
        array_float  = array_string.astype(np.float)
    else:
        #Se regresa una cadena vacia solo para que no de error
        array_float = []

    return array_float


"""
if __name__ == '__main__':
    file_name = "raw_data_file.txt"
    open_file(file_name)


    row_counter = 1
    row_data = get_row()
    while 1:
        #La lectura de datos es más veloz que la escritura así que si nos encontramos
        #una lectura que nos regrese un arreglo vacio porque ya se llegó al final del archivo
        #la desechamos e intentamos nuevamente hasta que se escriban nuevos datos.
        if(len(row_data)>0):
            print(row_counter, end=": ")
            print(row_data)
            row_counter = row_counter + 1
        row_data = get_row()

    close_file()
"""