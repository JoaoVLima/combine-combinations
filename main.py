import itertools


def combinations(n, p):
    porcentagens = {}
    n_combinacoes = n_combinations(n, p)
    porcentagens['n_combinacoes'] = n_combinacoes
    numero_iniciador = 1
    acc = 0
    porcentagens[numero_iniciador] = acc
    for combination in generate_combinations(list(range(1, n+1)), p):
        if numero_iniciador != combination[0]:
            porcentagens[numero_iniciador] = (porcentagens[numero_iniciador] / n_combinacoes) * 100
            numero_iniciador = combination[0]
            porcentagens[numero_iniciador] = acc
        porcentagens[numero_iniciador] += 1

    return porcentagens


def next_combination(comb, n, p):
    # Percorre a combinação de trás para frente
    for i in reversed(range(p)):
        # Verifica se é possível incrementar o indice atual
        if comb[i] != i + n - p:
            break
    else:
        # Se não for possível incrementar, retorna False
        return False

    # Incrementa o indice atual
    comb[i] += 1
    # Atualiza os valores seguintes na combinação
    for j in range(i + 1, p):
        comb[j] = comb[j - 1] + 1
    return True

# Ordem Lexicografica
def generate_combinations(N, p):
    # n é o tamanho da lista N
    n = len(N)
    # Se p for maior que n, não é possível gerar combinações
    if p > n:
        return

    comb = list(range(p))
    while True:
        # Gera a combinação
        yield [N[i] for i in comb]
        # Prepara o comb para a próxima combinação, se não for possível, termina o loop
        if not next_combination(comb, n, p):
            break


def factorial(n):
    # n!
    acc = 1
    for i in range(1, n + 1):
        acc *= i
    return acc


def n_combinations(n, p):
    # n! / p! * (n-p)!
    return factorial(n) / (factorial(p) * factorial(n - p))


def main():
    n = 25
    p = 15

    import time
    a = time.time_ns()
    print(combinations(25, 15))
    print('TEMPO - ', time.time_ns()-a)
    a = time.time_ns()
    list(itertools.combinations(list(range(1, 26)), 15))
    print('TEMPO - ', time.time_ns()-a)


if __name__ == '__main__':
    main()
