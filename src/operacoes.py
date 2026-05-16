from src.registro import le_registro
from struct import pack, unpack
from src.constantes import FORMATO_TAM
from src.indices import atualiza_lst_inv_index_sec

#================== BUSCA ======================

def busca_binaria(chave, indice_pri): #código da valéria
    esq, dir = 0, len(indice_pri) - 1
    chave = int(chave)
    
    while esq <= dir:
        meio = (esq + dir) // 2
        id_meio = int(indice_pri[meio][0])
        if id_meio == chave:
            return indice_pri[meio][1]
        elif id_meio < chave:
            esq = meio + 1
        else:
            dir = meio - 1
    return -1

def busca_pri(chave, indice_pri, arquivo): #DÚVIDA

    offset = busca_binaria(chave, indice_pri)

    if offset == -1:
        return ""
    
    arquivo.seek(offset) #move o seek para o byte_offset encontrado na binaria
    registro = le_registro(arquivo) #le o registro do byte_offset atual

    if registro.startswith('*'): #remocao logica
        return ""
    else:
        return registro
    
def busca_sec_genero(chave, indice_sec_genero, indice_pri, lista_inv, arquivo):
    encontrados = []
    
    if chave in indice_sec_genero: # só faz a busca se a chave existir
        indice = indice_sec_genero[chave]

        while indice != -1: #enquanto tiver um indice válido, aponta para nada (-1)
            chave_pri = lista_inv[indice][0] #pega o byte_offset do registro atual
            offset = busca_binaria(chave_pri, indice_pri)
            arquivo.seek(offset)
            registro = le_registro(arquivo) 

            if not registro.startswith('*'): #se o registro n tiver sido removido logico, add ele na lista de encontrados
                encontrados.append(registro)

            indice = lista_inv[indice][1] #pega o próximo indice/reg do mesmo gênero 

    return encontrados

def busca_sec_publicadora(chave, indice_sec_publicadora, indice_pri, lista_inv, arquivo):
    encontrados = []

    if chave  in indice_sec_publicadora:
        indice = indice_sec_publicadora[chave]

        while indice != -1:
            offset = lista_inv[indice][0]
            arquivo.seek(offset)
            registro = le_registro(arquivo)

            if not registro.startswith('*'):
                encontrados.append(registro)

            indice = lista_inv[indice][2]

    return encontrados

#================INSERCAO =================

def insercao(registro: str, indice_pri: list[list], indice_sec_genero, indice_sec_publicadora, lista_inv: list, arq_games):
    chave = int(registro.split("|")[0])
    registro_ja_existe = busca_pri(chave, indice_pri, arq_games)
    if (registro_ja_existe):
        return False
    tam_reg = len(registro)
    arq_games.seek(0, 2)
    byte_offset = arq_games.tell()

    arq_games.write(pack(FORMATO_TAM, tam_reg))
    arq_games.write(registro.encode("utf-8"))

    indice_pri.append([chave, byte_offset])
    indice_pri.sort()

    genero = registro.split("|")[3]
    publicadora = registro.split("|")[4]

    lista_inv.append([byte_offset, -1, -1])

    atualiza_lst_inv_index_sec(genero, indice_sec_genero, lista_inv, 1)
    atualiza_lst_inv_index_sec(publicadora, indice_sec_publicadora, lista_inv, 2)

    return True
    



#================REMOCAO==================

def remocao(registro: str, indice_pri: list[list], indice_sec_genero, indice_sec_publicadora, lista_inv: list, arq_games):
    # print(f'Remoção do registro de chave "{chave}" (offset = {offset})')
    pass