# Checklist de Refatoração — Trabalho 1

## 🗂️ Organização e Imports
- [X] Criar `src/constantes.py` com `FORMATO_PRI`, `FORMATO_TAM`, `FORMATO_IDX`, `FORMATO_INV`, `SIZEOF_*`
- [X] Adicionar imports de `constantes.py` em `persistencia.py`
- [X] Adicionar `from struct import pack, unpack, calcsize` em `persistencia.py`
- [X] Adicionar `from src.registro import le_registro` em `operacoes.py`
- [X] Criar `.gitignore` com `data/` para ignorar `.dat`, `.ind`, `.lst`

## 📖 `src/registro.py`
- [X] Corrigir `le_registro`: checar `if len(tam) < 2` em vez de depender do valor 0
- [X] Corrigir byte-offset em `lista_de_registros`: guardar `arquivo.tell()` **antes** de chamar `le_registro`
- [X] Ignorar registros removidos (`*`) em `lista_de_registros` para não indexá-los no `-b`

## 📊 `src/indices.py`
- [X] Corrigir ordenação do índice primário para ser numérica

## 💾 `src/persistencia.py`
- [X] Trocar `open(...)` por `with open(...) as arq:` em todas as funções
- [X] Verificar se os arquivos de índice existem antes de tentar carregá-los (importante para o `-e`)

## ⚙️ `src/operacoes.py`
- [X] Corrigir formato de saída do `busca_pri`: remover `:` após "ID"
- [ ] Corrigir `busca_sec_genero` e `busca_sec_publicadora`:
  - [X] Remover `print("Registro removido")` — ignorar silenciosamente
  - [ ] Mover o `print` do cabeçalho para tratar o cenário de (0 registros) quando a chave não existir
- [ ] Implementar `insercao` de verdade:
  - [ ] Verificar duplicata no índice primário
  - [ ] Serializar e escrever no final do `games.dat`
  - [ ] Atualizar índice primário (mantendo ordenação)
  - [ ] Atualizar lista invertida e índices secundários
- [ ] Implementar `remocao` de verdade:
  - [ ] Buscar offset via índice primário
  - [ ] Seek no offset e sobrescrever primeiro byte com `*`
  - [ ] Remover entrada do índice primário e da lista invertida

## 🗜️ `src/compactacao.py`
- [ ] Implementar `compactacao`:
  - [ ] Ler `games.dat` ignorando registros com `*`
  - [ ] Reescrever o arquivo apenas com registros válidos
  - [ ] Reconstruir `primario.ind` com os novos byte-offsets

## 🚀 `main.py`
- [X] Corrigir ordem no modo `-b`: chamar leitura antes de construir índices
- [X] Modo `-b`: Sobrescrever arquivos de índice existentes e persistir ao final
- [X] Modo `-b`: Remover prints de debug
- [ ] Modo `-e`:
  - [ ] Verificar existência dos 5 arquivos antes de iniciar; encerrar com erro se faltar algum
  - [ ] Carregar os 4 índices em memória
  - [ ] Abrir e parsear o arquivo de operações (linha a linha)
  - [ ] Despachar cada linha para a função correspondente
  - [ ] Persistir os 4 índices no disco ao encerrar a execução
- [ ] Modo `-c`:
  - [ ] Chamar função de compactação
  - [ ] Reconstruir e persistir `primario.ind`