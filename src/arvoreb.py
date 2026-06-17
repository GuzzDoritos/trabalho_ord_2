from src.constantes import *
from typing import BinaryIO
from src.pagina import *
from struct import *
import os

def criaArvore(arq: BinaryIO): #gu
def leiaReg(arq: BinaryIO): #gu

#================PÁGINA================

def escrevePagina(rrn, pag, arq): #isa
    byte_offset = rrn * TAM_PAGE + TAM_HEADER #formula da prof
    arq.seek(byte_offset)
    #paginas.py, constroi os campos da pagina na ordem (vai incrementando)
    dados = []
    dados.append(pag.numChaves)
    dados.extend(pag.chaves)
    dados.extend(pag.offsets)
    dados.extend(pag.filhos)

    dados_bytes = pack(FORMATO_PAGE, *dados) #o * são varios argumentos separados
    arq.write(dados_bytes)

def lePagina(rrn, arq): #isa
    '''
    calcule o byte-offset da página a partir do rrn
    faça seek no arquivo árvore-B para o byte-offset calculado
    escreva pag no arquivo árvore-B
    '''
    byte_offset = rrn * TAM_PAGE + TAM_HEADER #formula da prof
    arq.seek(byte_offset)

    dados_bytes = arq.read(TAM_PAGE)
    dados = unpack(FORMATO_PAGE, dados_bytes)

    pag = Pagina() #cria objeto
    indice = 0
    pag.numChaves = dados[indice]

    indice += 1
    pag.chaves = list(dados[indice:indice + ORDEM - 1])

    indice += ORDEM - 1
    pag.offsets = list(dados[indice:indice + ORDEM - 1])

    indice += ORDEM - 1
    pag.filhos = list(dados[indice:indice + ORDEM])

    return pag
    
def buscaNaPagina(chave, pag): #isa
    pos = 0
    while pos < pag.numChaves and chave > pag.chaves[pos]:
        pos += 1
    if pos < pag.numChaves and chave == pag.chaves[pos]:
        return True, pos
    else:
        return False, pos

def novoRRN(arq): #isa
    arq.seek(0, os.SEEK_END) #seek para o fim do arq #efinir o ponto de referência de onde o cursor de um arquivo será movido, para o 0 (final)
    byte_offset = arq.tell() #recebe offset atual, com o tell
    return ((byte_offset - TAM_HEADER)) // TAM_PAGE

def divide(chave, filhoD, pag, arq): #gu
    pass

def insereChavePromo(chave, offset, filhoD, pag): #isa 
    #insere na pagina
    if pag.numChaves == ORDEM - 1: #estourou, ta cheia
        pag.chaves.append(NULO)
        pag.offsets.append(NULO)
        pag.filhos.append(NULO)

    i = pag.numChaves

    while i > 0 and chave < pag.chaves[i - 1]:
        pag.chaves[i] = pag.chaves[i - 1]
        pag.offsets[i] = pag.offsets[i - 1]
        pag.filhos[i + 1] = pag.filhos[i]
        i -= 1

    pag.chaves[i] = chave
    pag.offsets[i] = offset
    pag.filhos[i + 1] = filhoD
    pag.numChaves += 1

#================ÁRVORE================

def buscaNaArvore(chave, rrn, arq): #isa
    if rrn == NULO:
        return False, NULO, NULO
    else:
        pag = lePagina(rrn, arq) 
        achou, pos = buscaNaPagina(chave, pag) #pos recebe a posição q chave ocorre em pag ou deveria ocorrer se tivesse em pag

        if achou: #True
            return True, rrn, pos
        else:
            return buscaNaArvore(chave, pag.filhos[pos], arq) #recursiva

def insereChave(chave, rrn_atual, arq): #isa
    if rrn_atual == NULO:
        chavePro = chave
        filhoDpro = NULO
        return chavePro, filhoDpro, True
    else:
        pag = lePagina(rrn_atual, arq) 
        achou, pos = buscaNaPagina(chave, pag) 

    if achou: #True
        raise ValueError("Chave duplicada")
    
    chavePro, filhoDpro, promo = insereChave(chave, pag.filhos[pos], arq)
    
    if not promo:
        return NULO, NULO, False
    else:
        if pag.numChaves < ORDEM - 1: #se existe espaço para inserir
            insereChavePromo(chave, filhoDpro, pag)
            escrevePagina(rrn_atual, pag, arq)
            return NULO, NULO, False
        else:
            chavePro, filhoDpro, pag, novaPag = divide(chavePro, filhoDpro, pag, arq)
            escrevePagina(rrn_atual, pag, arq)
            escrevePagina(filhoDpro, novaPag, arq)
            return chavePro, filhoDpro, True


def insereNaArvore(chave, offset, rrn_atual, arq): #gu
    pass

#================ÍNDICE================

def criaIndice():
    pass

#================OPERAÇÕES================

def busca(chave):
    pass

def insere():
    pass

#================ÁRVORE================

def imprimirArvoreB(arq_btree):
    pass