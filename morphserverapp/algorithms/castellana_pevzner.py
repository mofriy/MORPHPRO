from .basic_operations import *

class CastellanaPevzner:

    def __init__(self,start,finish):
        self.start = start
        self.finish = finish
        # размер куба вокруг вершины в ангстремах
        self.lattice_width = 2
        # количество вершин решётки "в одном измерении".
        # таким образом всего вершин - @lattices**3
        self.lattices = 6

        self.proto = None

    def morph(self,k):
        p = [self.start]
        for i in range(k):
            tmp = intermediate(p[i - 1],self.finish, 1 / (k + 2 - i))
            proto = proteinize(tmp)
            p += [self.proto]

# протеинизирует цепочку, лежащую в proto
    def proteinize(self,protein):
        self.proto = protein
        n = len(self.proto)
        path = [[0 for i in range(n)] for j in range(self.lattices**3)]
        back = path.clone()

        for i in range(self.lattices**3):
            path[i][0] = vscore(i, 0)
            back[i][0] = -1

        for j in range(n):
            for i in range(self.lattices**3):
                min = float('inf')
                min_id = -1
                h = 0
                for h in range(self.lattices**3):
                    tmp = path[h][j-1]+escore(v(h,j-1),v(i,j))
                    if min > tmp:
                        min = tmp
                        min_id = h
                path[i][j] = vscore(i+1,j)+min
                back[i][j] = min_id

        best = float('inf')
        best_id = -1
        for i in range(self.lattices**3):
            if path[i][n-1] != -1 and path[i][n-1] < best:
                best = path[i][n-1]
                best_id = i

        if best_id == -1:
            return False
        else:
            backtrack(back,best_id,n-1)
            return True

    def backtrack(self,back, i, j):
        if i == -1: return
        self.proto[j] = v(i,j)
        self.backtrack(back,back[i][j],j-1)


    def intermediate(self,a, b, koeff):
        ans = []
        for i in range(len(a)):
            u = []
            for j in range(2):
                u += [a[i][j]*koeff + (1-koeff)*b[i][j]]
            ans += [u]
        return  ans

    # возвращаем i-ую вершину из решётки вокруг j-ой вершины цепочки proto
    # TODO в будущем это можно захардкодить, чтобы каждый раз не пересчитывать
    def v(self,i, j):
        s = self.lattices
        ss = self.lattices**2
        ix = i/ss
        iy = (i%ss)/s
        iz = i%s
        r = self.lattice_width/s
        m = self.lattice_width/2
        return [r*ix-m,r*iy-m,r*iz-m]


    def escore(self,v1, v2):
        d = dist(v1, v2)
        if d>=3.7 and d<=3.9:
            return 0
        else:
            return float('inf')


    def vscore(self,i, j):
        return dist(v(i, j), self.proto[j])
