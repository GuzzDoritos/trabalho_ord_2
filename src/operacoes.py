from src.registro import le_registro
from struct import pack, unpack
from src.constantes import FORMATO_TAM
from src.indices import atualiza_lst_inv_index_sec

#================== BUSCA ======================

def busca_binaria(chave, indice_pri): #código dos slides, alterado algumas coisas
    esq, dir = 0, len(indice_pri) - 1 #bb na lista indice_pri (ordenada por id)
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
    return -1 #retorna o byte_offset do registro se encontrar, ou -1 se não encontrar

def busca_pri(chave, indice_pri, arquivo): #DÚVIDA

    offset = busca_binaria(chave, indice_pri) #busca o byte_offset do registro no arquivo de dados usando a busca binária 

    if offset == -1:
        return "" #se o byte_offset for -1 (bb não encontrar o ID do jogo no índice primário,)
    
    arquivo.seek(offset) #move o seek para o byte_offset encontrado na binaria
    registro = le_registro(arquivo) #le o registro do byte_offset atual

    if registro.startswith('*'): #verifica se começa com * (removido logicamente)
        return ""
    else:
        return registro #retorna string do reg encontrado 
    
def busca_sec_genero(chave, indice_sec_genero, indice_pri, lista_inv, arquivo):
    encontrados = []
    
    if chave in indice_sec_genero: # só faz a busca se a chave existir
        indice = indice_sec_genero[chave]

        while indice != -1: #enquanto tiver um indice válido, aponta para nada (-1)
            chave_pri = lista_inv[indice][0] 
            offset = busca_binaria(chave_pri, indice_pri)#pega o byte_offset do registro atual
            arquivo.seek(offset) #move o seek para o byte_offset encontrado na binaria
            registro = le_registro(arquivo) #le o registro do byte_offset atual

            if not registro.startswith('*'): #se o registro n tiver sido removido logico, add ele na lista de encontrados
                encontrados.append(registro)

            indice = lista_inv[indice][1] #pega o próximo indice/reg do mesmo gênero 

    encontrados.sort() #ordena a lista de encontrados em ordem alfabética
    return encontrados

def busca_sec_publicadora(chave, indice_sec_publicadora, indice_pri, lista_inv, arquivo): #msm lógica do busca_sec_genero, mudando o [2]
    encontrados = []

    if chave  in indice_sec_publicadora:
        indice = indice_sec_publicadora[chave]

        while indice != -1:
            chave_pri = lista_inv[indice][0] #pega o byte_offset do registro atual
            offset = busca_binaria(chave_pri, indice_pri)
            arquivo.seek(offset)
            registro = le_registro(arquivo)

            if not registro.startswith('*'):
                encontrados.append(registro)

            indice = lista_inv[indice][2]
    
    encontrados.sort()
    return encontrados

#================INSERCAO =================

def insercao(registro: str, indice_pri: list[list], indice_sec_genero, indice_sec_publicadora, lista_inv: list, arq_games, num_bytes):
    chave = int(registro.split("|")[0])
    registro_ja_existe = busca_pri(chave, indice_pri, arq_games) 
    if (registro_ja_existe):
        return False
    arq_games.seek(0, 2) #move o seek para o final do arquivo de dados, para escrever o novo registro no final do arquivo
    byte_offset = arq_games.tell() #pega o byte_offset do final do arquivo, onde o novo registro vai ser escrito

    arq_games.write(pack(FORMATO_TAM, num_bytes)) #escreve o tamanho do registro em bytes (num_bytes) no arquivo de dados, usando o formato definido por FORMATO_TAM, e move o seek para o próximo campo do registro
    arq_games.write(registro.encode("utf-8")) #escreve o registro como bytes no arquivo de dados, usando a codificação utf-8, e move o seek para o próximo registro

    indice_pri.append([chave, byte_offset]) 
    indice_pri.sort()

    genero = registro.split("|")[3]
    publicadora = registro.split("|")[4]

    lista_inv.append([chave, -1, -1])

    atualiza_lst_inv_index_sec(genero, indice_sec_genero, lista_inv, 1)
    atualiza_lst_inv_index_sec(publicadora, indice_sec_publicadora, lista_inv, 2)

    return True

#================REMOCAO==================

def remocao(chave: int, offset: int, indice_pri: list[list], indice_sec_genero, indice_sec_publicadora, lista_inv: list, arq_games):
    arq_games.seek(offset) #move o seek para o byte_offset do registro a ser removido, para ler o registro e marcar ele como removido logicamente (* no início do registro)
    tam = int.from_bytes(arq_games.read(2), 'little') #lê os 2 bytes do tamanho do registro e move o seek para o próximo campo do registro, e armazena o tamanho do registro em tam
    arq_games.write(b"*") #escreve o byte b"*" no início do registro para marcar ele como removido logicamente, e move o seek para o próximo campo do registro
    registro = arq_games.read(tam - 1).decode("utf-8").split("|")
    indice_pri.remove([chave, offset]) #remove a entrada do índice primário que tem o ID do jogo e o byte_offset do registro removido

    genero = registro[3]
    publicadora = registro[4]
    
    compacta_lista_inv(genero, chave, indice_sec_genero, lista_inv, 1)
    
    compacta_lista_inv(publicadora, chave, indice_sec_publicadora, lista_inv, 2)


def compacta_lista_inv(chave_sec, chave_pri, index_sec, lst_inv, lst_inv_coluna):
    reg_anterior = None
    reg = lst_inv[index_sec[chave_sec]]
    while reg[0] != chave_pri and reg[lst_inv_coluna] != -1:
        reg_anterior = reg
        reg = lst_inv[reg[lst_inv_coluna]]

    if reg_anterior is None:
        index_sec[chave_sec] = reg[lst_inv_coluna]
    else:
        reg_anterior[lst_inv_coluna] = reg[lst_inv_coluna]