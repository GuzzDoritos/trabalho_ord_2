def construir_indice_pri(registros):
    #id (chave) + referencia (byteoffset)
    indice_pri = []

    for reg in registros:
        indice_pri.append([reg[1], reg[0]])

    indice_pri.sort()
    return indice_pri

def construir_indice_sec(registros, lista_inv):
    indice_sec_genero = {}
    index_sec_publicadora = {}

    for i in range(len(registros)):
        genero = registros[i][4]
        publicadora = registros[i][5]
        lista_inv.append([registros[i][0], -1, -1])  # registros[i][0] é o byte_offset 

        if genero not in indice_sec_genero:
            indice_sec_genero[genero] = len(lista_inv) - 1
        else:
            reg = lista_inv[indice_sec_genero[genero]]
            while reg[1] != -1:
                reg = lista_inv[reg[1]]
            reg[1] = len(lista_inv) - 1
        

        if publicadora not in index_sec_publicadora:
            index_sec_publicadora[publicadora] = len(lista_inv) - 1
        else:
            reg = lista_inv[index_sec_publicadora[publicadora]]
            while reg[2] != -1:
                reg = lista_inv[reg[2]]
            reg[2] = len(lista_inv) - 1

    return [indice_sec_genero, index_sec_publicadora]