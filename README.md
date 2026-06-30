# Problema 3 — Busca de Elemento Máximo em Array Unimodal

## Grupo

- João Roberto Nogueira Menna Barreto
- Daniel Ramos Maia
- Thiago Silva Leite
- Ramon Falcão de Souza Oliveira
- Juan Victor Sequeira Santos

**Módulo 2: Conjuntos Totalmente Ordenados & Busca**

Disciplina: Matemática Discreta & Verificação Formal de Programas  
Prof. Edjard Mota — Instituto de Computação / UFAM — 2026

---

## 1. Especificação

| Item | Definição |
|------|-----------|
| **Pré-condição** | `A` cresce estritamente até um pico e decresce estritamente a partir dele (array *unimodal*, com `len(A) >= 1`). |
| **Pós-condição** | Retorna `A[k]`, onde `k` é o índice do pico — o elemento **máximo** do array. |
| **Função variante** | `V(low, high) = high - low`, que deve decrescer estritamente em direção ao limite `0`. |

**Data Set**

```
A = [1, 3, 8, 12, 4, 2]  =>  12
A = [10, 20, 5]          =>  20
```

---

## 2. Fundamentação teórica

O Módulo 2 ancora o algoritmo em duas propriedades de relações de ordem, no
sentido formal de Mendelson, *Introduction to Mathematical Logic*.

### 2.1. Ordem total e tricotomia

Uma **ordem total (reflexiva)** é uma ordem parcial em que, para quaisquer `x`
e `y` do campo da relação, vale `x = y`, ou `x R y`, ou `y R x`. A relação `<`
sobre os inteiros é o exemplo canônico de ordem total; `<=` é a ordem total
reflexiva associada (Mendelson, Introdução, def. de *total order*).

Essa propriedade — a **tricotomia** — é o que torna a busca correta: ao comparar
`A[mid]` com `A[mid+1]`, exatamente uma das três relações vale. Cada ramo do
`if` usa essa decisão para **descartar metade** do subespaço linear:

- `A[mid] < A[mid+1]` → ainda estamos na **subida**; o pico está estritamente à
  direita de `mid`, logo `mid` não pode ser o pico.
- caso contrário → estamos na **descida** (ou exatamente no pico); o pico está em
  `mid` ou à esquerda, então `mid` permanece candidato.

### 2.2. Boa-ordenação e terminação

Os naturais `N0` com a relação `<` formam um conjunto **bem-ordenado**: toda ordem
total cujo todo subconjunto não-vazio possui *menor elemento* é uma boa-ordenação,
e `<` sobre os inteiros não-negativos é o exemplo dado por Mendelson. A todo
conjunto bem-ordenado está associado um **princípio de indução completa**.

É isso que justifica a função variante: como `V = high - low` assume valores em
`N0` e **não pode decrescer infinitamente** dentro de um conjunto bem-ordenado, se
provarmos que cada iteração faz `V` decrescer estritamente, a terminação está
garantida — não há sequência infinita estritamente decrescente em `N0`.

### 2.3. Indução / invariante de loop

O invariante de loop é a tradução operacional do princípio de indução: provamos
que ele vale no **caso base** (inicialização) e que se preserva da iteração `k`
para `k+1` (**passo indutivo / manutenção**). Aqui:

```
I(low, high):  0 <= low <= high <= len(A) - 1
               e o pico de A está contido em A[low .. high]
```

Combinando invariante (correção parcial) + variante (terminação) obtemos a
**correção total** do algoritmo.

---

## 3. O bug do código original

```python
def find_peak_broken(A: list) -> int:
    low, high = 0, len(A) - 1
    while low < high:
        mid = (low + high) // 2
        if A[mid] < A[mid + 1]:
            low = mid          # BUG
        else:
            high = mid
    return A[low]
```

### Causa-raiz (razão aritmética / geométrica)

A divisão inteira faz `mid = (low + high) // 2` **arredondar para baixo**. Quando
o intervalo encolhe para dois elementos adjacentes, isto é, `high = low + 1`,
temos:

```
mid = (low + (low + 1)) // 2 = (2*low + 1) // 2 = low
```

Se nesse ponto `A[mid] < A[mid+1]` for verdadeiro, o código executa
`low = mid = low` — **`low` não muda e `high` não muda**. A função variante
`V = high - low` permanece em `1` indefinidamente: ela **estagna** em vez de
decrescer, violando a condição de terminação sobre o conjunto bem-ordenado `N0`.
O resultado é um **loop infinito**.

Geometricamente: o algoritmo "trava" no degrau final da subida porque o ponto
médio coincide com o extremo esquerdo da janela, e a regra `low = mid` é incapaz
de empurrar a fronteira para frente.

> Esse defeito ocorre nos **dois** casos do Data Set:
> `[1,3,8,12,4,2]` trava em `(low=2, high=3)` e `[10,20,5]` trava em `(low=0, high=1)`.

### A correção

```python
if A[mid] < A[mid + 1]:
    low = mid + 1     # subida estrita: mid nunca é o pico
else:
    high = mid
```

Como `A[mid] < A[mid+1]` garante que `mid` **não** é o pico, podemos descartá-lo
com segurança fazendo `low = mid + 1`. Isso assegura `nova_variante < velha_variante`
em todo passo, restaurando a terminação sem afetar a correção parcial.

---

## 4. Instrumentação por asserções (Roteiro)

O arquivo [`problema_03.py`](./problema_03.py) implementa, na função
`find_peak_instrumentado`, os passos exigidos pelo *Roteiro de Diretrizes*:

| Passo do roteiro | Asserção no código |
|---|---|
| **1. Pré-condição** | `assert len(A) >= 1` |
| **2. Inicialização (caso base)** | `assert 0 <= low <= high <= len(A)-1` antes do `while` |
| **4a. Variante + limite inferior** | `velha_variante = high - low; assert velha_variante >= 0` |
| **3. Manutenção (passo indutivo)** | `assert 0 <= low <= high <= len(A)-1` ao fim do corpo |
| **4b. Decremento estrito** | `assert nova_variante < velha_variante` |
| **5. Pós-condição (dedução final)** | `assert` que os vizinhos de `A[low]` não o excedem |

---

## 5. Passo 6 — Execução e análise da falha

Rodando o módulo (`python3 problema_03.py`) sobre o Data Set, a versão
instrumentada bugada falha exatamente na **Asserção de Decremento**:

```
Data Set  A = [1, 3, 8, 12, 4, 2]   (esperado: 12)
  -> AssertionError: Loop em execucao infinita (sem progresso)!

Data Set  A = [10, 20, 5]   (esperado: 20)
  -> AssertionError: Loop em execucao infinita (sem progresso)!
```

**Asserção que estoura:** `assert nova_variante < velha_variante`
(*Asserção de Progresso e Limite — função variante*).

**Razão aritmética do estouro:** com `high = low + 1`, o ponto médio satisfaz
`mid = low`; a atribuição `low = mid` deixa `low` e `high` inalterados, então
`nova_variante == velha_variante` (não decresce). A asserção de progresso detecta
a estagnação da variante no conjunto bem-ordenado `N0`, que é precisamente a
manifestação formal do loop infinito.

A versão corrigida (`find_peak_corrigido`) passa por todas as asserções e retorna
os valores esperados:

```
A = [1, 3, 8, 12, 4, 2] -> 12  [OK]
A = [10, 20, 5]         -> 20  [OK]
```

---

## 6. Como executar

```bash
python3 problema_03.py
```

---

## 7. Referências

- MENDELSON, Elliott. *Introduction to Mathematical Logic*. (Ordem total,
  tricotomia, relação de boa-ordenação e princípio de indução completa.)
- Material da disciplina de Matemática Discreta — Prof. Edjard Mota, IComp/UFAM.
