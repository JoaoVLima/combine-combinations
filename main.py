import itertools
import time
from functools import wraps


def convert_nanoseconds(ns):
    # Constants for time conversions
    ns_per_us = 1_000
    ns_per_ms = 1_000_000
    ns_per_s = 1_000_000_000
    ns_per_min = 60 * ns_per_s
    ns_per_hour = 60 * ns_per_min

    if ns < ns_per_us:
        return f"{ns}ns"
    elif ns < ns_per_ms:
        us = ns / ns_per_us
        return f"{us:.3f}us"
    elif ns < ns_per_s:
        ms = ns / ns_per_ms
        return f"{ms:.3f}ms"
    elif ns < ns_per_min:
        s = ns / ns_per_s
        return f"{s:.3f}s"
    elif ns < ns_per_hour:
        minutes = ns // ns_per_min
        seconds = (ns % ns_per_min) // ns_per_s
        return f"{minutes}m {seconds}s"
    else:
        hours = ns // ns_per_hour
        minutes = (ns % ns_per_hour) // ns_per_min
        seconds = (ns % ns_per_min) // ns_per_s
        return f"{hours}h {minutes}m {seconds}s"


def timer_ns(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Executing Function '{func.__name__}'...")
        start_time = time.perf_counter_ns()
        result = func(*args, **kwargs)
        end_time = time.perf_counter_ns()
        elapsed_time = end_time - start_time
        print(f"Executing Function '{func.__name__}' took {convert_nanoseconds(elapsed_time)} to complete")
        return result

    return wrapper


@timer_ns
def combinations(n, p):
    result = {}
    result['size'] = n_combinations(n, p)
    for combination in generate_combinations(list(range(1, n + 1)), p):
        first_10 = str(combination[0:10])
        if first_10 not in result:
            result[first_10] = []
        result[first_10].append(combination)
    return result


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


def subset(s1, s2):
    result = []

    # Percorre cada lista em s1
    for sublist1 in s1:
        for sublist2 in s2:
            # Verifica se todos os elementos de sublist2 estão em sublist1
            if all(elem in sublist1 for elem in sublist2):
                result.append(sublist1)
                break

    return result


@timer_ns
def find_subsets(dict1, dict2):
    result_dict = {}
    result_dict['size'] = 0

    # Itera sobre cada chave em dict1
    for key in dict1:
        if key in dict2 and key != 'size':
            s1_lists = dict1[key]
            s2_lists = dict2[key]
            # Chama a função subset para as listas correspondentes e armazena o resultado
            result_dict[key] = subset(s1_lists, s2_lists)
            result_dict['size'] += len(result_dict[key])

    return result_dict


def main():
    s15 = combinations(25, 15)
    print(f"s15: {s15['size']}")
    s14 = combinations(25, 14)
    print(f"s14: {s14['size']}")
    s13 = combinations(25, 13)
    print(f"s13: {s13['size']}")
    s12 = combinations(25, 12)
    print(f"s12: {s12['size']}")
    s11 = combinations(25, 11)
    print(f"s11: {s11['size']}")

    sb15_14 = find_subsets(s15, s14)
    print(f"sb15_14: {sb15_14['size']}")
    sb15_13 = find_subsets(s15, s13)
    print(f"sb15_13: {sb15_13['size']}")
    sb15_12 = find_subsets(s15, s12)
    print(f"sb15_12: {sb15_12['size']}")
    sb15_11 = find_subsets(s15, s11)
    print(f"sb15_11: {sb15_11['size']}")

    print(f"lotofacil: R$ {sum([sb15_14['size'],sb15_13['size'],sb15_12['size'],sb15_11['size']])*3}")


if __name__ == '__main__':
    main()
