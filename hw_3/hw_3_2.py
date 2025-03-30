import copy
import numpy as np

np.random.seed(0)

class StrMixin:
    def __str__(self):
        max_digit = max([len(str(el)) for row in self.value for el in row])
        beauty_number = lambda numb: f"{numb:>{max_digit}}"
        beauty_row = lambda row: f"[{' '.join(map(beauty_number, row))}]"
        return '[' + '\n '.join(map(beauty_row, self.value)) + ']'

class OutMixin:
    def to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self))

class PropertyMixin:
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        if len(set(map(len, value))) > 1:
            raise ValueError("Invalid matrix dimensions")
        self._value = copy.deepcopy(value)

class Matrix(np.lib.mixins.NDArrayOperatorsMixin, 
                PropertyMixin, 
                StrMixin, 
                OutMixin,
                ):
    def __init__(self, value):
        self.value = value

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):

        inputs = tuple(x.value if isinstance(x, Matrix) else x
                    for x in inputs)
        result = getattr(ufunc, method)(*inputs, **kwargs)
        
        if isinstance(result, np.ndarray):
            return Matrix(result)
        return result
        

def main():
    data1 = np.random.randint(0, 10, (10, 10)).tolist()  
    data2 = np.random.randint(0, 10, (10, 10)).tolist()
    m1 = Matrix(data1)
    m2 = Matrix(data2)

    (m1 + m2).to_file('artifacts/matrix_add_2.txt')
    (m1 * m2).to_file('artifacts/matrix_mul_2.txt')
    (m1 @ m2).to_file('artifacts/matrix_matmul_2.txt')

if __name__ == "__main__":
    main()

