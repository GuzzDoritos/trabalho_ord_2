from src.constantes import FORMATO_PRI, 
                           FORMATO_TAM, 
                           FORMATO_IDX, 
                           FORMATO_INV, 
                           SIZEOF_PRI,
                           SIZEOF_TAM,
                           SIZEOF_INV

from struct import pack, unpack, calcsize

def arq_indice_prim(indice_pri): #msm lógica do arq_indice_listainv
    #12 bytes por entrada: 4 (id) + 8 (offset)
    ##id (chave) + referencia (byteoffset) = indice_pri
    if indice_pri is not None:  # salva
        arq = open("primario.ind", "wb")
        for id, offset in indice_pri:
            arq.write(pack(FORMATO_PRI, int(id), offset))
    else:  # carrega
        indice_pri = []
        arq = open("primario.ind", 'rb')
        while True:
            dados = arq.read(SIZEOF_PRI)
            if len(dados) < SIZEOF_PRI:
                break
            id, offset = unpack(FORMATO_PRI, dados)
            indice_pri.append([str(id), offset])
        return indice_pri

def arq_indice_genero(indice_sec_genero):
    #2 bytes (tamanho) + N bytes (gênero) + 4 bytes (índice)
    if indice_sec_genero is not None:  # salva
        arq = open("genero.ind", "wb")
        for genero, indice in indice_sec_genero.items():
            genero_bytes = genero.encode('utf-8') #string para bytes
            arq.write(pack(FORMATO_TAM, len(genero_bytes)))# tamanho do gênero
            arq.write(genero_bytes)# gênero
            arq.write(pack(FORMATO_IDX, indice))# indice na lista inv
    else:  # carrega
        indice_sec_genero = {}
        arq = open("genero.ind", "rb")
        while True:
            tam = arq.read(SIZEOF_TAM)
            if len(tam) < SIZEOF_TAM:
                break
            tam = unpack(FORMATO_TAM, tam)[0]
            genero = arq.read(tam).decode('utf-8') #bytes para string
            indice = unpack(FORMATO_IDX, arq.read(4))[0]
            indice_sec_genero[genero] = indice
        return indice_sec_genero

def arq_indice_publicadora(indice_sec_publicadora):
    #2 bytes (tamanho) + N bytes (publicadora) + 4 bytes (índice)
    if indice_sec_publicadora is not None:  # salva
        arq = open("publicadora.ind", "wb")
        for publicadora, indice in indice_sec_publicadora.items():
            publicadora_bytes = publicadora.encode('utf-8') #string para bytes
            arq.write(pack(FORMATO_TAM, len(publicadora_bytes)))# tamanho da publicadora
            arq.write(publicadora_bytes)# publicadora
            arq.write(pack(FORMATO_IDX, indice))# indice na lista inv
    else:  # carrega
        indice_sec_publicadora = {}
        arq = open("publicadora.ind", "rb")
        while True:
            tam = arq.read(SIZEOF_TAM)
            if len(tam) < SIZEOF_TAM:
                break
            tam = unpack(FORMATO_TAM, tam)[0]
            publicadora = arq.read(tam).decode('utf-8') #bytes para string
            indice = unpack(FORMATO_IDX, arq.read(4))[0]
            indice_sec_publicadora[publicadora] = indice
        return indice_sec_publicadora

def arq_indice_listainv(lista_inv): #msm lógica do arq_indice_prim
    ## 8 bytes (offset) + 4 bytes (prox_genero) + 4 bytes (prox_publicadora) = 16 bytes
    ##[byte_offset, prox_genero, prox_publicadora] = lista_inv
    if lista_inv is not None:  # salva
        arq = open("listaInvertida.lst", "wb")
        for offset, prox_genero, prox_publicadora in lista_inv:
            arq.write(pack(FORMATO_INV, offset, prox_genero, prox_publicadora))
    else:  # carrega
        lista_inv = []
        arq = open("listaInvertida.lst", 'rb')
        while True:
            dados = arq.read(SIZEOF_INV)
            if len(dados) < SIZEOF_INV:
                break
            offset, prox_genero, prox_publicadora = unpack(FORMATO_INV, dados)
            lista_inv.append([offset, prox_genero, prox_publicadora])
        return lista_inv