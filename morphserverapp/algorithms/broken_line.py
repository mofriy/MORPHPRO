# Input: pa, pb - two broken lines, k - number of morphing steps
# делает морфинг между двумя ломанными линиями.
# каждая ломанная задана своими точками. Каждая точка - тройка координат (x, y, z). Они заданы
# в виде массива из трёх элементов.
# Sample:
# [[0, 0, 0], [1, 1, 1]]
# В примере задана ломанная из двух точек.
# Output: array of K broken lines

def morph(pa, pb, k):
    if len(pa) != len(pb):
      return None

    ans = []
    for iter in  range(k):
      interp = []
      for i in range(len(pa)):
        elem = []
        for j in range(len(pa[i])):
          elem += [pa[i][j] + (pb[i][j] - pa[i][j]) * iter / k]
        interp += [elem]
      ans += [interp]
    return ans


