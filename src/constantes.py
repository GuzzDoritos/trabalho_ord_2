ARQUIVO = "data/games.dat"

#CONSTANTES
FORMATO_PRI = "iq"  #2 inteiros de 4 bytes e 8 bytes # i = 4 bytes, q = 8 bytes
FORMATO_TAM = 'h'   # 2 bytes 
FORMATO_IDX = 'i'   # 4 bytes 
FORMATO_INV = 'qii' #3 inteiros de 8bytes e 4 bytes e 4 bytes # q = 8 bytes, i = 4 bytes

SIZEOF_PRI = calcsize(FORMATO_PRI)
SIZEOF_TAM = calcsize(FORMATO_TAM)
SIZEOF_INV = calcsize(FORMATO_INV)