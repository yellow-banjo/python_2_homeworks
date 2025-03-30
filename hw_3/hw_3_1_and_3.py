import copy
import numpy as np

np.random.seed(0)

class Matrix:
    def __init__(self, data):
        if len(set(map(len, data))) > 1:
            raise ValueError("Invalid matrix dimensions")
        
        self.data = copy.deepcopy(data)
        self.rows = len(data)
        self.cols = len(data[0])
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            result = [[elem + other for elem in row] for row in self.data]
        elif isinstance(other, Matrix):
            if self.rows != other.rows or self.cols != other.cols:
                raise ValueError("Matrices must have the same dimensions for addition")
            result = [
                [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
                for i in range(self.rows)
            ]
        else:
            raise TypeError("Unsupported operand type for +")
        return self.__class__(result)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            result = [[elem * other for elem in row] for row in self.data]
        elif isinstance(other, Matrix):
            if self.rows != other.rows or self.cols != other.cols:
                raise ValueError("Matrices must have the same dimensions for component-wise multiplication")
            result = [
                [self.data[i][j] * other.data[i][j] for j in range(self.cols)]
                for i in range(self.rows)
            ]
        else:
            raise TypeError("Unsupported operand type for *")
        return self.__class__(result)
    
    __rmul__ = __mul__

    def __matmul__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Unsupported operand type for @")
        
        if self.cols != other.rows:
            raise ValueError("Incompatible dimensions for matrix multiplication")
        result = [
            [
                sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                for j in range(other.cols)
            ]
            for i in range(self.rows)
        ]
        return self.__class__(result)

    def __str__(self):
        max_digits = max([len(str(el)) for row in self.data for el in row])
        beauty_number = lambda numb: f"{numb:>{max_digits}}"
        beauty_row = lambda row: f"[{' '.join(map(beauty_number, row))}]"
        return '[' + '\n '.join(map(beauty_row, self.data)) + ']'

class HashMixin:
    """The simplest hash function is the sum of the matrix elements."""
    def __hash__(self):
        return sum(flatten(self.data))

class CompMixin:
    def __eq__(self, other):
        return all([el_s == el_o for el_s, el_o in zip(flatten(self.data), flatten(other.data))])
    
    def __ne__(self, other):
        return any([el_s != el_o for el_s, el_o in zip(flatten(self.data), flatten(other.data))])

class HashableMatrix(Matrix, CompMixin, HashMixin):
    __hash__ = HashMixin.__hash__

def write_file(data, filename, access_mode = 'w'):
    with open(filename, access_mode) as f:
        f.write(str(data))

def flatten(matrix):
    return [el for row in matrix for el in row]

def main():
    data1 = np.random.randint(0, 10, (10, 10)).tolist()  
    data2 = np.random.randint(0, 10, (10, 10)).tolist()
    m1 = Matrix(data1)
    m2 = Matrix(data2)

    write_file(m1 + m2, 'artifacts/matrix_add.txt')
    write_file(m1 * m2, 'artifacts/matrix_mul.txt')
    write_file(m1 @ m2, 'artifacts/matrix_matmul.txt')

    A = HashableMatrix([[1, 2], [3, 4]])
    B = HashableMatrix([[5, 2], [3, 6]])
    C = HashableMatrix([[2, 2], [3, 3]])
    D = HashableMatrix([[5, 2], [3, 6]])
    assert (hash(A) == hash(C)) and (A != C) and (B == D) and (A @ B != C @ B)

    write_file(A, 'artifacts/A.txt')
    write_file(B, 'artifacts/B.txt')
    write_file(C, 'artifacts/C.txt')
    write_file(D, 'artifacts/D.txt')
    write_file(A @ B, 'artifacts/AB.txt')
    write_file(C @ D, 'artifacts/CD.txt')
    write_file(', '.join(map(str, [hash(A @ B), hash(C @ D)])), 'artifacts/hash.txt')
    

if __name__ == "__main__":
    main()

