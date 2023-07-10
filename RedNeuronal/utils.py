import os
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt

from itertools import permutations
total = 0
max_cols = 32
max_rows = 15


def generate_permutations(matrix):
    global total
    num_rows = len(matrix)
    if num_rows > 6:
        num_rows = 10
    row_indices = list(range(num_rows))
    permutations_list = list(permutations(row_indices))
    permuted_matrices = []
    for permutation in permutations_list:
        permuted_matrix = [matrix[i] for i in permutation]
        permuted_matrices.append(permuted_matrix)
    total = total +len(permuted_matrices)
    return permuted_matrices


def recorrer_carpeta(carpeta):
    matrixes = []
    numero = 0
    for root, dirs, files in os.walk(carpeta):
        for file in files:
            ruta_completa = os.path.join(root, file)
            print(numero, ruta_completa)
            numero = numero +1
            df = pd.read_excel(ruta_completa)
            matrix = df.values
            matrixes.append(matrix)
    return matrixes


def get_data_set():
    cronogramas = []
    carpeta_a_recorrer = "DatasetTesis"
    matrixes = recorrer_carpeta(carpeta_a_recorrer)
    for matrix in matrixes:
        cronograma = []
        for person in matrix:
            person_cronograma = []
            row = person[1:]
            #print(person)
            for col in row:
                turno = [0,0,0]
                if type(col) == str:
                    val = col.split('/')
                    for i in val:
                        if i[0]=='M':
                            turno[0]=1
                        if i[0] == 'T':
                            turno[1]=1
                        if i[0] == 'D':
                            turno[0]=1
                            turno[1]=1
                        if i[0] == 'N':
                            turno[2]=1
                        if i[0:2] == 'GD':
                            turno[0]=1
                            turno[1]=1
                        if i[0:2] == 'GN':
                            turno[2]=1
                person_cronograma.append(turno)
            cronograma.append(person_cronograma)
        cronogramas.append(cronograma)
    return cronogramas



def per_data_set():
    total = 0
    result = []
    cronogramas = get_data_set()
    for i in cronogramas:
        per = generate_permutations(i)
        total = total + len(per)
        for j in per:
            result.append(j)
    print(total)
    return result


def per_data_set_full(cronogramas):
    total = 0
    result = []
    for i in cronogramas:
        per = generate_permutations(i)
        total = total + len(per)
        for j in per:
            result.append(j)
    print(total)
    return result

def get_data_set_full():
    cronogramas = []
    default = []
    carpeta_a_recorrer = "DatasetTesis"
    matrixes = recorrer_carpeta(carpeta_a_recorrer)
    for matrix in matrixes:
        cronograma = []
        default_cronograma = []
        for person in matrix:
            person_cronograma = []
            default_persona_cronograma = []
            row = person[1:]
            for i in range(max_cols):
                if i >= len(row):
                    person_cronograma.append([-1,-1,-1])
                    default_persona_cronograma.append([-1,-1,-1])
                    continue
                col = row[i]
                turno = [0,0,0]
                turno_default = [0,0,0]
                if type(col) == str:
                    val = col.split('/')
                    for i in val:
                        if i[0]=='M':
                            turno[0]=1
                        if i[0] == 'T':
                            turno[1]=1
                        if i[0] == 'D':
                            turno[0]=1
                            turno[1]=1
                        if i[0] == 'N':
                            turno[2]=1
                        if i[0:2] == 'GD':
                            turno[0]=1
                            turno[1]=1
                        if i[0:2] == 'GN':
                            turno[2]=1

                person_cronograma.append(turno)
                default_persona_cronograma.append(turno_default)

            cronograma.append(person_cronograma)
            default_cronograma.append(default_persona_cronograma)


        for i in range(max_rows - len(cronograma)):
            df = []
            for _ in range(max_cols):
                df.append([-1,-1,-1])
            default_cronograma.append(df)

        variaciones = generate_permutations(cronograma)


        for variacion in variaciones:
            default.append(default_cronograma)
            for i in range(max_rows - len(variacion)):
                df = []
                for _ in range(max_cols):
                    df.append([-1,-1,-1])
                variacion.append(df)
            cronogramas.append(variacion)               
    return default, cronogramas 


def eval_result(matriz):
    num_filas = len(matriz)
    num_columnas = len(matriz[0])
    score = []
    for columna in range(num_columnas):
        default = [0,0,0]
        for fila in range(num_filas):
            elemento = matriz[fila][columna]
            default = [x or y for x, y in zip(default, elemento)]
        score.append(default)
    total_elementos = 0
    contador_unos = 0
    num_columnas = len(score[0])
    for fila in score:
        for elemento in fila:
            total_elementos += 1
            if elemento == 1:
                contador_unos += 1
    porcentaje = (contador_unos / total_elementos) * 100
    print("acc",porcentaje)
    return porcentaje



def eval_descansos(matriz):
    personas = len(matriz)
    dias = len(matriz[0])
    total = 0
    aciertos = 0
    for fila in range(personas):
        for columna in range(dias):
            if matriz[fila][columna][2]:
                total = total + 1
                if np.all(matriz[fila][columna+1] == 0):
                    aciertos = aciertos + 1
    if total == 0:
        return -1
    print('restricciones',aciertos/total)
    porcentaje = (aciertos/total)*100
    return porcentaje

def graficar(matrices,labels):
    linea = 1
    for key,matriz in enumerate(matrices):
        print(matriz)
        num_filas = len(matriz)
        num_filas = 5
        num_columnas = len(matriz[0])
        score = []
        x = []
        dia = 0
        # Recorrer por columnas
        for columna in range(num_columnas):
            default = [0,0,0]
            x.append(dia)
            x.append(dia+1)
            x.append(dia+2)
            dia = dia+3
            for fila in range(num_filas):
                elemento = matriz[fila][columna]
                default = default+elemento
            for i in range(3):
                if default[i] < 0:
                    default[i] = 0
            score.append(default)
        print(score)
        my_array = np.array(score)
        reshaped_array = my_array.reshape(-1)
        print(reshaped_array)
        print(len(reshaped_array))
        print(len(x))
        plt.plot(x, reshaped_array, label=f'{labels[key]}')
        linea +=1
        plt.xlabel('Turno')
        plt.ylabel('Personas')
        plt.title('Personas por turno')

    plt.legend()
    plt.show()


def graficar_matrices(matrices,labels):
    for key, matriz in enumerate(matrices):
        x = list(range(2, 32,5))
        plt.plot(x, matriz, label=f'{labels[key]}')
        plt.xlabel('Epoch')
        plt.ylabel('Percentage')
        plt.title('Disminución del error')

    plt.legend()
    plt.show()