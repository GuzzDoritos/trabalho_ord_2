from src.constantes import (
    FORMATO_PRI, FORMATO_TAM, FORMATO_IDX,
    FORMATO_INV, SIZEOF_PRI, SIZEOF_TAM, SIZEOF_IDX, SIZEOF_INV
)

from struct import pack, unpack

## ------- ARQUIVO INDICE PRIMARIO -------

def arq_indice_prim(indice_pri):
    if indice_pri is not None:
        _salva_fixo("data/primario.ind", FORMATO_PRI, indice_pri)
    else:
        return _carrega_fixo("data/primario.ind", FORMATO_PRI, SIZEOF_PRI)

## ------- ARQUIVO INDICE LISTA INVERTIDA -------

def arq_indice_listainv(lista_inv):
    if lista_inv is not None:
        _salva_fixo("data/listaInvertida.lst", FORMATO_INV, lista_inv)
    else:
        return _carrega_fixo("data/listaInvertida.lst", FORMATO_INV, SIZEOF_INV)

## ------- ARQUIVO INDICE SECUNDARIO GENERO -------

def arq_indice_genero(indice_sec_genero):
    if indice_sec_genero is not None:
        _salva_variavel("data/genero.ind", indice_sec_genero)
    else:
        return _carrega_variavel("data/genero.ind")

## ------- ARQUIVO INDICE SECUNDARIO PUBLICADORA -------

def arq_indice_publicadora(indice_sec_publicadora):
    if indice_sec_publicadora is not None:
        _salva_variavel("data/publicadora.ind", indice_sec_publicadora)
    else:
        return _carrega_variavel("data/publicadora.ind")

## ------- SALVAMENTO E CARREGAMENTO PARA REGISTROS DE TAMANHO FIXO -------
## (INDICE PRIMARIO E LISTA INVERTIDA)
def _salva_fixo(caminho, formato, registros):
    with open(caminho, "wb") as arq:
        for reg in registros:
            arq.write(pack(formato, *reg))

def _carrega_fixo(caminho, formato, sizeof):
    lista = []
    with open(caminho, "rb") as arq:
        while True:
            dados = arq.read(sizeof)
            if len(dados) < sizeof:
                break
            lista.append(list(unpack(formato, dados)))
    return lista

## ------- SALVAMENTO E CARREGAMENTO PARA REGISTROS DE TAMANHO VARIAVEL -------
## (INDICE SECUNDARIO GENERO E PUBLICADORA)
def _salva_variavel(caminho, dicionario):
    with open(caminho, "wb") as arq:
        for chave, indice in dicionario.items():
            chave_bytes = chave.encode('utf-8')
            arq.write(pack(FORMATO_TAM, len(chave_bytes)))
            arq.write(chave_bytes)
            arq.write(pack(FORMATO_IDX, indice))

def _carrega_variavel(caminho):
    dicionario = {}
    with open(caminho, "rb") as arq:
        while True:
            tam = arq.read(SIZEOF_TAM)
            if len(tam) < SIZEOF_TAM:
                break
            tam = unpack(FORMATO_TAM, tam)[0]
            chave = arq.read(tam).decode('utf-8')
            indice = unpack(FORMATO_IDX, arq.read(SIZEOF_IDX))[0]
            dicionario[chave] = indice
    return dicionario