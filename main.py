from sys import argv
from src.registro import lista_de_registros
from src.indices import construir_indice_pri, construir_indice_sec
from src.persistencia import (
    arq_indice_prim, arq_indice_genero,
    arq_indice_publicadora, arq_indice_listainv
)

ARQUIVO = "data/games.dat"

def modo_b(): # Construção de índices
    with open(ARQUIVO, 'rb') as entrada:
        registros = lista_de_registros(entrada)
    
    lista_inv = []
    indice_pri = construir_indice_pri(registros)
    indice_sec = construir_indice_sec(registros, lista_inv)

    arq_indice_prim(indice_pri)
    arq_indice_genero(indice_sec[0])
    arq_indice_publicadora(indice_sec[1])
    arq_indice_listainv(lista_inv)

def modo_e(arquivo_operacoes): # Execução do arquivo de operações
    pass  # TODO

def modo_c(): # Modo de compactação do arquivo
    pass  # TODO

def main():
    if argv[1] == '-b':
        modo_b()
    elif argv[1] == '-e':
        modo_e(argv[2])
    elif argv[1] == '-c':
        modo_c()

if __name__ == "__main__":
    main()