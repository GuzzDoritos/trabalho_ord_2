from sys import argv, os
from src.arvoreb import *

ARQUIVO_DADOS = "data/games.dat"

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
    
    with open(ARQUIVO_DADOS, "rb+") as arq_games:
        with open(arquivo_operacoes, "r", encoding="utf-8") as arq_ops:
            buffer = arq_ops.readline().strip()
            while buffer:
                comando = buffer.split(None, 1)
                buffer = arq_ops.readline().strip() 
                match comando[0]:
                    case 'b':
                        pass
                    case 'i':
                        pass

def main():
    if argv[1] == '-b':
        try:
            with open(ARQUIVO_DADOS, "rb", encoding='utf-8') as arq:
                cria_arvore(arq)
        except FileNotFoundError:
            print("Erro: O arquivo games.dat não pôde ser encontrado na pasta \"/data/\".")

    elif argv[1] == '-e':
        modo_e(argv[2])
    elif argv[1] == '-p':
        imprimir_arvoreb()

if __name__ == "__main__":
    main()