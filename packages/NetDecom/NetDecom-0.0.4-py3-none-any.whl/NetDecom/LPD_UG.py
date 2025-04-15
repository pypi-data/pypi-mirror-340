#An undirected graph and a MCS sequence are passed into the networkX library to obtain local decomposition
import networkx as nx
from Convex_hull_UG import * 

class LPD_UG:

    def __init__(self, input_tuple):

        self.graph = input_tuple[0]
        self.mcs = input_tuple[1]

    def Local_decom_CMSA(self):
        block = []
        G_c = self.graph.copy()
        hull = Convex_hull_UG(G_c)
        V = set(G_c)
        for i in self.mcs:
            if i in G_c:       
                N_v = (set(G_c[i])|{i})          
                for k in block:
                    if N_v.issubset(k):
                        H = N_v
                        break
                else:
                    if len(N_v)*(len(N_v)-1)/2 == len(nx.subgraph(G_c, N_v).edges):
                        H = N_v
                    else:
                        H =  hull.CMSA(N_v)#CMSA((N_v, G_c))
                    block.append(H)                
                V -= H
                N_V = set(nx.node_boundary(G_c, nbunch1=V, nbunch2=H))         
                V |= N_V                          
                G_c = nx.subgraph(G_c, V)
        return block
    
    def Local_decom_IPA(self):
        block = []
        G_c = self.graph.copy()
        hull = Convex_hull_UG(G_c)
        V = set(G_c)
        for i in self.mcs:
            if i in G_c:       
                N_v = (set(G_c[i])|{i})          
                for k in block:
                    if N_v.issubset(k):
                        H = N_v
                        break
                else:
                    if len(N_v)*(len(N_v)-1)/2 == len(nx.subgraph(G_c, N_v).edges):
                        H = N_v
                    else:
                        H =  hull.IPA(N_v)
                    block.append(H)                
                V -= H
                N_V = set(nx.node_boundary(G_c, nbunch1=V, nbunch2=H))         
                V |= N_V                          
                G_c = nx.subgraph(G_c, V)
        return block
    
#LPD_UG((G, mcs_sequence)).Local_decom_CMSA()
#LPD_UG((G, mcs_sequence)).Local_decom_IPA()