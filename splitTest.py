import csv
from csvsort import csvsort

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
    def __init__(self,id, data,left,right,axis,dimensions):
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
                left = int(row[71]) if row[71] else None
                right = int(row[72]) if row[72] else None
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
    
    point_list.sort(key=lambda point: point[axis])
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
createExternalPart('saved_db_1m.csv', size=90000, dimensions=70, axis=0, sel_axis=None, lstCount=lstcnt)
NodeSerializer.serialize_to_csv(nodes, 'output.csv')

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

