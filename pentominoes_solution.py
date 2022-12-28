pentominoes = {
    # F
    (
        (0,1,1),
        (1,1,0),
        (0,1,0),
    ),
    # I
    (
        (1,1,1,1,1),
    ),
    # L
    (
        (1,1,1,1),
        (0,0,0,1),
    ),
    # N
    (
        (1,1,0,0),
        (0,1,1,1),
    ),
    # P
    (
        (1,1,1),
        (0,1,1),
    ),
    # T
    (
        (1,1,1),
        (0,1,0),
        (0,1,0),
    ),
    # U
    (
        (1,0,1),
        (1,1,1),
    ),
    # V
    (
        (1,0,0),
        (1,0,0),
        (1,1,1),
    ),
    # W
    (
        (1,0,0),
        (1,1,0),
        (0,1,1),
    ),
    # X
    (
        (0,1,0),
        (1,1,1),
        (0,1,0),
    ),
    # Y
    (
        (0,0,1,0),
        (1,1,1,1),
    ),
    # Z
    (
        (1,1,0),
        (0,1,0),
        (0,1,1),
    )
}

class Node():
    def __init__(self, value):
        self.value = value
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.row_head = None
        self.col_head = None

class LinkedList():
    def __init__(self, width):
        self.width = width
        self.head = None
        self.size = 0

    def append(self, value):
        new_node = Node(value)

        if self.head is None:
            self.head = left_node = right_node = up_node = down_node = new_node
        elif self.size % self.width == 0:
            up_node = self.head.up
            down_node = self.head
            left_node = right_node = new_node
        else:
            left_node = self.head.up.left
            right_node = left_node.right
            if left_node is left_node.up:
                up_node = down_node = new_node
            else:
                up_node = left_node.up.right
                down_node = up_node.down

        new_node.up = up_node
        new_node.down = down_node
        new_node.left = left_node
        new_node.right = right_node
        new_node.row_head = right_node
        new_node.col_head = down_node

        up_node.down = new_node
        down_node.up = new_node
        right_node.left = new_node
        left_node.right = new_node
        self.size += 1

    def insert_row(self, node):
        current_node = node
        while current_node:
            up_node = current_node.up
            down_node = current_node.down

            up_node.down = current_node
            down_node.up = current_node

            current_node = current_node.right
            if current_node is node:
                break

    def insert_column(self, node):
        current_node = node
        while current_node:
            left_node = current_node.left
            right_node = current_node.right

            left_node.right = current_node
            right_node.left = current_node

            current_node = current_node.down
            if current_node is node:
                break

    def delete_row(self, node):
        current_node = node
        while current_node:
            up_node = current_node.up
            down_node = current_node.down

            if current_node is self.head:
                self.head = down_node
                if current_node is down_node:
                    self.head = None

            up_node.down = down_node
            down_node.up = up_node

            current_node = current_node.right
            if current_node is node:
                break

    def delete_column(self, node):
        current_node = node
        while current_node:
            left_node = current_node.left
            right_node = current_node.right

            if current_node is self.head:
                self.head = right_node
                if current_node is right_node:
                    self.head = None

            left_node.right = right_node
            right_node.left = left_node

            current_node = current_node.down
            if current_node is node:
                break

    def check_nonzero_column(self, node):
        current_node = node
        while current_node:
            if current_node.value and current_node.row_head is not self.head:
                yield current_node
            current_node = current_node.down
            if current_node is node:
                break

    def check_nonzero_row(self, node):
        current_node = node
        while current_node:
            if current_node.value and current_node.col_head is not self.head:
                yield current_node
            current_node = current_node.right
            if current_node is node:
                break

class Board():
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.pentominoes = pentominoes
        self.solutions = set()
        self.linked_list = None
        self.start_board = [[0] * columns for _ in range(rows)]
        self.rotation_count = 0

    def find_solutions(self):
        named_pentominoes = set(enumerate(self.pentominoes, 1))
        all_shapes = self.fetch_unique_shapes(named_pentominoes)

        self.linked_list = LinkedList(self.rows * self.columns + 1)
        generated_positions = self.generate_positions(all_shapes, self.rows, self.columns)

        for line in generated_positions:
            for val in line:
                self.linked_list.append(val)
        self.reduce_linked_list(self.linked_list)
        self.algo_x(self.linked_list, self.start_board)
        return len(self.solutions)

    def find_minimum_column(self, linked_list, min_column):
        min_column_sum = float("inf")
        for col in linked_list.check_nonzero_row(linked_list.head):
            tmp = sum(1 for item in linked_list.check_nonzero_column(col))
            if tmp < min_column_sum:
                min_column = col
                min_column_sum = tmp
        return min_column, min_column_sum

    def find_shape_positions(self, value):
        row = value // self.columns
        column = value - row * self.columns
        return row, column

    def rotation(self, shape):
        return tuple(zip(*shape[::-1]))

    def reflection(self, shape):
        return tuple(shape[::-1])

    def reduce_linked_list(self, linked_list):
        for col_head_node in linked_list.check_nonzero_row(linked_list.head):
            row, col = self.find_shape_positions(col_head_node.value - 1)
            if self.start_board[row][col]:
                linked_list.delete_column(col_head_node)

    def is_unique_solution(self, solution):
        reflected_solution = self.reflection(solution)
        for sol in [solution, reflected_solution]:
            if sol in self.solutions:
                return
            for _ in range(3):
                sol = self.rotation(sol)
                if sol in self.solutions:
                    return
        return 1

    def tiling_shape_to_board(self, shape_row, prev_steps_result):
        new_board = prev_steps_result.copy()
        for node in self.linked_list.check_nonzero_row(shape_row):
                row, col = self.find_shape_positions(node.col_head.value - 1)
                new_board[row][col] = node.row_head.value
        return new_board

    def fetch_unique_shapes(self, named_pentominoes):
        rotation = set(named_pentominoes)
        for name, shape in named_pentominoes:
            rotation.add((name, self.reflection(shape)))

        all_rotation = set(rotation)
        for name, shape in rotation:
            for _ in range(3):
                shape = self.rotation(shape)
                all_rotation.add((name, shape))

        return all_rotation

    def algo_x(self, linked_list, board):
        if linked_list.head.down is linked_list.head:
            self.rotation_count += 1
            if linked_list.head.right is linked_list.head:
                solution = tuple(tuple(row) for row in board)
                if self.is_unique_solution(solution):
                    self.solutions.add(solution)
                    self.print_board(solution)
                return
        min_column, min_column_sum = self.find_minimum_column(linked_list, linked_list.head)
        if min_column_sum == 0:
            self.rotation_count += 1
            return

        intersected_rows = []
        for node in linked_list.check_nonzero_column(min_column):
            intersected_rows.append(node.row_head)

        for selected_row in intersected_rows:
            retraveresed_rows = []

            new_board = self.tiling_shape_to_board(selected_row, board)

            for shape_node in linked_list.check_nonzero_column(linked_list.head):
                if shape_node.value == selected_row.value:
                    retraveresed_rows.append(shape_node)
                    linked_list.delete_row(shape_node)

            columns_to_restore = []

            for col_node in linked_list.check_nonzero_row(selected_row):
                for row_node in linked_list.check_nonzero_column(col_node.col_head):
                    retraveresed_rows.append(row_node.row_head)
                    linked_list.delete_row(row_node.row_head)
                columns_to_restore.append(col_node.col_head)
                linked_list.delete_column(col_node.col_head)
            self.algo_x(linked_list, new_board)

            for row in retraveresed_rows:
                linked_list.insert_row(row)

            for col in columns_to_restore:
                linked_list.insert_column(col)

    def generate_positions(self, rotation, rows, columns):
        def check_shape_rotation(name, shape, y, x, width, height):
            line = [cell for row in self.start_board for cell in row]
            for r in range(height):
                for c in range(width):
                    if shape[r][c]:
                        num = (r + y) * columns + x + c
                        if line[num]:
                            return
                        line[num] = shape[r][c]
            line.insert(0, name)
            return line
        yield [i for i in range(rows * columns + 1)]

        for name, shape in rotation:
            shape_height = len(shape)
            shape_width = len(shape[0])
            for row in range(rows):
                if row + shape_height > rows:
                    break
                for col in range(columns):
                    if col + shape_width > columns:
                        break
                    new_line = check_shape_rotation(name, shape, row, col, shape_width, shape_height)
                    if new_line:
                        yield new_line

    def print_board(self, board):
        for row in board:
            for cell in row:
                print(f"{cell: >3}", end='')
            print()
        print()
        print("-" * 80)

if __name__ == '__main__':
    board = Board(3, 20)
    sol_count = board.find_solutions()
    print(f"3X20 # of solutions: {sol_count}")
    board = Board(4, 15)
    sol_count = board.find_solutions()
    print(f"4X15 # of solutions: {sol_count}")
    board = Board(5, 12)
    sol_count = board.find_solutions()
    print(f"5X12 # of solutions: {sol_count}")
    board = Board(6, 10)
    sol_count = board.find_solutions()
    print(f"6X10 # of solutions: {sol_count}")