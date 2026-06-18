# Análise do Projeto — Árvore-B (Trabalho 2) — v6

> **Source-of-truth:** `EspecificacaoTrab2-ES.pdf` (especificação) e `Aula 11 - Arvore B - Busca e Insercao (1).pdf` (pseudocódigo da aula)
>
> **Última atualização:** 2026-06-18 — código relido integralmente

---

## ✅ Corrigido desde a v5

| Item | Status |
|---|---|
| `divide()` recebia `offset` em vez de `offsetPro` (linha 167 atual) | ✅ Corrigido |
| Print de debug `"Buscando chave..."` em `buscaNaArvore` | ✅ Removido |
| Print de debug `"RRN RAIZ ="` em `busca()` | ✅ Removido |
| Comentário `#DANDO ERRO` desatualizado | ✅ Removido |
| Aspas na mensagem de erro de busca `"chave não encontrada"` | ✅ Corrigido (L226) |
| `case 'i': pass` no `modo_e()` | ✅ Agora chama `insere()` (L37) |
| Mensagem final no modo `-e` | ✅ Adicionada (L38) |
| `main()` agora chama `modo_p()` em vez de inline | ✅ Corrigido (L52) |

---

## 🔴 Erros / Bugs

### 1. `insereChave()` — chave duplicada faz `print` mas **não para a execução**

**Arquivo:** [arvoreb.py:154-157](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/src/arvoreb.py#L154-L157)

```python
if achou: #True
    print("Chave duplicada")

chavePro, offsetPro, filhoDpro, promo = insereChave(chave, offset, pag.filhos[pos], arq)
```

O `raise ValueError` anterior foi trocado por `print("Chave duplicada")`, **mas a execução continua para a linha 157** e tenta inserir a chave mesmo assim. Isso causa:
- Inserção de chave duplicada na árvore (corrompe o índice)
- **Deve** interromper a inserção retornando algo como `return NULO, NULO, NULO, False` logo após o print, ou usar `raise` com `try/except` no chamador.

Pseudocódigo da aula (slide 10):
```
se achou então
    gere um erro de valor – "Chave duplicada"
```

> [!CAUTION]
> Este é o bug mais grave atualmente. Qualquer busca que encontre chave duplicada vai continuar inserindo, corrompendo a árvore inteira.

---

### 2. `insere()` — chamada sem argumentos e corpo vazio (`pass`)

**Arquivo:** [arvoreb.py:231-232](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/src/arvoreb.py#L231-L232) e [main.py:37](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/main.py#L37)

```python
# arvoreb.py — definição:
def insere():
    pass

# main.py — chamada (L37):
case 'i':
    insere()   # ← sem argumentos, não passa o registro nem os arquivos
```

Dois problemas:
1. O corpo da função é `pass` — nenhuma lógica implementada
2. A chamada em `main.py` L37 não passa nenhum argumento. Deveria passar pelo menos a string do registro (`comando[1]`), e os file handles de `games.dat` e `btree.dat`

Conforme a spec (pág. 2), a inserção deve:
- Extrair a chave primária do registro
- Verificar duplicata no `btree.dat` → se duplicada: `Erro: chave "X" duplicada`
- Escrever o registro no final de `games.dat` (2 bytes de tamanho + conteúdo)
- Inserir `{chave, byte-offset}` na árvore-B e atualizar a raiz
- Imprimir:
  ```
  Inserção do registro de chave "14"
  14|The Last of Us|2013|Action-Adventure|Sony|PlayStation 3| (59 bytes - offset 9416)
  ```

---

### 3. `imprimirArvoreB()` — não implementada (`pass`)

**Arquivo:** [arvoreb.py:236-237](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/src/arvoreb.py#L236-L237)

A spec (pág. 3) exige o formato exato (exemplo para ORDEM=5):

```
Página 0:
Chaves =  197 | 346 | -1 | -1
Offsets = 342 | 456 | -1 | -1
Filhos =  -1 | -1 | -1 | -1 | -1

Página 1:
Chaves =  707 | 875 | -1 | -1
Offsets = 136, 275, -1 | -1
Filhos =  -1 | -1 | -1 | -1 | -1

- - - - - - - - - - Raiz - - - - - - - - - -
Página 2:
Chaves =  348 | 484 | -1 | -1
Offsets = 93 | 0 | -1 | -1
Filhos =  0 | 3 | 1 | -1 | -1
- - - - - - - - - - - - - - - - -- - - - - -

Página 3:
Chaves =  393, 403, -1 | -1
Offsets = 189, 392, -1 | -1
Filhos =  -1 | -1 | -1 | -1 | -1
```

Deve:
1. Abrir `btree.dat`, ler cabeçalho para obter `rrn_raiz`
2. Calcular total de páginas: `(tamanho_arquivo - TAM_HEADER) // TAM_PAGE`
3. Iterar de RRN 0 até total-1, imprimindo cada página
4. Envolver a página raiz com `- - - - - - - - - - Raiz - - - - - - - - - -`

---

### 4. `modo_e()` não abre `btree.dat` — inserção impossível

**Arquivo:** [main.py:26-38](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/main.py#L26-L38)

```python
with open(ARQ_GAMES, "rb+") as arq_games:
    with open(arquivo_operacoes, "r", encoding="utf-8") as arq_ops:
```

O `modo_e()` abre `games.dat` e o arquivo de operações, mas **não abre `btree.dat`**. Para que inserções funcionem, `btree.dat` precisa estar aberto em modo `r+b` (leitura e escrita). Sem isso, `insere()` não tem como acessar/atualizar o índice.

> [!NOTE]
> A função `busca()` abre `btree.dat` internamente (L210), então buscas funcionam. Mas para inserções, o arquivo precisa ser aberto em modo escrita.

---

### 5. Mensagem final do modo `-e` usa aspas simples em vez de aspas duplas

**Arquivo:** [main.py:38](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/main.py#L38)

```python
# ATUAL:
print(f"As operações do arquivo '{arquivo_operacoes}' foram executadas com sucesso!")

# SPEC EXIGE (pág. 2):
# As operações do arquivo "operacoes.txt" foram executadas com sucesso!
```

Aspas simples `'...'` em vez de aspas duplas `"..."`. A spec usa aspas duplas ao redor do nome do arquivo.

---

### 6. `ORDEM = 15` — valor diferente do exemplo da spec

**Arquivo:** [constantes.py:3](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/src/constantes.py#L3)

```python
ORDEM = 15
```

O exemplo da spec usa ORDEM = 5 e os testes provavelmente usarão esse valor. A spec diz: *"Esteja ciente de que o seu programa será testado com árvores de diferentes ordens."*

> [!WARNING]
> Isso não é um bug per se (a spec pede que ORDEM seja uma constante global usável com qualquer valor), mas para **testes e validação** convém voltar para `ORDEM = 5` para comparar com o exemplo da spec. Se o programa funcionar com ORDEM = 5 e produzir a mesma árvore do exemplo, está correto.

---

### 7. `modo_p()` não verifica se `btree.dat` existe

**Arquivo:** [main.py:40-41](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/main.py#L40-L41)

```python
def modo_p():
    imprimirArvoreB(ARQ_BTREE)
```

A spec (pág. 3): *"Note que, para esse tipo de execução, o arquivo btree.dat deve existir. Caso contrário, o programa deve apresentar uma mensagem de erro e terminar."*

Falta verificar `os.path.exists(ARQ_BTREE)` antes de chamar `imprimirArvoreB`.

---

### 8. `divide()` — padding de `pNova.filhos` pode produzir lista com tamanho errado

**Arquivo:** [arvoreb.py:97](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/src/arvoreb.py#L94-L98)

```python
pNova.chaves = pag.chaves[meio+1:] + [NULO] * meio      # ORDEM-1-meio-1 + meio = ORDEM-2 ❌ (precisa ORDEM-1)
pNova.offsets = pag.offsets[meio+1:] + [NULO] * meio     # idem
pNova.filhos = pag.filhos[meio+1:] + [NULO] * meio       # ORDEM-meio-1 + meio = ORDEM-1 ❌ (precisa ORDEM)
```

Após `insereChavePromo`, `pag` tem ORDEM chaves (capacidade expandida) e ORDEM+1 filhos. Fazendo o slice:
- `pag.chaves[meio+1:]` → tem `ORDEM - meio - 1` elementos (pq agora tem ORDEM chaves no total, ex: ORDEM=5 → 5 chaves, meio=2, slice tem 2 elementos)
- `+ [NULO] * meio` → adiciona `meio` nulos (ex: 2)
- Total: `ORDEM - meio - 1 + meio = ORDEM - 1` ✅ (chaves OK)

Espera, recalculando com cuidado: após `insereChavePromo`, `pag.chaves` tem exatamente ORDEM elementos (era ORDEM-1, expandiu para ORDEM). `pag.chaves[meio+1:]` tem `ORDEM - meio - 1` elementos. `+ [NULO] * meio` dá `ORDEM - meio - 1 + meio = ORDEM - 1` ✅.

Para filhos: `pag.filhos` tem ORDEM+1 após expansão. `pag.filhos[meio+1:]` tem `ORDEM + 1 - meio - 1 = ORDEM - meio` elementos. `+ [NULO] * meio` dá `ORDEM - meio + meio = ORDEM` ✅.

**Recalculei: as contas batem. O padding está correto.** ~~Removo este item.~~

Porém para `pag` (a página que fica, linhas 104-106):
```python
pag.chaves = pag.chaves[:meio] + [NULO] * (ORDEM - meio - 1)  # meio + ORDEM-meio-1 = ORDEM-1 ✅
pag.offsets = pag.offsets[:meio] + [NULO] * (ORDEM - meio - 1) # ✅
pag.filhos = pag.filhos[:meio+1] + [NULO] * (ORDEM - meio - 1) # meio+1 + ORDEM-meio-1 = ORDEM ✅
```

**As contas estão corretas.** Este item é um falso positivo — removo.

---

### 9. `busca()` — saída inclui `\n` extra após cada resultado

**Arquivo:** [arvoreb.py:224](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/src/arvoreb.py#L224) e [arvoreb.py:226](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/src/arvoreb.py#L226)

```python
print(f'{reg} ({tam} bytes - offset {offset})\n')   # L224
print(f'Erro: chave "{chave}" não encontrada\n')     # L226
```

O `print()` já adiciona `\n`. Com o `\n` explícito na f-string, a saída terá uma **linha em branco extra** após cada resultado de busca. A spec mostra uma linha em branco entre operações diferentes, mas isso é entre o bloco de busca/inserção completo, não entre cada linha. Verificar se o output bate com a spec:

```
Busca pelo registro de chave "220"
220|Assassin's Creed 2|... (67 bytes - offset 4244)
                                                      ← linha em branco (spec tem)
Inserção do registro de chave "14"
...
```

A spec mostra uma linha em branco entre blocos. O `\n` no `print` produz essa linha. **Pode estar correto** se cada operação é um bloco separado. Mas a linha `Busca pelo registro de chave "X"` (L211) **não** tem `\n` extra, então a formatação seria:
```
Busca pelo registro de chave "220"
220|... (67 bytes - offset 4244)
                                   ← linha em branco ✅
```

Isso bate com a spec. **OK, provavelmente correto.** Porém se duas buscas falharem seguidas, pode produzir formatação inconsistente. Verificar manualmente.

---

## 🟡 Ajustes menores

| # | Problema | Onde | O que fazer |
|---|---|---|---|
| 1 | Mensagem do `FileNotFoundError` em `criaIndice()` usa path hardcoded `"/data/"` | [arvoreb.py:202](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/src/arvoreb.py#L202) | Usar `ARQ_GAMES` na mensagem |
| 2 | `lePagina()` docstring diz "escreva pag" mas a função **lê** | [arvoreb.py:51-55](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/src/arvoreb.py#L51-L55) | Corrigir docstring: "leia" em vez de "escreva" |

---

## ✅ Componentes corretos (verificados contra pseudocódigo da aula)

| Componente | Status | Notas |
|---|---|---|
| `Pagina` | ✅ | Inclui `offsets` conforme spec. Inicialização com listas de NULO corretas |
| Constantes (`FORMATO_PAGE`, `TAM_PAGE`, etc.) | ✅ | `ORDEM` usada como constante global. Formato de pack correto |
| `leiaReg()` | ✅ | Lê 2 bytes de tamanho + conteúdo, retorna (chave, offset) |
| `escrevePagina()` | ✅ | `rrn * TAM_PAGE + TAM_HEADER`, empacota na ordem correta |
| `lePagina()` | ✅ | Simétrica com `escrevePagina`, desempacota na ordem correta |
| `buscaNaPagina()` | ✅ | Busca linear conforme pseudocódigo |
| `buscaNaArvore()` | ✅ | Recursiva conforme pseudocódigo |
| `insereChavePromo()` | ✅ | Adaptada para offset. Expande lista quando cheia (slide 28) |
| `novoRRN()` | ✅ | `(offset - TAM_HEADER) // TAM_PAGE` (slide 32) |
| `divide()` | ✅ | Divisão correta, padding correto, retorna 5 valores com offset |
| `insereChave()` | ⚠️ | Correto exceto **bug #1** (chave duplicada não interrompe) |
| `insereNaArvore()` | ✅ | Nova raiz com chave/offset/filhos corretos (slide 34) |
| `criaArvore()` | ✅ | Loop de leitura + inserção |
| `criaIndice()` | ✅ | Cabeçalho, criação, atualização raiz. Sobrescreve `btree.dat` |
| `busca()` | ✅ | Formato de saída correto (aspas corrigidas) |
| `modo_b()` | ✅ | Chama `criaIndice()` |
| `modo_e()` | ⚠️ | Verifica existência de arquivos, mas falta abrir `btree.dat` e passar args para `insere()` |
| `modo_p()` | ⚠️ | Existe mas falta verificação de `btree.dat` |

---

## 📋 Ordem de prioridade para correção

1. 🔴 **Bug #1** — `insereChave` chave duplicada não para execução → corrompe árvore (CRÍTICO)
2. 🔴 **Bug #2** — Implementar `insere()` com assinatura correta e conectar no `main.py`
3. 🔴 **Bug #3** — Implementar `imprimirArvoreB()`
4. 🔴 **Bug #4** — `modo_e()` abrir `btree.dat` em `r+b`
5. 🟠 **Bug #5** — Aspas da mensagem final do modo `-e`
6. 🟠 **Bug #6** — `ORDEM = 15` → voltar para 5 para validação
7. 🟡 **Bug #7** — Verificação de `btree.dat` no `modo_p()`
8. 🟡 **Ajustes menores** — docstring, mensagem hardcoded
