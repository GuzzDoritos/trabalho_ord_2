from src.registro import le_registro

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
    print(f'Busca pelo registro de ID: "{chave}"')

    offset = busca_binaria(chave, indice_pri)

    if offset == -1:
        print("Registro não encontrado")
        return
    
    arquivo.seek(offset) #move o seek para o byte_offset encontrado na binaria
    registro = le_registro(arquivo) #le o registro do byte_offset atual

    if registro.startswith('*'): #remocao logica
        print("Registro não encontrado")
    else:
        print(registro)
    
def busca_sec_genero(chave, indice_sec_genero, lista_inv, arquivo):
    if chave not in indice_sec_genero:
        print("Registro não encontrado")
        return
    
    indice = indice_sec_genero[chave]
    encontrados = []

    while indice != -1: #enquanto tiver um indice válido, aponta para nada (-1)
        offset = lista_inv[indice][0] #pega o byte_offset do registro atual
        arquivo.seek(offset)
        registro = le_registro(arquivo) 

        if not registro.startswith('*'): #se o registro n tiver sido removido logico, add ele na lista de encontrados
            encontrados.append(registro)
        else:
            print("Registro removido")

        indice = lista_inv[indice][1] #pega o próximo indice/reg do mesmo gênero 

    print(f'Busca por registros de gênero "{chave}" ({len(encontrados)} registros)')
    for reg in encontrados:
        print(reg)

def busca_sec_publicadora(chave, indice_sec_publicadora, lista_inv, arquivo):
    if chave not in indice_sec_publicadora:
        print("Registro não encontrado")
        return
    indice = indice_sec_publicadora[chave]
    encontrados = []

    while indice != -1:
        offset = lista_inv[indice][0]
        arquivo.seek(offset)
        registro = le_registro(arquivo)

        if not registro.startswith('*'):
            encontrados.append(registro)
        else:
            print("Registro removido")

        indice = lista_inv[indice][2]

    print(f'Busca por registros de publicadora "{chave}" ({len(encontrados)} registros)')
    for reg in encontrados:
        print(reg)

#================INSERCAO =================

def insercao(chave, num_bytes):
    print(f'Inserção do registro de chave "{chave}" ({num_bytes} bytes)')

#================REMOCAO==================

def remocao(chave, offset):
    print(f'Remoção do registro de chave "{chave}" (offset = {offset})')