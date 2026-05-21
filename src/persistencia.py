from src.constantes import (
    FORMATO_PRI, FORMATO_TAM, FORMATO_IDX,
    FORMATO_INV, SIZEOF_PRI, SIZEOF_TAM, SIZEOF_IDX, SIZEOF_INV
)

from struct import pack, unpack

## ------- ARQUIVO INDICE PRIMARIO -------

def arq_indice_prim(indice_pri):
    if indice_pri is not None: #salva -> índice primário do arquivo 
        _salva_fixo("data/primario.ind", FORMATO_PRI, indice_pri)
    else: #carrega -> índice primário do arquivo
        return _carrega_fixo("data/primario.ind", FORMATO_PRI, SIZEOF_PRI)

## ------- ARQUIVO INDICE LISTA INVERTIDA -------

def arq_indice_listainv(lista_inv):
    if lista_inv is not None: #salva -> lista invertida do arquivo
        _salva_fixo("data/listaInvertida.lst", FORMATO_INV, lista_inv)
    else: #carrega -> lista invertida do arquivo
        return _carrega_fixo("data/listaInvertida.lst", FORMATO_INV, SIZEOF_INV)

## ------- ARQUIVO INDICE SECUNDARIO GENERO -------

def arq_indice_genero(indice_sec_genero):
    if indice_sec_genero is not None: #salva -> índice secundário de gênero do arquivo
        _salva_variavel("data/genero.ind", indice_sec_genero)
    else: #carrega -> índice secundário de gênero do arquivo
        return _carrega_variavel("data/genero.ind")

## ------- ARQUIVO INDICE SECUNDARIO PUBLICADORA -------

def arq_indice_publicadora(indice_sec_publicadora):
    if indice_sec_publicadora is not None: #salva -> índice secundário de publicadora do arquivo
        _salva_variavel("data/publicadora.ind", indice_sec_publicadora)
    else: #carrega -> índice secundário de publicadora do arquivo
        return _carrega_variavel("data/publicadora.ind")

## ------- SALVAMENTO E CARREGAMENTO PARA REGISTROS DE TAMANHO FIXO -------
## (INDICE PRIMARIO E LISTA INVERTIDA)
def _salva_fixo(caminho, formato, registros): #escreve cada entrada como bytes empacotados
    with open(caminho, "wb") as arq: 
        for reg in registros:
            arq.write(pack(formato, *reg)) #pack = converte os dados para bytes e escreve no arquivo, o *reg é para passar cada elemento da lista como um argumento separado para o pack

def _carrega_fixo(caminho, formato, sizeof): #lê blocos de tamanho fixo (SIZEOF_PRI ou SIZEOF_INV) em loop
    lista = [] #lista de listas, onde cada lista tem os campos do registro lido do arquivo de índices
    with open(caminho, "rb") as arq:
        while True:
            dados = arq.read(sizeof) #lê os bytes do arquivo de índices, o sizeof é o tamanho em bytes de cada registro
            if len(dados) < sizeof: #EOF
                break
            lista.append(list(unpack(formato, dados))) #unpack = converte os bytes lidos do arquivo de índices para os definidos no formato, e add a lista de listas, onde cada lista tem os campos do registro lido do arquivo de índices
    return lista

## ------- SALVAMENTO E CARREGAMENTO PARA REGISTROS DE TAMANHO VARIAVEL -------
## (INDICE SECUNDARIO GENERO E PUBLICADORA)
def _salva_variavel(caminho, dicionario):
    with open(caminho, "wb") as arq:
        for chave, indice in dicionario.items(): #para cada chave e índice do dicionário, escreve a chave como bytes empacotados, o tamanho da chave em bytes e o índice como bytes empacotados no arquivo de índices secundários
            chave_bytes = chave.encode('utf-8') #encode = converte a string da chave para bytes, e armazena em chave_bytes
            arq.write(pack(FORMATO_TAM, len(chave_bytes))) #pack do tamanho da chave em bytes (o número de bytes que a chave ocupa no arquivo de índices secundários) e escreve no arquivo de índices secundários
            arq.write(chave_bytes) #escreve a chave como bytes no arquivo de índices secundários
            arq.write(pack(FORMATO_IDX, indice)) #pack do índice como bytes (o número de bytes que o índice ocupa no arquivo de índices secundários) e escreve no arquivo de índices secundários

def _carrega_variavel(caminho):
    dicionario = {}
    with open(caminho, "rb") as arq:
        while True:
            tam = arq.read(SIZEOF_TAM) #lê os bytes do tamanho da chave, o SIZEOF_TAM é o número de bytes que o tamanho da chave ocupa no arquivo de índices secundários
            if len(tam) < SIZEOF_TAM: #EOF
                break
            tam = unpack(FORMATO_TAM, tam)[0] #unpack do tamanho da chave lida do arquivo de índices secundários para o formato definido por FORMATO_TAM, e armazena o valor do tamanho da chave em tam
            chave = arq.read(tam).decode('utf-8') #lê os bytes da chave do arquivo de índices secundários, o número de bytes lidos é o valor do tamanho da chave (tam), e decodifica os bytes lidos para string, e armazena em chave
            indice = unpack(FORMATO_IDX, arq.read(SIZEOF_IDX))[0] #unpack do índice lido do arquivo de índices secundários para o formato definido por FORMATO_IDX, e armazena o valor do índice em indice
            dicionario[chave] = indice # adiciona a chave e o índice ao diciionário
    return dicionario