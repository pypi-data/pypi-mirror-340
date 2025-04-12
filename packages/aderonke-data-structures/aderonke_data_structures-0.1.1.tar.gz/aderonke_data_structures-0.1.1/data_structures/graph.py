class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, vertex1, vertex2):
        if vertex1 not in self.adj_list:
            self.add_vertex(vertex1)
        if vertex2 not in self.adj_list:
            self.add_vertex(vertex2)
        if vertex2 not in self.adj_list[vertex1]:
            self.adj_list[vertex1].append(vertex2)
        if vertex1 not in self.adj_list[vertex2]:
            self.adj_list[vertex2].append(vertex1)

    def remove_edge(self, vertex1, vertex2):
        if vertex1 in self.adj_list and vertex2 in self.adj_list[vertex1]:
            self.adj_list[vertex1].remove(vertex2)
        if vertex2 in self.adj_list and vertex1 in self.adj_list[vertex2]:
            self.adj_list[vertex2].remove(vertex1)

    def remove_vertex(self, vertex):
        if vertex in self.adj_list:
            for adjacent in self.adj_list[vertex]:
                self.adj_list[adjacent].remove(vertex)
            del self.adj_list[vertex]

    def display(self):
        for vertex in self.adj_list:
            print(vertex, ":", self.adj_list[vertex])
