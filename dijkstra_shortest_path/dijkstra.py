from ast import literal_eval


class Dijkstra:
    """
    Dijkstra's shortest path algorithm implementation

    Attributes
    ----------
        graph : dictionary
            edges of connected graph, every node is a key, it's value is a list of tuples of all its
            connected nodes and their distances {node: [(node1, distance1), (node2, distance2), ...]}
        shortest_paths : dictionary
            every node is a key, its value is a tuple of its shortest distance and path from source
            {destination node: (shortest path, [node1, node2,...]), ...}

    Methods
    -------
        find_shortest_paths(self, source)
            find the shortest distance and path from source to all other connected nodes
    """

    def __init__(self, adj_file):
        """
        reads text file represents adjacency list of undirected connected graph, where colunms are
        separated by taps, first colunm is a particular node and each other colunm in the same row
        represents a connected node and its distance separated by a comma

        Attributes
        ----------
        _graph : dictionary
            edges of connected graph, every node is a key, it's value is a list of tuples of all its
            connected nodes and their distances {node: [(node1, distance1), (node2, distance2), ...]}
        """

        self._graph = {}
        with open(adj_file) as file:
            for line in file:
                self._graph[int(line.split()[0])] = [literal_eval(edge) for edge in line.split()[1:]]

    @property
    def graph(self):
        """Get graph"""
        return self._graph

    def find_shortest_paths(self, source):
        """
        finds the shortest path from a given source node to all other connected nodes

        Parameters
        ----------
        source : int
            source from which all shortest distance and paths will be found to all connected nodes

        Return
        ------
        shortest_paths : dictionary
            every node is a key, its value is a tuple of its shortest distance and path from source
            {destination node: (shortest path, [node1, node2,...]), ...}
        """

        shortest_paths = {}
        visited = set()  # track visited nodes
        for node in self._graph.keys():
            shortest_paths[node] = (float("inf"), [])  # set all paths to infinity
        shortest_paths[source] = (0, [])  # correct the distance and path to source itself
        visited.add(source)
        while self._graph.keys() - visited:  # still not yet visited nodes
            frontier = None  # tail of edge with overall shortest distance from source
            min_edge = ()  # (head of edge with overall shortest distance from source, distance)
            for node in visited:  # for every visited nodes, check all edges crossing to unvisited
                for edge in self._graph[node]:
                    if edge[0] in visited:  # ingore edges to another visited node
                        continue
                    # find the edge with overall shortest distance from source
                    if not min_edge or shortest_paths[node][0] + edge[1] < min_edge[1]:
                        # update min_edge (head of edge, distance from source)
                        min_edge = (edge[0], shortest_paths[node][0] + edge[1])
                        frontier = node  # tail of edge
            # update shortest_paths, key=destination node, value=(shortest path, [path])
            shortest_paths[min_edge[0]] = (min_edge[1], shortest_paths[frontier][1] + [min_edge[0]])
            visited.add(min_edge[0])  # add new destination node to visited
        return shortest_paths


# driver test code
if __name__ == '__main__':
    print("Testing...")
    dijkstra = Dijkstra('dijkstra_data.txt')
    shortest_paths = dijkstra.find_shortest_paths(1)
    nodes = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]
    expected_lenghts = [2599, 2610, 2947, 2052, 2367, 2399, 2029, 2442, 2505, 3068]
    dijkstra_lengths = [shortest_paths[i][0] for i in nodes]
    print("Test OK" if dijkstra_lengths == expected_lenghts else "Test FAILED!")
