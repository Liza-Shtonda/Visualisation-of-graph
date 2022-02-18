import networkx as nx
import matplotlib.pyplot as plt


pos = {i: (i, 3) for i in range(0, 6)}
pos.update({i: (i-6, 1) for i in (10, 11, 12)})
pos.update({i: (i-5.5, 2) for i in (6, 8)})
pos.update({i: (i-6.5, 1) for i in (7, 9)})


def read_adjlist(path):
    H = nx.read_adjlist(path, create_using=nx.Graph, nodetype=int)
    return H


def draw_graph(graph, pos):
    plt.axes().set_aspect('equal', adjustable='datalim')
    nx.draw(graph, pos=pos, with_labels=True, node_color='white', font_color='black', edgecolors='black')


def draw_diameter(graph, pos,  edges_colors, nodes_colors):
    nx.draw(graph, pos=pos, with_labels=True, font_color='black', edgecolors='black',
            node_color=nodes_colors, edge_color=edges_colors)


def automatic_graph(g,  path_to):
    nx.draw_shell(g, with_labels=True, font_color='black', edgecolors='black', node_color='white')
    save_graph(path_to)
    return g


def save_graph(path):
    plt.savefig(path, format='jpg')


def manual_graph(g, pos, path_to):
    draw_graph(g, pos)
    save_graph(path_to)
    return g


def general_information(g):
    h = 0
    components = ['First', 'Second', 'Third', 'Fourth']
    for i in nx.connected_components(g):
        print(f"{components[h]} component: ", end='\n')
        name = g.subgraph(i)
        h += 1
        print('\tnumber of nodes: ', end='')
        print(len(nx.nodes(name)))
        print('\tnumber of edges: ', end='')
        print(len(nx.edges(name)))
        print('\tdegree and eccentricity of nodes: \n', end='')
        for j in i:
            print('\t', j, ': ', name.degree(j), '; ', nx.eccentricity(name, j), sep='')
        print('\tradius: ', nx.radius(name), sep='')
        print('\tdiameter: ', nx.diameter(name), sep='', end='\n\n')


def diameter_bfs(g, color, path):
    for i in nx.connected_components(g):
        g1 = g.subgraph(i)
        diam = nx.diameter(g1)
        lst = []
        for v, w in nx.bfs_edges(g1, list(i)[0]):
            lst.append([v, w])
        lst = lst[:diam]
        v = lst[0][0]
        w = lst[0][1]
        g1[v][w]['color'] = color
        edges_colors = [color for a, b, color in g1.edges.data(data='color', default='black')]
        nodes_colors = [color for v, color in g1.nodes.data(data='color', default='white')]
        for j in (v, w):
            if j in g1.nodes:
                ind = list(g1.nodes).index(j)
                nodes_colors[ind] = color
        draw_diameter(g1, pos, edges_colors, nodes_colors)
    save_graph(path)


def forest_graph(g, color):
    g1 = g.copy()
    for v, w in nx.dfs_edges(g1):
        g1[v][w]['color'] = color
    edges_colors = [color for a, b, color in g1.edges.data(data='color', default='black')]
    draw_diameter(g1, pos, edges_colors, 'white')
    save_graph('forest.jpg')


g = read_adjlist('graph_adjlist.txt')
automatic_graph(g, 'g_automatically.jpg')
manual_graph(g, pos, 'g_manually.jpg')
general_information(g)
diameter_bfs(g, 'pink', 'diameter_bfs.jpg')
forest_graph(g, 'red')


