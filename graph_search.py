from common import get_distance

class Graph:

    def __init__(self, edges):
        self.edges = edges

    def get_adjacecy_list(self):
        adjacency_list = {}
        for edge in self.edges:
            n1 = edge[0]
            n2 = edge[1]
            if n1 not in adjacency_list:
                adjacency_list[n1] = set([n2])
            else:
                adjacency_list[n1].add(n2)
            if n2 not in adjacency_list:
                adjacency_list[n2] = set([n1])
            else:
                adjacency_list[n2].add(n1)
        return adjacency_list

    def dijkstra(self, start, goal):
        adjacency_list = self.get_adjacecy_list()
        if start not in adjacency_list:
            print 'Start node not in adjacency list...'
            return
        if goal not in adjacency_list:
            print 'Goal node not in adjacency list...'
            return
        visited = []
        distances = {}
        predecessors = {} 
        min_node = start

        while True:
            if not visited:
                distances[min_node] = 0
            for neighbor in adjacency_list[min_node]:
                if neighbor not in visited:
                        temp = distances[min_node] + get_distance(min_node, neighbor)
                        if temp < distances.get(neighbor, float('inf')):
                            distances[neighbor] = temp
                            predecessors[neighbor] = min_node
            visited.append(min_node)
            unvisited={}
            for n in adjacency_list:
                if n not in visited:
                    unvisited[n] = distances.get(n, float('inf'))
            if min_node == goal:
                path = []
                pred = goal
                while pred != None:
                    path.insert(0, pred)
                    pred = predecessors.get(pred, None)
                return path, distances[goal]
            min_node = min(unvisited, key=unvisited.get)


