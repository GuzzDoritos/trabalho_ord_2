# Análise de Pendências e Erros

## 1. Funções não implementadas — nota zero nessas partes

| Função | Problema | Arquivo |
|---|---|---|
| `criaArvore(arq)` | Núcleo do modo `-b`: lê o `games.dat` e insere todos os registros na árvore-B. Sem isso nada funciona. | `arvoreb.py` — linha 92 |
| `leiaReg(arq)` | Deve ler um registro do `games.dat` e retornar a chave (ID) e o byte-offset capturado antes da leitura. | `arvoreb.py` — linha 95 |
| `divide(chave, filhoD, pag, arq)` | Sem a divisão de página, qualquer inserção que cause overflow trava o programa. | `arvoreb.py` — linha 154 |
| `insereNaArvore(chave, offset, rrn_atual, arq)` | A lógica atual ignora o offset — ele nunca é propagado nem inserido na página. | `arvoreb.py` — linha 219 |
| `criaIndice()` | Deve abrir os arquivos, escrever o cabeçalho do `btree.dat` e orquestrar toda a criação. | `arvoreb.py` — linha 224 |
| `busca(chave)` e `insere()` | Ambas vazias. São chamadas pelo modo `-e`; os dois `case` do `match` ficam com `pass`. | `arvoreb.py` — linhas 229/232 |
| `imprimirArvoreB(arq_btree)` | O modo `-p` não imprime absolutamente nada. | `arvoreb.py` — linha 237 |


## 3. Lógica incompleta ou incorreta

| Problema | Descrição | Onde |
|---|---|---|
| `insereChave` passa argumentos errados para `insereChavePromo` | Na linha 209, passa `(chave, filhoDpro, pag)` mas a função espera `(chave, offset, filhoD, pag)` — 4 argumentos. Vai travar com `TypeError`. | `arvoreb.py` — linha 209 |
| `insereChave` propaga `chave` em vez de `chavePro` | Após retorno da recursão, deve usar `chavePro` (chave promovida), não a chave original. | `arvoreb.py` — linha 209 |
| `ValueError` não capturada no fluxo de operações | `raise ValueError("Chave duplicada")` não é tratado no modo `-e`. O programa encerra com traceback em vez de imprimir a mensagem de erro esperada. | `arvoreb.py` — linha 201 |
| Busca no modo `-e` não usa o offset | Após encontrar a chave no índice, é preciso usar o offset retornado para fazer `seek` direto no `games.dat` e imprimir o registro. | Não implementado |
| Inserção no modo `-e` não grava no `games.dat` | O novo registro deve ser acrescentado ao fim do `games.dat` e o byte-offset capturado antes da escrita para inserir na árvore. | Não implementado |


## 5. Pontos de atenção

| Ponto | Descrição |
|---|---|
| Caminho do `games.dat` inconsistente | A verificação no modo `-e` usa `data/games.dat`, mas `ARQ_GAMES` aponta para `'games.dat'`. Padronize um único caminho. |
| Nenhum número mágico pode aparecer no código | O enunciado avisa que o programa será testado com ordens diferentes. Confirme que `ORDEM` é usada em todo lugar — nenhum `4` ou `5` hardcoded. |
| Parsing do argumento de inserção | A linha `i 14\|The Last of Us\|...` precisa ser parseada por `\|` para extrair os campos antes de gravar no `games.dat`. |
=======
## 1. Funções não implementadas

| `divide(chave, filhoD, pag, arq)` | Sem a divisão de página, qualquer inserção que cause overflow trava o programa. | `arvoreb.py` — linha 154 |
| `busca(chave)` e `insere()` | Ambas vazias. São chamadas pelo modo `-e`; os dois `case` do `match` ficam com `pass`. | `arvoreb.py` — linhas 229/232 |
| `imprimirArvoreB(arq_btree)` | O modo `-p` não imprime absolutamente nada. | `arvoreb.py` — linha 237 |

## 2. Bugs ativos

| Problema | Descrição | Onde |
|---|---|---|
| `criaArvore` ignora o `arqBTree` recebido e abre um novo `open(ARQ_BTREE, 'wb')` internamente | O arquivo passado por `criaIndice` (aberto em `'w+b'` com o cabeçalho já escrito) é ignorado. O `open` interno sobrescreve tudo com `'wb'`, apagando o cabeçalho. O `arqBTree` do parâmetro nunca é usado. | `arvoreb.py` — `criaArvore` |
| `insereNaArvore` usa `offset` do parâmetro atual em vez de `offsetPro` na nova raiz | Quando ocorre promoção, `pNova.offsets[0] = offset` guarda o offset do último registro inserido, não o offset associado à `chavePro` que subiu. O offset errado fica na raiz. | `arvoreb.py` — `insereNaArvore` |
| `insereChave` ainda usa `chave` em vez de `chavePro` no `insereChavePromo` | Na linha `insereChavePromo(chave, offset, filhoDpro, pag)`, deveria ser `chavePro` — a chave que voltou da recursão. Com arquivos pequenos isso passa despercebido; com qualquer promoção, a chave errada é inserida na página pai. | `arvoreb.py` — `insereChave` |

## 3. Pontos de atenção

| Ponto | Descrição |
|---|---|
| Caminho do `games.dat` inconsistente | `modo_e` em `main.py` verifica `"data/games.dat"`, mas `ARQ_GAMES` em `constantes.py` é `'games.dat'`. Padronize um único caminho. |
| `from constantes import *` em `pagina.py` | Sem o prefixo `src.`. Quebra quando importado via `from src.pagina import *`. Deve ser `from src.constantes import *`. |
| Nenhum número mágico no código | O enunciado avisa que o programa será testado com ordens diferentes. Confirme que `ORDEM` é usada em todo lugar. |
| Parsing do argumento de inserção no modo `-e` | A linha `i 14\|The Last of Us\|...` precisa ser parseada por `\|` para extrair os campos antes de gravar no `games.dat`. |


TAM_HEADER = 4
TAM_PAGE = 56
deu bom o teste de criação de índices

numChaves -> 1 inteiro
chaves    -> 4 inteiros
offsets   -> 4 inteiros
filhos    -> 5 inteiros
= 14 inteiros * 4 = 56bytes
ta dando certo até o primeiro overflow, pq n fizemos a função de divisão()
>>>>>>> ae13650784bd0c3201df5cb7fa402f0907417fd5
