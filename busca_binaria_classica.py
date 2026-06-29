"""
============================================================================
 Busca Binaria Classica (busca de um valor em vetor ordenado)
 Modulo 2: Conjuntos Totalmente Ordenados & Busca
============================================================================
 Disciplina : Matematica Discreta & Verificacao Formal de Programas
 Professor  : Edjard Mota -- Instituto de Computacao / UFAM
 Aluno      : Ramon Falcao de Souza Oliveira
 Data       : 2026
----------------------------------------------------------------------------
 ESPECIFICACAO
   Pre-condicao : A esta ordenado de forma nao-decrescente (Ordem Total).
   Pos-condicao : retorna idx tal que A[idx] == v, ou -1 se v ausente.
   Variante     : V(lo, hi) = hi - lo  (decresce estritamente -> N0).
 Data Set
   A = [10, 20, 30, 40, 50], v = 40 => idx = 3
   A = [10, 20, 30, 40, 50], v = 25 => idx = -1
============================================================================

IDEIA DA BUSCA BINARIA
----------------------
Procuramos um valor v num vetor ORDENADO. A cada passo olhamos o ponto
medio mid e, pela TRICOTOMIA da ordem total < sobre os inteiros (Mendelson),
exatamente uma das tres relacoes vale entre A[mid] e v:

  - A[mid] == v  -> achamos: retorna mid.
  - A[mid] <  v  -> v (se existe) esta a DIREITA. Descarta [lo..mid]: lo = mid + 1
  - A[mid] >  v  -> v (se existe) esta a ESQUERDA. Descarta [mid..hi]: hi = mid - 1

Cada comparacao elimina METADE do espaco restante, dando custo O(log n).
A funcao variante V = hi - lo vive no conjunto bem-ordenado N0 e decresce
estritamente a cada passo, o que garante a TERMINACAO (nao existe sequencia
infinita estritamente decrescente em N0).

Este modulo contem:
  1. assert_ordenado            : verifica a PRE-CONDICAO (vetor ordenado).
  2. busca_binaria_instrumentado: BUSCA BINARIA bugada + asserções do Roteiro
     -> estoura AssertionError ao rodar o Data Set.
  3. busca_binaria_corrigida    : BUSCA BINARIA correta, mesma instrumentacao.
"""


# ===========================================================================
# 0) VERIFICACAO DA PRE-CONDICAO -- VETOR ORDENADO
#    A Ordem Total < garante que faz sentido falar em "esquerda/direita"
#    de mid: o vetor deve ser nao-decrescente.
# ===========================================================================
def assert_ordenado(A: list) -> None:
    for i in range(len(A) - 1):
        assert A[i] <= A[i + 1], f"Nao ordenado em {i}"
    print("OK: vetor esta ordenado")


# ===========================================================================
# 1) BUSCA BINARIA INSTRUMENTADA -- VERSAO BUGADA
#    -> deve estourar AssertionError ao rodar o Data Set
# ===========================================================================
def busca_binaria_instrumentado(A: list, v: int) -> int:
    # ---- PASSO 1: ASSERCAO DE PRE-CONDICAO ------------------------------
    assert_ordenado(A)

    lo, hi = 0, len(A) - 1

    # ---- PASSO 2: ASSERCAO DE INICIALIZACAO (CASO BASE) -----------------
    # Invariante I(lo, hi): 0 <= lo  e  hi <= len(A)-1  e, se v esta em A,
    #                       entao v esta em A[lo .. hi].
    assert 0 <= lo and hi <= len(A) - 1, \
        "Invariante falhou na inicializacao!"

    while lo <= hi:
        # ---- PASSO 4a: CAPTURA DA VARIANTE E LIMITE INFERIOR ------------
        velha_variante = hi - lo
        assert velha_variante >= 0, "Variante violou o limite inferior!"

        # nucleo da BUSCA BINARIA: ponto medio
        mid = (lo + hi) // 2

        if A[mid] == v:
            # ---- PASSO 5: POS-CONDICAO (saida por sucesso) -------------
            assert A[mid] == v, "Pos-condicao: indice retornado nao casa com v!"
            return mid
        elif A[mid] < v:
            lo = mid           # BUG off-by-one classico de busca binaria:
                               # mid ja foi testado e e diferente de v, mas
                               # lo=mid NAO o descarta -> quando hi=lo+1 o
                               # mid se repete e a janela nao encolhe.
                               # O correto seria lo = mid + 1.
        else:
            hi = mid - 1

        # ---- PASSO 3: ASSERCAO DE MANUTENCAO (PASSO INDUTIVO) ----------
        assert 0 <= lo and hi <= len(A) - 1, \
            "Invariante violado no corpo do loop!"

        # ---- PASSO 4b: ASSERCAO DE DECREMENTO (PROGRESSO/TERMINACAO) ----
        nova_variante = hi - lo
        assert nova_variante < velha_variante, \
            "Loop em execucao infinita (sem progresso)!"

    # ---- PASSO 5: ASSERCAO DE POS-CONDICAO (saida por ausencia) --------
    assert v not in A, "Pos-condicao: retornou -1 mas v existe em A!"
    return -1


# ===========================================================================
# 2) BUSCA BINARIA CORRIGIDA (mesma instrumentacao, passa no Data Set)
# ===========================================================================
def busca_binaria_corrigida(A: list, v: int) -> int:
    # ---- PASSO 1: ASSERCAO DE PRE-CONDICAO ------------------------------
    assert_ordenado(A)

    lo, hi = 0, len(A) - 1

    # ---- PASSO 2: ASSERCAO DE INICIALIZACAO (CASO BASE) -----------------
    assert 0 <= lo and hi <= len(A) - 1, \
        "Invariante falhou na inicializacao!"

    while lo <= hi:
        # ---- PASSO 4a: CAPTURA DA VARIANTE E LIMITE INFERIOR ------------
        velha_variante = hi - lo
        assert velha_variante >= 0, "Variante violou o limite inferior!"

        mid = (lo + hi) // 2

        if A[mid] == v:
            assert A[mid] == v, "Pos-condicao: indice retornado nao casa com v!"
            return mid
        elif A[mid] < v:
            lo = mid + 1       # CORRECAO: descarta mid (ja testado) e a esquerda
        else:
            hi = mid - 1       # descarta mid (ja testado) e a direita

        # ---- PASSO 3: ASSERCAO DE MANUTENCAO (PASSO INDUTIVO) ----------
        assert 0 <= lo and hi <= len(A) - 1, \
            "Invariante violado no corpo do loop!"

        # ---- PASSO 4b: ASSERCAO DE DECREMENTO (PROGRESSO/TERMINACAO) ----
        nova_variante = hi - lo
        assert nova_variante < velha_variante, \
            "Loop em execucao infinita (sem progresso)!"

    # ---- PASSO 5: ASSERCAO DE POS-CONDICAO (saida por ausencia) --------
    assert v not in A, "Pos-condicao: retornou -1 mas v existe em A!"
    return -1


# ===========================================================================
# PASSO 6: EXECUCAO E ANALISE DE FALHA
# ===========================================================================
if __name__ == "__main__":
    import sys
    import traceback

    DATA_SET = [
        ([10, 20, 30, 40, 50], 40, 3),
        ([10, 20, 30, 40, 50], 25, -1),
        ([10, 20, 30, 40, 50], 50, 4),
    ]

    print("=" * 68)
    print(" PASSO 6 -- BUSCA BINARIA INSTRUMENTADA (BUGADA): deve falhar")
    print("=" * 68)
    for A, v, esperado in DATA_SET:
        print(f"\nData Set  A = {A}, v = {v}   (esperado: {esperado})")
        try:
            r = busca_binaria_instrumentado(list(A), v)
            print(f"  -> retornou {r} (NENHUMA falha detectada)")
        except AssertionError as e:
            linha = traceback.extract_tb(sys.exc_info()[2])[-1].lineno
            print(f"  -> AssertionError na linha {linha}: {e}")

    print("\n" + "=" * 68)
    print(" BUSCA BINARIA CORRIGIDA: deve passar em todo o Data Set")
    print("=" * 68)
    for A, v, esperado in DATA_SET:
        r = busca_binaria_corrigida(list(A), v)
        status = "OK" if r == esperado else "ERRO"
        print(f"  A = {A}, v = {v:<3} -> idx = {r}  (esperado {esperado})  [{status}]")
