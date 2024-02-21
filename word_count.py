#
# Escriba la función load_input que recive como parámetro un folder y retorna
# una lista de tuplas donde el primer elemento de cada tupla es el nombre del
# archivo y el segundo es una línea del archivo. La función convierte a tuplas
# todas las lineas de cada uno de los archivos. La función es genérica y debe
# leer todos los archivos de folder entregado como parámetro.
#
# Por ejemplo:
#   [
#     ('text0'.txt', 'Analytics is the discovery, inter ...'),
#     ('text0'.txt', 'in data. Especially valuable in ar...').
#     ...
#     ('text2.txt'. 'hypotheses.')
#   ]
#

"""Taller evaluable"""

import glob

import pandas as pd


def load_input(input_directory):
    """Load text files in 'input_directory/'"""
    #
    # Lea los archivos de texto en la carpeta input/ y almacene el contenido en
    # un DataFrame de Pandas. Cada línea del archivo de texto debe ser una
    # entrada en el DataFrame.
    #

    filenames = glob.glob(input_directory + '/*.*')
    dataframes = [
        pd.read_csv(filename, index_col = None, sep=';', names=['text']) for filename in filenames
    ]
    dataframe = pd.concat(dataframes).reset_index(drop=True)
    return dataframe
def clean_text(dataframe):
    """Text cleaning"""
    #
    # Elimine la puntuación y convierta el texto a minúsculas.
    #
    dataframe = dataframe.copy()
    dataframe['text'] = dataframe['text'].str.replace(',', '').str.replace('.','').str.lower()
    return dataframe

def count_words(dataframe):
    """Word count"""
    dataframe = dataframe.copy()
    dataframe['text'] = dataframe['text'].str.split(' ')
    dataframe = dataframe.explode('text').reset_index(drop=True) #Voltea la lista de palabras en filas de dataframe
    dataframe = dataframe.rename(columns = {'text':'word'})
    dataframe['count'] = 1

    conteo = dataframe.groupby(['word'], as_index = False).agg(
        {
            'count': sum
        }
    )
    return conteo

def save_output(dataframe, output_filename):
    """Save output to a file."""
    dataframe.to_csv(output_filename, sep=';', index=False)


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run(input_directory, output_filename):
    """Call all functions."""
    dataframe = load_input(input_directory)
    dataframe = clean_text(dataframe)
    dataframe = count_words(dataframe)
    save_output(dataframe, output_filename)
    


if __name__ == "__main__":
    run(
        "input",
        "output.txt",
    )
