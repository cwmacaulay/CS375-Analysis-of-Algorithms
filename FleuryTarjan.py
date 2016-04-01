# Implementation of Fleury's Algorithm
# Using tarjan's bridge finding algorithm.
# Charles Macaulay
# CS 481
# 12-19-15

# Sources I used to come up with this algorithm:
# For the tarjan bridge finding part:
# Huayi Zhang, Github: https://gist.github.com/irachex/3922704
# For the general structure of Fleury's algorithm:
# Dawid Kulig, Github: https://github.com/dejvidk/fleury-algorithm




import copy
import tarjan

class FleuryT:

    # Initialization takes a graph input.
    def __init__(self, graph):
        self.graph = graph
        self.bridges = None
        self.trail_Vs_tour = ''

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
    # N is the number of vertices, S is the source node,
    # T is the target node. Edges is a list of edges.
    # The function sets self.bridges to the list of
    # bridges that it encounters.
    def tarjan(self, N, S, T, edges):
        count = 0
        bridges = []
        visit = [0 for i in range(N)]
        low = [N + 1 for i in range(N)]
        ret = [False for i in range(N)]
        q = [0 for i in range(N + 1)]
        q[0] = (S, -1, -1)
        top = 0
        while top >= 0:
            i, father, v = q[top]
            if v == -1:
                ret[i] = (i == T)
                count = count + 1
                visit[i] = low[i] = count
            elif v < len(edges[i]):
                j, w, flag = edges[i][v]
                if flag:
                    if j == q[top + 1][0]:
                        ret[i] = ret[i] or ret[j]
                        if ret[i]: low[i] = min(low[i], low[j])
            v += 1
            q[top] = (i, father, v)
            if v < len(edges[i]):
                j, w, flag = edges[i][v]
                if flag:
                    if not visit[j]:
                        top += 1
                        q[top] = (j, i, -1)
                else:
                    if j != father and visit[j]:
                        low[i] = min(low[i], visit[j])
            else:
                if low[i] == visit[i] and ret[i]:
                    if father >=0:
                        bridges.append((father, i))
                top -= 1
        print bridges
        self.bridges = bridges

    # Function returns a list of even-degree nodes.
    def even_deg_n(self, G):
        even_deg_ns = []
        odd_deg_ns = []
        for n in G:
            if len(G[n]) % 2 == 0:
                even_deg_ns.append(n)
            else:
                odd_deg_ns.append(n)
        return even_deg_ns, odd_deg_ns

    # Function considers the even degree nodes and returns
    # true if the graph is Eulerian and false if it isn't.
    # Does this by subtracting the length of even degree
    # nodes from the total number of nodes and checking
    # if the result is zero.
    def degree_condition(self, even_deg_n, graph_len):
        if ((graph_len - len(even_deg_n)) == 0):
            self.trail_Vs_tour = 'Tour'
        elif  ((graph_len - len(even_deg_n)) == 2):
            self.trail_Vs_tour = 'Trail'

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
        edn,odn = self.even_deg_n(G)
        self.degree_condition(edn, len(G))
        # if the graph is all even degree vertices,
        if (self.trail_Vs_tour == 'Tour'):
            # the algorithm can just pick any vertex to start.
            n = edn[0]
        # if the graph has exactly two odd degree vertices,
        elif (self.trail_Vs_tour == 'Trail'):
            # the algorithm must begin at one of the two odd vertices
            # and end at the other.
            n = odn[0]
            end = odn[1]
            # run an initial tarjan's bridge finding algorithm for the
            # graph.
            self.tarjan(len(G.keys()), n, end, self.listofedges(G))
        else: # (self.trail_Vs_tour == ''):
            print "The graph does not have an Eulerian path. \n"
            exit()

        g = copy.copy(G)
        path = []
        while (len(self.listofedges(g))) > 0:
            curvert = n
            for n in list(g[curvert]):
                #if g[curvert]
                g[curvert].remove(n)
                g[n].remove(curvert)
                #self.tarjan(len(g.keys()), n, end, self.listofedges(g))
            path.append((curvert,n))
        return path

if __name__ == '__main__':

    #G = {0: [1,2], 1:[0,3], 2:[0,3,4], 3: [1,2], 4:[2,3,5], 5: [3,4]}
    G = {0: [1, 4, 5], 1: [0, 2, 3, 4, 5], 2: [1, 3, 4, 5], 3: [1, 2], 4: [0, 1, 2, 5], 5: [0, 1, 2, 4]}
    test = FleuryT(G)
    test.findcircuit()
