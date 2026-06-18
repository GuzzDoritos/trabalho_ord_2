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