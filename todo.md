# Análise de Pendências e Erros

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