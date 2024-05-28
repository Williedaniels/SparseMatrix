from collections import defaultdict

class SparseMatrix:
    def __init__(self, file_path=None, num_rows=0, num_cols=0):
        self.rows = num_rows
        self.cols = num_cols
        self.data = defaultdict(dict)

        if file_path:
            self.load_from_file(file_path)

    def load_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                self.rows = int(lines[0].split('=')[1])
                self.cols = int(lines[1].split('=')[1])

                for line in lines[2:]:
                    row, col, value = (int(x) for x in line.strip('()').split(', '))
                    self.set_element(row, col, value)
        except (IndexError, ValueError):
            raise ValueError("Input file has wrong format")

    def get_element(self, row, col):
        return self.data[row].get(col, 0)

    def set_element(self, row, col, value):
        self.data[row][col] = value

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices have different dimensions")

        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        for row, col_map in self.data.items():
            for col, value in col_map.items():
                result.set_element(row, col, value)

        for row, col_map in other.data.items():
            for col, value in col_map.items():
                result.set_element(row, col, result.get_element(row, col) + value)

        return result

    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices have different dimensions")

        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        for row, col_map in self.data.items():
            for col, value in col_map.items():
                result.set_element(row, col, value)

        for row, col_map in other.data.items():
            for col, value in col_map.items():
                result.set_element(row, col, result.get_element(row, col) - value)

        return result

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError("Matrices cannot be multiplied")

        result = SparseMatrix(num_rows=self.rows, num_cols=other.cols)
        for row, col_map in self.data.items():
            for col, value in col_map.items():
                for i in range(other.cols):
                    result.set_element(row, i, result.get_element(row, i) + value * other.get_element(col, i))

        return result

def main():
    matrix1 = SparseMatrix("sample_inputs/matrix1.txt")
    matrix2 = SparseMatrix("sample_inputs/matrix2.txt")

    print("Select operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    choice = int(input())

    try:
        if choice == 1:
            (matrix1.add(matrix2)).print()
        elif choice == 2:
            (matrix1.subtract(matrix2)).print()
        elif choice == 3:
            (matrix1.multiply(matrix2)).print()
        else:
            print("Invalid choice")
    except ValueError as e:
        print("Error:", e)

if __name__ == "__main__":
    main()