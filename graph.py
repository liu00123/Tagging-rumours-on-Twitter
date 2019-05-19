# Graph
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import os,sys

path = os.path.dirname(os.path.realpath(__file__))
# Making graph
def computeDistances(G = None,max_num=6):
    node_path_dict = nx.all_pairs_shortest_path(G)
    node_path_dict = dict(node_path_dict)
    nodes_num = G.number_of_nodes()
    nodes_list = G.nodes()
    distances_dict = {}
    for node in nodes_list:
        sum_d = 0
        for node2 in nodes_list:
            if node == node2:
                continue
            node_path = node_path_dict.get(node2, {})
            temp_v = node_path.get(node,[])
            if len(temp_v)>=max_num:
                temp_v = []
            temp_len = 1 if len(temp_v) else nodes_num-len(temp_v)-1
            sum_d += temp_len
            #print node,"=",node2,"=",node_path,"=",temp_v,"=",temp_len,"=",sum_d
            distances_dict[node] = float(nodes_num-1)/sum_d
    return distances_dict


def generateNet(filename=""):
    follow_list ,unfollow_list = readMatrixFromFile(filename=filename)

    DG = nx.DiGraph()
    # Nodes
    # List
    DG.add_nodes_from(unfollow_list)
    # UserA to B
    DG.add_weighted_edges_from(follow_list)
    return DG

def readMatrixFromFile(filename):
    # Open the graph
    with open(filename, 'r') as f:

        follow_list = []
        unfollow_list = []
        for line in f:
            # Whether following
            is_follow = line.strip().split(',')[2]
            # Following judgement
            if is_follow == '1':
                follow_list.append(line.strip().split(','))
            else:
                unfollow_list.append(line.strip().split(',')[0])
    return follow_list,unfollow_list

def draw_picture(filename):
    # Open graph
    with open(filename, 'r') as f:

        follow_list = []
        unfollow_list = []
        for line in f:

            is_follow = line.strip().split(',')[2]

            if is_follow == '1':
                follow_list.append(line.strip().split(','))
            else:
                unfollow_list.append(line.strip().split(',')[0])
    # networkx Function
    DG = nx.DiGraph()
    # Nodes
    # List
    DG.add_nodes_from(unfollow_list)

    DG.add_weighted_edges_from(follow_list)
    # Draw
    nx.draw(DG, with_labels=True)
    # Picture
    plt.show()

def computeNodesFeather(filename,max_num=9):
    G = generateNet(filename=filename)
    dict_nodes = computeDistances(G=G,max_num=max_num)
    return pd.DataFrame(dict_nodes,index=[0])

def draw_picture(filename):
    DG = generateNet(filename=filename)
    nx.draw(DG, with_labels=True)
    # Show the picture
    plt.savefig(path+"/output/relation.png")
    plt.show()


if __name__ == "__main__":
    file_path = path + "/output/"
    file_name = "following.csv"
    feather = computeNodesFeather(filename=file_path+file_name,max_num=9)
    feather.to_excel(file_path+"feather.xlsx",index=False)
    draw_picture(file_path+file_name)





