from collections import defaultdict

class Graph():
    def __init__(self) -> None:
        '''
        Create dictionairy that represents graph values
        '''
        self.graph = defaultdict(list)
    
    def addValues(self,u,v):
        '''
        add values by the path to the dictionary
        e.g 2->3 will be inputted into the dict as {2:3}
        '''
        self.graph[u].append(v)

    def DFSutil(self,v, visited):
        '''
        Add the current node to visited set
        Print it out
        find all the neighbours to that node which it points to by using the current node v as the new u
        and search by that
        then if the neighbour is not in visited set
        visit it with the new visited set
        continue until all nodes are in visited
        uses recursion
        '''
        visited.append(v)
        print(v, end=' ')

        for neighbours in self.graph[v]:
            if neighbours not in visited:
                self.DFSutil(neighbours, visited)

    def DFS(self,v):
        '''
        Create's visited set and goes straigh into DFSutil
        '''
        visited = []
        self.DFSutil(v,visited)

'''
Adds nodes and paths to graph
'''
graph = Graph()
graph.addValues(0,1)
graph.addValues(0,2)
graph.addValues(1,2)
graph.addValues(2,0)
graph.addValues(2,3)
graph.addValues(3,3)


'''
Start transversing from x node
'''
graph.DFS(1)

