from struct import calcsize

ORDEM = 5

NULO = -1
FORMATO_PAG = f'i{ORDEM - 1}i{ORDEM - 1}i{ORDEM}i'
TAM_PAG = calcsize(FORMATO_PAG)
ARQ_GAMES = 'games.dat'
ARQ_BTREE = 'btree.dat'