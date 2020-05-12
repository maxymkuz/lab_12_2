# Implements the Maze ADT using a 2-D array.
from arrays import Array2D
from arrays import Array


class Maze:
    # Define constants to represent contents of the maze cells.
    MAZE_WALL = "*"
    PATH_TOKEN = "x"
    TRIED_TOKEN = "o"

    # Creates a maze object with all cells marked as open.
    def __init__(self, num_rows, num_cols):
        self._mazeCells = Array2D(num_rows, num_cols)
        self._startCell = None
        self._exitCell = None

    # Returns the number of rows in the maze.
    def num_rows(self):
        return self._mazeCells.num_rows()

    # Returns the number of columns in the maze.
    def num_cols(self):
        return self._mazeCells.num_cols()

    # Fills the indicated cell with a "wall" marker.
    def setWall(self, row, col):
        assert 0 <= row < self.num_rows() and \
               0 <= col < self.num_cols(), f"Cell index out of range." \
                                           f"{row, col}"
        self._mazeCells[row, col] = self.MAZE_WALL

    # Sets the starting cell position.
    def setStart(self, row, col):
        assert 0 <= row < self.num_rows() and \
               0 <= col < self.num_cols(), "Cell index out of range."
        self._startCell = _CellPosition(row, col)

    # Sets the exit cell position.
    def setExit(self, row, col):
        assert 0 <= row < self.num_rows() and \
               0 <= col < self.num_cols(), "Cell index out of range."
        self._exitCell = _CellPosition(row, col)

    def bfs_the_graph(self, cur):
        """
        Performs BFS on maze and finds the shortest path
        possible, returns False if not possible
        """
        if self._exitFound(cur.row, cur.col):
            res = Array(10)
            return [cur]
        elif self._been_here(cur.row, cur.col):
            return False
        self._markTried(cur.row, cur.col)
        # Finding the shortest path possible
        min_length = -1
        res = False
        for i in range(-1, 2):
            for j in range(-1, 2):
                if abs(i) == abs(j):
                    continue
                # if the next move is not valid:
                if not self._validMove(cur.row + i, cur.col + j):
                    continue
                is_possible = self.bfs_the_graph(
                    _CellPosition(cur.row + i, cur.col + j))
                if is_possible:
                    if len(is_possible) < min_length or min_length == -1:
                        res = is_possible + [cur]
                        min_length = len(res)
        return res

    # Attempts to solve the maze by finding a path from the starting cell
    # to the exit. Returns True if a path is found and False otherwise.
    def findPath(self):
        """
        Performs BFS on maze and finds the shortest path
        possible, returns False if not possible
        """
        if self._startCell is None or self._exitCell is None:
            raise ValueError('start and end cells are not defined')
        x = self.bfs_the_graph(self._startCell)
        self._markTried(self._startCell.row, self._startCell.col)
        if x:
            x = x[::-1]
            print('The shortest path is through the following cells:')
            for cell in x:
                self._markPath(cell.row, cell.col)
                print(str(cell), ' ', end='')
            print()
        else:
            print("No possible solutions")
        return x

    # Resets the maze by removing all "path" and "tried" tokens.
    def reset(self):
        for row in range(self.num_rows()):
            for col in range(self.num_rows()):
                if self._mazeCells[row, col] != self.MAZE_WALL:
                    self._mazeCells[row, col] = None

    # Prints a text-based representation of the maze.
    def draw(self):
        for row in range(self.num_rows()):
            for col in range(self.num_rows()):
                el = self._mazeCells[row, col]
                print(el if el else '_', end='')
            print()
        print()

    # Returns True if the given cell position is a valid move.
    def _validMove(self, row, col):
        return 0 <= row < self.num_rows() \
               and 0 <= col < self.num_cols() \
               and self._mazeCells[row, col] is None

    # Helper method to determine if the exit was found.
    def _exitFound(self, row, col):
        return row == self._exitCell.row and col == self._exitCell.col

    # Drops a "tried" token at the given cell.
    def _markTried(self, row, col):
        self._mazeCells[row, col] = self.TRIED_TOKEN

    # Drops a "path" token at the given cell.
    def _markPath(self, row, col):
        self._mazeCells[row, col] = self.PATH_TOKEN

    # Checks if I have been here before:
    def _been_here(self, row, col):
        return self._mazeCells[(row, col)] is not None


# Private storage class for holding a cell position.
class _CellPosition(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return f'({self.row}, {self.col})'


if __name__ == '__main__':
    test_maze = Maze(5, 5)
    test_maze.setStart(4, 1)
    test_maze.setExit(3, 4)
    test_maze.setWall(0, 0)
    test_maze.setWall(0, 1)
    test_maze.setWall(0, 2)
    test_maze.setWall(0, 3)
    test_maze.setWall(0, 4)
    test_maze.setWall(1, 0)
    test_maze.setWall(1, 2)
    test_maze.setWall(1, 4)
    test_maze.setWall(2, 0)
    # test_maze.setWall(2, 2)
    test_maze.setWall(2, 4)
    test_maze.setWall(3, 0)
    test_maze.setWall(3, 2)
    test_maze.setWall(4, 2)
    test_maze.setWall(4, 3)
    test_maze.setWall(4, 4)
    test_maze.draw()
    test_maze.findPath()
    test_maze.draw()
    test_maze.reset()
    test_maze.draw()
