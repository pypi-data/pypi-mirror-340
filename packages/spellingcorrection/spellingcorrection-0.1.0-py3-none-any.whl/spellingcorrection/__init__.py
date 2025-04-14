def addition(numbers: list) -> float:
    return sum(numbers)
def show_code():
    code = '''
import numpy as np

class SpellingCorrection:
    def __init__(self):
        self.v = {"apple", "banana", "orange", "pear", "peach"}

    def ld(self, w1, w2):
        m, n = len(w1), len(w2)
        d = np.zeros((m + 1, n + 1), dtype=int)
        d[:, 0], d[0, :] = np.arange(m + 1), np.arange(n + 1)
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                d[i][j] = min(d[i - 1][j] + (w1[i - 1] != w2[j - 1]), 
                              d[i][j - 1] + 1, 
                              d[i - 1][j - 1] + (w1[i - 1] != w2[j - 1]))
        return d[m][n]

    def correct(self, w):
        return min(self.v, key=lambda x: self.ld(w, x))


class IRS:
    def __init__(self, docs):
        self.d = docs

    def search(self, q):
        return [doc for doc in self.d if q in doc]


documents = [
    "I love apples.",
    "Banana bread is delicious",
    "Orange juice is refreshing",
    "Pear tarts are amazing",
    "Peach cobbler is my favorite dessert"
]


sc = SpellingCorrection()
irs = IRS(documents)

q = "aplee"

cq = sc.correct(q)
print("Corrected query:", cq)

sr = irs.search(cq)
print("Search results:", sr)

    '''
    print(code)