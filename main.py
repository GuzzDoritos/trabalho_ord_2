from sys import argv
from struct import pack, unpack, calcsize
from src.registro import lista_de_registros
from src.indices import construir_indice_pri, construir_indice_sec

arquivo = "data/games.dat"

def main():
    '''Esse programa lê os dados gravados no arquivo criado pelo programa
    escreve_registros
    Os registros devem ser lidos do arquivo um a um e apresentados em tela'''
    NOME_ARQ = 'games.dat'
    ENTRADA = open(NOME_ARQ, 'rb')

    if argv[1] == '-b':
        print("Modo de construção de índice")

        lista_inv = []
        indicesec = construir_indice_sec(registros, lista_inv)
        indicepri = construir_indice_pri(registros)
        registros = lista_de_registros(ENTRADA)

    elif argv[1] == '-e':
        print("Modo de leitura de arquivo de operações")

    elif argv[1] == '-c':
        print("Modo compactação do arquivo")


    arq_indice_prim(indicepri)
    carregado = arq_indice_prim(None)
    print(carregado)

    arq_indice_genero(indicesec[0])
    carregado2 = arq_indice_genero(None)
    print(carregado2)

    arq_indice_publicadora(indicesec[1])
    carregado3 = arq_indice_publicadora(None)
    print(carregado3)

    arq_indice_listainv(lista_inv)
    carregado4 = arq_indice_listainv(None)
    print(carregado4)

    ENTRADA.close()

if __name__ == "__main__":
    main()