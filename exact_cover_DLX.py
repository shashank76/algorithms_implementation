# This is exact cover/ algorithm X(dancing links) implementation
class ExactCover(object):
    __slots__ = ('root', 'solution', 'num_solutions', 'num_searches')

    def __init__(self, matrix=None, secondary=0, state=None):
        self.root = None
        self.solution = []
        self.num_solutions = 0
        self.num_searches = 0

        if state:
            self.solution = state.solution
            self.num_solutions = state.num_solutions
            self.num_searches = state.num_searches
        if matrix:
            self.load_matrix(matrix, secondary)

    def load_matrix(self, matrix, secondary=0):
        self.root = root = Root()
        root.left = root.right = root
        columns = []
        prev = root
        for name in matrix[0]:
            column = Column(name=name, left=prev, right=root)
            prev.right = column
            root.left = column
            column.up = column.down = column
            columns.append(column)
            prev = column
        for i in range(secondary):
            column = root.left
            root.left = column.left
            root.left.right = root
            column.left = column.right = column
        for row in matrix[1:]:
            first = None
            last = None
            for i, item in enumerate(row):
                if item:
                    column = columns[i]
                    value = values(column=column, up=column.up, down=column)
                    if first is None:
                        first = value
                        last = value
                    column.up.down = value
                    column.up = value
                    value.left = last
                    value.right = first
                    last.right = value
                    first.left = value
                    column.size += 1
                    last = value

    def solve(self, level=0):
        if self.root.right is self.root:
            yield list(self.solution)
            return
        self.num_searches += 1
        c = self.root.choose_column()
        c.cover()
        for r in c.down_siblings():
            row = sorted(d.column.name for d in r.row_data())
            if len(self.solution) > level:
                if self.solution[level] != row:
                    continue
            else:
                self.solution.append(row)
            for j in r.right_siblings():
                j.column.cover()
            for solution in self.solve(level+1):
                yield solution
            self.solution.pop()
            for j in r.left_siblings():
                j.column.uncover()
        c.uncover()

    def format_solution(self):
        self.num_solutions += 1
        parts = ['solution %i:' % self.num_solutions]
        for row in self.solution:
            parts.append(' '.join(cell for cell in row
                            if not ((',' in cell) and (cell.endswith('i')))))
        return '\n'.join(parts)

class values(object):
    __slots__ = ('up', 'down', 'left', 'right', 'column')

    def __init__(self, up=None, down=None, left=None, right=None, column=None):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.column = column

    def row_data(self):
        return [self] + self.right_siblings()

    def right_siblings(self):
        next = self.right
        sibs = []
        while next != self:
            sibs.append(next)
            next = next.right
        return sibs

    def left_siblings(self):
        next = self.left
        sibs = []
        while next != self:
            sibs.append(next)
            next = next.left
        return sibs

    def down_siblings(self):
        next = self.down
        sibs = []
        while next != self:
            sibs.append(next)
            next = next.down
        return sibs

    def up_siblings(self):
        next = self.up
        sibs = []
        while next != self:
            sibs.append(next)
            next = next.up
        return sibs

class Column(values):
    __slots__ = ('name', 'size')

    def __init__(self, up=None, down=None, left=None, right=None, column=None,
                 name=None, size=0):
        values.__init__(self, up, down, left, right, column)
        self.name = name
        self.size = size

    def cover(self):
        self.right.left = self.left
        self.left.right = self.right
        for i in self.down_siblings():
            for j in i.right_siblings():
                j.down.up = j.up
                j.up.down = j.down
                j.column.size -= 1

    def uncover(self):
        for i in self.up_siblings():
            for j in i.left_siblings():
                j.column.size += 1
                j.down.up = j
                j.up.down = j
        self.right.left = self
        self.left.right = self

class Root(values):
    __slots__ = ('name',)

    up = None
    down = None
    column = None

    def __init__(self, left=None, right=None):
        name = 'root'
        self.left = left
        self.right = right

    def __str__(self):
        seen = set()
        header = []
        columns = {}
        width = 0
        for i, column in enumerate(self.right_siblings()):
            value = '%s/%s' % (column.name, column.size)
            header.append(value)
            width = max(width, len(value))
            columns[column] = i
        lines = [' '.join('%-*s' % (width, h) for h in header)]
        for i, column in enumerate(self.right_siblings()):
            for row in column.down_siblings():
                if row in seen:
                    continue
                line = []
                lastcol = -1
                for item in row.row_data():
                    seen.add(item)
                    colnum = columns[item.column]
                    line.extend([' '] * (colnum - lastcol - 1))
                    line.append(item.column.name)
                    lastcol = colnum
                lines.append(' '.join('%-*s' % (width, item)
                                      for item in line))
        return '\n'.join(lines)

    def choose_column(self):
        for column in self.right_siblings():
            size = column.size
        return column


if __name__ == '__main__':
    column_name = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    matrix = [column_name,
        [0, 0, 1, 0, 1, 0, 0],
        [1, 0, 0, 1, 0, 0, 1],
        [0, 1, 1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 1, 0, 1]]
    matrix_values = ExactCover(matrix)
    print('matrix root representation =', matrix_values.root)
    for solution in matrix_values.solve():
        print(matrix_values.format_solution())
        print('unformatted values =', solution)
    print(matrix_values.num_searches, 'searches')