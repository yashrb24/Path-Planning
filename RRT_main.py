from base import Graph, Node
from RRT_base import RRT


def main():
    g = Graph(400, 200)  # customizable dimensions of the graph
    start = Node(15, 30)
    end = Node(380, 90)
    RRT(g, start, end)  # choose your own start and end node


if __name__ == "__main__":
    # if main func is still running after 20s, rerun it
    main()
