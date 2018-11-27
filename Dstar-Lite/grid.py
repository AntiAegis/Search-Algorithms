#------------------------------------------------------------------------------
#   Libraries
#------------------------------------------------------------------------------
from graph import Node, Graph


#------------------------------------------------------------------------------
#   Class of Grid
#------------------------------------------------------------------------------
class GridWorld(Graph):
    def __init__(self, x_dim, y_dim, connect8=True):
        self.x_dim = x_dim
        self.y_dim = y_dim

        self.cells = [0] * y_dim
        for i in range(y_dim):
            self.cells[i] = [0] * x_dim

        self.connect8 = connect8
        self.graph = {}
        self.generateGraphFromGrid()


    def __str__(self):
        msg = 'Graph:'
        for i in self.graph:
            msg += '\n  node: ' + i + ' g: ' + \
                str(self.graph[i].g) + ' rhs: ' + str(self.graph[i].rhs) + \
                ' neighbors: ' + str(self.graph[i].children)
        return msg


    def __repr__(self):
        return self.__str__()


    def printGrid(self):
        print('** GridWorld **')
        for row in self.cells:
            print(row)


    def printGValues(self):
        for j in range(self.y_dim):
            str_msg = ""
            for i in range(self.x_dim):
                node_id = 'x' + str(i) + 'y' + str(j)
                node = self.graph[node_id]
                if node.g == float('inf'):
                    str_msg += ' - '
                else:
                    str_msg += ' ' + str(node.g) + ' '
            print(str_msg)


    def generateGraphFromGrid(self, edge_weight=1):
        for i in range(len(self.cells)):
            row = self.cells[i]
            for j in range(len(row)):
                node = Node('x' + str(i) + 'y' + str(j))

                if i > 0:  # not top row
                    node.parents['x' + str(i - 1) + 'y' + str(j)] = edge_weight
                    node.children['x' + str(i - 1) + 'y' + str(j)] = edge_weight
                if i + 1 < self.y_dim:  # not bottom row
                    node.parents['x' + str(i + 1) + 'y' + str(j)] = edge_weight
                    node.children['x' + str(i + 1) + 'y' + str(j)] = edge_weight
                if j > 0:  # not left col
                    node.parents['x' + str(i) + 'y' + str(j - 1)] = edge_weight
                    node.children['x' + str(i) + 'y' + str(j - 1)] = edge_weight
                if j + 1 < self.x_dim:  # not right col
                    node.parents['x' + str(i) + 'y' + str(j + 1)] = edge_weight
                    node.children['x' + str(i) + 'y' + str(j + 1)] = edge_weight

                if self.connect8:
                    if (i > 0) and (j > 0):
                        node.parents['x' + str(i - 1) + 'y' + str(j - 1)] = edge_weight
                        node.children['x' + str(i - 1) + 'y' + str(j - 1)] = edge_weight
                    if (i > 0) and (j + 1 < self.x_dim):
                        node.parents['x' + str(i - 1) + 'y' + str(j + 1)] = edge_weight
                        node.children['x' + str(i - 1) + 'y' + str(j + 1)] = edge_weight
                    if (i + 1 < self.y_dim) and (j > 0):
                        node.parents['x' + str(i + 1) + 'y' + str(j - 1)] = edge_weight
                        node.children['x' + str(i + 1) + 'y' + str(j - 1)] = edge_weight
                    if (i + 1 < self.y_dim) and (j + 1 < self.x_dim):
                        node.parents['x' + str(i + 1) + 'y' + str(j + 1)] = edge_weight
                        node.children['x' + str(i + 1) + 'y' + str(j + 1)] = edge_weight

                self.graph['x' + str(i) + 'y' + str(j)] = node