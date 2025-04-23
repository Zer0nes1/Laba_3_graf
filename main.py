import random
import numpy as np

class CCSMatrix:
    """Класс для работы с разреженной матрицей в формате CCS (Compressed Column Storage)"""
    def __init__(self):
        self.rows = 0           # Количество строк
        self.cols = 0           # Количество столбцов
        self.values = []        # Массив значений ненулевых элементов
        self.row_indices = []   # Массив индексов строк для ненулевых элементов
        self.col_pointers = [0]  # Массив указателей на начало столбцов в values и row_indices

    def create_random_matrix(self, rows: int, cols: int, density: float):
        """
        Создает случайную разреженную матрицу.
        
        Входные параметры:
        - rows: количество строк (int)
        - cols: количество столбцов (int)
        - density: плотность матрицы (float от 0 до 1)
        
        Выходные данные: нет (изменяет состояние объекта)
        
        Оценка сложности: O(rows * cols) в худшем случае (когда density = 1)
        """
        if not (0 < density <= 1):
            raise ValueError("Плотность должна быть в диапазоне (0, 1]")
        
        # Очищаем текущие данные
        self.rows = rows
        self.cols = cols
        self.values = []
        self.row_indices = []
        self.col_pointers = [0]
        
        # Генерация случайной матрицы
        for col in range(cols):
            for row in range(rows):
                if random.random() < density:
                    self.values.append(random.randint(1, 100))
                    self.row_indices.append(row)
            self.col_pointers.append(len(self.values))

    def read_matrix_from_file(self, filename: str):
        """
        Читает матрицу из файла.
        
        Входные параметры:
        - filename: имя файла (str)
        
        Выходные данные: нет (изменяет состояние объекта)
        
        Формат файла:
        - Первая строка: rows cols
        - Вторая строка: values
        - Третья строка: row_indices
        - Четвертая строка: col_pointers
        
        Оценка сложности: O(n), где n - размер файла
        """
        try:
            with open(filename, 'r') as f:
                # Чтение размеров матрицы
                self.rows, self.cols = map(int, f.readline().split())
                
                # Чтение массивов данных
                self.values = list(map(float, f.readline().split()))
                self.row_indices = list(map(int, f.readline().split()))
                self.col_pointers = list(map(int, f.readline().split()))
        except Exception as e:
            raise ValueError(f"Ошибка чтения файла: {e}")

    def input_matrix_from_keyboard(self):
        """
        Ввод матрицы с клавиатуры.
        
        Входные параметры: нет (ввод с клавиатуры)
        Выходные данные: нет (изменяет состояние объекта)
        
        Оценка сложности: O(n), где n - количество вводимых элементов
        """
        try:
            self.rows = int(input("Введите количество строк: "))
            self.cols = int(input("Введите количество столбцов: "))
            
            print("Введите массив values через пробел (ненулевые элементы):")
            self.values = list(map(float, input().split()))
            
            print("Введите массив row_indices через пробел (индексы строк для ненулевых элементов):")
            self.row_indices = list(map(int, input().split()))
            
            print("Введите массив col_pointers через пробел (указатели на столбцы):")
            self.col_pointers = list(map(int, input().split()))
            
            # Проверка корректности введенных данных
            if len(self.col_pointers) != self.cols + 1:
                raise ValueError("Длина col_pointers должна быть равна cols + 1")
            if len(self.values) != len(self.row_indices):
                raise ValueError("Длины values и row_indices должны совпадать")
        except Exception as e:
            raise ValueError(f"Ошибка ввода: {e}")

    def save_matrix_to_file(self, filename: str):
        """
        Сохраняет матрицу в файл.
        
        Входные параметры:
        - filename: имя файла (str)
        
        Выходные данные: нет (создает файл)
        
        Оценка сложности: O(n), где n - количество элементов матрицы
        """
        try:
            with open(filename, 'w') as f:
                f.write(f"{self.rows} {self.cols}\n")
                f.write(" ".join(map(str, self.values)) + "\n")
                f.write(" ".join(map(str, self.row_indices)) + "\n")
                f.write(" ".join(map(str, self.col_pointers)) + "\n")
            print(f"Матрица сохранена в файл {filename}")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")

    def calculate_column_sums(self):
        """
        Вычисляет сумму элементов для каждого столбца.
        
        Входные параметры: нет
        Выходные данные: список сумм столбцов (list)
        
        Оценка сложности: O(nnz), где nnz - количество ненулевых элементов
        """
        column_sums = [0.0] * self.cols
        for col in range(self.cols):
            start = self.col_pointers[col]
            end = self.col_pointers[col + 1]
            column_sums[col] = sum(self.values[start:end])
        return column_sums

    def sort_columns_by_sum(self):
        """
        Сортирует столбцы по возрастанию сумм элементов.
        
        Входные параметры: нет
        Выходные данные: нет (изменяет состояние объекта)
        
        Оценка сложности: O(n log n) для сортировки + O(nnz) для перестроения матрицы
        """
        # Вычисляем суммы столбцов
        column_sums = self.calculate_column_sums()
        
        # Получаем индексы для сортировки
        sorted_indices = sorted(range(self.cols), key=lambda i: column_sums[i])
        
        # Создаем новые массивы для отсортированной матрицы
        sorted_values = []
        sorted_row_indices = []
        sorted_col_pointers = [0]  # Первый указатель всегда 0
        
        # Перестраиваем матрицу в соответствии с новым порядком столбцов
        for col in sorted_indices:
            start = self.col_pointers[col]
            end = self.col_pointers[col + 1]
            
            # Копируем данные для текущего столбца
            sorted_values.extend(self.values[start:end])
            sorted_row_indices.extend(self.row_indices[start:end])
            
            # Обновляем указатель на столбец
            sorted_col_pointers.append(sorted_col_pointers[-1] + (end - start))
        
        # Обновляем данные матрицы
        self.values = sorted_values
        self.row_indices = sorted_row_indices
        self.col_pointers = sorted_col_pointers
        
        print("Столбцы отсортированы по возрастанию сумм.")

    def print_matrix(self):
        """
        Выводит матрицу в консоль в разреженном формате.
        
        Входные параметры: нет
        Выходные данные: нет (вывод в консоль)
        """
        print(f"Размеры матрицы: {self.rows}x{self.cols}")
        print(f"Values (ненулевые элементы): {self.values}")
        print(f"Row Indices (индексы строк): {self.row_indices}")
        print(f"Col Pointers (указатели столбцов): {self.col_pointers}")
        
        # Дополнительно выводим суммы столбцов
        if self.cols <= 10:  # Чтобы не перегружать вывод для больших матриц
            sums = self.calculate_column_sums()
            print(f"Суммы столбцов: {sums}")

    def print_dense_matrix(self):
        """
        Выводит матрицу в плотном формате (для небольших матриц).
        
        Входные параметры: нет
        Выходные данные: нет (вывод в консоль)
        
        Оценка сложности: O(rows * cols)
        """
        if self.rows > 20 or self.cols > 20:
            print("Матрица слишком большая для плотного вывода")
            return
            
        dense = np.zeros((self.rows, self.cols))
        for col in range(self.cols):
            start = self.col_pointers[col]
            end = self.col_pointers[col + 1]
            for i in range(start, end):
                row = self.row_indices[i]
                dense[row, col] = self.values[i]
        
        print("Матрица в плотном формате:")
        print(dense)


def main():
    """
    Основная функция программы с меню взаимодействия.
    """
    matrix = CCSMatrix()
    
    while True:
        print("\nМеню:")
        print("1. Вывести текущую матрицу (разреженный формат)")
        print("2. Вывести текущую матрицу (плотный формат, если небольшая)")
        print("3. Сохранить матрицу в файл")
        print("4. Отсортировать столбцы по возрастанию сумм элементов")
        print("5. Сгенерировать случайную матрицу")
        print("6. Ввести матрицу с клавиатуры")
        print("7. Загрузить матрицу из файла")
        print("8. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == '1':
            matrix.print_matrix()

        elif choice == '2':
            matrix.print_dense_matrix()

        elif choice == '3':
            filename = input("Введите имя файла для сохранения: ").strip()
            matrix.save_matrix_to_file(filename)

        elif choice == '4':
            try:
                matrix.sort_columns_by_sum()
            except Exception as e:
                print(f"Ошибка при сортировке: {e}")

        elif choice == '5':
            try:
                rows = int(input("Введите количество строк: "))
                cols = int(input("Введите количество столбцов: "))
                density = float(input("Введите плотность матрицы (0-1): "))
                matrix.create_random_matrix(rows, cols, density)
                print(f"Матрица {rows}x{cols} с плотностью {density} успешно сгенерирована.")
            except ValueError as e:
                print(f"Ошибка: {e}")

        elif choice == '6':
            try:
                matrix.input_matrix_from_keyboard()
                print("Матрица успешно введена.")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == '7':
            filename = input("Введите имя файла: ").strip()
            try:
                matrix.read_matrix_from_file(filename)
                print("Матрица успешно загружена.")
            except Exception as e:
                print(f"Ошибка при чтении файла: {e}")

        elif choice == '8':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор! Пожалуйста, введите число от 1 до 8.")


if __name__ == "__main__":
    main()