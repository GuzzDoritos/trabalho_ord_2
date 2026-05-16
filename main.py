import os
import re
from rich import print
from sys import argv
from src.registro import lista_de_registros
from src.indices import construir_indice_pri, construir_indice_sec
from src.persistencia import (
    arq_indice_prim, arq_indice_genero,
    arq_indice_publicadora, arq_indice_listainv
)
from src.operacoes import *
from src.compactacao import compactacao


from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.theme import Theme

class Highlighter(RegexHighlighter):

    base_style = "theme."
    highlights = [r"(?P<pipe>[|])", r"(?P<text>[\w])"]

theme = Theme({"theme.pipe": "dark_red", "theme.text": "light_steel_blue1"})
print_reg = Console(highlighter=Highlighter(), theme=theme)


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
    with open("data/games.dat", "rb+") as arq_games:
        with open(arquivo_operacoes, "r", encoding="utf-8") as arq_ops:
            buffer = arq_ops.readline().strip()
            while buffer:
                comando = buffer.split(None, 1)
                buffer = arq_ops.readline().strip()
                match comando[0]:
                    case 'bp':
                        print(f'[thistle1]Busca pelo registro de ID[/] [thistle1]"[cornsilk1]{int(comando[1])}[/][thistle1]"[/][/]')
                        resultado = busca_pri(int(comando[1]), indice_pri, arq_games)
                        if resultado:
                            print_reg.print(re.sub(rf"({comando[1]})", f"[cornsilk1]{comando[1]}[/]", resultado))
                        else:
                            print("Registro não encontrado!")
                        print('\n')
                    case 'bs1' | 'bs2':
                        chave = comando[1]
                        if comando[0] == 'bs1':
                            encontrados = busca_sec_genero(chave, indice_sec_genero, indice_pri, lista_inv, arq_games)
                            pesquisa = 'gênero'
                        elif comando[0] == 'bs2':
                            encontrados = busca_sec_publicadora(chave, indice_sec_publicadora, indice_pri, lista_inv, arq_games)
                            pesquisa = 'publicadora'
                        print(f'[thistle1]Busca por registros de {pesquisa} "[/][cornsilk1]{chave}[/][thistle1]"[/] [grey82]({len(encontrados)} registros)[/]')
                        for reg in encontrados:
                            print_reg.print(re.sub(rf"({chave})", f"[cornsilk1]{chave}[/]", reg))
                        print('\n')
                    case 'i':
                        chave = comando[1].split("|")[0]
                        num_bytes = len(comando[1].encode("utf-8"))

                        print(f'[thistle1]Inserção do registro de chave "[/][cornsilk1]{chave}[/][thistle1]"[/] [grey82]({num_bytes} bytes)[/]')
                        retorno = insercao(comando[1], indice_pri, indice_sec_genero, indice_sec_publicadora, lista_inv, arq_games)

                        if not retorno:
                            print("[red]Elemento de mesma chave já existe.[/]")
                        else:
                            print("[light_green]Inserido com sucesso.[/]")
                        print('\n')
                    case 'r':
                        # print('remoção', ' '.join(comando[1:]))
                        # print('\n')
                        pass
                arq_indice_prim(indice_pri)
                arq_indice_genero(indice_sec_genero)
                arq_indice_publicadora(indice_sec_publicadora)
                arq_indice_listainv(lista_inv)


def modo_c(): # Modo de compactação do arquivo
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