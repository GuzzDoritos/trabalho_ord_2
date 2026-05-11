# Checklist de Refatoração — Trabalho 1

## 🗂️ Organização e Imports

- [X] Criar `src/constantes.py` com `FORMATO_PRI`, `FORMATO_TAM`, `FORMATO_IDX`, `FORMATO_INV`, `SIZEOF_*`
- [x] Adicionar imports de `constantes.py` em `persistencia.py`
- [X] Adicionar `from struct import pack, unpack, calcsize` em `persistencia.py`
- [X] Adicionar `from src.registro import le_registro` em `operacoes.py`
- [ ] Adicionar `src/__init__.py` vazio (se necessário)
- [X] Criar `.gitignore` com `data/` para ignorar `.dat`, `.ind`, `.lst`

---

## 📖 `src/registro.py`

- [X] Corrigir `le_registro`: checar `if len(tam) < 2` em vez de depender do valor 0
- [X] Corrigir byte-offset em `lista_de_registros`: guardar `arquivo.tell()` **antes** de chamar `le_registro`, não depois
- [X] Ignorar registros removidos (`*`) em `lista_de_registros` para não indexá-los no `-b`

---

## 📊 `src/indices.py`

- [X] Corrigir ordenação do índice primário para ser numérica:
  ```python
  indice_pri.sort(key=lambda x: int(x[0]))
  ```

---

## 💾 `src/persistencia.py`

- [X] Trocar `open(...)` por `with open(...) as arq:` em todas as funções
- [ ] Verificar se os arquivos existem antes de abrir no modo leitura (para o `-e`)

---

## ⚙️ `src/operacoes.py`

- [ ] Corrigir formato de saída do `busca_pri`: remover `:` após "ID"
  - ❌ `Busca pelo registro de ID: "{chave}"`
  - ✅ `Busca pelo registro de ID "{chave}"`
- [ ] Corrigir `busca_sec_genero` e `busca_sec_publicadora`:
  - [ ] Remover `print("Registro removido")` — removidos devem ser ignorados silenciosamente
  - [ ] Mover o `print` do cabeçalho para **antes** do loop
  - [ ] Quando chave não existe, imprimir `(0 registros)` em vez de `"Registro não encontrado"`
- [ ] Implementar `insercao` de verdade:
  - [ ] Verificar duplicata no índice primário
  - [ ] Serializar o registro no formato `ID|Nome|Ano|Gênero|Publicadora|Plataforma|`
  - [ ] Calcular tamanho (corpo + 2 bytes do campo de tamanho)
  - [ ] Escrever no final do `games.dat` (seek para o fim)
  - [ ] Atualizar índice primário mantendo ordenação numérica
  - [ ] Atualizar lista invertida e índices secundários
  - [ ] Imprimir `Inserção do registro de chave "<ID>" (<N> bytes)`
- [ ] Implementar `remocao` de verdade:
  - [ ] Buscar offset via índice primário
  - [ ] Seek no offset e sobrescrever primeiro byte com `*`
  - [ ] Remover entrada do índice primário
  - [ ] Remover ID das cadeias da lista invertida (gênero e publicadora)
  - [ ] Imprimir `Remoção do registro de chave "<ID>" (offset = <offset>)`

---

## 🗜️ `src/compactacao.py`

- [ ] Implementar `compactacao`:
  - [ ] Ler `games.dat` sequencialmente ignorando registros com `*`
  - [ ] Reescrever o arquivo apenas com registros válidos
  - [ ] Reconstruir `primario.ind` com os novos byte-offsets

---

## 🚀 `main.py`

- [ ] Corrigir ordem no modo `-b`: chamar `lista_de_registros` **antes** de construir índices
- [ ] Modo `-b`:
  - [ ] Sobrescrever arquivos de índice existentes
  - [ ] Persistir os 4 arquivos ao final
  - [ ] Remover prints de debug (`print(indicesec)`, linha de "aaa...")
- [ ] Modo `-e`:
  - [ ] Verificar existência dos 5 arquivos antes de qualquer coisa; encerrar com erro se faltar algum
  - [ ] Carregar os 4 índices em memória
  - [ ] Abrir e parsear o arquivo de operações linha a linha
  - [ ] Despachar cada linha para a função correta (`bp` → `busca_pri`, `bs1`, `bs2`, `i`, `r`)
  - [ ] Persistir os 4 índices no disco ao encerrar
- [ ] Modo `-c`:
  - [ ] Chamar `compactacao`
  - [ ] Reconstruir e persistir `primario.ind`
- [ ] Remover código solto fora dos `if/elif` (chamadas a `arq_indice_*` que executam em qualquer modo)
- [ ] Usar `with open(...)` para `games.dat`
