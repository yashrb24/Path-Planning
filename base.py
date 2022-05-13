import random
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
from matplotlib.collections import LineCollection


class Node:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Node({self.x}, {self.y})"

    def manhattan_dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


class Graph:

    param = 0.15

    def __init__(self, width: int, height: int):

        self.width = width
        self.height = height
        self.dimensions = (width, height)
        self.node_dict = {}
        self.node_set = set()

        self.obstacle_count = 20
        t = min(self.width, self.height)
        self.obs_width, self.obs_height = t * Graph.param, t * Graph.param
        self.obstacle_patches = set()

        self.start = Node(0, 0)
        self.end = Node(self.width - 1, self.height - 1)

    def add_node(self, node: Node):
        self.node_dict[(node.x, node.y)] = node
        self.node_set.add(node)

    def get_nearest_node(self, node: Node):
        min_dist = 1e6
        nearest = None
        for n in self.node_set:
            dist = node.manhattan_dist(n)
            if dist < min_dist:
                nearest = n
                min_dist = dist
        return nearest

    def generate_obstacles(self):
        obs = set()
        for _ in range(self.obstacle_count):
            lower_x = random.randint(0, int(self.width - self.obs_width))
            lower_y = random.randint(0, int(self.height - self.obs_height))
            condition_1 = lower_x <= self.start.x <= lower_x + self.obs_width and lower_y <= self.start.y <= lower_y + self.obs_height
            condition_2 = lower_x <= self.end.x <= lower_x + self.obs_width and lower_y <= self.end.y <= lower_y + self.obs_height
            while condition_1 or condition_2:
                lower_x, lower_y = random.randint(0, self.width - self.obs_width), random.randint(0, self.height - self.obs_height)
            obs.add((lower_x, lower_y))
            self.obstacle_patches.add(plt.Rectangle((lower_x, lower_y), self.obs_width, self.obs_height, color="grey"))
        return obs

    def node_isObstacle(self, node: Node):
        patch: ptch.Patch
        if len(self.obstacle_patches) == 0:
            return False
        for patch in self.obstacle_patches:
            if patch.contains_point((node.x, node.y)):
                return True
        return False

    def draw_graph(self, tree_dict: dict):
        X = []
        Y = []
        segments = []
        for k, v in tree_dict.items():
            node = k
            X.append(node.x)
            Y.append(node.y)
            segments.append([(k.x, k.y), (v.x, v.y)])
        ax = plt.gca()
        for patch in self.obstacle_patches:
            ax.add_patch(patch)
        plt.scatter(X, Y, s=10, c="red")
        line_segments = LineCollection(segments, linewidths=0.5)
        ax.add_collection(line_segments)

        ax.add_patch(ptch.Circle((self.start.x, self.start.y), 5))
        ax.add_patch(ptch.Circle((self.end.x, self.end.y), 5))
        plt.annotate("start", (self.start.x, self.start.y), fontsize=15)
        plt.annotate("end", (self.end.x, self.end.y), fontsize=15)

        plt.show()

    def visualiser(self, tree_dict: dict):
        ax = plt.gca()

        for patch in self.obstacle_patches:
            ax.add_patch(patch)
        X = []
        Y = []
        segments = []
        for k, v in tree_dict.items():
            node = k
            X.append(node.x)
            Y.append(node.y)
            segments.append([(k.x, k.y), (v.x, v.y)])
        plt.scatter(X, Y, s=10, c="red")
        line_segments = LineCollection(segments, linewidths=0.5)
        ax.add_collection(line_segments)

        path_segments = LineCollection(self.get_path(tree_dict, self.end), linewidths=1.5, edgecolors="black")
        ax.add_collection(path_segments)

        ax.add_patch(ptch.Circle((self.start.x, self.start.y), 5))
        ax.add_patch(ptch.Circle((self.end.x, self.end.y), 5))
        plt.annotate("start", (self.start.x, self.start.y), fontsize=15)
        plt.annotate("end", (self.end.x, self.end.y), fontsize=15)

        plt.title("RRT Visualisation")
        plt.show()

    def get_path(self, reversed_tree, stop_node):
        path = [stop_node]
        curr = stop_node
        while curr != self.start:
            path.append(reversed_tree[curr])
            curr = reversed_tree[curr]

        path_segments = []
        path.reverse()
        for i in range(len(path) - 1):
            path_segments.append([(path[i].x, path[i].y), (path[i+1].x, path[i+1].y)])
        return path_segments
