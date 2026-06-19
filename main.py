import os
from sys import argv
from src.arvoreb import *
from src.constantes import *

def modo_b():
    criaIndice() 

def modo_e(arquivo_operacoes):
    # Trata o caso do argumento chegar vazia ou nula
    if not arquivo_operacoes: 
        print("Erro: Arquivo de operações não informado. Encerrando.")
        return
    
    arquivos_necessarios = [
        ARQ_GAMES, 
        ARQ_BTREE,
        arquivo_operacoes
    ]
    
    for caminho in arquivos_necessarios:
        if not os.path.exists(caminho):
            print(f"Erro: Arquivo necessário não encontrado ({caminho}). Encerrando.")
            return            
    
    with open(ARQ_GAMES, "rb+") as arqGames:
        with open(ARQ_BTREE, "r+b") as arqBTree:
            with open(arquivo_operacoes, "r", encoding="utf-8") as arqOps:
                buffer = arqOps.readline().strip()
                while buffer:
                    comando = buffer.split(None, 1) 
                    match comando[0]:
                        case 'b':
                            chave = int(comando[1])
                            busca(chave)
                        case 'i':
                            registro = comando[1]
                            insere(registro)

                    buffer = arqOps.readline().strip()
    print(f'As operações do arquivo "{arquivo_operacoes}" foram executadas com sucesso!')
    
def modo_p():
    if not os.path.exists(ARQ_BTREE):
        print("Erro: Arquivo btree.dat não encontrado. Encerrando.")
        return

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
        modo_p()

if __name__ == "__main__":
    main()