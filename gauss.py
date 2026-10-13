from sys import argv

class Matrix:
    contents: list[float] = []   

    def __init__(self, content: list[float]):
        self.contents = content

    def at(self, fila: int, col: int) -> float:
        return self.contents[fila * 4 + col]


class Vec3:
    x: float; y: float; z: float

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0


class Parametric:
    x1: float; x2: float; y1: float; y2: float

    def __init__(self):
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0


def read_from_file(path: str) -> list[int]:
    numbers = []
    with open(path) as f:
        for x in f:
            tok = x.split(' ')
            for i in tok:
                numbers.append(float(i))
    return numbers


def simplify(mat: Matrix) -> Matrix:
    content = []
    for i in range(4):
        content.append(mat.at(0, i))
    for i in range(4):
        content.append(mat.at(1, 0) * mat.at(0, i) - mat.at(0, 0) * mat.at(1, i))

    k = mat.at(1, 0) * mat.at(0, 1) - mat.at(0, 0) * mat.at(1, 1)
    m = mat.at(2, 0) * mat.at(0, 1) - mat.at(0, 0) * mat.at(2, 1)

    content.append(0)
    content.append(0)
    content.append(m * (mat.at(1, 0) * mat.at(0, 2) - mat.at(0, 0) * mat.at(1, 2)) - k * (mat.at(2, 0) * mat.at(0, 2) - mat.at(0, 0) * mat.at(2, 2)))
    content.append(m * (mat.at(1, 0) * mat.at(0, 3) - mat.at(0, 0) * mat.at(1, 3)) - k * (mat.at(2, 0) * mat.at(0, 3) - mat.at(0, 0) * mat.at(2, 3)))

    result = Matrix(content)
    return result


def has_solution(mat: Matrix) -> bool:
    return not(mat.at(2, 2) == 0 and mat.at(2, 3) != 0)


def has_one_solution(mat: Matrix) -> bool:
    return mat.at(2, 2) != 0 and mat.at(2, 3) != 0


def get_single_solution(mat: Matrix) -> Vec3:
    solution = Vec3()
    solution.z = mat.at(2, 3) / mat.at(2, 2)
    solution.y = (mat.at(1, 3) - solution.z * mat.at(1, 2)) / mat.at(1, 1)
    solution.x = (mat.at(0, 3) - solution.z * mat.at(0, 2) - solution.y * mat.at(0, 1)) / mat.at(0, 0)
    return solution


def get_inf_solutions(mat: Matrix) -> Parametric:
    solution = Parametric()
    solution.y1 = mat.at(1, 3) / mat.at(1, 1)
    solution.y2 = - mat.at(1, 2) / mat.at(1, 1)

    solution.x1 = mat.at(0, 3) / mat.at(0, 0) - mat.at(0, 1) * mat.at(1, 3) / (mat.at(1, 1) * mat.at(0, 0))
    solution.x2 = (mat.at(0, 1) * mat.at(1, 2) - mat.at(0, 2) * mat.at(1, 1)) / (mat.at(1, 1) * mat.at(0, 0))

    return solution


def print_solutions(mat: Matrix):
    if not has_solution(mat):
        print("El sistema no tiene solución")
    elif has_one_solution(mat):
        sol = get_single_solution(mat)
        print("El sistema tiene una solución:")
        print("x = ", sol.x, ", y = ", sol.y, ", z = ", sol.z)
    else:
        sol = get_inf_solutions(mat)
        print("El sistema tiene infinitas soluciones:")
        print("x = ", sol.x1, " + ", sol.x2, " * \u03BB, y = ", sol.y1, " + ", sol.y2, " * \u03BB, z = \u03BB")


def main():
    if len(argv) < 2:
        print("No hay suficientes argumentos")
        print("Escribe el nombre un archivo con tu matriz de este directorio")
        print("Ejemplo: python3 gauss.py mi_matriz.txt")
        return
    equation = Matrix(read_from_file(argv[1]))
    simp = simplify(equation)
    print_solutions(simp)


main()