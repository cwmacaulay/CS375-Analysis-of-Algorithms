# Implementation of Hierholzer's Algorithm
# Charles Macaulay
# CS 481
# 12-19-15

# Sources I used to come up with this algorithm:
# Feynman Liang, Github: https://github.com/feynmanliang/Euler-Tour/blob/master/FindEulerTour.py
# Gregor Ulm, http://gregorulm.com/finding-an-eulerian-path/


from collections import defaultdict

def Hierholzer_tour(G):
    tour = []
    E = G
    edgenum = defaultdict(int)

    # recursive function implements Hierholzer's algorithm.
    def find_tour(u):
        for e in E:
            if u == e[0]:
                u,v = e
                E.remove(e)
                find_tour(v)
            elif u == e[1]:
                v,u = e
                E.remove(e)
                find_tour(v)
        tour.insert(0,u)

    # this is the preliminary check to make sure there aren't any odd vertices.
    for i,j in G:
        edgenum[i] += 1
        edgenum[j] += 1

    for i,j in edgenum.iteritems():
        if not (j % 2 == 0):
            print "Hierholzer cannot find tour if odd vertices"
            exit()

    find_tour(G[0][0])

    print tour


if __name__ == '__main__':

    G = [(1,2),(2,3),(3,4),(4,1)]
    Hierholzer_tour(G)
