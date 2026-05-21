from src.registro import le_registro, lista_de_registros
from src.constantes import FORMATO_TAM
from struct import pack, unpack, calcsize
from src.persistencia import arq_indice_prim
import os

def compactacao():
    """
    Compacta o arquivo de dados removendo registros marcados como deletados.
    Recalcula e atualiza o índice primário CASO EXISTA.
    """
    # Verifica se o índice primário existe
    if not os.path.exists("data/primario.ind"):
        print("primario.ind não encontrado")
        return
    
    # Carrega os registros válidos (não deletados)
    reg_validos = []
    with open("data/games.dat", "rb") as arq:
        registros = lista_de_registros(arq)
        for reg in registros:
            if not reg[2].startswith('*'):  # Se não for deletado logicamente
                reg_validos.append(reg)
    
    # Cria novo arquivo com registros válidos E recalcula offsets
    novo_indice_pri = []
    
    with open("data/games_novo.dat", "wb") as arq_novo:
        for reg in reg_validos:
            novo_byte_offset = arq_novo.tell() # Captura o byteoffset antes de escrever o reg
            buffer_bytes = (str(reg[1]) + reg[2]).encode('utf-8')
            arq_novo.write(pack(FORMATO_TAM, len(buffer_bytes)))
            arq_novo.write(buffer_bytes)
            
            id_reg = reg[1]
            novo_indice_pri.append([id_reg, novo_byte_offset])
    
    
    novo_indice_pri.sort() # Ordena o índice primário por chave(id)
    arq_indice_prim(novo_indice_pri) # Salva o novo índice primário
        
    
