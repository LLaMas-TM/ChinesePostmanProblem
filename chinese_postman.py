import heapq
from collections import defaultdict, Counter
import networkx as nx
import matplotlib.pyplot as plt


class ChinesePostman:
    def __init__(self):
        """
        Initialize an empty graph using adjacency list representation.

        The graph is represented using two data structures:
        - self.graph: A defaultdict storing adjacency lists with weights
        - self.edges: A list storing all edges as tuples (u, v, weight)
        """
        self.graph = defaultdict(list)
        self.edges = []

    def add_node(self, u, v, weight):
        """
        Add an undirected edge between vertices u and v with given weight.

        Args:
            u: First vertex of the edge
            v: Second vertex of the edge
            weight: Weight/cost of the edge between u and v

        The edge is added to both the adjacency list and edges list representations.
        Since the graph is undirected, the edge is added in both directions.
        """
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))
        self.edges.append((u, v, weight))

    def dijkstra(self, start):
        """
        Implement Dijkstra's shortest path algorithm.

        Args:
            start: Starting vertex for shortest path calculation

        Returns:
            dict: Dictionary mapping each vertex to the shortest distance from start vertex

        The algorithm uses a priority queue for efficient vertex selection and
        maintains a distances dictionary to track shortest paths found so far.
        """
        distances = {node: float("inf") for node in self.graph}
        distances[start] = 0
        priority_queue = [(0, start)]
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            if current_distance > distances[current_node]:
                continue
            for neighbor, weight in self.graph[current_node]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
        return distances

    def find_shortest_path(self, start, end):
        """
        Find shortest path between start and end vertices using Dijkstra's algorithm.

        Args:
            start: Starting vertex
            end: Target vertex

        Returns:
            tuple: (distance, path) where:
                - distance (float): Length of shortest path
                - path (list): Sequence of vertices forming shortest path

        Additionally tracks predecessors to reconstruct the actual path.
        """
        distances = {node: float("inf") for node in self.graph}
        distances[start] = 0
        predecessors = {node: None for node in self.graph}
        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            if current_distance > distances[current_node]:
                continue
            if current_node == end:
                break

            for neighbor, weight in self.graph[current_node]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        # Reconstruct path
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()

        return distances[end], path

    def find_odd_degree_nodes(self):
        """
        Find vertices with odd degree in the graph.

        Returns:
            list: List of vertices that have an odd number of incident edges

        Uses a Counter to track vertex degrees and filters for odd values.
        Odd degree vertices are important for solving the Chinese Postman Problem.
        """
        degree_count = Counter()
        for u, v, _ in self.edges:
            degree_count[u] += 1
            degree_count[v] += 1
        return [node for node, degree in degree_count.items() if degree % 2 != 0]

    def solve(self):
        """
        Solve the Chinese Postman Problem to find the optimal circuit.

        The solution follows these steps:
        1. Find vertices with odd degree
        2. Find minimum weight perfect matching between odd degree vertices
        3. Add edges from matching to create augmented graph where all vertices have even degree
        4. Find Eulerian circuit in the augmented graph

        Returns:
            tuple: (total_cost, path) where:
                - total_cost is the sum of original edge weights plus any additional edges needed
                - path is list of vertices in order they should be visited
        """

        # Find vertices with odd degree
        odd_vertices = self.find_odd_degree_nodes()

        # If no odd vertices, the original graph has an Eulerian circuit
        if not odd_vertices:
            path = self.find_eulerian_path(self.graph)
            total_cost = sum(weight for _, _, weight in self.edges)
            return total_cost, path

        # Find minimum weight perfect matching for odd vertices
        min_weight_matches = self.find_min_weight_matching(odd_vertices)

        # Create augmented graph by adding edges from matching
        augmented_graph = defaultdict(list)
        for v1, v2 in self.graph.items():
            augmented_graph[v1] = v2.copy()

        additional_cost = 0
        for v1, v2, weight in min_weight_matches:
            # Get the actual path between v1 and v2
            _, path = self.find_shortest_path(v1, v2)

            # Add all edges along the path
            for i in range(len(path) - 1):
                start, end = path[i], path[i + 1]
                # Find the weight of this edge in original graph
                for neighbor, w in self.graph[start]:
                    if neighbor == end:
                        edge_weight = w
                        break
                augmented_graph[start].append((end, edge_weight))
                augmented_graph[end].append((start, edge_weight))
                additional_cost += edge_weight

        # Find Eulerian circuit in the augmented graph
        path = self.find_eulerian_path(augmented_graph)
        total_cost = sum(weight for _, _, weight in self.edges) + additional_cost

        return total_cost, path

    def find_min_weight_matching(self, odd_vertices):
        """
        Find minimum weight perfect matching for odd degree vertices.

        Args:
            odd_vertices (list): List of vertices with odd degree

        Returns:
            list: List of tuples (v1, v2, weight) representing matching edges

        Implements a greedy algorithm to find a minimum weight perfect matching
        between odd degree vertices. For each vertex, finds closest unmatched vertex.
        """
        matches = []
        vertices = odd_vertices.copy()

        while vertices:
            v1 = vertices[0]
            min_cost = float("inf")
            min_v2 = None

            for v2 in vertices[1:]:
                # Get distance and path from find_shortest_path
                distance, path = self.find_shortest_path(v1, v2)
                # Compare only the distance part
                if distance < min_cost:
                    min_cost = distance
                    min_v2 = v2

            matches.append((v1, min_v2, min_cost))
            vertices.remove(v1)
            vertices.remove(min_v2)

        return matches

    def find_eulerian_path(self, graph=None, start_vertex=None):
        """
        Find Eulerian path in the graph using Hierholzer's algorithm.

        Args:
            graph (dict, optional): Graph to find path in. Defaults to self.graph
            start_vertex (Any, optional): Starting vertex. Defaults to first vertex

        Returns:
            list: Sequence of vertices forming an Eulerian path

        Implements Hierholzer's algorithm to find an Eulerian path/circuit.
        Works by following unused edges and backing up when stuck.
        """
        if graph is None:
            graph = self.graph

        if not start_vertex:
            start_vertex = list(graph.keys())[0]

        # Create copy of graph for modification
        curr_graph = {}
        for v in graph:
            curr_graph[v] = graph[v].copy()

        path = []
        stack = [start_vertex]

        while stack:
            curr_v = stack[-1]

            if curr_graph[curr_v]:
                # Take an edge
                next_v = curr_graph[curr_v][0][0]
                weight = curr_graph[curr_v][0][1]
                curr_graph[curr_v].remove((next_v, weight))
                curr_graph[next_v].remove((curr_v, weight))
                stack.append(next_v)
            else:
                # No more edges - add to path
                path.append(stack.pop())

        return path[::-1]

    def plot_route(self):
        """
        Visualize the graph using networkx and matplotlib.

        Creates a visual representation of the graph where:
        - Vertices are shown as labeled circles
        - Edges are shown with their weights
        - Uses a spring layout for vertex positioning
        """
        G = nx.Graph()
        for u, v, weight in self.edges:
            G.add_edge(u, v, weight=weight)
        pos = nx.spring_layout(G)
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="lightblue",
            node_size=500,
            font_size=10,
            font_weight="bold",
        )
        edge_labels = {(u, v): f"{weight}" for u, v, weight in self.edges}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.show()
