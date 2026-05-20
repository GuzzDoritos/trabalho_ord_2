from src.registro import le_registro
from src.constantes import FORMATO_TAM
from struct import pack, unpack, calcsize
from src.persistencia import arq_indice_prim
import os

def compactacao():
    reg_validos = []
    with open("data/games.dat", "rb") as arquivo:
        BUFFER = le_registro(arquivo) #buffer é string do reg atual
        while BUFFER:
            if not BUFFER[0] == '*':
                reg_validos.append(BUFFER)
            BUFFER = le_registro(arquivo)

    novo_indice_pri = []
                
    with open("data/games_novo.dat", "wb") as arq:
        for reg in reg_validos:
            novo_byte_offset = arq.tell() #antes de ler
            buffer_bytes = reg.encode('utf-8')
            arq.write(pack(FORMATO_TAM, len(buffer_bytes)))
            arq.write(buffer_bytes)

            #lógica parecida com construir_indice_pri no arquivo indices.py -> vamos atualizar o indice primário (pq removeu logicamente alguns arquivos)
            #id (chave) + referencia (byteoffset)
            id_reg = int(reg.split('|')[0]) #primeiro 
            novo_indice_pri.append([id_reg, novo_byte_offset])

    novo_indice_pri.sort()
    arq_indice_prim(novo_indice_pri)
    
    
