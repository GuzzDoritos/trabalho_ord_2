import os
from sys import argv
from src.registro import lista_de_registros
from src.indices import construir_indice_pri, construir_indice_sec
from src.persistencia import (
    arq_indice_prim, arq_indice_genero,
    arq_indice_publicadora, arq_indice_listainv
)
from src.operacoes import *
from src.compactacao import compactacao


ARQUIVO = "data/games.dat"

def modo_b():
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
            
    indice_pri = arq_indice_prim(None)
    indice_sec_genero = arq_indice_genero(None)
    indice_sec_publicadora = arq_indice_publicadora(None)
    lista_inv = arq_indice_listainv(None)
    
    with open("data/games.dat", "rb+") as arq_games:
        with open(arquivo_operacoes, "r", encoding="utf-8") as arq_ops:
            buffer = arq_ops.readline().strip()
            while buffer:
                comando = buffer.split(None, 1)
                buffer = arq_ops.readline().strip()
                match comando[0]:
                    case 'bp':
                        print(f'Busca pelo registro de ID "{int(comando[1])}"')
                        resultado = busca_pri(int(comando[1]), indice_pri, arq_games)
                        if resultado:
                            print(resultado)
                        else:
                            print("Registro não encontrado!")
                        print()
                    case 'bs1' | 'bs2':
                        chave = comando[1]
                        if comando[0] == 'bs1':
                            encontrados = busca_sec_genero(chave, indice_sec_genero, indice_pri, lista_inv, arq_games)
                            pesquisa = 'gênero'
                        elif comando[0] == 'bs2':
                            encontrados = busca_sec_publicadora(chave, indice_sec_publicadora, indice_pri, lista_inv, arq_games)
                            pesquisa = 'publicadora'
                        print(f'Busca por registros de {pesquisa} "{chave}" ({len(encontrados)} registros)')
                        for reg in encontrados:
                            print(reg)
                        print()
                    case 'i':
                        chave = comando[1].split("|")[0]
                        num_bytes = len(comando[1].encode("utf-8"))
                        print(f'Inserção do registro de chave "{chave}" ({num_bytes} bytes)')
                        retorno = insercao(comando[1], indice_pri, indice_sec_genero, indice_sec_publicadora, lista_inv, arq_games, num_bytes)
                        if not retorno:
                            print("ID duplicado! Registro descartado.")
                        else:
                            print("Inserido com sucesso.")
                        print()
                    case 'r':
                        chave = int(comando[1])
                        offset = busca_binaria(chave, indice_pri)
                        if offset > -1:
                            print(f'Remoção do registro de chave "{chave}" (offset = {offset})\n')
                            remocao(chave, offset, indice_pri, indice_sec_genero, indice_sec_publicadora, lista_inv, arq_games)
                        else:
                            print(f'Remoção do registro de chave "{chave}"')
                            print('Elemento não existe.\n')

    arq_indice_prim(indice_pri)
    arq_indice_genero(indice_sec_genero)
    arq_indice_publicadora(indice_sec_publicadora)
    arq_indice_listainv(lista_inv)


def modo_c():
    compactacao()


def main():
    if argv[1] == '-b':
        modo_b()
    elif argv[1] == '-e':
        modo_e(argv[2])
    elif argv[1] == '-c':
        modo_c()

if __name__ == "__main__":
    main()