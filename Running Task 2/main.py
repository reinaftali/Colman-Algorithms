def belongs_to_language(grammar, word):
    n = len(word)
    variables = list(set(rule[0] for rule in grammar))
    var_to_index = {v: i for i, v in enumerate(variables)}

    T = [[[False for _ in range(len(variables))] for _ in range(n)] for _ in range(n)]

    # Initialize base case
    for i, char in enumerate(word):
        for rule in grammar:
            if len(rule) == 2 and rule[1] == char:
                T[i][i][var_to_index[rule[0]]] = True

    # Fill the table
    for length in range(2, n + 1):
        for start in range(n - length + 1):
            end = start + length - 1
            for rule in grammar:
                if len(rule) == 3:
                    X, Y, Z = rule
                    X_index = var_to_index[X]
                    Y_index = var_to_index[Y]
                    Z_index = var_to_index[Z]
                    for split in range(start, end):
                        if T[start][split][Y_index] and T[split + 1][end][Z_index]:
                            T[start][end][X_index] = True

    return T[0][n - 1][var_to_index['S']]


# Example grammar
grammar = [
    ('S', 'A', 'X'), ('S', 'B', 'Y'), ('S', 'S', 'S'), ('S', 'A', 'B'), ('S', 'B', 'A'),
    ('X', 'S', 'B'), ('Y', 'S', 'A'), ('A', 'a'), ('B', 'b')
]

# Test cases
test_words = [
    'a' * 15 + 'b' * 15,
    'ab' * 15,
    'abba' * 7 + 'ab'
]

for word in test_words:
    result = belongs_to_language(grammar, word)
    print(f"Word: {word}")
    print(f"Length: {len(word)}")
    print(f"Belongs to language: {result}\n")

