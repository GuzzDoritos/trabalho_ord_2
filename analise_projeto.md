# Análise do Projeto — Árvore-B (Trabalho 2) — v6

> **Source-of-truth:** `EspecificacaoTrab2-ES.pdf` (especificação) e `Aula 11 - Arvore B - Busca e Insercao (1).pdf` (pseudocódigo da aula)
>
> **Última atualização:** 2026-06-18 — código relido integralmente


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

2. 🔴 **Bug #2** — Implementar `insere()` com assinatura correta e conectar no `main.py`
3. 🔴 **Bug #3** — Implementar `imprimirArvoreB()`
