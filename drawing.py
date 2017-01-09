import turtle

RED = 'red'
GREEN = 'green'
BLUE = 'blue'
BLACK = 'black'
PURPLE = 'purple'
RADIUS = 3
PATH_WIDTH = 2

class DrawingTools:

    def __init__(self, map_file):
        
        f = open(map_file)

        # read map data
        line1 = f.readline().split(' ')
        world_size = (int(line1[0]), int(line1[1]))
        line2 = f.readline().split(' ')
        start_pos = (float(line2[0]), float(line2[1]))
        line3 = f.readline().split(' ')
        goal_pos = (float(line3[0]), float(line3[1]))

        # read obstacle data
        num_obstacles = int(f.readline())
        obstacles = []
        for i in range(num_obstacles):
            num_vertices = int(f.readline())
            vertices = []
            for j in range(num_vertices):
                line = f.readline().split(' ')
                vertices.append((float(line[0]), float(line[1])))
            obstacles.append(vertices)

        # set up turtle
        turtle.setup(world_size[0]+100, world_size[1]+100)
        turtle.setworldcoordinates(0, 0, world_size[0], world_size[1])
        screen = turtle.Screen()
        screen.title("Path Planning Demo")
        t = turtle.Turtle()
        t.speed(0)
        t.hideturtle()

        self.world_size = world_size
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.obstacles = obstacles
        self.turtle = t
        self.screen = screen

    def get_map_info(self):
        return self.world_size, self.start_pos, self.goal_pos, self.obstacles

    def draw_map(self):
        self.draw_boundaries(BLUE)
        self.draw_obstacles(self.obstacles, BLUE)

    def draw_boundaries(self, color):
        x, y = self.world_size[0], self.world_size[1]
        self.turtle.pencolor(color)
        self.turtle.penup()
        self.turtle.goto(0, 0)
        self.turtle.pendown()
        self.turtle.goto(x, 0)
        self.turtle.goto(x, y)
        self.turtle.goto(0, y)
        self.turtle.goto(0, 0)
        self.turtle.penup()

    def draw_obstacles(self, obstacles, color):
        for obstacle in obstacles:
            self.draw_polygon(obstacle, color)

    def draw_polygon(self, vertices, color):
        self.turtle.pencolor(color)
        self.turtle.penup()
        self.turtle.goto(vertices[-1][0], vertices[-1][1])
        self.turtle.pendown()
        for i in range(len(vertices)):
            self.turtle.goto(vertices[i][0], vertices[i][1])
        self.turtle.penup()

    def draw_point(self, point, color):
        self.turtle.penup()
        self.turtle.goto(point)
        self.turtle.dot(RADIUS, color)
        self.turtle.penup()

    def draw_nodes(self, nodes, color):
        for n in nodes:
            self.draw_point(n, color)

    def draw_edges(self, edges, color):
        self.turtle.pencolor(color)
        for edge in edges:
            self.turtle.penup()
            self.turtle.goto(edge[0])
            self.turtle.pendown()
            self.turtle.goto(edge[1])
            self.turtle.penup()

    def draw_path(self, path, color, width=None):
        self.turtle.pencolor(color)
        self.turtle.width(width)
        self.turtle.penup()
        self.turtle.goto(path[0])
        self.turtle.pendown()
        for i in range(1, len(path)):    
            self.turtle.goto(path[i])
        self.turtle.penup()

    def finished_drawing(self):
        self.screen.exitonclick()
