import math

# умножает матрицу 3х3 на вектор
def multiply(matrix, vector):
    ans = []
    for i in range(len(matrix)):
        sum = 0
        for j in range(len(vector)):
            sum += matrix[i][j] * vector[j]
        ans += [sum]
    return ans


# возвращает центроид для множества точек
def centroid(vectors):
    sum = [0, 0, 0]
    for v in vectors:
        for j in range(3):
            sum[j] += v[j]
    return [x/len(vectors) for x in sum]


def minus(va,vb):
    return [va[i]-vb[i] for i in range(len(va))]


# расстояние между двумя точками
def dist(va, vb):
    return math.sqrt(sum([x*x for x in minus(va,vb)]))



# квадратичное отклонение точек от центра
def rms(va):
    c = centroid(va)
    return math.sqrt(sum([dist(minus(v,c)) for v in va])/len(va))

# для двух цепочек векторов возвращает одну, составленную из попарных минусов
def minus_lines(l1, l2):
    return [minus(l1[i],l2[i]) for i in range(len(l1))]
