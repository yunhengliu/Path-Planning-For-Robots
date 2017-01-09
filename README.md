# Path Planning Algorithms

1. [Bidirectional rapidly exploring random trees](https://en.wikipedia.org/wiki/Rapidly-exploring_random_tree)

Usage: python rrt.py map_file num_iter step_size bias_step eps
-map_file: format given below
-step_size: Euclidean distance between nodes
-bias_step: bias towards the other tree
-eps: minimum seperation between tree nodes

Example: python rrt.py maps/map1.txt 5000 3 2 2
![alt tag](/img/rrt.png)

2. [Visibility graph](https://en.wikipedia.org/wiki/Visibility_graph)

Usage: python vgraph.py map_file robot_width robot_length ref_idx
-map_file: format given below
-robot_width: width of robot
-robot_length: length of robot
-ref_idx: specifies a point in robot configuration as reference for obstacle growing 
(0=bottom left, 1=bottom right, 2=top right, 3=top left)

Example: python vgraph.py maps/map3.txt 10 15 0
![alt tag](/img/rrt.png)