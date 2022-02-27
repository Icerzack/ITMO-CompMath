INPUT = "input.txt"


def read_from_file():
    with open(INPUT, 'r', encoding='utf-8') as input:
        try:
            matrix = []
            number = int(input.readline())
            lines = input.readlines()
            for r in lines:
                row = []
                coefs = r.strip().split()
                for coef in coefs:
                    row.append(float(coef))
                if len(row) != (number + 1):
                    raise ValueError
                matrix.append(row)
            if len(matrix) != number:
                raise ValueError
        except ValueError:
            print("Неверно составлен файл.")
            return None
    return matrix


def read_from_console():
    while (True):
        n = int(input("Размерность матрицы: "))
        if n <= 0:
            print("Порядок > 0!")
        elif n > 20:
            print("Порядок <= 20!")
        else:
            break
    matrix = []
    print("Коэффициенты матрицы (через пробел): ")
    try:
        for i in range(n):
            row = []
            coefs = input().strip().split()
            for coef in coefs:
                row.append(float(coef))
            if len(row) != (n + 1):
                raise ValueError
            matrix.append(row)
    except ValueError:
        print("Неверно введены данные.")
        return None
    return matrix


def solve_minor(matrix, i, j):
    n = len(matrix)
    return [[matrix[row][col] for col in range(n) if col != j] for row in range(n) if row != i]


def solve_det(matrix):
    # Нахождение определителя матрицы
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    current_sign = 1
    for i in range(n):
        det += current_sign * matrix[0][i] * solve_det(solve_minor(matrix, 0, i))
        current_sign *= -1
    return det


def solve_advanced_Gauss(matrix):
    # Реализация метода Гаусса с выбором главного элемента по столбцам
    n = len(matrix)
    det = solve_det(matrix)
    if det == 0:
        return None

    # Прямой ход
    for i in range(n):
        # Поиск максимального элемента в столбце
        index_of_col_max_value = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[index_of_col_max_value][i]):
                index_of_col_max_value = j

        # Перестановка строк
        if index_of_col_max_value != i:
            for j in range(n + 1):
                matrix[i][j], matrix[index_of_col_max_value][j] = matrix[index_of_col_max_value][j], matrix[i][j]

        # Исключение i-ого неизвестного
        for k in range(i + 1, n):
            coefficient = matrix[k][i] / matrix[i][i]
            for j in range(i, n + 1):
                matrix[k][j] -= coefficient * matrix[i][j]

    # Обратный ход
    roots = [0] * n
    for i in range(n - 1, -1, -1):
        calculated_part = 0

        for j in range(i + 1, n):
            calculated_part += matrix[i][j] * roots[j]

        roots[i] = (matrix[i][n] - calculated_part) / matrix[i][i]

    # Вычисление невязок
    residuals = [0] * n
    for i in range(n):
        calculated_part = 0

        for j in range(n):
            calculated_part += matrix[i][j] * roots[j]

        residuals[i] = calculated_part - matrix[i][n]

    return det, matrix, roots, residuals


# --------------------------------------------------------------------------
# main part
# --------------------------------------------------------------------------
print("Введите 'f' для выбора матрицы из файла или 'k' для того, чтобы ввести матрицу с консоли: ", end="")
data_entry_method = input("")

while (data_entry_method != 'f') and (data_entry_method != 'k'):
    print("Введите 'f' для выбора матрицы из файла или 'k' для того, чтобы ввести матрицу с консоли: ", end="")
    data_entry_method = input("")

if data_entry_method == 'f':
    matrix = read_from_file()
elif data_entry_method == 'k':
    matrix = read_from_console()

if matrix is None:
    print("При считывании матрицы произошла ошибка!")
    exit()

answer = solve_advanced_Gauss(matrix)
if answer is None:
    print("\nСистема не имеет решение или имеет бесконечное множество решений")
    exit()

det, result_matrix, roots, residuals = answer

print("\nОпределитель: ", end="")
print(det)

print("\nТреугольная матрица:")
for row in result_matrix:
    for value in row:
        print('{}'.format(round(value, 3)), end='\t')
    print()

print("\nВектор неизвестных:")
for root in roots:
    print(root)

print("\nВектор невязок:")
for residual in residuals:
    print('{}'.format(round(residual, 32)))
