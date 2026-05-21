from src.registro import le_registro, lista_de_registros
from src.constantes import FORMATO_TAM
from struct import pack, unpack, calcsize
from src.persistencia import arq_indice_prim
import os

def compactacao():
    if not os.path.exists("data/primario.ind"): #verifica se o arquivo do índice primário existe
        print("primario.ind não encontrado")
        return
    
    reg_validos = []# Carrega os registros válidos (não deletados)
    with open("data/games.dat", "rb") as arq:
        registros = lista_de_registros(arq) #lista de registros, onde cada registro é uma lista com os campos do registro lido do arquivo de dados, e os registros são lidos em ordem de byte_offset
        for reg in registros:
            if not reg[2].startswith('*'):  # Se não for deletado logicamente
                reg_validos.append(reg)
    
    novo_indice_pri = []# Cria novo arquivo com registros válidos E recalcula offsets
    with open("data/games.dat", "wb") as arq_novo:
        for reg in reg_validos: 
            novo_byte_offset = arq_novo.tell() # Captura o byteoffset antes de escrever o reg
            buffer_bytes = (f"{str(reg[1])}|{'|'.join(reg[2:])}|").encode('utf-8') # Converte o registro para bytes, formatando a string do registro e depois codificando para bytes usando utf-8
            arq_novo.write(pack(FORMATO_TAM, len(buffer_bytes))) # Escreve o tamanho do registro em bytes no arquivo de dados, FORMATO_TAM
            arq_novo.write(buffer_bytes) # Escreve o registro como bytes no arquivo de dados, e move o seek para o próximo registro
            
            id_reg = reg[1] # ID do jogo, que é a chave do índice primário
            novo_indice_pri.append([id_reg, novo_byte_offset]) # Adiciona a nova entrada do índice primário, com o ID do jogo e o novo byte_offset do registro no arquivo de dados
    
    
    novo_indice_pri.sort() # Ordena o índice primário por chave(id)
    arq_indice_prim(novo_indice_pri) # Salva o novo índice primário
        
    
