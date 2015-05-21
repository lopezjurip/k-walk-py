# -*- coding: utf-8 -*-

import numpy

__author__ = 'Patricio Lopez Juri'


class Matrix():

    def __init__(self, vertical_items, horizontal_items, matrix=None):
        if matrix is not None:
            self.matrix = numpy.copy(matrix)
        else:
            self.matrix = numpy.zeros((len(vertical_items), len(horizontal_items)))

        self.vertical_items = vertical_items
        self.vertical_mapping = {vertical_items[i]: i for i in
                                 range(len(vertical_items))}
        self.horizontal_items = horizontal_items
        self.horizontal_mapping = {horizontal_items[j]: j for j in
                                   range(len(horizontal_items))}

    @classmethod
    def square(cls, items, matrix=None):
        return cls(vertical_items=items, horizontal_items=items, matrix=matrix)

    def __getitem__(self, key):
        if isinstance(key, int):
            print("HEY!")
            return None
        elif isinstance(key, tuple):
            l, r = key
            if isinstance(l, slice) and isinstance(r, slice):
                return Matrix(self.vertical_items[l.start: l.stop],
                              self.horizontal_items[r.start: r.stop],
                              self.matrix[l.start: l.stop, r.start: r.stop])
            else:
                i = self.vertical_mapping[l]
                j = self.horizontal_mapping[r]
                return self.matrix[i, j]
        elif isinstance(key, slice):
            print("HEY!")
            return None

    def __setitem__(self, pos, value):
        i, j = pos
        i = self.vertical_mapping[i]
        j = self.horizontal_mapping[j]
        self.matrix[i, j] = value

    def __add__(self, other):
        v_items = list(set(self.vertical_items) | set(other.vertical_items))
        h_items = list(set(self.horizontal_items) | set(other.horizontal_items))
        new = Matrix(v_items, h_items)

        def add(a, b):
            if (a, b) in self and (a, b) in other:
                return self[a, b] + other[a, b]
            elif (a, b) in self:
                return self[a, b]
            elif (a, b) in other:
                return other[a, b]
            else:
                return 0

        return new.map(function=add)

    def __sub__(self, other):
        return Matrix(vertical_items=self.vertical_items,
                      horizontal_items=other.horizontal_items,
                      matrix=numpy.subtract(self.matrix, other.matrix))

    def __mul__(self, other):
        # self * other
        if self.width != other.height:
            # TODO: exception
            return None

        return Matrix(vertical_items=self.vertical_items,
                      horizontal_items=other.horizontal_items,
                      matrix=numpy.dot(self.matrix, other.matrix))

    def __rmul__(self, other):
        # other * self
        if self.height != other.width:
            # TODO: exception
            return None

        return Matrix(vertical_items=other.vertical_items,
                      horizontal_items=self.horizontal_items,
                      matrix=numpy.dot(other.matrix, self.matrix))

    def __len__(self):
        return len(self.vertical_items) * len(self.horizontal_items)

    @property
    def is_square(self):
        return len(self.vertical_items) == len(self.horizontal_items)

    def __contains__(self, item):
        i, j = item
        return i in self.vertical_items and j in self.horizontal_items

    def clone(self):
        return Matrix(self.vertical_items, self.horizontal_items, self.matrix)

    def clone_empty(self):
        return Matrix(self.vertical_items, self.horizontal_items)

    def clone_identity(self):
        if self.is_square:
            return Matrix(self.vertical_items,
                          self.horizontal_items,
                          numpy.identity(self.width))
        else:
            # TODO Exception
            return None

    def inverse(self):
        new = self.clone()
        new.matrix = numpy.linalg.inv(self.matrix)
        return new

    def map(self, function):
        new = self.clone_empty()
        for i in new.vertical_items:
            for j in new.horizontal_items:
                new[i, j] = function(i, j)
        return new

    @property
    def height(self):
        return len(self.vertical_items)

    @property
    def width(self):
        return len(self.horizontal_items)

    def swap_columns(self, frm, to):
        to_index = self.horizontal_mapping[to]
        from_index = self.horizontal_mapping[frm]
        self.matrix[:, [from_index, to_index]] = self.matrix[:, [to_index, from_index]]
        self.swap_columns_label(frm, to)
        self.swap(self.horizontal_items, frm, to)

    def swap_rows(self, frm, to):
        to_index = self.vertical_mapping[to]
        from_index = self.vertical_mapping[frm]
        self.matrix[[from_index, to_index], :] = self.matrix[[to_index, from_index], :]
        self.swap_rows_label(frm, to)
        self.swap(self.vertical_items, frm, to)

    def swap_rows_label(self, frm, to):
        aux = self.vertical_mapping[frm]
        self.vertical_mapping[frm] = self.vertical_mapping[to]
        self.vertical_mapping[to] = aux

    def swap_columns_label(self, frm, to):
        aux = self.horizontal_mapping[frm]
        self.horizontal_mapping[frm] = self.horizontal_mapping[to]
        self.horizontal_mapping[to] = aux

    @staticmethod
    def swap(collection, frm, to):
        a, b = collection.index(frm), collection.index(to)
        collection[b], collection[a] = collection[a], collection[b]

    def column(self, index):
        return self.matrix[:, self.horizontal_mapping[index]]

    def row(self, index):
        return self.matrix[self.vertical_mapping[index], :]

    def __str__(self):
        result = "\t |_" + "__\t_".join(self.vertical_items) + "_|\n"
        for i in self.vertical_items:
            result += str(i) + ":\t ["
            result += " \t".join([str(numpy.around(self[i, j], 2)) for j in self.horizontal_items])
            result += "]\n"
        return result
