import sys, math
from common import *
from drawing import *
from graph_search import *

EPS = 0.05

class VisibilityGraph:

    def __init__(self, world_size, start, goal, obstacles, robot_size, ref_idx):
        self.world_size = world_size
        self.start = start
        self.goal = goal
        self.obstacles = obstacles
        self.robot_size = robot_size
        self.ref_idx = ref_idx
        self.init_config = self.get_robot_config(self.start)
        self.end_config = self.get_robot_config(self.goal)
        ref_offsets = self.get_ref_offsets()
        self.grown_obstacles = self.grow_obstacles(ref_offsets)
        self.obstacle_edges = get_obstacle_edges(self.grown_obstacles)

    def get_robot_config(self, center_point):
        w, h = self.robot_size[0], self.robot_size[1]
        cx, cy = center_point[0], center_point[1]
        t = math.radians(get_orientation(self.start, self.goal))
        vs = [(cx-h/2, cy-w/2), (cx-h/2, cy+w/2), (cx+h/2, cy+w/2), (cx+h/2, cy-w/2)]
        # map to origin
        tmp = map(lambda v: (v[0] - cx, v[1] - cy), vs)
        # rotate
        rot = map(lambda v: (v[0]*math.cos(t)-v[1]*math.sin(t), v[0]*math.sin(t)+v[1]*math.cos(t)), tmp)
        # map back
        vertices = map(lambda v: (v[0] + cx, v[1] + cy), rot)
        return vertices

    def get_ref_offsets(self):
        ref_pt = self.init_config[self.ref_idx]
        offsets = []
        for i in range(len(self.init_config)):
            if i != self.ref_idx:
                cur_pt = self.init_config[i]
                # reflect about x-axis
                new_pt_x = cur_pt[0] + (ref_pt[0] - cur_pt[0]) * 2
                # reflect about y-axis
                new_pt_y = cur_pt[1] + (ref_pt[1] - cur_pt[1]) * 2
                # calculate offset
                offsets.append((new_pt_x - ref_pt[0], new_pt_y - ref_pt[1]))
        return offsets

    def grow_obstacles(self, ref_offsets):
        new_obstacles = []
        for obstacle in self.obstacles:
            new_vertices = []
            for v in obstacle:
                for offset in ref_offsets:
                    new_vertices.append((v[0]+offset[0], v[1]+offset[1]))
                new_vertices.append((v[0], v[1]))
            new_obstacles.append(new_vertices)
        
        # find convex hull of each set of vertices
        chs = []
        for points in new_obstacles:
            points = sorted(points)
            # build lower hull 
            lower = []
            for p in points:
                while len(lower) >= 2 and not ccw(lower[-2], lower[-1], p):
                    lower.pop()
                lower.append(p)
            # build upper hull
            upper = []
            for p in reversed(points):
                while len(upper) >= 2 and not ccw(upper[-2], upper[-1], p):
                    upper.pop()
                upper.append(p)
            temp_ch = lower[:-1] + upper[:-1]
            # clean convex hull to find charateristic points
            for p in temp_ch:
                for q in temp_ch:
                    for r in temp_ch:
                        if p == q or p == r or q == r:
                            pass
                        else:
                            if abs(get_distance(p, r) - (get_distance(p, q) + get_distance(q, r))) < EPS:
                                if q in temp_ch:
                                    temp_ch.remove(q)
            chs.append(temp_ch)
        return chs

    def get_all_edges(self):
        all_edges = []
        for ch1 in self.grown_obstacles:
            for pt in ch1:
                all_edges.append((self.init_config[self.ref_idx], pt))
                all_edges.append((pt, self.end_config[self.ref_idx]))
            for ch2 in self.grown_obstacles:
                if ch1 != ch2:
                    for p1 in ch1:
                        for p2 in ch2:
                            all_edges.append((p1, p2))
        return all_edges

    def get_visible_edges(self):
        visible_edges = []
        for edge in self.get_all_edges():
            to_add = True
            for obstacle_edge in self.obstacle_edges:
                if intersect(edge, obstacle_edge):
                    to_add = False
                    break
            if to_add:
                visible_edges.append(edge)
        return visible_edges

def main():

    if len(sys.argv) != 5:
        print "Usage: python vgraph.py map_file robot_width robot_length ref_idx"
        exit(0)

    map_file = sys.argv[1]
    robot_size = (float(sys.argv[2]), float(sys.argv[3]))
    ref_idx = int(sys.argv[4])

    dts = DrawingTools(map_file)
    world_size, start, goal, obstacles = dts.get_map_info()
    vgraph = VisibilityGraph(world_size, start, goal, obstacles, robot_size, ref_idx)
    start_pt, goal_pt = vgraph.init_config[ref_idx], vgraph.end_config[ref_idx]
    visible_edges = vgraph.get_visible_edges()
    g = Graph(visible_edges+vgraph.obstacle_edges)
    path, cost = g.dijkstra(start_pt, goal_pt)
    print 'Cost: ' + str(cost)

    dts.draw_map()
    dts.draw_obstacles(vgraph.grown_obstacles, RED)
    dts.draw_point(start_pt, RED)
    dts.draw_point(goal_pt, BLACK)
    dts.draw_edges(visible_edges, PURPLE)
    dts.draw_path(path, GREEN, PATH_WIDTH)
    dts.finished_drawing()

if __name__ == "__main__": 
    main()