import random
import numpy as np

class CCSMatrix:
    """Класс для работы с разреженной матрицей в формате CCS"""
    def __init__(self):
        self.rows = 0           # Количество строк
        self.cols = 0           # Количество столбцов
        self.values = []        # Массив значений ненулевых элементов
        self.row_indices = []   # Массив индексов строк
        self.col_pointers = []  # Массив указателей столбцов

    def create_random_matrix(self, rows: int, cols: int, density: float):
        """
        Создает случайную разреженную матрицу.
        :param rows: количество строк
        :param cols: количество столбцов
        :param density: плотность матрицы (от 0 до 1)
        """
        if not (0 < density <= 1):
            raise ValueError("Плотность должна быть в диапазоне (0, 1]")
        self.rows = rows
        self.cols = cols
        self.values = []
        self.row_indices = []
        self.col_pointers = [0]
        
        for col in range(cols):
            for row in range(rows):
                if random.random() < density:
                    self.values.append(random.randint(1, 100))
                    self.row_indices.append(row)
            self.col_pointers.append(len(self.values))

    def read_matrix_from_file(self, filename: str):
        """
        Читает матрицу из файла.
        Формат файла:
        - Первая строка: размеры матрицы (строки, столбцы)
        - Вторая строка: массив values
        - Третья строка: массив row_indices
        - Четвертая строка: массив col_pointers
        """
        with open(filename, 'r') as f:
            self.rows, self.cols = map(int, f.readline().split())
            self.values = list(map(float, f.readline().split()))
            self.row_indices = list(map(int, f.readline().split()))
            self.col_pointers = list(map(int, f.readline().split()))

    def input_matrix_from_keyboard(self):
        """Ввод матрицы с клавиатуры."""
        self.rows = int(input("Введите количество строк: "))
        self.cols = int(input("Введите количество столбцов: "))
        self.values = list(map(float, input("Введите массив values: ").split()))
        self.row_indices = list(map(int, input("Введите массив row_indices: ").split()))
        self.col_pointers = list(map(int, input("Введите массив col_pointers: ").split()))

    def save_matrix_to_file(self, filename: str):
        """Сохраняет матрицу в файл."""
        with open(filename, 'w') as f:
            f.write(f"{self.rows} {self.cols}\n")
            f.write(" ".join(map(str, self.values)) + "\n")
            f.write(" ".join(map(str, self.row_indices)) + "\n")
            f.write(" ".join(map(str, self.col_pointers)) + "\n")
        print(f"Матрица сохранена в файл {filename}")

    def calculate_column_sums(self):
        """Вычисляет сумму элементов для каждого столбца."""
        column_sums = [0] * self.cols
        for col in range(self.cols):
            start = self.col_pointers[col]
            end = self.col_pointers[col + 1]
            column_sums[col] = sum(self.values[start:end])
        return column_sums

    def sort_columns_by_sum(self):
        """Сортирует столбцы по возрастанию сумм элементов."""
        column_sums = self.calculate_column_sums()
        sorted_indices = sorted(range(self.cols), key=lambda i: column_sums[i])

        sorted_values = []
        sorted_row_indices = []
        sorted_col_pointers = [0]

        for col in sorted_indices:
            start = self.col_pointers[col]
            end = self.col_pointers[col + 1]
            sorted_values.extend(self.values[start:end])
            sorted_row_indices.extend(self.row_indices[start:end])
            sorted_col_pointers.append(sorted_col_pointers[-1] + (end - start))

        self.values = sorted_values
        self.row_indices = sorted_row_indices
        self.col_pointers = sorted_col_pointers
        print("Столбцы отсортированы по возрастанию сумм.")

    def print_matrix(self):
        """Выводит матрицу в консоль."""
        print(f"Размеры: {self.rows}x{self.cols}")
        print("Values:", self.values)
        print("Row Indices:", self.row_indices)
        print("Col Pointers:", self.col_pointers)


def main():
    matrix = CCSMatrix()

    while True:
        print("\nМеню:")
        print("1. Вывести текущую матрицу")
        print("2. Сохранить матрицу в файл")
        print("3. Представить столбцы по возрастанию сумм элементов")
        print("4. Сгенерировать случайную матрицу")
        print("5. Ввести матрицу с клавиатуры")
        print("6. Загрузить матрицу из файла")
        print("7. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == '1':
            matrix.print_matrix()

        elif choice == '2':
            filename = input("Введите имя файла для сохранения: ")
            matrix.save_matrix_to_file(filename)

        elif choice == '3':
            matrix.sort_columns_by_sum()

        elif choice == '4':
            try:
                rows = int(input("Введите количество строк: "))
                cols = int(input("Введите количество столбцов: "))
                density = float(input("Введите плотность матрицы (0-1): "))
                matrix.create_random_matrix(rows, cols, density)
                print("Матрица успешно сгенерирована.")
            except ValueError as e:
                print(f"Ошибка: {e}")

        elif choice == '5':
            try:
                matrix.input_matrix_from_keyboard()
                print("Матрица успешно введена.")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == '6':
            filename = input("Введите имя файла: ")
            try:
                matrix.read_matrix_from_file(filename)
                print("Матрица успешно загружена.")
            except Exception as e:
                print(f"Ошибка при чтении файла: {e}")

        elif choice == '7':
            print("Выход.")
            break

        else:
            print("Неверный выбор!")


if __name__ == "__main__":
    main()