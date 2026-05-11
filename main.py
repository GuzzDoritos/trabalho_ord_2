import os
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

def modo_e(arquivo_operacoes):
    # Trata o caso do argumento chegar vazia ou nula
    if not arquivo_operacoes:
        print("Erro: Arquivo de operações não informado. Encerrando.")
        return
    
    arquivos_necessarios = [
        "data/games.dat", 
        "data/primario.ind", 
        "data/genero.ind", 
        "data/publicadora.ind", 
        "data/listaInvertida.lst",
        arquivo_operacoes
    ]
    
    for caminho in arquivos_necessarios:
        if not os.path.exists(caminho):
            print(f"Erro: Arquivo necessário não encontrado ({caminho}). Encerrando.")
            return
            
    # carregar índices passando 'None' (como programado no persistencia.py)
    indice_pri = arq_indice_prim(None)
    indice_sec_genero = arq_indice_genero(None)
    indice_sec_publicadora = arq_indice_publicadora(None)
    lista_inv = arq_indice_listainv(None)
    
    # abrir o games.dat e o arquivo de operações
    with open("data/games.dat", "rb+") as arq_games, open(arquivo_operacoes, "r", encoding="utf-8") as arq_ops:
        pass # TODO

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