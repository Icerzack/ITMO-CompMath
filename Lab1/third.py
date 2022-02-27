# Importing NumPy Library
import numpy as np
import sys
import copy

INPUT = "input.txt"
A = []
residuals = []


def print_data(mat):
    for i in range(number):
        print('X%d = %0.2f' % (i, mat[i]), end='\t')
    print()


def print_matrix(mat):
    for row in mat:
        for value in row:
            print('{}'.format(round(value, 3)), end='\t')
        print()


def check_matrix(det):
    if det == 0:
        print("\nСистема не имеет решение или имеет бесконечное множество решений!")
        sys.exit()


def read_from_file():
    with open(INPUT, 'r', encoding='utf-8') as input:
        try:
            temp = []
            global number
            number = int(input.readline())
            lines = input.readlines()
            for r in lines:
                row = []
                coefs = r.strip().split()
                counter = -1
                for coef in coefs:
                    counter += 1
                    row.append(float(coef))
                    if counter == (number - 1):
                        A.append(copy.copy(row))
                if len(row) != (number + 1):
                    raise ValueError
                temp.append(row)
            if len(temp) != number:
                raise ValueError
        except ValueError:
            print("\nНеверно составлен файл.")
            return None
    return temp


def read_from_console():
    while True:
        n = int(input("\nРазмерность матрицы: "))
        if n <= 0:
            print("\nПорядок > 0!")
        elif n > 20:
            print("\nПорядок <= 20!")
        else:
            break
    temp = []
    print("\nКоэффициенты матрицы (через пробел): ")
    try:
        for i in range(n):
            row = []
            coefs = input().strip().split()
            for coef in coefs:
                row.append(float(coef))
            if len(row) != (n + 1):
                raise ValueError
            temp.append(row)
    except ValueError:
        print("\nНеверно введены данные.")
        return None
    return temp


def solve_minor(mat, i, j):
    n = len(mat)
    return [[mat[row][col] for col in range(n) if col != j] for row in range(n) if row != i]


def solve_det(mat):
    n = len(mat)
    if n == 1:
        return mat[0][0]
    det = 0
    current_sign = 1
    for i in range(n):
        det += current_sign * mat[0][i] * solve_det(solve_minor(mat, 0, i))
        current_sign *= -1
    return det


def is_singular(m):
    for i in range(len(m)):
        if not m[i][i]:
            return True
    return False


def bubble_max_row(m, col):
    max_element = m[col][col]
    max_row = col
    for i in range(col + 1, len(m)):
        if abs(m[i][col]) > abs(max_element):
            max_element = m[i][col]
            max_row = i
    if max_row != col:
        m[col], m[max_row] = m[max_row], m[col]


def gauss_method():
    for i in range(number):
        if matrix[i][i] == 0.0:
            bubble_max_row(matrix, i)
        for j in range(i + 1, number):
            ratio = matrix[j][i] / matrix[i][i]
            for k in range(number + 1):
                matrix[j][k] = matrix[j][k] - ratio * matrix[i][k]


def back_substitution():
    roots[number - 1] = matrix[number - 1][number] / matrix[number - 1][number - 1]
    for i in range(number - 2, -1, -1):
        roots[i] = matrix[i][number]
        for j in range(i + 1, number):
            roots[i] = roots[i] - matrix[i][j] * roots[j]
        roots[i] = roots[i] / matrix[i][i]


def count_residuals():
    global residuals
    residuals = [0] * number
    for i in range(number):
        calculated_part = 0

        for j in range(number):
            calculated_part += matrix[i][j] * roots[j]

        residuals[i] = calculated_part - matrix[i][number]


while True:
    method = input("\nУкажите способ (файл - 0, консоль - 1):")
    global matrix
    if method == "0":
        matrix = read_from_file()
        break
    elif method == "1":
        matrix = read_from_console()
        break
    else:
        continue

original_matrix = copy.copy(matrix)
print("\nИсходная матрица:")
print_matrix(matrix)
roots = np.zeros(number)
print("\nОпределитель:")
det = solve_det(matrix)
check_matrix(det)
print(det)
print("\nПриведенная матрица:")
gauss_method()
print_matrix(matrix)
print("\nКорни:")
back_substitution()
print_data(roots)
print("\nВектор невязок:")
count_residuals()
print_data(residuals)

