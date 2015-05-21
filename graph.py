# -*- coding: utf-8 -*-

from index_matrix import Matrix

__author__ = 'Patricio Lopez Juri'


class Graph:

    def __init__(self, V, E, K):
        self.V = V
        self.E = E
        self.K = K
        self.A = Matrix.square(items=V)
        for a, b in self.E:
            self.A[a, b] = 1

    @property
    def order(self):
        return len(self.V)

    @property
    def n(self):
        return self.order

    @property
    def k(self):
        return len(self.K)

    def d(self, i):
        return self.A.row(i).sum()

    def D(self):
        D = Matrix.square(items=self.V)
        for item in self.V:
            D[item, item] = self.d(item)
        return D

    def p(self, i, j):
        return self.A[i, j] / self.d(i)

    def p_star(self, start, i, j):
        absorbents = [k for k in self.K if k != start]
        if i in absorbents and i == j:
            return 1
        elif i in absorbents and i != j:
            return 0
        else:
            return self.p(i, j)

    def P(self):
        return self.D().inverse() * self.A

    def P_star(self, start):

        def function(i, j):
            return self.p_star(start, i, j)

        P_star = self.A.map(function=function)

        absorbents = [k for k in self.K if k != start]
        for i, absorbent in enumerate(absorbents):
            P_star.swap_columns(P_star.horizontal_items[-(1 + i)], absorbent)

        return P_star

    def Q_star(self, start):
        size = self.n - self.k + 1
        return self.P_star(start)[0:size, 0:size]

    def R_star(self, start):
        size = self.n - self.k + 1
        return self.P_star(start)[0:size, size:(size + self.k - 1)]

    def Zero_star(self, start):
        pass

    def I_star(self, start):
        size = self.n - self.k + 1
        range = size + self.k - 1
        return self.P_star(start)[size:range, size:range]

    def N_star(self, start):
        Q_star = self.Q_star(start)
        identity = Q_star.clone_identity()
        return (identity - Q_star).inverse()
