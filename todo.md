## modo `-e`
- [x] Ler e fazer o parse do arquivo de operações (linha a linha) dentro do `with open` no `modo_e`.
- [x] Criar o despachante (if/elif): identificar o comando (`bp`, `bs1`, `bs2`, `i`, `r`) e chamar a função correspondente em `operacoes.py` passando os parâmetros corretos.
- [ ] **Very important:** Salvar os 4 índices (primário, gênero, publicadora, lista invertida) de volta no disco usando as funções de `persistencia.py` no **final** da execução do `modo_e` (depois do loop do arquivo de operações).

## implementação da `insercao` (`src/operacoes.py`) - gu
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

Teste foi concluído, todos estão corretos (falta testar -r e -c(precisa da remoção))

================================================================
🔴 CRÍTICO — FALTA DE IMPLEMENTAÇÃO (tiram nota com certeza)
================================================================

1. REMOÇÃO — função remocao() em src/operacoes.py está com pass
----------------------------------------------------------------
A função existe mas não faz nada. O case 'r' no main.py também
tem apenas um pass e não chama a função.

O que precisa ser implementado:
  - Buscar o ID no indice_pri via busca binária.
  - Se não encontrar:
      imprimir: Remoção do registro de chave "<ID>"
      imprimir: Registro não encontrado!
  - Se encontrar:
      imprimir: Remoção do registro de chave "<ID>" (offset = X)
      fazer seek(offset + 2) no games.dat  ← pula os 2 bytes de tamanho
      sobrescrever o primeiro byte com '*'  ← remoção lógica
      remover a entrada do indice_pri
      atualizar a lista_inv: percorrer a cadeia de ponteiros do
      gênero e da publicadora e "desligar" o nó removido,
      apontando o anterior para o próximo do removido.

Saída esperada pela spec (exemplo do enunciado):
  Remoção do registro de chave "121" (offset = 936)
  Remoção do registro de chave "754"
  Registro não encontrado!


FEITO - 2. COMPACTAÇÃO — src/compactacao.py incompleta
----------------------------------------------------------------
A leitura dos registros válidos está feita, mas faltam 2 coisas:

  a) O arquivo novo é salvo como "games_novo.dat" em vez de
     substituir o "games.dat" original. Precisa renomear ou
     reescrever diretamente no games.dat.

  b) Não reconstrói o primario.ind após reescrever o arquivo.
     Todos os byte-offsets mudam com a compactação, então o
     índice primário fica desatualizado. É preciso recalcular
     os offsets durante a reescrita e salvar o novo primario.ind.

  c) A spec diz: "o arquivo de índice primário deverá ser
     reconstruído e atualizado, CASO EXISTA". Falta verificar
     se primario.ind existe antes de tentar reconstruir.

Esqueleto do que falta na compactacao():

  novo_indice_pri = []
  offset_atual = 0
  with open("data/games.dat", "wb") as arq:
      for reg in reg_validos:
          buf = reg.encode('utf-8')
          arq.write(pack(FORMATO_TAM, len(buf)))
          arq.write(buf)
          chave = int(reg.split('|')[0])
          novo_indice_pri.append([chave, offset_atual])
          offset_atual += 2 + len(buf)

  novo_indice_pri.sort()

  if os.path.exists("data/primario.ind"):
      arq_indice_prim(novo_indice_pri)


================================================================
🟡 BUGS DE LÓGICA (podem travar na apresentação)
================================================================

FEITO - 3. SALVAMENTO DOS ÍNDICES NO LUGAR ERRADO — main.py
----------------------------------------------------------------
O salvamento dos 4 índices está DENTRO do loop de operações
(linhas 132–135 do main.py), o que faz salvar no disco após
cada linha do arquivo de operações.

A spec diz: "Os arquivos de índice serão atualizados no
dispositivo de armazenamento sempre que uma execução for
encerrada." — ou seja, deve ser DEPOIS do loop.

Correção: mover as 4 chamadas de arq_indice_* para fora e
após o bloco "with open(...) as arq_ops".


4. SEEK ERRADO NA REMOÇÃO LÓGICA
----------------------------------------------------------------
Ao marcar '*', o seek deve apontar para o início do CONTEÚDO,
não para o início do registro (que inclui os 2 bytes de tamanho).

Errado:  arquivo.seek(offset)
Correto: arquivo.seek(offset + 2)   ← pula o campo de tamanho

Se fizer seek(offset), vai sobrescrever o campo de tamanho,
corrompendo a estrutura do arquivo.


5. CONTAGEM DE BYTES NA INSERÇÃO — verificar saída
----------------------------------------------------------------
No main.py:
  num_bytes = len(comando[1].encode("utf-8"))

Isso conta só o conteúdo da string. O registro no arquivo
ocupa conteúdo + 2 bytes (campo de tamanho). Confira se a
saída esperada pelo enunciado ("48 bytes") refere-se ao
tamanho da string ou ao tamanho total no arquivo.

Exemplo do enunciado:
  Inserção do registro de chave "539" (48 bytes)
  Registro: 539|Minecraft|2011|Sandbox|Microsoft Studios|PC|
  Contando: len("539|Minecraft|2011|Sandbox|Microsoft Studios|PC|") = 48

Neste caso específico dá certo, mas confirme com outros casos
se deve ou não somar os 2 bytes do cabeçalho.


================================================================
🟢 DETALHES DE SAÍDA (pequenos, mas visíveis na apresentação)
================================================================

FEITO - 6. MENSAGEM DE ID DUPLICADO DIFERENTE DA SPEC
----------------------------------------------------------------
O que o código imprime:
  "Elemento de mesma chave já existe."

O que a spec sugere (pelo contexto):
  "ID duplicado! Registro descartado."

Recomendação: alinhar a mensagem com o que foi discutido
com a professora ou com o que está no enunciado.


FEITO - 7. BUSCA SECUNDÁRIA — ORDEM DOS RESULTADOS
----------------------------------------------------------------
A ordem dos registros retornados pela busca secundária depende
da ordem de inserção na lista invertida. Confira se a ordem
apresentada bate com a esperada nos exemplos do enunciado,
pois a professora pode testar com o arquivo original.


================================================================
RESUMO DE PRIORIDADE
================================================================

PRIORIDADE | O QUE FALTA
-----------|------------------------------------------------------
🔴 ALTA    | Implementar remocao() completamente
🔴 ALTA    | Chamar remocao() no case 'r' do main.py
🔴 ALTA    | Compactação: substituir games.dat e reconstruir primario.ind com os novos offsets
🟡 MÉDIA   | Mover salvamento dos índices para fora do loop
🟡 MÉDIA   | Corrigir seek na remoção lógica (offset + 2)
🟡 MÉDIA   | Verificar contagem de bytes na inserção
🟠 BAIXA   | Verificar existência do primario.ind antes de reconstruir na compactação
🟢 BAIXA   | Ajustar mensagem de ID duplicado

================================================================