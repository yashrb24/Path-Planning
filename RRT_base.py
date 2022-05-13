from base import Graph, Node
from random import randint
import matplotlib.patches as ptch


def RRT(graph: Graph, start: Node, end: Node):
    graph.start = start
    graph.end = end

    graph.generate_obstacles()

    end_patch = ptch.Circle((graph.end.x, graph.end.y), 5)

    delta = 0.05 * min(graph.width, graph.height)
    limit = 1300

    graph.add_node(start)
    reversed_tree = {}
    for i in range(limit):
        random_node = Node(randint(0, graph.width), randint(0, graph.height))
        while graph.node_isObstacle(random_node):
            random_node = Node(randint(0, graph.width), randint(0, graph.height))

        nearest = graph.get_nearest_node(random_node)
        d = random_node.manhattan_dist(nearest)

        if d < delta:
            random_node.parent = nearest
            graph.add_node(random_node)
            reversed_tree[random_node] = nearest

            if end_patch.contains_point((nearest.x, nearest.y)):
                graph.end = nearest
                print("End node found!")
                break
        else:
            new_x = int(nearest.x + (random_node.x - nearest.x) * delta / d)
            new_y = int(nearest.y + (random_node.y - nearest.y) * delta / d)
            new_node = Node(new_x, new_y)

            if graph.node_isObstacle(new_node):
                continue
            else:
                new_node.parent = nearest
                graph.add_node(new_node)
                reversed_tree[new_node] = nearest

                if end_patch.contains_point((new_node.x, new_node.y)):
                    graph.end = new_node
                    print("End node found")
                    break

    else:
        print("end node not found")
        graph.draw_graph(reversed_tree)
        return

    graph.visualiser(reversed_tree)
