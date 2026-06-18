import os
from sys import argv
from src.arvoreb import *
from src.constantes import *

def modo_b():
    criaIndice() #teste

def modo_e(arquivo_operacoes):
    # Trata o caso do argumento chegar vazia ou nula
    if not arquivo_operacoes: 
        print("Erro: Arquivo de operações não informado. Encerrando.")
        return
    
    arquivos_necessarios = [
        "data/games.dat", 
        "data/btree.dat",
        arquivo_operacoes
    ]
    
    for caminho in arquivos_necessarios:
        if not os.path.exists(caminho):
            print(f"Erro: Arquivo necessário não encontrado ({caminho}). Encerrando.")
            return            
    
    with open(ARQ_GAMES, "rb+") as arq_games:
        with open(arquivo_operacoes, "r", encoding="utf-8") as arq_ops:
            buffer = arq_ops.readline().strip()
            while buffer:
                comando = buffer.split(None, 1)
                buffer = arq_ops.readline().strip() 
                match comando[0]:
                    case 'b':
                        chave = int(comando[1])
                        busca(chave)
                    case 'i':
                        pass
    
def modo_p():
    imprimirArvoreB(ARQ_BTREE)

def main():

    if len(argv) == 1:
        print('uso:\ncriar árvore: python main.py -b\noperações: python main.py -e [caminho arquivo]\nimpressão da árvore: main.py -p')
        return
    if argv[1] == '-b':
        modo_b()
    elif argv[1] == '-e':
        modo_e(argv[2])
    elif argv[1] == '-p':
        imprimirArvoreB(ARQ_BTREE)

if __name__ == "__main__":
    main()