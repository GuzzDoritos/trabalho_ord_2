## modo `-e`
- [x] Ler e fazer o parse do arquivo de operações (linha a linha) dentro do `with open` no `modo_e`.
- [ ] Criar o despachante (if/elif): identificar o comando (`bp`, `bs1`, `bs2`, `i`, `r`) e chamar a função correspondente em `operacoes.py` passando os parâmetros corretos.
- [ ] **Very important:** Salvar os 4 índices (primário, gênero, publicadora, lista invertida) de volta no disco usando as funções de `persistencia.py` no **final** da execução do `modo_e` (depois do loop do arquivo de operações).

## implementação da `insercao` (`src/operacoes.py`)
- [ ] Duplicidade: checar se o ID já existe no `indice_pri`. Se sim, imprimir: `ID duplicado! Registro descartado.`.
- [ ] **Escrita no disco:** 
  - [ ] Calcular o tamanho do registro (serialização: `ID|Nome|Ano|Gênero|Publicadora|Plataforma|`).
  - [ ] Dar `seek` para o final do arquivo (`games.dat`) e gravar os 2 bytes de tamanho + a string do registro.
- [ ] **Atualização em memória:**
  - [ ] Atualizar o `indice_pri` e garantir que continue ordenado numericamente.
  - [ ] Adicionar os ponteiros na `lista_inv`.
  - [ ] Atualizar as chaves em `indice_sec_genero` e `indice_sec_publicadora` se forem gêneros/publicadoras novas.
- [ ] **Saída:** Imprimir: `Inserção do registro de chave "<ID>" (<N> bytes)` (Onde N é o tamanho da string + 2 bytes).

## 🗑️ Implementação da `remocao` (`src/operacoes.py`)
- [ ] **Verificação de existência:** Checar se o ID existe via `indice_pri`. Se não existir, imprimir: `Remoção do registro de chave "<ID>"` e na linha seguinte `Registro não encontrado!`.
- [ ] **Remoção Lógica (Disco):** Dar `seek` pro offset do registro no `games.dat` e sobrescrever o primeiro byte com `*`.
- [ ] **Remoção Lógica (Memória):** - [ ] Remover a entrada do ID no `indice_pri`.
  - [ ] *Desafio:* Atualizar a `lista_inv` para remover/pular esse ID nas cadeias de ponteiros de gênero e publicadora correspondentes.

## 🗜️ Modo `-c`: Compactação (`src/compactacao.py` e `main.py`)
- [ ] Chamar a função de compactação na função `modo_c` do `main.py`.
- [ ] **Lógica da compactação:**
  - [ ] Ler o `games.dat` inteiro, pulando os registros que começam com `*`.
  - [ ] Reescrever o `games.dat` apenas com os registros válidos (removendo os "buracos").
  - [ ] Reconstruir a estrutura do `primario.ind` (pegando os novos byte-offsets gerados pela reescrita) e salvar o novo índice no disco.