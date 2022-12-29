from ctypes import sizeof
import fileinput
import collections

class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def startHeap(self, n):
        heap = []
        return heap

    def insert(self, heap, item):
        heap.append(item)
        self.heapifyDown(heap, 0, len(heap)-1)

    def delete(self, index):
        popped_item = heap.pop()
        deleted_item = heap[index]
        heap[index] = popped_item
        self.heapifyUp(heap, index)
        return deleted_item

    def delete_item(self, item):
        index = heap.index(item)
        self.delete(index)

    def findMin(self):
        return heap[0]

    def extractMin(self, heap):
        last_del = heap.pop()
        if heap:
            item = heap[0]
            heap[0] = last_del
            self.heapifyUp(heap, 0)
            return item
        return last_del

    def changeKey(self, item, new_item):
        index = heap.index(item)
        old_item = heap[index]
        heap[index] = new_item
        self.heapify(heap)
        return old_item

    def heapify(self, x):
        n = len(x)
        for i in reversed(range(n//2)):
            self.heapifyUp(x, i)

    def heapifyDown(self, heap, startpos, pos):
        newitem = heap[pos]
        while pos > startpos:
            parentpos = (pos - 1) >> 1
            parent = heap[parentpos]
            if newitem < parent:
                heap[pos] = parent
                pos = parentpos
                continue
            break
        heap[pos] = newitem

    def heapifyUp(self, heap, pos):
        endpos = len(heap)
        startpos = pos
        newitem = heap[pos]
        childpos = 2*pos + 1
        while childpos < endpos:
            rightpos = childpos + 1
            if rightpos < endpos and not heap[childpos] < heap[rightpos]:
                childpos = rightpos
            heap[pos] = heap[childpos]
            pos = childpos
            childpos = 2*pos + 1
        heap[pos] = newitem
        self.heapifyDown(heap, startpos, pos)

    def getShortestPath(self, graph, start, end):
        paths = []
        queue, visited = [(0, start, [])], set()
        self.heapify(queue)
        while queue:
            (cost, node, path) = self.extractMin(queue)
            if node not in visited:
                visited.add(node)
                path = path + [node]
                if int(node) == int(end):
                    paths.append((cost, path))
                    for i in range(len(queue)):
                        (new_cost, node, path) = self.extractMin(queue)
                        if cost == new_cost:
                            visited.add(node)
                            path = path + [node]
                            paths.append((new_cost, path))
                    return paths
                for c, neighbour in graph[node]:
                    if neighbour not in visited:
                        self.insert(queue, (cost + c, neighbour, path))
        return -1
    
    def eliminateShortestPathEdges(self, path, graph):
        sp = []
        for i in range(0,len(path)-1):
            sp.append((path[i],path[i+1]))
        for u, v in sp:
            for index, value  in enumerate(graph[u]):
                if value[1] == v:
                    graph[u].pop(index) 
        return graph

    def almostShortestPath(self, edges, start, end):
        graph = collections.defaultdict(list)
        for l, r, c in edges:
            graph[l].append((int(c),r))
        outcomes =  myQueue.getShortestPath(graph, start, end)
        if outcomes == -1:
            return outcomes
        for outcome in outcomes:
            shortestpath = outcome[1]
            new_graph = myQueue.eliminateShortestPathEdges(shortestpath, graph)
        almost_shortest =  myQueue.getShortestPath(new_graph, start, end)
        if almost_shortest == -1:
            return almost_shortest
        else: 
            return almost_shortest[0][0]

if __name__ == '__main__':
    prev_input = []
    heap = []
    for line in fileinput.input(files =('./INPUT.txt')):
        new_input = line.split(' ')
        if len(new_input) == 1 or (new_input[0] == 0 and new_input[1] == 0):
            break
        elif (len(new_input) == 2 and len(prev_input) == 3):
            n, m = new_input[0], new_input[1]
            myQueue = PriorityQueue()
            print (myQueue.almostShortestPath(heap, i, j))
        elif (len(new_input) == 2 and len(prev_input) == 2):
            i, j = new_input[0], new_input[1]
            heap = []
        elif (len(new_input) == 3):
            temp  = tuple(new_input)
            heap.append(temp)
            if line.find('\n') == -1:
                myQueue = PriorityQueue()
                print (myQueue.almostShortestPath(heap, i, j))
        prev_input = new_input