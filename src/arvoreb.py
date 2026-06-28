from src.constantes import *
from typing import BinaryIO #tipagem de arquivo tipo dado
from src.pagina import *
from struct import *
import os

def criaArvore(arqGames: BinaryIO, arqBTree: BinaryIO): 
    
    rrn_raiz = NULO # com 0 n vai, da pra tentar com -1
    while True:
        dados = leiaReg(arqGames)
        if dados is None:
            break

        chave, offset = dados #chave_reg e chave -> nomes trocados por causa de leiareg

        rrn_raiz = insereNaArvore(chave, offset, rrn_raiz, arqBTree)
    return rrn_raiz

def leiaReg(arq: BinaryIO):
    offset = arq.tell()
    
    tam_bytes = arq.read(2)
    if not tam_bytes:
        return None
    
    tam = int.from_bytes(tam_bytes, "little")
    registro = arq.read(tam).decode("utf-8")
    
    registro = registro.split('|', 1)
    chave = int(registro[0])

    return chave, offset

#================PÁGINA================

def escrevePagina(rrn, pag, arq):
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

def lePagina(rrn, arq):
    '''
    calcule o byte-offset da página a partir do rrn
    faça seek no arquivo árvore-B para o byte-offset calculado
    leia pag do arquivo árvore-B
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
    
def buscaNaPagina(chave, pag): 
    pos = 0
    while pos < pag.numChaves and chave > pag.chaves[pos]:
        pos += 1
    if pos < pag.numChaves and chave == pag.chaves[pos]:
        return True, pos
    else:
        return False, pos

def novoRRN(arq): 
    arq.seek(0, os.SEEK_END) #seek para o fim do arq #efinir o ponto de referência de onde o cursor de um arquivo será movido, para o 0 (final)
    byte_offset = arq.tell() #recebe offset atual, com o tell
    return ((byte_offset - TAM_HEADER)) // TAM_PAGE

def divide(chave, filhoD, offset, pag: Pagina, arq):
    insereChavePromo(chave, offset, filhoD, pag)
    meio = ORDEM // 2
    pNova = Pagina()
    pNova.chaves = pag.chaves[meio+1:] + [NULO] * meio
    pNova.offsets = pag.offsets[meio+1:] + [NULO] * meio
    pNova.filhos = pag.filhos[meio+1:] + [NULO] * meio
    pNova.numChaves = ORDEM - meio - 1

    chavePro = pag.chaves[meio]
    offsetPro = pag.offsets[meio]
    filhoDpro = novoRRN(arq)
    
    pag.chaves = pag.chaves[:meio] + [NULO] * (ORDEM - meio - 1)
    pag.offsets = pag.offsets[:meio] + [NULO] * (ORDEM - meio - 1)
    pag.filhos = pag.filhos[:meio+1] + [NULO] * (ORDEM - meio - 1)

    pag.numChaves = meio
    return chavePro, offsetPro, filhoDpro, pag, pNova

def insereChavePromo(chave, offset, filhoD, pag): 
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

def buscaNaArvore(chave, rrn, arq): 
    if rrn == NULO:
        return False, NULO, NULO
    else:
        pag = lePagina(rrn, arq) 
        achou, pos = buscaNaPagina(chave, pag) #pos recebe a posição q chave ocorre em pag ou deveria ocorrer se tivesse em pag

        if achou: #True
            return True, rrn, pos
        else:
            return buscaNaArvore(chave, pag.filhos[pos], arq) #recursiva

def insereChave(chave, offset, rrn_atual, arq):
    if rrn_atual == NULO:
        chavePro = chave
        filhoDpro = NULO
        return chavePro, offset, filhoDpro, True
    else:
        pag = lePagina(rrn_atual, arq) 
        achou, pos = buscaNaPagina(chave, pag) 

    if achou: #True
        raise ValueError(f'Erro: chave "{chave}" duplicada')
    
    chavePro, offsetPro, filhoDpro, promo = insereChave(chave, offset, pag.filhos[pos], arq)
    
    if not promo:
        return NULO, NULO, NULO, False
    else:
        if pag.numChaves < ORDEM - 1: #se existe espaço para inserir
            insereChavePromo(chavePro, offsetPro, filhoDpro, pag)
            escrevePagina(rrn_atual, pag, arq)
            return NULO, NULO, NULO, False
        else:
            chavePro, offsetPro, filhoDpro, pag, novaPag = divide(chavePro, filhoDpro, offsetPro, pag, arq) #offsetPro -> divisão em cascata
            escrevePagina(rrn_atual, pag, arq)
            escrevePagina(filhoDpro, novaPag, arq)
            return chavePro, offsetPro, filhoDpro, True


def insereNaArvore(chave, offset, rrn_raiz, arq): 
    chavePro, offsetPro, filhoDpro, promoção = insereChave(chave, offset, rrn_raiz, arq)
    if promoção: #True
        pNova = Pagina() #inicializa nova raiz/pagina
        pNova.chaves[0] = chavePro #nova chave raiz
        pNova.offsets[0] = offsetPro #precisa
        pNova.filhos[0] = rrn_raiz #filho esquerdo é a raiz antiga
        pNova.filhos[1] = filhoDpro #filho direito é a nova página criada

        pNova.numChaves = 1 #TESTE SEM INCREMENTAR
        rrn_nova = novoRRN(arq) #novo RRN para nova raiz
        escrevePagina(rrn_nova, pNova, arq) #escreve nova raiz no arquivo
        return rrn_nova
    return rrn_raiz

#================ÍNDICE================

def criaIndice():
    '''trato os erros aq'''
    try:
        with open(ARQ_GAMES, 'rb') as arqGames:
            with open(ARQ_BTREE, 'w+b') as arqBTree:
                arqBTree.write(pack(FORMATO_HEADER, NULO)) #AQ TBM DA ERRO COM 0
                rrn_raiz = criaArvore(arqGames, arqBTree)

                arqBTree.seek(0)
                arqBTree.write(pack(FORMATO_HEADER, rrn_raiz))
        print("Índice criado com sucesso")
    except FileNotFoundError:
        print(f"Erro: O arquivo {ARQ_GAMES} não pôde ser encontrado.")

#================OPERAÇÕES================

def busca(chave, arqBTree, arqGames): 
    '''realiza a busca no arquivo btree.dat, pego o byte-offset do reg correspondente e acesso de forma direta no games.dat'''
    try:
        print(f'Busca pelo registro de chave "{chave}"')
        arqBTree.seek(0)
        rrn_raiz = unpack(FORMATO_HEADER, arqBTree.read(TAM_HEADER))[0]
        achou, rrn, pos = buscaNaArvore(chave, rrn_raiz, arqBTree) #true, rrn, pos 
        
        if achou:
            pag = lePagina(rrn, arqBTree)
            offset = pag.offsets[pos]
            arqGames.seek(offset)

            tam = int.from_bytes(arqGames.read(2),"little")
            reg = arqGames.read(tam).decode("utf-8")

            print(f'{reg} ({tam} bytes - offset {offset})\n')
        else:
            print(f'Erro: chave "{chave}" não encontrada\n')

    except Exception as e:
        print(f"Erro na busca: {e}")

def insere(registro, arqBTree, arqGames):
    try:
        campos = registro.split('|', 1)
        chave = int(campos[0])
        
        # verifica se a chave já existe
        arqBTree.seek(0)
        rrn_raiz = unpack(FORMATO_HEADER, arqBTree.read(TAM_HEADER))[0]
        achou, _, _ = buscaNaArvore(chave, rrn_raiz, arqBTree)
        
        if achou:
            print(f'Erro: chave "{chave}" duplicada\n')
            return
            
        # escreve no final do games.dat
        arqGames.seek(0, os.SEEK_END)
        offset = arqGames.tell()
        
        reg_bytes = registro.encode("utf-8")
        tam = len(reg_bytes)
        arqGames.write(tam.to_bytes(2, "little"))
        arqGames.write(reg_bytes)
        
        # insere na árvore B
        novo_rrn_raiz = insereNaArvore(chave, offset, rrn_raiz, arqBTree)
        
        # atualiza cabeçalho se a raiz mudou
        if novo_rrn_raiz != rrn_raiz:
            arqBTree.seek(0)
            arqBTree.write(pack(FORMATO_HEADER, novo_rrn_raiz))
            
        print(f'Inserção do registro de chave "{chave}"')
        print(f'{registro} ({tam} bytes - offset {offset})\n')

    except Exception as e:
        print(f"Erro na inserção: {e}")

#================IMPRIMIR================

def imprimirArvoreB(arq_btree):
    try:
        with open(arq_btree, 'rb') as arqBTree:
            arqBTree.seek(0, os.SEEK_END)
            tam_arquivo = arqBTree.tell()
            
            if tam_arquivo < TAM_HEADER:
                return
                
            arqBTree.seek(0)
            rrn_raiz = unpack(FORMATO_HEADER, arqBTree.read(TAM_HEADER))[0]
            
            total_paginas = (tam_arquivo - TAM_HEADER) // TAM_PAGE
            
            for rrn in range(total_paginas):
                if rrn == rrn_raiz:
                    print('- - - - - - - - - - Raiz - - - - - - - - - -')
                    
                pag = lePagina(rrn, arqBTree)
                print(f'Página {rrn}:')
                
                str_chaves = " | ".join(str(c) for c in pag.chaves)
                str_offsets = " | ".join(str(o) for o in pag.offsets)
                str_filhos = " | ".join(str(f) for f in pag.filhos)
                
                print(f'Chaves = {str_chaves}')
                print(f'Offsets = {str_offsets}')
                print(f'Filhos = {str_filhos}')
                
                if rrn == rrn_raiz:
                    print('- - - - - - - - - - - - - - - - -- - - - - -')
                else:
                    print()
    except Exception as e:
        print(f"Erro ao imprimir árvore: {e}")