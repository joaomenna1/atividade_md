"""
============================================================================
 Problema 3 -- Busca de Elemento Maximo em Array Unimodal
 Modulo 2: Conjuntos Totalmente Ordenados & Busca
 (versao com VERIFICACAO PREVIA DE UNIMODALIDADE integrada a pre-condicao)
============================================================================
 Disciplina : Matematica Discreta & Verificacao Formal de Programas
 Professor  : Edjard Mota -- Instituto de Computacao / UFAM
 Aluno      : Ramon Falcao de Souza Oliveira
 Data       : 2026
----------------------------------------------------------------------------
 ESPECIFICACAO
   Pre-condicao : A cresce estritamente ate um pico e decresce
                  estritamente a partir dele (array unimodal, |A| >= 1).
   Pos-condicao : retorna A[k], onde k e o indice do pico (maximo global).
   Variante     : V(low, high) = high - low  (decresce estritamente -> N0).
 Data Set
   A = [1, 3, 8, 12, 4, 2] => 12
   A = [10, 20, 5]         => 20
============================================================================

Este modulo contem:

  1. assert_unimodal         : verifica explicitamente a PRE-CONDICAO,
     ou seja, que o array e estritamente crescente ate o pico e
     estritamente decrescente depois dele (apoiado na TRICOTOMIA da
     ordem total <).

  2. find_peak_instrumentado : versao BUGADA do enunciado, instrumentada
     com asserções conforme o Roteiro. Ao rodar o Data Set, levanta um
     AssertionError na ASSERCAO DE DECREMENTO (progresso da terminacao).

  3. find_peak_corrigido     : versao CORRIGIDA, com a mesma instrumentacao.
     Passa por todo o Data Set sem levantar excecoes.
"""


# ===========================================================================
# 0) VERIFICACAO DA PRE-CONDICAO -- ARRAY UNIMODAL
#    Tras explicitamente a definicao de unimodalidade para o espaco de
#    execucao: estritamente crescente ate o pico, estritamente decrescente
#    depois. Cada comparacao usa a TRICOTOMIA da ordem total < sobre os
#    inteiros (Mendelson): entre A[i] e A[i+1] vale exatamente uma relacao.
# ===========================================================================
def assert_unimodal(A: list) -> None:
    assert len(A) >= 1, "Pre-condicao violada: array vazio!"

    # Indice do pico (maximo global). Pela ordem total dos inteiros, o
    # maximo de um conjunto finito nao-vazio existe e e unico aqui.
    max_idx = A.index(max(A))

    # Ramo crescente: A[0] < A[1] < ... < A[max_idx]
    for i in range(max_idx):
        assert A[i] < A[i + 1], f"Nao e crescente em {i}"

    # Ramo decrescente: A[max_idx] > A[max_idx+1] > ... > A[len-1]
    for i in range(max_idx, len(A) - 1):
        assert A[i] > A[i + 1], f"Nao e decrescente em {i}"

    print("OK: array e unimodal valido")


# ===========================================================================
# 1) VERSAO INSTRUMENTADA DO CODIGO BUGADO (a do enunciado)
#    -> deve estourar AssertionError ao rodar o Data Set
# ===========================================================================
def find_peak_instrumentado(A: list) -> int:
    # ---- PASSO 1: ASSERCAO DE PRE-CONDICAO ------------------------------
    # A pre-condicao agora e verificada de forma construtiva: alem de exigir
    # array nao-vazio, comprova que ele e de fato unimodal.
    assert_unimodal(A)

    low, high = 0, len(A) - 1

    # ---- PASSO 2: ASSERCAO DE INICIALIZACAO (CASO BASE) -----------------
    # Invariante I(low, high):  0 <= low <= high <= len(A)-1
    #                           e o pico de A esta contido em A[low .. high].
    assert 0 <= low <= high <= len(A) - 1, \
        "Invariante falhou na inicializacao!"

    while low < high:
        # ---- PASSO 4a: CAPTURA DA VARIANTE E LIMITE INFERIOR ------------
        velha_variante = high - low
        assert velha_variante >= 0, "Variante violou o limite inferior!"

        mid = (low + high) // 2

        # Pela TRICOTOMIA, exatamente uma relacao vale entre A[mid] e A[mid+1].
        if A[mid] < A[mid + 1]:
            low = mid          # BUG: deveria ser low = mid + 1
        else:
            high = mid

        # ---- PASSO 3: ASSERCAO DE MANUTENCAO (PASSO INDUTIVO) ----------
        assert 0 <= low <= high <= len(A) - 1, \
            "Invariante violado no corpo do loop!"

        # ---- PASSO 4b: ASSERCAO DE DECREMENTO (PROGRESSO/TERMINACAO) ----
        # O defeito se revela aqui: quando high == low + 1, mid == low,
        # entao low = mid == low e a variante NAO decresce.
        nova_variante = high - low
        assert nova_variante < velha_variante, \
            "Loop em execucao infinita (sem progresso)!"

    # ---- PASSO 5: ASSERCAO DE POS-CONDICAO (DEDUCAO FINAL) -------------
    pico = A[low]
    assert (low == 0 or A[low - 1] < pico) and \
           (low == len(A) - 1 or A[low + 1] < pico), \
        "A pos-condicao falhou na terminacao!"
    return pico


# ===========================================================================
# 2) VERSAO CORRIGIDA (mesma instrumentacao, passa em todo o Data Set)
# ===========================================================================
def find_peak_corrigido(A: list) -> int:
    # ---- PASSO 1: ASSERCAO DE PRE-CONDICAO ------------------------------
    assert_unimodal(A)

    low, high = 0, len(A) - 1

    # ---- PASSO 2: ASSERCAO DE INICIALIZACAO (CASO BASE) -----------------
    assert 0 <= low <= high <= len(A) - 1, \
        "Invariante falhou na inicializacao!"

    while low < high:
        # ---- PASSO 4a: CAPTURA DA VARIANTE E LIMITE INFERIOR ------------
        velha_variante = high - low
        assert velha_variante >= 0, "Variante violou o limite inferior!"

        mid = (low + high) // 2

        if A[mid] < A[mid + 1]:
            # Subida estrita: o pico esta a DIREITA de mid; mid nunca e pico.
            low = mid + 1      # CORRECAO: garante progresso estrito
        else:
            # Descida: o pico esta em mid ou a esquerda; mid segue candidato.
            high = mid

        # ---- PASSO 3: ASSERCAO DE MANUTENCAO (PASSO INDUTIVO) ----------
        assert 0 <= low <= high <= len(A) - 1, \
            "Invariante violado no corpo do loop!"

        # ---- PASSO 4b: ASSERCAO DE DECREMENTO (PROGRESSO/TERMINACAO) ----
        nova_variante = high - low
        assert nova_variante < velha_variante, \
            "Loop em execucao infinita (sem progresso)!"

    # ---- PASSO 5: ASSERCAO DE POS-CONDICAO (DEDUCAO FINAL) -------------
    pico = A[low]
    assert (low == 0 or A[low - 1] < pico) and \
           (low == len(A) - 1 or A[low + 1] < pico), \
        "A pos-condicao falhou na terminacao!"
    return pico


# ===========================================================================
# PASSO 6: EXECUCAO E ANALISE DE FALHA
# ===========================================================================
if __name__ == "__main__":
    import sys
    import traceback

    DATA_SET = [
        ([1, 3, 8, 12, 4, 2], 12),
        ([10, 20, 5], 20),
    ]

    print("=" * 68)
    print(" PASSO 6 -- VERSAO INSTRUMENTADA (BUGADA): deve falhar")
    print("=" * 68)
    for A, esperado in DATA_SET:
        print(f"\nData Set  A = {A}   (esperado: {esperado})")
        try:
            r = find_peak_instrumentado(list(A))
            print(f"  -> retornou {r} (NENHUMA falha detectada)")
        except AssertionError as e:
            linha = traceback.extract_tb(sys.exc_info()[2])[-1].lineno
            print(f"  -> AssertionError na linha {linha}: {e}")

    print("\n" + "=" * 68)
    print(" VERSAO CORRIGIDA: deve passar em todo o Data Set")
    print("=" * 68)
    for A, esperado in DATA_SET:
        r = find_peak_corrigido(list(A))
        status = "OK" if r == esperado else "ERRO"
        print(f"  A = {str(A):<18} -> {r}  (esperado {esperado})  [{status}]")

    print("\n" + "=" * 68)
    print(" TESTE EXTRA -- rejeicao de array NAO-unimodal")
    print("=" * 68)
    try:
        find_peak_corrigido([1, 3, 2, 5, 1])
    except AssertionError as e:
        print(f"  -> AssertionError (esperado): {e}")
