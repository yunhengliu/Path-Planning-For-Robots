import sys, random, math
from drawing import *
from common import *
from graph_search import *

MAX_SAMPLE = 50
CONNECT_STEP = 30

class RRT:

    def __init__(self, world_size, start, goal, obstacles, num_iter, step_size, bias_step, eps):
        
        # correct minumum distance
        if eps < step_size:
            eps = step_size

        # adjust bias to avoid division by 0
        if bias_step == 0:
            bias_step = num_iter

        self.world_size = world_size
        self.start = start
        self.goal = goal
        self.obstacles = obstacles
        self.obs_edges = get_obstacle_edges(obstacles)
        self.num_iter = num_iter
        self.step_size = step_size
        self.bias_step = bias_step
        self.eps = eps

    def get_sample(self):
        return (random.random()*self.world_size[0], random.random()*self.world_size[1])

    def get_nearest_neighbor(self, tree, rn):
        nn = tree[0]
        smallest_dist = get_distance(nn, rn)
        for n in tree:
            dist = get_distance(n, rn)
            if dist < smallest_dist:
                nn = n
                smallest_dist = dist
        return nn

    def intersect_obstacle_edge(self, edge):
        for obs_edge in self.obs_edges:
            if intersect(edge, obs_edge):
                return True
        return False

    def inside_obstacles(self, pt):
        for polygon in self.obstacles:
            if inside_polygon(pt, polygon):
                return True
        return False

    def check_new_node(self, tree, new_node, new_edge):
        x, y = new_node[0], new_node[1]
        if x < 0 or y < 0 or x > self.world_size[0] or y > self.world_size[1]:
            return False
        for n in tree:
            if get_distance(new_node, n) < self.eps:
                return False
        return (not self.intersect_obstacle_edge(new_edge)) and (not self.inside_obstacles(new_node))

    def get_new_node(self, tree, goal, bias=False):
        rn = goal if bias else self.get_sample()
        nn = self.get_nearest_neighbor(tree, rn)
        theta = math.atan2(rn[1]-nn[1], rn[0]-nn[0])
        new_node = (nn[0] + self.step_size*math.cos(theta), nn[1] + self.step_size*math.sin(theta))
        new_edge = (nn, new_node)
        return new_node, new_edge
   
    def extend_tree(self, tree, goal, bias=False):
        new_node, new_edge = self.get_new_node(tree, goal, bias)
        if not self.check_new_node(tree, new_node, new_edge):
            for i in range(MAX_SAMPLE):
                new_node, new_edge = self.get_new_node(tree, goal)
                if self.check_new_node(tree, new_node, new_edge):
                    return new_node, new_edge
        else:
            return new_node, new_edge
        return None, None

    def get_min_distance(self, tree1, tree2):
        min_dist = get_distance(tree1[0], tree2[0])
        new_edge = None
        for n1 in tree1:
            for n2 in tree2:
                if not self.intersect_obstacle_edge((n1, n2)) and get_distance(n1, n2) < min_dist:
                    new_edge = (n1, n2)
                    min_dist = get_distance(n1, n2)
        return min_dist, new_edge

    def generate_trees(self):

        edges = []
        tree1 = [self.start]
        tree2 = [self.goal]
        new_node1 = self.start
        new_node2 = self.goal
        
        for i in range(self.num_iter):
            print 'Iteration: ' + str(i)
            
            stuck1, stuck2 = False, False
            bias = (i != 0) and (i % self.bias_step == 0)
            
            # grow tree 1
            new_node1, new_edge1 = self.extend_tree(tree1, new_node2, bias)
            
            if new_node1 == None and new_edge1 == None:
                # reset bias
                new_node1 = self.start
                stuck1 = True
            else:
                print "Tree 1 new node:", new_node1
                tree1.append(new_node1)
                edges.append(new_edge1)
            
            # grow tree 2
            new_node2, new_edge2 = self.extend_tree(tree2, new_node1, bias)
            
            if new_node2 == None and new_edge2 == None:
                # reset bias
                new_node2 = self.goal
                stuck2 = True
            else:
                print "Tree 2 new node:", new_node2
                tree2.append(new_node2)
                edges.append(new_edge2)
            
            # cannot grow either tree
            if stuck1 and stuck2:
                print "Stuck..."
                break

            # connect two trees
            if (i != 0) and (i % CONNECT_STEP == 0):
                dist, new_edge = self.get_min_distance(tree1, tree2)
                if new_edge != None and dist < self.step_size:
                    edges.append(new_edge)
                    print "trees connnected..."
                    break

        return tree1, tree2, edges


def main():

    if len(sys.argv) != 6:
        print "Usage: python rrt.py map_file num_iter step_size bias_step eps"
        exit(0)

    map_file = sys.argv[1]
    num_iter = int(sys.argv[2])
    step_size = int(sys.argv[3])
    bias_step = int(sys.argv[4])
    eps = int(sys.argv[5])

    dts = DrawingTools(map_file)
    world_size, start, goal, obstacles = dts.get_map_info()
    rrt_planner = RRT(world_size, start, goal, obstacles, num_iter, step_size, bias_step, eps)
    tree1, tree2, edges = rrt_planner.generate_trees()
    g = Graph(edges)
    path, cost = g.dijkstra(start, goal)
    print 'Cost: ' + str(cost)

    dts.draw_map()
    dts.draw_nodes(tree1, DOT_COLOR1)
    dts.draw_nodes(tree2, DOT_COLOR2)
    dts.draw_path(path, PATH_COLOR)
    dts.finished_drawing()

if __name__ == "__main__": 
    main()