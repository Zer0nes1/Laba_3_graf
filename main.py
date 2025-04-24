import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import time
from typing import List, Tuple

class CCSMatrix:
    """Класс для работы с разреженной матрицей в формате CCS (Compressed Column Storage)"""
    def __init__(self):
        self.rows = 0           # Количество строк
        self.cols = 0           # Количество столбцов
        self.values = []        # Массив значений ненулевых элементов
        self.row_indices = []   # Массив индексов строк для ненулевых элементов
        self.col_pointers = [0] # Массив указателей на начало столбцов

    def create_random_matrix(self, rows: int, cols: int, density: float) -> None:
        """Создает случайную разреженную матрицу"""
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

    def read_matrix_from_file(self, filename: str) -> None:
        """Читает матрицу из файла"""
        with open(filename, 'r') as f:
            self.rows, self.cols = map(int, f.readline().split())
            self.values = list(map(float, f.readline().split()))
            self.row_indices = list(map(int, f.readline().split()))
            self.col_pointers = list(map(int, f.readline().split()))

    def save_matrix_to_file(self, filename: str) -> None:
        """Сохраняет матрицу в файл"""
        with open(filename, 'w') as f:
            f.write(f"{self.rows} {self.cols}\n")
            f.write(" ".join(map(str, self.values)) + "\n")
            f.write(" ".join(map(str, self.row_indices)) + "\n")
            f.write(" ".join(map(str, self.col_pointers)) + "\n")

    def calculate_column_sums(self) -> List[float]:
        """Вычисляет сумму элементов для каждого столбца"""
        column_sums = [0.0] * self.cols
        for col in range(self.cols):
            start = self.col_pointers[col]
            end = self.col_pointers[col + 1]
            column_sums[col] = sum(self.values[start:end])
        return column_sums

    def rearrange_columns_by_sum(self) -> Tuple[float, List[Tuple[int, int, float]]]:
        """
        Физически переставляет столбцы по возрастанию сумм элементов
        Возвращает: (время выполнения, список изменений)
        """
        start_time = time.perf_counter()
        
        column_sums = self.calculate_column_sums()
        sorted_indices = sorted(range(self.cols), key=lambda i: column_sums[i])
        
        # Сохраняем информацию о старых индексах и суммах
        changes = [(i, sorted_indices[i], column_sums[sorted_indices[i]]) 
                  for i in range(self.cols)]
        
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

        self.values = sorted_values
        self.row_indices = sorted_row_indices
        self.col_pointers = sorted_col_pointers
        
        end_time = time.perf_counter()
        elapsed_time = (end_time - start_time) * 1000  # в миллисекундах
        
        return elapsed_time, changes

    def to_dense_matrix(self) -> np.ndarray:
        """Конвертирует разреженную матрицу в плотный формат"""
        dense = np.zeros((self.rows, self.cols))
        for col in range(self.cols):
            start = self.col_pointers[col]
            end = self.col_pointers[col + 1]
            for i in range(start, end):
                row = self.row_indices[i]
                dense[row, col] = self.values[i]
        return dense

    def print_matrix(self, max_rows: int = 20, max_cols: int = 20) -> None:
        """Выводит матрицу в консоль"""
        if self.rows == 0 or self.cols == 0:
            print("Матрица пуста")
            return

        dense = self.to_dense_matrix()
        dense = dense[:max_rows, :max_cols]
        
        print("\nМатрица:")
        print("     " + " ".join([f"{col:>6}" for col in range(min(self.cols, max_cols))]))
        
        for row in range(min(self.rows, max_rows)):
            print(f"{row:>3} |", end="")
            for col in range(min(self.cols, max_cols)):
                val = dense[row, col]
                print(f"{val:>6.1f}" if val != 0 else "     0", end="")
            print()
        
        if self.rows > max_rows or self.cols > max_cols:
            print(f"\nПоказаны первые {max_rows} строк и {max_cols} столбцов")

    def visualize_matrix(self, max_size: int = 15) -> None:
        """Визуализирует матрицу с отображением значений"""
        if self.rows == 0 or self.cols == 0:
            print("Матрица пуста")
            return

        dense = self.to_dense_matrix()
        display_rows = min(self.rows, max_size)
        display_cols = min(self.cols, max_size)
        dense = dense[:display_rows, :display_cols]
        
        plt.figure(figsize=(12, 8))
        plt.imshow(dense, cmap='viridis', aspect='auto', vmin=0)
        plt.colorbar(label='Значение элемента')
        plt.title(f"Матрица {self.rows}x{self.cols}")
        
        for i in range(dense.shape[0]):
            for j in range(dense.shape[1]):
                plt.text(j, i, f'{dense[i,j]:.1f}', 
                        ha='center', va='center',
                        color='white' if dense[i,j] > np.max(dense)/2 else 'black')
        
        plt.show()

def performance_test():
    """Тестирование производительности перестановки столбцов"""
    sizes = [(10, 10), (100, 100), (1000, 1000), (10000, 10000)]
    densities = [0.1, 0.3, 0.5]
    
    print("\nТест производительности:")
    print("Размер | Плотность | Время (мс)")
    print("-------------------------------")
    
    for rows, cols in sizes:
        for density in densities:
            matrix = CCSMatrix()
            matrix.create_random_matrix(rows, cols, density)
            
            time_ms, _ = matrix.rearrange_columns_by_sum()
            print(f"{rows}x{cols} |    {density:.1f}    |  {time_ms:.3f}")

def main():
    """Основная функция с интерфейсом командной строки"""
    matrix = CCSMatrix()
    
    while True:
        print("\nМеню:")
        print("1. Создать случайную матрицу")
        print("2. Загрузить матрицу из файла")
        print("3. Сохранить матрицу в файл")
        print("4. Вывести матрицу")
        print("5. Визуализировать матрицу")
        print("6. Переставить столбцы по сумме")
        print("7. Тест производительности")
        print("8. Выход")
        
        choice = input("Выберите действие: ").strip()
        
        if choice == '1':
            try:
                rows = int(input("Количество строк: "))
                cols = int(input("Количество столбцов: "))
                density = float(input("Плотность (0-1): "))
                matrix.create_random_matrix(rows, cols, density)
                print(f"Создана матрица {rows}x{cols} с плотностью {density}")
            except Exception as e:
                print(f"Ошибка: {e}")
        
        elif choice == '2':
            filename = input("Имя файла: ")
            try:
                matrix.read_matrix_from_file(filename)
                print(f"Загружена матрица {matrix.rows}x{matrix.cols}")
            except Exception as e:
                print(f"Ошибка: {e}")
        
        elif choice == '3':
            filename = input("Имя файла: ")
            matrix.save_matrix_to_file(filename)
            print("Матрица сохранена")
        
        elif choice == '4':
            matrix.print_matrix()
        
        elif choice == '5':
            matrix.visualize_matrix()
        
        elif choice == '6':
            if matrix.rows == 0 or matrix.cols == 0:
                print("Матрица пуста!")
                continue
                
            time_ms, changes = matrix.rearrange_columns_by_sum()
            
            print("\nИзменения столбцов:")
            print("Новая позиция | Старый индекс | Сумма")
            print("-----------------------------------")
            for new_pos, old_idx, col_sum in changes:
                print(f"{new_pos:13} | {old_idx:13} | {col_sum:.1f}")
            
            print(f"\nПерестановка выполнена за {time_ms:.3f} мс")
            print("Матрица после перестановки:")
            matrix.print_matrix()
        
        elif choice == '7':
            performance_test()
        
        elif choice == '8':
            print("Выход")
            break
        
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main()