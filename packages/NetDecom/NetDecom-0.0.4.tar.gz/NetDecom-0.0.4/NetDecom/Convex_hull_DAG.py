#This is a convex hull algorithm that absorbs minimal separations, inputs the directed graph and sets of concerns, and obtains the convex hull.
import networkx as nx

class Convex_hull_DAG:
    def __init__(self, graph):
        self.graph = graph

    def An(self,g, source): #获得祖先集
        G_pred = g.pred
        seen = set()
        nextlevel = source
        while nextlevel:
            thislevel = nextlevel
            nextlevel = set()
            for v in thislevel:
                if v not in seen:
                    seen.add(v)
                    nextlevel.update(G_pred[v])
        return seen

    def Pass(self,e,u,f,v,Re,An_Re): #bayes-ball 检查是否可传递
        if u not in An_Re: #指向该节点的边为0，指出为1
            if e == 0 and f == 1:
                return False
            else:
                return True
        elif u in Re:
            if e == 0 and f == 1:
                return True
            else:
                return False
        else:
            return True
    
    def Rech(self,g, source, Re):    
        An_Re = self.An(g, Re) 
        Q = []
        P = set()
        for ch in set(g.successors(source)):
            Q.append((0,ch))
            P.add((0,ch))
        for pa in set(g.predecessors(source)):
            Q.append((1,pa))
            P.add((1,pa))
        while Q:
            eV = Q.pop(0)
            for ch in set(g.successors(eV[1])):
                if (0,ch) not in P and self.Pass(eV[0],eV[1],0,ch,Re,An_Re):
                    Q.append((0,ch))
                    P.add((0,ch))
            for pa in set(g.predecessors(eV[1])):
                if (1,pa) not in P and self.Pass(eV[0],eV[1],1,pa,Re,An_Re):
                    Q.append((1,pa))
                    P.add((1,pa))
        reachable = {item[1] for item in P}
        return reachable

    def FCMS(self,g,u,v):
        An = nx.subgraph(g, nx.ancestors(g, u) | nx.ancestors(g, v)|{u,v})
        mb_u = set([parent for child in An.successors(u) for parent in An.predecessors(child)]) | set(An.successors(u)) | set(An.predecessors(u))
        mb_u.discard(u)
        reach_v = self.Rech(g, v, mb_u)
        return mb_u & reach_v

    def CMDSA(self,r):
        #d_connected_components 可用这个简化搜索node_boundary(G, nbunch1, nbunch2=None)
        g = self.graph
        ang = nx.subgraph(g, self.An(g, r))
        h = r
        s = 1
        mark = set()
        while s:
            s = 0
            Q = set()
            m = set(g.nodes)-h
            mb = nx.node_boundary(g, m, h)
            h_ch_in_m = nx.node_boundary(g, h, m)
            for v in mb:
                pa = set(g.predecessors(v))
                Q |= (pa & h)
            for v in h_ch_in_m:
                Q |= (h & set(g.predecessors(v)))
            Q |= mb
            if len(Q)>1:
                for a in Q.copy():
                    Q.remove(a)
                    for b in Q:                    
                        if (a,b) not in mark and g.has_edge(a, b)==False: 
                            mark.add((a,b))
                            mark.add((b,a))
                            if g.has_edge(b,a)==False: 
                                S_a = self.FCMS(ang,a,b)                           
                                if not S_a:
                                    continue
                                S_b = self.FCMS(ang,b,a)
                                if ( S_a | S_b) - (( S_a | S_b) & h):
                                    s = 1
                                    h |= ( S_a | S_b)  
                                break               
                else:
                    continue
                break
        return h
    
#from Convex_hull_DAG import *
#hull = Convex_hull_DAG(G)
#hull.CMDSA(R)