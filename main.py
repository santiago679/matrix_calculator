import datetime
import random

class Matrix:
    def __init__(self, data):
        if not data or not data[0]:
            raise ValueError("La matriz no puede estar vacía.")
        # Validar que todas las filas tengan la misma longitud
        columns = len(data[0])
        for row in data:
            if len(row) != columns:
                raise ValueError("Todas las filas deben tener la misma cantidad de columnas.")
        self.data = [row[:] for row in data]
        self.rows = len(self.data)
        self.columns = len(self.data[0])

    def __str__(self):
        return "\n".join("\t".join(f"{x:8.4f}" for x in row) for row in self.data)

    def _validate_size(self, other):
        if self.rows != other.rows or self.columns != other.columns:
            raise ValueError(
                f"Tamaños incompatibles: ({self.rows}x{self.columns}) vs ({other.rows}x{other.columns})"
            )

    def is_square(self):
        return self.rows == self.columns

    # Operaciones binarias
    def add(self, other):
        self._validate_size(other)
        result = [
            [self.data[i][j] + other.data[i][j] for j in range(self.columns)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def subtract(self, other):
        self._validate_size(other)
        result = [
            [self.data[i][j] - other.data[i][j] for j in range(self.columns)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def multiply(self, other):
        if self.columns != other.rows:
            raise ValueError(
                f"Dimensiones incompatibles: ({self.rows}x{self.columns}) y ({other.rows}x{other.columns})"
            )
        result = [[0.0 for _ in range(other.columns)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(other.columns):
                total = 0.0
                for k in range(self.columns):
                    total += self.data[i][k] * other.data[k][j]
                result[i][j] = total
        return Matrix(result)

    def element_multiply(self, other):
        self._validate_size(other)
        result = [
            [self.data[i][j] * other.data[i][j] for j in range(self.columns)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def element_divide(self, other):
        self._validate_size(other)
        result = []
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                if other.data[i][j] == 0:
                    raise ZeroDivisionError(f"División por cero en ({i+1}, {j+1})")
                row.append(self.data[i][j] / other.data[i][j])
            result.append(row)
        return Matrix(result)

    # Operaciones unarias
    def scalar_multiply(self, scalar):
        result = [
            [self.data[i][j] * scalar for j in range(self.columns)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def transpose(self):
        result = [
            [self.data[i][j] for i in range(self.rows)]
            for j in range(self.columns)
        ]
        return Matrix(result)

    def determinant(self):
        if not self.is_square():
            raise ValueError("La matriz debe ser cuadrada para calcular determinante.")
        return self._determinant_recursive(self.data)

    def _determinant_recursive(self, matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        if n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        
        det = 0
        for j in range(n):
            submatrix = [[matrix[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += matrix[0][j] * ((-1) ** j) * self._determinant_recursive(submatrix)
        return det

    def inverse(self):
        if not self.is_square():
            raise ValueError("La matriz debe ser cuadrada para calcular inversa.")
        
        det = self.determinant()
        if det == 0:
            raise ValueError("La matriz es singular (determinante = 0), no tiene inversa.")
        
        n = self.rows
        # Matriz identidad
        identity = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        # Copia de la matriz original
        copy = [row[:] for row in self.data]
        
        # Eliminación Gauss-Jordan
        for i in range(n):
            # Buscar pivote
            pivot = copy[i][i]
            if pivot == 0:
                for k in range(i + 1, n):
                    if copy[k][i] != 0:
                        copy[i], copy[k] = copy[k], copy[i]
                        identity[i], identity[k] = identity[k], identity[i]
                        pivot = copy[i][i]
                        break
                else:
                    raise ValueError("La matriz no es invertible.")
            
            # Normalizar fila
            for j in range(n):
                copy[i][j] /= pivot
                identity[i][j] /= pivot
            
            # Eliminar otras filas
            for k in range(n):
                if k != i:
                    factor = copy[k][i]
                    for j in range(n):
                        copy[k][j] -= factor * copy[i][j]
                        identity[k][j] -= factor * identity[i][j]
        
        return Matrix(identity)

    def power(self, exponent):
        if not self.is_square():
            raise ValueError("La matriz debe ser cuadrada para elevar a potencia.")
        if exponent < 0:
            raise ValueError("El exponente debe ser un entero no negativo.")
        if exponent == 0:
            # Matriz identidad del mismo tamaño
            identity = [[1.0 if i == j else 0.0 for j in range(self.columns)] for i in range(self.rows)]
            return Matrix(identity)
        
        result = Matrix([row[:] for row in self.data])
        for _ in range(1, exponent):
            result = result.multiply(self)
        return result

# Funciones de entrada con validaciones robustas
def read_number(message):
    """Lee un número (float o int) con validación."""
    while True:
        try:
            value = input(message).strip()
            if not value:
                print("Error: no puede ingresar un valor vacío.")
                continue
            # Intentar como int primero, luego como float
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            print("Error: debe ingresar un número válido (ej. 5 o 3.14).")

def read_positive_integer(message):
    """Lee un entero positivo con validación."""
    while True:
        try:
            value = input(message).strip()
            if not value:
                print("Error: no puede ingresar un valor vacío.")
                continue
            num = int(value)
            if num <= 0:
                print("Error: debe ser un número positivo (mayor a 0).")
                continue
            return num
        except ValueError:
            print("Error: debe ingresar un número entero (ej. 3).")

def read_non_negative_integer(message):
    """Lee un entero no negativo (0 o positivo) con validación."""
    while True:
        try:
            value = input(message).strip()
            if not value:
                print("Error: no puede ingresar un valor vacío.")
                continue
            num = int(value)
            if num < 0:
                print("Error: debe ser un número no negativo (0 o mayor).")
                continue
            return num
        except ValueError:
            print("Error: debe ingresar un número entero (ej. 2).")

def read_yes_no_option(message):
    """Lee una respuesta sí/no con validación."""
    while True:
        response = input(message).strip().lower()
        if response in ['s', 'n', 'si', 'no']:
            return response in ['s', 'si']
        print("Error: responda 's' (sí) o 'n' (no).")

def read_menu_option(message):
    """Lee una opción del menú con validación básica."""
    while True:
        option = input(message).strip()
        if option:
            return option
        print("Error: no puede ingresar un valor vacío.")

def create_manual_matrix():
    """Crea una matriz con entrada manual celda por celda."""
    print("\n--- Creación manual ---")
    rows = read_positive_integer("Filas: ")
    columns = read_positive_integer("Columnas: ")
    data = []
    for i in range(rows):
        row = []
        for j in range(columns):
            row.append(read_number(f"Valor [{i+1}][{j+1}]: "))
        data.append(row)
    return Matrix(data)

def create_random_matrix():
    """Crea una matriz con valores aleatorios."""
    print("\n--- Creación aleatoria ---")
    rows = read_positive_integer("Filas: ")
    columns = read_positive_integer("Columnas: ")
    minimum = read_number("Valor mínimo: ")
    maximum = read_number("Valor máximo: ")
    
    if minimum > maximum:
        print("Error: el valor mínimo no puede ser mayor que el máximo.")
        minimum, maximum = maximum, minimum
        print(f"Intercambiando: mínimo = {minimum}, máximo = {maximum}")
    
    data = [[random.uniform(minimum, maximum) for _ in range(columns)] for _ in range(rows)]
    return Matrix(data)

def display_matrix(m, name="Matriz"):
    """Muestra una matriz con formato."""
    print(f"\n{name} ({m.rows}x{m.columns}):")
    print(m)

def register_history(operation, result_str):
    """Registra la operación en el archivo de historial."""
    try:
        with open("historial.txt", "a", encoding="utf-8") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} | {operation}\n")
            f.write(f"Resultado:\n{result_str}\n")
            f.write("-" * 50 + "\n")
    except Exception as e:
        print(f"Error al guardar historial: {e}")

def display_history():
    """Muestra el historial de operaciones."""
    try:
        with open("historial.txt", "r", encoding="utf-8") as f:
            content = f.read()
            if content.strip():
                print("\n" + "=" * 60)
                print("         HISTORIAL DE OPERACIONES")
                print("=" * 60)
                print(content)
            else:
                print("El historial está vacío.")
    except FileNotFoundError:
        print("No hay historial aún. Realice algunas operaciones primero.")

def matrix_creation_menu():
    """Menú para seleccionar cómo crear las matrices."""
    print("\n--- Crear Matrices ---")
    print("1. Manual (ingresar valores uno por uno)")
    print("2. Aleatoria (generar valores aleatorios)")
    option = read_menu_option("Elija opción (1-2): ")
    
    while option not in ['1', '2']:
        print("Error: opción no válida. Elija 1 o 2.")
        option = read_menu_option("Elija opción (1-2): ")
    
    if option == '1':
        return create_manual_matrix()
    else:
        return create_random_matrix()

def main_menu():
    """Menú principal de la calculadora."""
    print("\n" + "=" * 60)
    print("         CALCULADORA DE MATRICES")
    print("=" * 60)
    print("Operaciones disponibles: Suma, Resta, Multiplicación matricial,")
    print("Multiplicación elemento a elemento, División elemento a elemento,")
    print("Multiplicación por escalar, Transpuesta, Determinante, Inversa, Potencia.")

    # Primera creación de matrices
    print("\nDefinamos las matrices A y B:")
    print("\n--- Matriz A ---")
    A = matrix_creation_menu()
    print("\n--- Matriz B ---")
    B = matrix_creation_menu()
    
    print("\nMatrices creadas:")
    display_matrix(A, "A")
    display_matrix(B, "B")

    while True:
        print("\n" + "-" * 60)
        print("--- Menú de Operaciones ---")
        print("  1. Suma (A + B)")
        print("  2. Resta (A - B)")
        print("  3. Multiplicación matricial (A * B)")
        print("  4. Multiplicación elemento a elemento (A ⊙ B)")
        print("  5. División elemento a elemento (A / B)")
        print("  6. Multiplicación por escalar (k * A)")
        print("  7. Transpuesta de A")
        print("  8. Determinante de A")
        print("  9. Inversa de A")
        print(" 10. Potencia de A (A^n)")
        print("  ---")
        print("  c. Cambiar matrices (A y B)")
        print("  h. Ver historial")
        print("  0. Salir")

        option = read_menu_option("Elija opción: ")

        if option == "0":
            print("\n¡Hasta luego!")
            break

        elif option == "c":
            print("\n--- Crear nuevas matrices ---")
            print("\n--- Nueva Matriz A ---")
            A = matrix_creation_menu()
            print("\n--- Nueva Matriz B ---")
            B = matrix_creation_menu()
            display_matrix(A, "A")
            display_matrix(B, "B")
            continue

        elif option == "h":
            display_history()
            continue

        # Manejo de operaciones
        try:
            result = None
            operation_str = ""
            
            if option == "1":
                result = A.add(B)
                operation_str = "Suma A + B"
            elif option == "2":
                result = A.subtract(B)
                operation_str = "Resta A - B"
            elif option == "3":
                result = A.multiply(B)
                operation_str = "Multiplicación matricial A * B"
            elif option == "4":
                result = A.element_multiply(B)
                operation_str = "Multiplicación elemento a elemento A ⊙ B"
            elif option == "5":
                result = A.element_divide(B)
                operation_str = "División elemento a elemento A / B"
            elif option == "6":
                scalar = read_number("Ingrese el escalar (k): ")
                result = A.scalar_multiply(scalar)
                operation_str = f"Multiplicación por escalar {scalar} * A"
            elif option == "7":
                result = A.transpose()
                operation_str = "Transpuesta de A"
            elif option == "8":
                det = A.determinant()
                print(f"\nDeterminante de A: {det:.4f}")
                register_history(f"Determinante de A", f"{det:.4f}")
                # No hay resultado matricial para reemplazar
                continue
            elif option == "9":
                result = A.inverse()
                operation_str = "Inversa de A"
            elif option == "10":
                exponent = read_non_negative_integer("Ingrese el exponente (n): ")
                result = A.power(exponent)
                operation_str = f"Potencia A^{exponent}"
            else:
                print("Error: opción no válida.")
                continue

            # Mostrar y registrar resultado (para operaciones que devuelven matriz)
            if result is not None:
                print("\nResultado:")
                display_matrix(result, "Resultado")
                register_history(operation_str, str(result))
                
                # Preguntar si reemplazar A o B
                print("\n¿Desea reemplazar alguna matriz con el resultado?")
                if read_yes_no_option("¿Reemplazar A por el resultado? (s/n): "):
                    A = result
                    print("A ha sido actualizada.")
                elif read_yes_no_option("¿Reemplazar B por el resultado? (s/n): "):
                    B = result
                    print("B ha sido actualizada.")

        except ValueError as e:
            print(f"\nError de validación: {e}")
        except ZeroDivisionError as e:
            print(f"\nError matemático: {e}")
        except Exception as e:
            print(f"\nError inesperado: {e}")

if __name__ == "__main__":
    main_menu()