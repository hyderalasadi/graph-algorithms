from random import choice

def read(file):
    """
    pre-process input text file

    Parameters
    ----------
    file : text file
        representats adjacency list of a simple undirected graph, the first column in
        each row is a node and the rest of the row are it's adjacent nodes

    Return
    ------
    graph : list
        list of adjacency lists of a simple undirected graph, the first element in each
        list is a node and the rest of the elements are it's adjacent nodes
    """

    with open(file, 'r') as f:
        ls = f.readlines()
        graph = [list(map(int, i.split('\t')[:-1])) for i in ls]
    return graph

def create():
    """create a copy from graph"""
    global graph
    return [i.copy() for i in graph]

def mincut(g):
    """
    Karger's minimum cut algorithm implementation

    Parameters
    ----------
    g : list
        list of adjacency lists of a simple undirected graph, the first element in each
        list is a node and the rest of the elements are it's adjacent nodes

    Return
    ------
        min-cut crossing edge count and all node merges in sequence
    """

    A = []  # list of node merges
    while len(g) > 2:  # while there are more than 2 nodes
        c1 = choice(range(len(g)))  # choose 1st node to merge (to delete)
        v_del = g.pop(c1)  # pop its row
        c2 = choice(range(1, len(v_del)))  # choose 2nd node to merge (adjacent)
        v1, v2 = v_del[0], v_del[c2]  # assign nodes values
        A.append((v1, v2))  # append (v1, v2) to the list
        while v2 in v_del:  # remove all self-loop caused by v2
            v_del.remove(v2)
        for i in range(len(g)):  # go over all rows
            if g[i][0] == v2:  # if it’s v2 row
                g[i] += v_del  # append v1 edges
                while v1 in g[i]:  # remove all self-loop caused by v1
                    g[i].remove(v1)
            for j in range(len(g[i])):  # if it’s not v2 row
                g[i][j] = v2 if g[i][j] == v1 else g[i][j]  # change v1 edge to v2
    return len(g[0])-1, A  # g has 2 rows (sides) with equal length (number of edges)

def find_mincut_nodes(graph, mincut_merges):
    """
    post-processing mincut merge sequence to extract elements of the two sides of mincut

    Parameters
    ----------
    graph : list
        list of adjacency lists of a simple undirected graph, the first element in each
        list is a node and the rest of the elements are it's adjacent nodes
    mincut_merges : list
        sequence of all merges executed by mincut algorithm

    Return
    ------
    A, B : list
        nodes of each side of the mincut
    """

    merged_nodes = [i[0] for i in mincut_merges]  # all merged nodes
    all_nodes = [i[0] for i in graph]  # all graph nodes
    unmerged_nodes = []  # last 2 nodes (unmerged)
    for i in all_nodes:
        if i not in merged_nodes:
            unmerged_nodes.append(i)
    rev_mincut_merges = [(i[1], i[0]) for i in mincut_merges[::-1]]  # reverse mincut merge sequence
    A, B = [unmerged_nodes[0]], [unmerged_nodes[1]]  # initiate the two sides of mincut with unmerged nodes
    for i in rev_mincut_merges:  # go over all merges
        if i[0] in A:  # if the merged-to node in A
            A.append(i[1])  # then the merged node is in A as well
        elif i[0] in B:  # if the merged-to node in B
            B.append(i[1])  # then the merged node is in B as well
    return A, B


# driver code
if __name__ == "__main__":
    N = 100  # number of iteration, the higher the N, the lower chance of failure
    graph = read("mincut_data.txt")
    nodes = len(graph)
    mincut_count = nodes*(nodes-1)/2  # initiate to max number of edges
    # save best cut
    for i in range(N):
        count, merges = mincut(create())
        if count < mincut_count:
            mincut_count = count
            mincut_merges = merges.copy()

    # post-processing mincut merge sequence to extract elements of the two sides of mincut
    A, B = find_mincut_nodes(graph, mincut_merges)

    # value test
    correct_cut = mincut_count == 17

    # length test
    equal_len = len(A)+len(B) == nodes

    # overlap test
    no_overlap = []
    for i in A:
        if i in B:
            no_overlap.append(False)
        else:
            no_overlap.append(True)
    all(no_overlap)

    print("Value test OK" if correct_cut else "Value test FAILED!")
    print("Length test OK" if equal_len else "Length test FAILED!")
    print("Overlap test OK" if all(no_overlap) else "Overlap test FAILED!")
    print(f'All tests OK\nNumber of iteration = {N}\nMinimum cut = {mincut_count}\nA = {A}\nB = {B}'\
        if correct_cut and equal_len and all(no_overlap) else "One or more tests FAILED!")
