import cmath
import math
from typing import List

def fft(arr: List[complex], invert: bool) -> None:
    n = len(arr)
    if n == 1:
        return

    arr1, arr2 = [], []
    for i in range(n // 2):
        arr1.append(arr[2*i])
        arr2.append(arr[2*i+1])
    fft(arr1, invert)
    fft(arr2, invert)

    ang = 2 * cmath.pi / n * (-1 if invert else 1)
    w, wn = 1, complex(cmath.cos(ang), cmath.sin(ang))
    for i in range(n // 2):
        arr[i] = arr1[i] + w * arr2[i]
        arr[i + n//2] = arr1[i] - w * arr2[i]
        if invert:
            arr[i] /= 2
            arr[i + n//2] /= 2
        w *= wn

def multiply(a: List[int], b: List[int]) -> List[int]:
    arr1 = [complex(x, 0) for x in a]
    arr2 = [complex(x, 0) for x in b]
    n = 1
    while n < len(a) + len(b):
        n <<= 1
    arr1 += [0] * (n - len(arr1))
    arr2 += [0] * (n - len(arr2))
    fft(arr1, False)
    fft(arr2, False)
    for i in range(n):
        arr1[i] *= arr2[i]
    fft(arr1, True)

    result = [0] * n
    for i in range(n):
        result[i] = round(arr1[i].real)
    return result

if __name__ == '__main__':
    a = [1, 2, 3]
    b = [4, 5, 6]
    result = multiply(a, b)
    print(result)