# -*- coding: utf-8 -*-

from graph import Graph

__author__ = 'Patricio Lopez Juri'


if __name__ == '__main__':

    def nodes():
        return [str(i) for i in range(1, 12)]  # [1, ..., 11]

    def paths():
        def clique(items):
            return {(str(i), str(j)) for i in items for j in items if i != j}

        E = set()
        E = E.union(clique([1, 2, 3, 4, 5]))
        E = E.union(clique([6, 7, 8, 9, 10]))
        E = E.union(clique([3, 6, 11]))
        return E

    graph1 = Graph(V=nodes(), E=paths(), K=['1', '9'])

    '''
    print("V:")
    print(graph1.V)

    print("E:")
    print(graph1.E)

    print("A:")
    print(graph1.A)

    print("D:")
    print(graph1.D())

    print("P:")
    print(graph1.P())

    print("*P:")
    print(graph1.P_star('1'))

    print("*Q:")
    print(graph1.Q_star('1'))

    print("*R:")
    print(graph1.R_star('1'))

    print("*I:")
    print(graph1.I_star('1'))
    '''

    print("*N: From '1'")
    G1 = graph1.N_star('1')
    print(G1)

    print("*N: From '9'")
    G2 = graph1.N_star('9')
    print(G2)

    print("Combined *N:")
    print(G1 + G2)
