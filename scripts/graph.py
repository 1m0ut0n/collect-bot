"""Graph class for handling data in graph form."""

class Graph():
    def __init__(self, nodes, init_graph={}):
        """
        Initializes the graph with the given nodes and an optional initial graph.
        Args:
            nodes (list): A list of nodes to be included in the graph.
            init_graph (dict, optional): An optional dictionary representing the initial graph structure. Defaults to an empty dictionary.
        The graph is represented as a dictionary of dictionaries, where the keys are node identifiers 
        and the values are dictionaries of adjacent nodes and their corresponding edge values.
        Example:
            nodes = ['A', 'B', 'C']
            init_graph = {
                'A': {'B': 1},
                'B': {'A': 1, 'C': 2},
                'C': {'B': 2}
            }
            graph = Graph(nodes, init_graph)
        """
        
        # Put the nodes as index in a dictionary
        graph = {}
        for node in nodes:
            graph[node] = {}
        
        # If there is an initial graph, update the graph with it
        graph.update(init_graph)
        
        # Add the edges in both directions
        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value

    def addEdge(self, node1, node2, value):
        """
        Adds an edge between two nodes in the graph with a specified value.

        Parameters:
        node1 (hashable): The first node of the edge.
        node2 (hashable): The second node of the edge.
        value (any): The value or weight of the edge.

        Returns:
        None
        """
        self.graph[node1][node2] = value
        self.graph[node2][node1] = value
    
    def getNode(self, node):
        """
        Returns the neighbors of a node in the graph.

        Parameters:
        node (hashable): The node to get the neighbors of.

        Returns:
        dict: A dictionary of the neighbors of the node and their corresponding edge values.
        """
        return self.graph[node]
    
    def value(self, node1, node2):
        """
        Returns the value of an edge between two nodes in the graph.

        Parameters:
        node1 (hashable): The first node of the edge.
        node2 (hashable): The second node of the edge.

        Returns:
        any: The value of the edge between the two nodes.
        """
        return self.graph[node1][node2]