# Análise do Projeto — Árvore-B (Trabalho 2) — v7

> **Source-of-truth:** `EspecificacaoTrab2-ES.pdf` (especificação) e `Aula 11 - Arvore B - Busca e Insercao (1).pdf` (pseudocódigo da aula)
>
> **Última atualização:** 2026-06-19 — código relido integralmente

---

## ✅ Corrigido desde a v6

| Item | Status |
|---|---|
| `ORDEM = 15` → `ORDEM = 5` | ✅ Corrigido ([constantes.py:3](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/src/constantes.py#L3)) |
| `modo_e()` não abria `btree.dat` | ✅ Agora abre em `r+b` ([main.py:27](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/main.py#L27)) |
| `insere()` chamada sem argumentos | ✅ Agora recebe `registro = comando[1]` ([main.py:37-38](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/main.py#L37-L38)) |
| Mensagem final usava aspas simples | ✅ Agora usa aspas duplas ([main.py:41](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/main.py#L41)) |
| `modo_p()` não verificava existência de `btree.dat` | ✅ Adicionada verificação ([main.py:44-46](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/main.py#L44-L46)) |
| `arquivos_necessarios` usava strings hardcoded | ✅ Agora usa `ARQ_GAMES` e `ARQ_BTREE` ([main.py:16-17](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/main.py#L16-L17)) |
| `readline` no início do loop pulava operações | ✅ Movido para o final do loop ([main.py:40](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/main.py#L40)) |

---

## 🔴 Erros / Bugs

### 1. `insereChave()` — f-string da `ValueError` com aspas quebradas

**Arquivo:** [arvoreb.py:155](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/src/arvoreb.py#L155)

```python
# ATUAL (errado):
raise ValueError(f'Erro: chave "{chave} duplicada')

# CORRETO:
raise ValueError(f'Erro: chave "{chave}" duplicada')
```

Falta a aspa dupla de fechamento após `{chave}`. A saída atual seria:
```
Erro: chave "14 duplicada
```
Quando a spec exige:
```
Erro: chave "14" duplicada
```

---

### 2. `insere()` — corpo essencialmente vazio, lógica não implementada

**Arquivo:** [arvoreb.py:232-238](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/src/arvoreb.py#L232-L238)

```python
def insere(registro):
    try:
        #rrn_raiz = insereNaArvore(chave, offset, rrn_raiz, arqBTree)
        pass
    except ValueError as e:
        print(e)
```

A estrutura `try/except` está correta (captura o `raise ValueError` de `insereChave`), mas falta toda a lógica interna. Conforme a spec (pág. 2), a função deve:

1. Extrair a chave do registro: `registro.split('|', 1)` → `chave = int(campos[0])`
2. Abrir `games.dat` e ir ao final (`seek(0, SEEK_END)`)
3. Capturar o `offset = arq.tell()`
4. Escrever o registro: 2 bytes de tamanho (little-endian) + conteúdo em bytes
5. Abrir `btree.dat`, ler `rrn_raiz` do cabeçalho
6. Chamar `insereNaArvore(chave, offset, rrn_raiz, arqBTree)`
7. Atualizar `rrn_raiz` no cabeçalho
8. Imprimir no formato exato:
   ```
   Inserção do registro de chave "14"
   14|The Last of Us|2013|Action-Adventure|Sony|PlayStation 3| (59 bytes - offset 9416)
   ```

> [!IMPORTANT]
> A função precisa receber os file handles de `arqGames` e `arqBTree` que já estão abertos em `modo_e()`, ou abri-los internamente. Atualmente só recebe `registro`.

---

### 3. `insere()` — assinatura incompatível com a chamada em `modo_e()`

**Arquivo:** [arvoreb.py:232](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/src/arvoreb.py#L232) e [main.py:38](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/main.py#L38)

`insere(registro)` recebe apenas a string do registro, mas `modo_e()` já tem `arqGames` e `arqBTree` abertos (L26-27). A função `insere` precisará desses file handles para:
- Escrever no `games.dat`
- Ler/atualizar `rrn_raiz` no cabeçalho de `btree.dat`
- Chamar `insereNaArvore(chave, offset, rrn_raiz, arqBTree)`

A chamada em `main.py:38` deveria ser algo como:
```python
insere(registro, arqGames, arqBTree)
```

---

### 4. `busca()` abre `btree.dat` internamente em modo somente leitura (`rb`)

**Arquivo:** [arvoreb.py:210](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/src/arvoreb.py#L210)

```python
with open(ARQ_BTREE, 'rb') as arqBTree:
```

No contexto do `modo_e()`, o `btree.dat` **já está aberto** em `r+b` (L27 do `main.py`). A função `busca()` abre uma **segunda instância** do arquivo em modo `rb`. Isso funciona para buscas isoladas (`modo_e` com só buscas), mas se houver inserções intercaladas com buscas:
- `insere()` modifica `btree.dat` via o handle de `modo_e()`
- `busca()` abre uma nova instância `rb` que pode ler dados desatualizados (cache do OS / buffering)

A solução seria: `busca()` receber o `arqBTree` já aberto como parâmetro (como `criaArvore` faz), ou fazer `flush` após cada inserção.

> [!WARNING]
> Este problema pode causar resultados incorretos quando buscas e inserções são intercaladas no mesmo arquivo de operações (cenário do exemplo da spec, pág. 2).

---

### 5. `imprimirArvoreB()` — não implementada (`pass`)

**Arquivo:** [arvoreb.py:242-243](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/src/arvoreb.py#L242-L243)

A spec (pág. 3) exige impressão de todas as páginas na ordem de RRN, com a raiz identificada. Formato exato:

```
Página 0:
Chaves =  197 | 346 | -1 | -1
Offsets = 342 | 456 | -1 | -1
Filhos =  -1 | -1 | -1 | -1 | -1

- - - - - - - - - - Raiz - - - - - - - - - -
Página 2:
Chaves =  348 | 484 | -1 | -1
Offsets = 93 | 0 | -1 | -1
Filhos =  0 | 3 | 1 | -1 | -1
- - - - - - - - - - - - - - - - -- - - - - -
```

Deve:
1. Abrir `btree.dat`, ler cabeçalho (`rrn_raiz`)
2. Calcular total de páginas: `(tamanho_arquivo - TAM_HEADER) // TAM_PAGE`
3. Para cada RRN (0 até total-1), ler a página e imprimir chaves, offsets e filhos separados por ` | `
4. Envolver a página raiz com as linhas decorativas

---

## 🟡 Ajustes menores

| # | Problema | Onde | Impacto |
|---|---|---|---|
| 1 | Mensagem do `FileNotFoundError` em `criaIndice()` usa path hardcoded `"/data/"` | [arvoreb.py:202](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/src/arvoreb.py#L202) | Cosmético — usar `ARQ_GAMES` |
| 2 | `lePagina()` docstring diz "escreva pag" mas a função **lê** | [arvoreb.py:51-55](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/src/arvoreb.py#L51-L55) | Cosmético — corrigir docstring |
| 3 | `busca()` imprime `\n` extra no final de cada resultado | [arvoreb.py:224](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/src/arvoreb.py#L224) e [arvoreb.py:226](file:///c:/Users/Asus%20VivoBook/Documents/GitHub/trabalho_ord_2/src/arvoreb.py#L226) | Pode bater com a spec (linha em branco entre operações), mas atenção se produzir linhas extras no final |

---

## ✅ Componentes corretos

| Componente | Status | Notas |
|---|---|---|
| `Pagina` | ✅ | Inclui `offsets` conforme spec |
| Constantes | ✅ | `ORDEM = 5`, formatos corretos |
| `leiaReg()` | ✅ | Lê 2 bytes tamanho + conteúdo |
| `escrevePagina()` | ✅ | Empacota na ordem correta |
| `lePagina()` | ✅ | Desempacota corretamente |
| `buscaNaPagina()` | ✅ | Busca linear conforme pseudocódigo |
| `buscaNaArvore()` | ✅ | Recursiva, sem prints de debug |
| `insereChavePromo()` | ✅ | Adaptada para offset (slide 28) |
| `novoRRN()` | ✅ | `(offset - TAM_HEADER) // TAM_PAGE` (slide 32) |
| `divide()` | ✅ | Divisão e padding corretos |
| `insereChave()` | ⚠️ | Lógica correta exceto **bug #1** (f-string) |
| `insereNaArvore()` | ✅ | Nova raiz com chave/offset/filhos corretos (slide 34) |
| `criaArvore()` | ✅ | Loop leitura + inserção |
| `criaIndice()` | ✅ | Cabeçalho, criação, atualização raiz |
| `busca()` | ⚠️ | Funcional, mas abre `btree.dat` separadamente (**bug #4**) |
| `modo_b()` | ✅ | |
| `modo_e()` | ⚠️ | Estrutura OK, mas `insere()` incompleta e `busca()` não usa o handle aberto |
| `modo_p()` | ✅ | Verifica existência de `btree.dat` |

---

## 📋 Ordem de prioridade

1. 🔴 **Bug #1** — Corrigir f-string da `ValueError` (1 caractere: adicionar `"` antes de `duplicada`)
2. 🔴 **Bug #2 + #3** — Implementar `insere()` com a lógica completa e assinatura correta
3. 🔴 **Bug #5** — Implementar `imprimirArvoreB()`
4. 🟠 **Bug #4** — Refatorar `busca()` para receber `arqBTree` como parâmetro (evitar conflito com inserções)
5. 🟡 **Ajustes menores** — docstring, mensagem hardcoded
