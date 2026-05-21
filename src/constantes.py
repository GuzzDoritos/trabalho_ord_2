from struct import calcsize

ARQUIVO = "data/games.dat"

#basicamente, usamos o Struct para ler e escrever os dados binários, e o formato é definido por uma string que indica o tipo e o tamanho dos dados (jeito mais saudavel de fazer)
#CONSTANTES -> usamos em operacoes.py e persistencia.py
FORMATO_PRI = "iq"  #2 inteiros de 4 bytes e 8 bytes # i = 4 bytes, q = 8 bytes
FORMATO_TAM = 'h'   # 2 bytes #exemplo do tamanho
FORMATO_IDX = 'i'   # 4 bytes #exemplo do ID
FORMATO_INV = 'qii' #3 inteiros de 8bytes e 4 bytes e 4 bytes # q = 8 bytes, i = 4 bytes
#as strings "i", "q" e "h" são padronização do módulo

SIZEOF_PRI = calcsize(FORMATO_PRI)
SIZEOF_TAM = calcsize(FORMATO_TAM)
SIZEOF_INV = calcsize(FORMATO_INV)
SIZEOF_IDX = calcsize(FORMATO_IDX)
#calcsize = tamanho em bytes de uma estrutura 