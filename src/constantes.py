from struct import calcsize

ORDEM = 5

NULO = -1
FORMATO_PAGE = f'i{ORDEM - 1}i{ORDEM - 1}i{ORDEM}i'
TAM_PAGE = calcsize(FORMATO_PAGE)
FORMATO_HEADER = 'i' #cabecalho, vale 4 bytes
TAM_HEADER = calcsize(FORMATO_HEADER)
ARQ_GAMES = 'games.dat'
ARQ_BTREE = 'btree.dat'