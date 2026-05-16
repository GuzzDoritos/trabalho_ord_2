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
        
        atualiza_lst_inv_index_sec(genero, indice_sec_genero, lista_inv, 1)
        atualiza_lst_inv_index_sec(publicadora, index_sec_publicadora, lista_inv, 2)

    return [indice_sec_genero, index_sec_publicadora]

def atualiza_lst_inv_index_sec(chave, index_sec, lst_inv, lst_inv_coluna):
        if chave not in index_sec:
            index_sec[chave] = len(lst_inv) - 1
        else:
            reg = lst_inv[index_sec[chave]]
            while reg[lst_inv_coluna] != -1:
                reg = lst_inv[reg[lst_inv_coluna]]
            reg[lst_inv_coluna] = len(lst_inv) - 1