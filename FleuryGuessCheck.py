# Implementation of Fleury's Algorithm
# Using removal-and-check for bridges.
# Charles Macaulay
# CS 481
# 12-19-15


# Sources I used to come up with this algorithm:
# Dawid Kulig, Github: https://github.com/dejvidk/fleury-algorithm

import copy

class Fleury:

    COLOR_WHITE = 'white'
    COLOR_GRAY = 'grey'
    COLOR_BLACK = 'black'

    # Initialization takes a graph input.
    def __init__(self, graph):
        self.graph = graph

    # Runs the algorithm and prints to the terminal whether
    # or not an Eulerian Path can be found. Prints out the
    # path if it is found.
    def findcircuit(self):
        print "Running Fleury's algorithm for this graph:\n"
        for node in self.graph:
            print node, ' -> ', self.graph[node]
        print '\n'

        # Call the actual algorithm:
        output = self.fleury(self.graph)
        if output:
            print 'Found Eulerian Cycle: '
            for node in output:
                    print node
            print '\n Finished execution.'


    # Function calls tarjan's algorithm to make sure we
    # aren't getting rid of any bridges.
    def is_connected(self, G):
        start_node = list(G)[0]
        color = {}
        iterator = 0;
        for v in G:
            color[v] = Fleury.COLOR_WHITE
        color[start_node] = Fleury.COLOR_GRAY
        S = [start_node]
        while len(S) != 0:
            u = S.pop()
            for v in G[u]:
                if color[v] == Fleury.COLOR_WHITE:
                    color[v] = Fleury.COLOR_GRAY
                    S.append(v)
                color[u] = Fleury.COLOR_BLACK
        return list(color.values()).count(Fleury.COLOR_BLACK) == len(G)

    # Function returns a list of even-degree nodes.
    def even_deg_n(self, G):
        even_deg_ns = []
        for n in G:
            if len(G[n]) % 2 == 0:
                even_deg_ns.append(n)
        return even_deg_ns

    # Function considers the even degree nodes and returns
    # true if the graph is Eulerian and false if it isn't.
    # Does this by subtracting the length of even degree
    # nodes from the total number of nodes and checking
    # if the result is zero.
    def is_eulerian(self, even_deg_n, graph_len):
        return ((graph_len - len(even_deg_n)) == 0)


    # Function takes in the graph and gets the list of edges
    # so that the length of edges can be evaluated in the
    # algorithm.
    def listofedges(self, G):
        edges = []
        for u in G:
            for v in G[u]:
                edges.append( (u,v) )
        return edges


    # Function is the actual Fleury's algorithm.

    def fleury(self, G):
        edn = self.even_deg_n(G)
        if not self.is_eulerian(edn, len(G)):
            print "The graph does not have an Eulerian path. \n"
            exit()
        g = copy.copy(G)
        path = []

        # start at any node that doesn't have degree 0.
        n = edn[0]

        # This while loop removes edges, because edges can
        # be removed from an Eulerian path and it will still
        # be an Eulerian path. It ensures that it doesn't
        # remove an edge by testing the removal then checking
        # if the graph is still connected via DFS marking.
        while (len(self.listofedges(g))) > 0:
            curvert = n
            for n in list(g[curvert]):
                g[curvert].remove(n)
                g[n].remove(curvert)

                # Need to check whether edges are bridges here.
                bridge = not self.is_connected(g)
                if bridge:
                    g[curvert].append(n)
                    g[n].append(curvert)
                else:
                    break
            if bridge:
                g[curvert].remove(n)
                g[n].remove(curvert)
                g.pop(curvert)
            path.append((curvert,n))
        return path

if __name__ == '__main__':

    #G = {0: [1,2], 1:[0,3], 2:[0,3,4], 3: [1,2], 4:[2,3,5], 5: [3,4]}
    G = {0: [4, 5], 1: [2, 3, 4, 5], 2: [1, 3, 4, 5], 3: [1, 2], 4: [0, 1, 2, 5], 5: [0, 1, 2, 4]}
    test = Fleury(G)
    test.findcircuit()
