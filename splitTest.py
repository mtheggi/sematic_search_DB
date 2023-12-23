import csv
from csvsort import csvsort
import heapq
import itertools
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def split_csv(input_file, output_file1, output_file2, middle_row):
    """
    Middle row is execluded from the the output files
    It is used as a boundary
    But it is returned
    """
    with open(input_file, 'r', newline='') as infile, \
        open(output_file1, 'w', newline='') as outfile1, \
        open(output_file2, 'w', newline='') as outfile2:

        reader = csv.reader(infile)
        
        writer1 = csv.writer(outfile1)
        writer2 = csv.writer(outfile2)
        if middle_row==0: 
            for row in reader:
                return row 
            


        rowCount = 0
        returnRow=None
        for row in reader:
            # print("rowcount , " , rowCount)
            # print("middle_row , " , middle_row)
            if rowCount == middle_row:
                returnRow=row
            elif rowCount < middle_row:
                writer1.writerow(row)
            else:
                writer2.writerow(row)
            rowCount += 1
    return returnRow

# Usage
# ans=split_csv('saved_db_100k.csv', 'output1.csv', 'output2.csv', 50000)
# print(ans)


class Node(object):
    def __init__(self,id, data:list,left,right,axis,dimensions):
        self.data = data
        self.left = left
        self.right = right
        self.axis = axis
        self.dimensions = dimensions
        self.id = id

class NodeSerializer:
    @staticmethod
    def serialize_to_csv(nodes, csv_filename):
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            for node in nodes:
                # Write a row for each node's attributes
                writer.writerow([node.id, *node.data, node.left, node.right, node.axis, node.dimensions])

def ConvertNodestoDict(nodes): 
    nodesDict = {}
    for node in nodes:
        nodesDict[node.id] = node

    return nodesDict

class NodeDeserializer:
    @staticmethod
    def deserialize_from_csv(csv_filename):
        nodes = []

        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            # next(reader)  # Skip the header row

            for row in reader:
                # Extract values from the CSV row
                node_id = int(row[0])
                data = list(map(float, row[1:71]))  # Assuming the next 70 cells are for data
                if row[71] == '':
                    left = None
                else: 
                    if row[71][-1] =='v':
                        left = row[71]
                    else:
                        left = int(row[71])


                if row[72] == '':
                    right = None
                else:   
                    if row[72][-1] =='v':
                        right = row[72]
                    else:
                        right = int(row[72])
                # left = int(row[71]) if row[71] else None
                # right = int(row[72]) if row[72] else None
                axis = int(row[73]) if row[73] else None
                dimensions = int(row[74]) if row[74] else None
                # Create Node object and append to the list
                nodes.append(Node(node_id,data, left, right, axis, dimensions))

        return nodes


def ConvertFileToList(FileName):
    data_list = []

    with open(FileName, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        
        for row in reader:
            data_list.append(row)

    return data_list


ClusterCnt =0 
nodes=[] 
def createExternalPart(fileName=None, size=0,dimensions=None, axis=0, sel_axis=None,lstCount=0,clusterSize=1000):
    """ Creates a kd-tree from a list of points

    All points in the list must be of the same dimensionality.

    If no point_list is given, an empty tree is created. The number of
    dimensions has to be given instead.

    If both a point_list and dimensions are given, the numbers must agree.

    Axis is the axis on which the root-node should split.

    sel_axis(axis) is used when creating subnodes of a node. It receives the
    axis of the parent node and returns the axis of the child node. """

    # by default cycle through the axis
    global ClusterCnt
    global Internalnodes
    global nodes
    if size ==0 : 
        return None
    
    sel_axis = sel_axis or (lambda prev_axis: (prev_axis+1) % dimensions)

    # Sort point list and choose median as pivot element
    median = size // 2
    # print(f"Sorting {fileName} on axis {axis+1}")
    # print(f"size  is  {size}")
    
    csvsort(fileName, [axis+1], output_filename='saved_db.csv' , has_header=False)
    fileName1 = 'output'+str(lstCount+1)+'.csv'
    fileName2 = 'output'+str(lstCount+2)+'.csv'
    middle = split_csv('saved_db.csv', fileName1, fileName2, median)
    
    # print(middle) 

    nodeId=middle[0]
    nodeData=middle[1:]
    
    if median == 0:
        newNode =  Node(nodeId,nodeData,None,None,axis,dimensions)
        nodes.append(newNode)
        return newNode
    
    leftsize = size//2
    rightsize = size//2 - (size%2==0)

    if leftsize <= clusterSize and leftsize > 0:
        point_list = ConvertFileToList(fileName1)
        left = createInternalPart(point_list=point_list, dimensions=dimensions, axis=sel_axis(axis), sel_axis=None)
        ClusterFileName ='Cluster'+str(ClusterCnt)+'.csv'
        ClusterCnt= ClusterCnt+1 
        NodeSerializer.serialize_to_csv(Internalnodes, ClusterFileName)
        point_list= []
        Internalnodes=[]
        leftId = ClusterFileName

    else: 
        left  = createExternalPart(fileName= fileName1, size=leftsize ,dimensions= dimensions, axis=sel_axis(axis),lstCount=lstCount+2)
        if left != None:
            leftId=left.id
        else : 
            leftId= -1

    if rightsize <= clusterSize and rightsize > 0:
        point_list = ConvertFileToList(fileName2)
        right = createInternalPart(point_list=point_list, dimensions=dimensions, axis=sel_axis(axis), sel_axis=None)
        ClusterFileName ='Cluster'+str(ClusterCnt)+'.csv'
        ClusterCnt= ClusterCnt+1 
        NodeSerializer.serialize_to_csv(Internalnodes, ClusterFileName)
        point_list= []
        Internalnodes=[]
        rightId = ClusterFileName
        
    else:        
        right = createExternalPart(fileName= fileName2, size=rightsize,dimensions=dimensions, axis=sel_axis(axis),lstCount=lstCount+2)        
        if right !=None: 
            rightId=right.id
        else:
            rightId= -1

    newNode = Node(nodeId,nodeData, leftId, rightId, axis=axis,  dimensions=dimensions)
    nodes.append(newNode)
    return newNode



Internalnodes=[] 

def createInternalPart(point_list=None, dimensions=None, axis=0, sel_axis=None):
    """ Creates a kd-tree from a list of points

    All points in the list must be of the same dimensionality.

    If no point_list is given, an empty tree is created. The number of
    dimensions has to be given instead.

    If both a point_list and dimensions are given, the numbers must agree.

    Axis is the axis on which the root-node should split.

    sel_axis(axis) is used when creating subnodes of a node. It receives the
    axis of the parent node and returns the axis of the child node. """

    # by default cycle through the axis
    sel_axis = sel_axis or (lambda prev_axis: (prev_axis+1) % dimensions)

    if not point_list:
        return None 
    
    # Sort point list and choose median as pivot element
    point_list = list(point_list)
    
    point_list.sort(key=lambda point: point[axis+1])
    median = len(point_list) // 2

    loc   = point_list[median]
    left  = createInternalPart(point_list[:median], dimensions, sel_axis(axis))
    right = createInternalPart(point_list[median + 1:], dimensions, sel_axis(axis))
     

    if left != None:
        leftId=left.id
    else : 
        leftId= -1
    
    if right !=None: 
        rightId=right.id
    else:
        rightId= -1

    newNode = Node(loc[0], loc[1:],leftId,rightId, axis=axis, dimensions=dimensions)
    
    Internalnodes.append(newNode)

    return newNode

lstcnt =0 

def distance(v1, v2 ) :
        return 1 - cosine_similarity([v1], [v2])[0][0]

def search_knn_cluster(CurrentNode , point, k, results, get_dist, counter, nodes_Dic):
    if not CurrentNode:
        return

    nodeDist = get_dist(CurrentNode)
    # Add current node to the priority queue if it closer than
    # at least one point in the queue.
    #
    # If the heap is at its capacity, we need to check if the
    # current node is closer than the current farthest node, and if
    # so, replace it.
    item = (-nodeDist, next(counter), CurrentNode)
    if len(results) >= k:
        if -nodeDist > results[0][0]:
            heapq.heapreplace(results, item)
    else:
        heapq.heappush(results, item)
    # get the splitting plane
    split_plane = CurrentNode.data[CurrentNode.axis]
    # get the squared distance between the point and the splitting plane
    # (squared since all distances are squared).
    plane_dist = point[CurrentNode.axis] - split_plane
    plane_dist2 = plane_dist * plane_dist
    # Search the side of the splitting plane that the point is in
    if point[CurrentNode.axis] < split_plane:
        if CurrentNode.left is not None and CurrentNode.left != -1:
            Nextnode1= nodes_Dic[CurrentNode.left]
            search_knn_cluster(Nextnode1,point, k, results, get_dist, counter,nodes_Dic)
    else:
        if CurrentNode.right is not None and CurrentNode.right != -1:
            Nextnode2= nodes_Dic[CurrentNode.right]
            search_node(Nextnode2, point, k, results, get_dist, counter, nodes_Dic)
    # Search the other side of the splitting plane if it may contain
    # points closer than the farthest point in the current results.
    if -plane_dist2 > results[0][0] or len(results) < k:
        if point[CurrentNode.axis] < CurrentNode.data[CurrentNode.axis]:
            if CurrentNode.right is not None and CurrentNode.right != -1:
                Nextnode2= nodes_Dic[CurrentNode.right]
                search_node(Nextnode2, point, k, results, get_dist, counter, nodes_Dic)
        else:
            if CurrentNode.left is not None and CurrentNode.left != -1:
                Nextnode1= nodes_Dic[CurrentNode.left]
                search_knn_cluster(Nextnode1,point, k, results, get_dist, counter,nodes_Dic)



def search_knn(DirectoryName, point, k, dist=None):
    """ Return the k nearest neighbors of point and their distances
    point must be an actual point, not a node.
    k is the number of results to return. The actual results can be less
    (if there aren't more nodes to return) or more in case of equal
    distances.
    dist is a distance function, expecting two points and returning a
    distance value. Distance values can be any comparable type.
    The result is an ordered list of (node, distance) tuples.
    """
    nodes=NodeDeserializer.deserialize_from_csv(DirectoryName)
    Rootnode= nodes[-1]    
    nodes_Dic = ConvertNodestoDict(nodes)
    # print(nodes_Dic)
    

    if k < 1:
        raise ValueError("k must be greater than 0.")
    if dist is None:
        get_dist = lambda n: n.dist(point)
    else:
        get_dist = lambda n: dist(n.data, point)
    results = []
    search_node(Rootnode,point, k, results, get_dist, itertools.count(), nodes_Dic)
    # We sort the final result by the distance in the tuple
    # (<KdNode>, distance).
    return [(node, -d) for d, _, node in sorted(results, reverse=True)]



def search_node( CurrentNode , point, k, results, get_dist, counter, nodes_Dic):
    if not CurrentNode:
        return
    nodeDist = get_dist(CurrentNode)
    # Add current node to the priority queue if it closer than
    # at least one point in the queue.
    #
    # If the heap is at its capacity, we need to check if the
    # current node is closer than the current farthest node, and if
    # so, replace it.
    item = (-nodeDist, next(counter), CurrentNode)
    if len(results) >= k:
        if -nodeDist > results[0][0]:
            heapq.heapreplace(results, item)
    else:
        heapq.heappush(results, item)
    # get the splitting plane
    split_plane = CurrentNode.data[CurrentNode.axis]
    # get the squared distance between the point and the splitting plane
    # (squared since all distances are squared).
    plane_dist = point[CurrentNode.axis] - split_plane
    plane_dist2 = plane_dist * plane_dist
    # Search the side of the splitting plane that the point is in
    if point[CurrentNode.axis] < split_plane:
        if CurrentNode.left is not None and CurrentNode.left != -1:
            if isinstance(CurrentNode.left,int) : 
                nextNode = nodes_Dic[CurrentNode.left]
                search_node(nextNode,point, k, results, get_dist, counter,nodes_Dic)
            else: # clustered Node 
                clusterFileName = CurrentNode.left
                ClusterNodes = NodeDeserializer.deserialize_from_csv(clusterFileName)
                clusterNodeRoot= ClusterNodes[-1]
            
                ClusterNode_Dic= ConvertNodestoDict(ClusterNodes)
                # print("cluster Node left ") 
                # print(ClusterNode_Dic)
                search_knn_cluster(clusterNodeRoot, point, k, results, get_dist, counter, ClusterNode_Dic)            
    else:
        if CurrentNode.right is not None and CurrentNode.right != -1:
            if isinstance(CurrentNode.right,int) : 
                nextNode = nodes_Dic[CurrentNode.right]
                search_node(nextNode,point, k, results, get_dist, counter,nodes_Dic)
            else: # clustered Node 
                clusterFileName = CurrentNode.right
                ClusterNodes = NodeDeserializer.deserialize_from_csv(clusterFileName)
                clusterNodeRoot= ClusterNodes[-1]
                ClusterNode_Dic= ConvertNodestoDict(ClusterNodes)
                search_knn_cluster(clusterNodeRoot, point, k, results, get_dist, counter, ClusterNode_Dic)
    # Search the other side of the splitting plane if it may contain
    # points closer than the farthest point in the current results.
    if -plane_dist2 > results[0][0] or len(results) < k:
        if point[CurrentNode.axis] < CurrentNode.data[CurrentNode.axis]:
            if CurrentNode.right is not None and CurrentNode.right != -1:
                if isinstance(CurrentNode.right,int) : 
                    nextNode = nodes_Dic[CurrentNode.right]
                    search_node(nextNode,point, k, results, get_dist, counter,nodes_Dic)
                else: # clustered Node 
                    clusterFileName = CurrentNode.right
                    ClusterNodes = NodeDeserializer.deserialize_from_csv(clusterFileName)
                    clusterNodeRoot= ClusterNodes[-1]
                
                    ClusterNode_Dic= ConvertNodestoDict(ClusterNodes)
                    search_knn_cluster(clusterNodeRoot, point, k, results, get_dist, counter, ClusterNode_Dic)
        else:
            if CurrentNode.left is not None and CurrentNode.left != -1:
                if isinstance(CurrentNode.left,int) : 
                    nextNode = nodes_Dic[CurrentNode.left]
                    search_node(nextNode,point, k, results, get_dist, counter,nodes_Dic)
                else: # clustered Node 
                    clusterFileName = CurrentNode.left
                    ClusterNodes = NodeDeserializer.deserialize_from_csv(clusterFileName)
                    clusterNodeRoot= ClusterNodes[-1]
                    ClusterNode_Dic= ConvertNodestoDict(ClusterNodes)
                    search_knn_cluster(clusterNodeRoot, point, k, results, get_dist, counter, ClusterNode_Dic)        



# createExternalPart('saved_db_10.csv', size=10, dimensions=70, axis=0, sel_axis=None, lstCount=lstcnt)
# NodeSerializer.serialize_to_csv(nodes, 'output.csv')

# queryVector = [0.12718718215222624 , 0.963183636660174,0.6555424194210452,0.3133291851458011,0.3528919540205553,0.8668203118164016,0.39626652606370516,0.5728987611344992,0.7074240680371062,0.3864556399520991,0.08491579006631067,0.12291886859445211,0.7707808940776009,0.9327501058342144,0.3066966552889968,0.6419991261669797,0.8588535520215995,0.5824131586724725,0.6131204271127515,0.10286751773999914,0.0549109772028189,0.09352879476593146,0.17104268205957374,0.3824261140256915,0.15356499160275394,0.45347326938263244,0.6083887855272883,0.034960645056148154,0.24393845321453977,0.1278774678517305,0.2871856386640077,0.7512447588345483,0.4859451566973938,0.4199580731997844,0.293269784610794,0.2832464176481909,0.27805718845811844,0.24222588465297312,0.5349363899114752,0.6457376865917788,0.6219711816356497,0.13916395793040215,0.23964331972883335,0.2729502125224802,0.9498684905442188,0.6945602815435133,0.5639426863002537,0.501955681453989,0.3367429117001498,0.9704224868356233,0.007215061636175357,0.030600182627405492,0.09400716702268663,0.25025896502723133,0.14240458339455853,0.009607116915863467,0.2826491522554634,0.7810640954782109,0.9221179015408044,0.21099100150743078,0.18174101107943108,0.8444442653748049,0.2714691854526494,0.26828843222396526,0.4480176844538759,0.036925979004275744,0.05439050847352678,0.0388722829132947,0.08271671126005153,0.44219512781190307]

# print(search_knn("output.csv", queryVector , 1 ,  dist=distance)[0][0].id)

# csvsort('saved_db_10.csv', [1], output_filename='saved_db_10_sorted.csv' , has_header=False)


# deserialized_nodes = NodeDeserializer.deserialize_from_csv('output.csv')

# Print the deserialized nodes
# for node in deserialized_nodes:
#     print("ID " , node.id)
#     # print("Data " , node.data)
#     print("Left " , node.left)
#     print("Right " , node.right)
#     print("Axis " , node.axis)
#     print("Dimensions " , node.dimensions)
#     print("---------------------------------")

