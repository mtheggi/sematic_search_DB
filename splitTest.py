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


        rowCount = 1
        returnRow=None
        for row in reader:
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
    def __init__(self,id, data,left,right,axis,sel_axis,dimensions):
        self.data = data
        self.left = left
        self.right = right
        self.axis = axis
        self.sel_axis = sel_axis
        self.dimensions = dimensions
        self.id = id

class NodeSerializer:
    @staticmethod
    def serialize_to_csv(nodes, csv_filename):
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            for node in nodes:
                # Write a row for each node's attributes
                writer.writerow([node.id, *node.data, node.left, node.right, node.axis, node.sel_axis, node.dimensions])

class NodeDeserializer:
    @staticmethod
    def deserialize_from_csv(csv_filename):
        nodes = []

        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row

            for row in reader:
                # Extract values from the CSV row
                node_id, *data, left, right, axis, sel_axis, dimensions = map(int, row)

                # Create Node object and append to the list
                nodes.append(Node(data, left, right, axis, sel_axis, dimensions, node_id))

        return nodes

nodes=[] 
def createExternalPart(fileName=None, size=0,dimensions=None, axis=0, sel_axis=None,lstCount=0):
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

    # Sort point list and choose median as pivot element
    median = size // 2

    csvsort(fileName, [axis], output_filename='saved_db.csv' , has_header=False)
    fileName1 = 'output'+str(lstCount+1)+'.csv'
    fileName2 = 'output'+str(lstCount+2)+'.csv'
    middle = split_csv('saved_db.csv', fileName1, fileName2, median)

    nodeId=middle[0]
    nodeData=middle[1:]
    
    # if median == 0:
    #     newNode =  Node(nodeId,nodeData,None,None,axis,sel_axis,dimensions)
    #     nodes.append(newNode)
    #     return newNode
    
    # left  = createExternalPart(fileName1, dimensions, sel_axis(axis),lstCount+2)
    # right = createExternalPart(fileName2, dimensions, sel_axis(axis),lstCount+2)
    
    leftId=0
    rightId=0
    
    newNode = Node(nodeId,nodeData, leftId, rightId, axis=axis, sel_axis=sel_axis, dimensions=dimensions)
    nodes.append(newNode)
    return newNode


#createExternalPart('saved_db_10.csv', 10, 0, 0, None, 0)
#NodeSerializer.serialize_to_csv(nodes, 'output.csv')

csvsort('saved_db_10.csv', [1], output_filename='saved_db.csv' , has_header=False)

# nodes=[]
# nodes.append(Node([1,2,3],1,2,3,4,5,0))
# nodes.append(Node([1,2,3],1,2,3,4,5,1))
# nodes.append(Node([1,2,3],1,2,3,4,5,2))
# nodes.append(Node([1,2,3],1,2,3,4,5,3))
# nodes.append(Node([1,2,3],1,2,3,4,5,4))

# NodeSerializer.serialize_to_csv(nodes, 'output.csv')

# deserialized_nodes = NodeDeserializer.deserialize_from_csv('output.csv')

# # Print the deserialized nodes
# for node in deserialized_nodes:
#     print(vars(node))
