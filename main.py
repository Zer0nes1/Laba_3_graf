import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

class CCSMatrix:
    """Класс для работы с разреженной матрицей в формате CCS (Compressed Column Storage)"""
    def __init__(self):
        self.rows = 0           # Количество строк
        self.cols = 0           # Количество столбцов
        self.values = []        # Массив значений ненулевых элементов
        self.row_indices = []   # Массив индексов строк для ненулевых элементов
        self.col_pointers = [0] # Массив указателей на начало столбцов

    def create_random_matrix(self, rows: int, cols: int, density: float):
        """Создает случайную разреженную матрицу."""
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
        """Читает матрицу из файла."""
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
        """Показывает порядок столбцов по возрастанию сумм элементов (без изменения матрицы)"""
        column_sums = self.calculate_column_sums()
        sorted_indices = sorted(range(self.cols), key=lambda i: column_sums[i])
        
        print("\nПорядок столбцов по возрастанию сумм:")
        print("Столбец | Сумма")
        print("---------------")
        for idx in sorted_indices:
            print(f"{idx:6} | {column_sums[idx]:.1f}")

    def rearrange_columns(self):
        """Физически переставляет столбцы по возрастанию сумм с отображением изменений"""
        column_sums = self.calculate_column_sums()
        sorted_indices = sorted(range(self.cols), key=lambda i: column_sums[i])
        
        # Сохраняем старую матрицу для сравнения
        old_dense = self.to_dense_matrix()
        old_sums = column_sums.copy()
        
        # Переставляем столбцы
        sorted_values = []
        sorted_row_indices = []
        sorted_col_pointers = [0]
        
        for col in sorted_indices:
            start = self.col_pointers[col]
            end = self.col_pointers[col + 1]
            sorted_values.extend(self.values[start:end])
            sorted_row_indices.extend(self.row_indices[start:end])
            sorted_col_pointers.append(sorted_col_pointers[-1] + (end - start))
        
        # Обновляем матрицу
        self.values = sorted_values
        self.row_indices = sorted_row_indices
        self.col_pointers = sorted_col_pointers
        
        # Получаем новую матрицу
        new_dense = self.to_dense_matrix()
        new_sums = self.calculate_column_sums()
        
        # Выводим таблицу изменений
        print("\nТаблица изменений:")
        print("Старый Индекс | Новая Позиция | Старая Сумма | Новая Сумма")
        print("--------------------------------------------------------")
        for new_pos, old_idx in enumerate(sorted_indices):
            print(f"{old_idx:12} | {new_pos:13} | {old_sums[old_idx]:12.1f} | {new_sums[new_pos]:10.1f}")
        
        # Визуализация для небольших матриц
        if self.rows <= 10 and self.cols <= 10:
            print("\nСтарая матрица:")
            self._print_dense_with_columns(old_dense)
            
            print("\nНовая матрица:")
            self._print_dense_with_columns(new_dense, sorted_indices)
        else:
            print("\nДля полного сравнения выведите матрицы отдельно (пункты меню 1-3)")

    def _print_dense_with_columns(self, matrix, column_order=None):
        """Выводит матрицу с подписями столбцов"""
        if column_order is None:
            column_order = range(matrix.shape[1])
        
        print("     " + " ".join([f"{col:>6}" for col in column_order]))
        for row in range(matrix.shape[0]):
            print(f"{row:>3} |", end="")
            for col in range(matrix.shape[1]):
                val = matrix[row, col]
                if val != 0:
                    print(f"\033[94m{val:6.1f}\033[0m", end="")  # Синий цвет
                else:
                    print("     0", end="")
            print()

    def print_matrix(self):
        """Выводит матрицу в консоль."""
        print(f"Размеры: {self.rows}x{self.cols}")
        print("Values:", self.values)
        print("Row Indices:", self.row_indices)
        print("Col Pointers:", self.col_pointers)

    def to_dense_matrix(self):
        """Конвертирует разреженную матрицу в плотный формат (numpy array)"""
        dense = np.zeros((self.rows, self.cols))
        for col in range(self.cols):
            start = self.col_pointers[col]
            end = self.col_pointers[col + 1]
            for i in range(start, end):
                row = self.row_indices[i]
                dense[row, col] = self.values[i]
        return dense

    def print_matrix_detailed(self, max_rows=20, max_cols=20):
        """Выводит матрицу в виде таблицы с значениями"""
        if self.rows == 0 or self.cols == 0:
            print("Матрица пуста")
            return

        dense = self.to_dense_matrix()
        dense = dense[:max_rows, :max_cols]
        
        print("\nДетализированное представление матрицы:")
        print("Суммы столбцов:", [f"{sum:.1f}" for sum in self.calculate_column_sums()[:max_cols]])
        print("     " + " ".join([f"{col:>6}" for col in range(min(self.cols, max_cols))]))
        
        for row in range(min(self.rows, max_rows)):
            print(f"{row:>3} |", end="")
            for col in range(min(self.cols, max_cols)):
                val = dense[row, col]
                print(f"{val:>6.1f}" if val != 0 else "     0", end="")
            print()
        
        if self.rows > max_rows or self.cols > max_cols:
            print(f"\nПоказаны первые {max_rows} строк и {max_cols} столбцов")

    def visualize_matrix_with_values(self, max_size=15):
        """Визуализирует матрицу с отображением значений в ячейках"""
        if self.rows == 0 or self.cols == 0:
            print("Матрица пуста")
            return

        dense = self.to_dense_matrix()
        display_rows = min(self.rows, max_size)
        display_cols = min(self.cols, max_size)
        dense = dense[:display_rows, :display_cols]
        
        if self.rows > max_size or self.cols > max_size:
            print(f"Для визуализации отображаются первые {max_size} строк и столбцов")

        plt.figure(figsize=(12, 8))
        plt.imshow(dense, cmap='viridis', aspect='auto', vmin=0)
        plt.colorbar(label='Значение элемента')
        plt.title(f"Матрица {self.rows}x{self.cols} (первые {display_rows}x{display_cols})")
        
        for i in range(dense.shape[0]):
            for j in range(dense.shape[1]):
                plt.text(j, i, f'{dense[i,j]:.1f}', ha='center', va='center', 
                        color='white' if dense[i,j] > np.max(dense)/2 else 'black')
        
        plt.show()


def main():
    matrix = CCSMatrix()

    while True:
        print("\nМеню:")
        print("1. Вывести матрицу (разреженный формат)")
        print("2. Вывести матрицу (табличный формат с значениями)")
        print("3. Визуализировать матрицу (график с значениями)")
        print("4. Показать порядок столбцов по сумме")
        print("5. Физически переставить столбцы по сумме (с проверкой)")
        print("6. Сохранить матрицу в файл")
        print("7. Сгенерировать случайную матрицу")
        print("8. Ввести матрицу с клавиатуры")
        print("9. Загрузить матрицу из файла")
        print("10. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == '1':
            matrix.print_matrix()

        elif choice == '2':
            matrix.print_matrix_detailed()

        elif choice == '3':
            matrix.visualize_matrix_with_values()

        elif choice == '4':
            matrix.sort_columns_by_sum()

        elif choice == '5':
            matrix.rearrange_columns()

        elif choice == '6':
            filename = input("Введите имя файла для сохранения: ")
            matrix.save_matrix_to_file(filename)

        elif choice == '7':
            try:
                rows = int(input("Введите количество строк: "))
                cols = int(input("Введите количество столбцов: "))
                density = float(input("Введите плотность матрицы (0-1): "))
                matrix.create_random_matrix(rows, cols, density)
                print(f"Матрица {rows}x{cols} с плотностью {density} создана.")
            except ValueError as e:
                print(f"Ошибка: {e}")

        elif choice == '8':
            try:
                matrix.input_matrix_from_keyboard()
                print("Матрица успешно введена.")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == '9':
            filename = input("Введите имя файла: ")
            try:
                matrix.read_matrix_from_file(filename)
                print("Матрица успешно загружена.")
            except Exception as e:
                print(f"Ошибка при чтении файла: {e}")

        elif choice == '10':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор! Пожалуйста, введите число от 1 до 10.")


if __name__ == "__main__":
    main()