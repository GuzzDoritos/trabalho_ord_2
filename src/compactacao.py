from src.registro import le_registro
from src.constantes import *
from struct import pack, unpack, calcsize

def compactacao():
    reg_validos = []
    with open("data/games.dat", "rb") as arquivo:
        BUFFER = le_registro(arquivo) #buffer é string do reg atual
        while BUFFER:
            if not BUFFER[0] == '*':
                reg_validos.append(BUFFER)
            BUFFER = le_registro(arquivo)
                
    with open("data/games_novo.dat", "wb") as arq:
        for i in reg_validos:
            buffer_bytes = i.encode('utf-8')
            arq.write(pack(FORMATO_TAM, len(buffer_bytes)))
            arq.write(buffer_bytes)

'''
## 🗜️ Modo `-c`: Compactação (`src/compactacao.py` e `main.py`) - isa (quinta)
- [x] Chamar a função de compactação na função `modo_c` do `main.py`.
- [x] **Lógica da compactação:**
- [x] Ler o `games.dat` inteiro, pulando os registros que começam com `*`.
- [x] Reescrever o `games.dat` apenas com os registros válidos (removendo os "buracos").
- [ ] Reconstruir a estrutura do `primario.ind` (pegando os novos byte-offsets gerados pela reescrita) e salvar o novo índice no disco.
'''